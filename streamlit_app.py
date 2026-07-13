import json
import math
import re
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).parent


@st.cache_data
def load_config():
    text = (ROOT / "model3_config.js").read_text(encoding="utf-8")
    match = re.search(r"const MODEL3_CONFIG = (\{.*\});\s*$", text, re.S)
    if not match:
        raise ValueError("Cannot read locked Model 3 configuration.")
    return json.loads(match.group(1))


CFG = load_config()

FEATURE_LABELS = {
    "LDH_latest": "Latest LDH",
    "apache2": "APACHE II",
    "AST_latest": "Latest AST",
    "PLT_latest": "Latest platelet count",
    "UREA_latest": "Latest urea",
    "age": "Age",
    "LDH_change_from_first": "LDH change from first value",
    "pulse_rate": "Pulse rate",
    "CREA_latest": "Latest creatinine",
    "UREA_measure_n_so_far": "Number of urea measurements",
    "CREA_measure_n_so_far": "Number of creatinine measurements",
    "hypertension": "Hypertension",
    "CREA_time_since_last": "Time since last creatinine test",
    "UREA_time_since_last": "Time since last urea test",
    "LYMPH_ABS_latest": "Latest lymphocyte count",
    "temperature": "Temperature",
    "LYMPH_ABS_measure_n_so_far": "Number of lymphocyte measurements",
    "WBC_measure_n_so_far": "Number of WBC measurements",
    "WBC_latest": "Latest WBC",
    "PLT_measure_n_so_far": "Number of platelet measurements",
}

LAB_LABELS = {
    "PLT": "Platelet count",
    "WBC": "White blood cell count",
    "LYMPH_ABS": "Absolute lymphocyte count",
    "AST": "AST",
    "LDH": "LDH",
    "CREA": "Creatinine",
    "UREA": "Urea",
}

EXAMPLE = {
    "age": 67,
    "apache2": 12,
    "temperature": 37.8,
    "pulse_rate": 96,
    "hypertension": 0,
    "PLT": [62, 51, 48, 45, 45],
    "WBC": [2.1, 2.4, 2.9, 3.8, 5.0],
    "LYMPH_ABS": [0.42, 0.35, 0.31, 0.28, 0.22],
    "AST": [310, 420, 528, 650, 1100],
    "LDH": [900, 1080, 1374, 1700, 3998],
    "CREA": [78, 92, 138, 190, 569],
    "UREA": [7.8, 9.6, 13.39, 18.4, 36.89],
}


def logistic(lp):
    return 1 / (1 + math.exp(-lp))


def preprocessed_value(feature, raw_value):
    p = CFG["preprocessing"].get(feature)
    missing = raw_value is None or pd.isna(raw_value)
    value = p.get("imputationValue") if missing and p else raw_value

    if not p:
        return 0.0, missing
    if p.get("log1pTransform") and not missing:
        value = math.log1p(max(float(value), 0))
    if p.get("variableType") == "continuous":
        center = p.get("center")
        scale = p.get("scale")
        if center is not None and scale not in (None, 0):
            value = (float(value) - center) / scale
    return float(value), missing


def lab_history_feature(matrix, lab, landmark_index, feature_type):
    current = CFG["landmarks"][landmark_index]
    values = []
    for landmark in CFG["landmarks"][: landmark_index + 1]:
        value = matrix[lab].get(landmark["id"])
        if value is not None and not pd.isna(value):
            values.append({"value": float(value), "hour": landmark["hour"]})

    if feature_type == "latest":
        return values[-1]["value"] if values else None
    if feature_type == "change_from_first":
        return values[-1]["value"] - values[0]["value"] if values else None
    if feature_type == "measure_n_so_far":
        return len(values)
    if feature_type == "time_since_last":
        return current["hour"] - values[-1]["hour"] if values else None
    return None


def raw_feature_value(feature, baseline, matrix, landmark_index):
    if feature in baseline:
        return baseline[feature]
    match = re.match(r"^(PLT|WBC|LYMPH_ABS|AST|LDH|CREA|UREA)_(latest|change_from_first|measure_n_so_far|time_since_last)$", feature)
    if match:
        return lab_history_feature(matrix, match.group(1), landmark_index, match.group(2))
    return None


def calculate_landmark(baseline, matrix, landmark_index):
    lp = CFG["intercept"]
    contributions = []
    for coef in CFG["coefficients"]:
        feature = coef["feature"]
        raw = raw_feature_value(feature, baseline, matrix, landmark_index)
        value, missing = preprocessed_value(feature, raw)
        contribution = coef["coefficient"] * value
        lp += contribution
        contributions.append(
            {
                "feature": feature,
                "label": FEATURE_LABELS.get(feature, feature),
                "raw": raw,
                "contribution": contribution,
                "missing": missing,
            }
        )
    return {
        "landmark": CFG["landmarks"][landmark_index],
        "risk": logistic(lp),
        "contributions": contributions,
    }


def risk_stratum(risk):
    for item in CFG["riskStrata"]:
        if item["min"] <= risk < item["max"]:
            return item.get("name", item["label"])
    return CFG["riskStrata"][-1].get("name", CFG["riskStrata"][-1]["label"])



def build_matrix(edited, active_landmarks):
    matrix = {lab["key"]: {} for lab in CFG["labs"]}
    for row_label, lab in zip(edited.index, CFG["labs"]):
        for landmark in active_landmarks:
            value = edited.loc[row_label, landmark["id"]]
            matrix[lab["key"]][landmark["id"]] = value
    return matrix


st.set_page_config(page_title="SFTS Dynamic Risk Monitor", layout="wide")
st.title("SFTS Dynamic Risk Monitor")
st.caption("Sequential in-hospital mortality risk updating from baseline and repeated laboratory measurements.")

left, right = st.columns([1.05, 1])

with left:
    st.subheader("Baseline profile")
    c1, c2 = st.columns(2)
    age = c1.number_input("Age, years", min_value=0, max_value=120, value=EXAMPLE["age"], step=1)
    apache2 = c2.number_input("APACHE II score", min_value=0, max_value=71, value=EXAMPLE["apache2"], step=1)
    temperature = c1.number_input("Temperature, deg C", min_value=30.0, max_value=45.0, value=float(EXAMPLE["temperature"]), step=0.1)
    pulse_rate = c2.number_input("Pulse rate, beats/min", min_value=20, max_value=240, value=EXAMPLE["pulse_rate"], step=1)
    hypertension_label = c1.selectbox("Hypertension", ["No", "Yes"], index=int(EXAMPLE["hypertension"]))
    hypertension = 1 if hypertension_label == "Yes" else 0

    baseline = {
        "age": age,
        "apache2": apache2,
        "temperature": temperature,
        "pulse_rate": pulse_rate,
        "hypertension": hypertension,
    }

    st.subheader("Laboratory update")
    landmark_options = [item["label"] for item in CFG["landmarks"]]
    latest_label = st.selectbox(
        "Latest available laboratory panel",
        landmark_options,
        index=0,
    )
    latest_index = landmark_options.index(latest_label)
    active_landmarks = CFG["landmarks"][: latest_index + 1]

    lab_table = pd.DataFrame(
        {
            landmark["id"]: [EXAMPLE[lab["key"]][i] for lab in CFG["labs"]]
            for i, landmark in enumerate(active_landmarks)
        },
        index=[f'{LAB_LABELS.get(lab["key"], lab["label"])} ({lab["unit"]})' for lab in CFG["labs"]],
    )
    edited = st.data_editor(lab_table, use_container_width=True, num_rows="fixed", key="lab_table")
    update_clicked = st.button("Update risk", type="primary", use_container_width=True)

matrix = build_matrix(edited, active_landmarks)
results = [calculate_landmark(baseline, matrix, i) for i in range(latest_index + 1)]
trajectory = pd.DataFrame(
    {
        "Landmark": [r["landmark"]["id"] for r in results],
        "Hour": [r["landmark"]["hour"] for r in results],
        "Predicted mortality risk": [r["risk"] for r in results],
    }
).sort_values("Hour")
current = results[-1]
top_drivers = (
    pd.DataFrame(current["contributions"])
    .assign(abs_contribution=lambda x: x["contribution"].abs())
    .sort_values("abs_contribution", ascending=False)
    .head(10)
)

with right:
    st.subheader("Risk dashboard")
    m1, m2, m3 = st.columns(3)
    m1.metric("Latest update", current["landmark"]["label"])
    m2.metric("Mortality risk", f'{current["risk"] * 100:.1f}%')
    m3.metric("Risk category", risk_stratum(current["risk"]))

    chart_data = trajectory.set_index("Hour")[["Predicted mortality risk"]]
    st.line_chart(chart_data, height=260)

    st.subheader("Risk trajectory")
    display_trajectory = trajectory.copy()
    display_trajectory["Predicted mortality risk"] = display_trajectory["Predicted mortality risk"].map(lambda x: f"{x * 100:.1f}%")
    st.dataframe(display_trajectory[["Landmark", "Hour", "Predicted mortality risk"]], use_container_width=True, hide_index=True)

    st.subheader("Main risk drivers")
    driver_table = top_drivers[["label", "raw", "contribution"]].rename(
        columns={"label": "Feature", "raw": "Current value", "contribution": "Model contribution"}
    )
    driver_table["Model contribution"] = driver_table["Model contribution"].map(lambda x: round(float(x), 4))
    st.dataframe(driver_table, use_container_width=True, hide_index=True)
