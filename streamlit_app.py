import html
import json
import math
import re
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).parent
APP_BUILD = "2026-07-13-1230"


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
    if lp >= 0:
        z = math.exp(-lp)
        return 1 / (1 + z)
    z = math.exp(lp)
    return z / (1 + z)


def is_missing(value):
    return value is None or value == ""


def preprocessed_value(feature, raw_value):
    p = CFG["preprocessing"].get(feature)
    missing = is_missing(raw_value)
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
        if not is_missing(value):
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
    match = re.match(
        r"^(PLT|WBC|LYMPH_ABS|AST|LDH|CREA|UREA)_(latest|change_from_first|measure_n_so_far|time_since_last)$",
        feature,
    )
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


def format_value(value):
    if is_missing(value):
        return ""
    if isinstance(value, float):
        return f"{value:.3g}"
    return str(value)


def render_table(headers, rows):
    header_html = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    body_html = ""
    for row in rows:
        body_html += "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>"
    st.markdown(
        f"""
        <table class="risk-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{body_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


def render_trajectory(rows):
    if not rows:
        return
    max_risk = max(max(row["risk"] for row in rows), 0.01)
    marks = ""
    for row in rows:
        width = max(4, row["risk"] / max_risk * 100)
        marks += f"""
        <div class="traj-row">
            <div class="traj-label">{html.escape(row["landmark"]["id"])}</div>
            <div class="traj-bar-wrap"><div class="traj-bar" style="width:{width:.1f}%"></div></div>
            <div class="traj-value">{row["risk"] * 100:.1f}%</div>
        </div>
        """
    st.markdown(f"<div class='trajectory'>{marks}</div>", unsafe_allow_html=True)


st.set_page_config(page_title="SFTS Dynamic Risk Monitor", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1180px;}
    .risk-table {width: 100%; border-collapse: collapse; font-size: 0.92rem;}
    .risk-table th {text-align: left; border-bottom: 2px solid #222; padding: 0.45rem 0.55rem;}
    .risk-table td {border-bottom: 1px solid #ddd; padding: 0.42rem 0.55rem;}
    .trajectory {margin-top: 0.4rem;}
    .traj-row {display: grid; grid-template-columns: 68px 1fr 64px; gap: 10px; align-items: center; margin: 0.45rem 0;}
    .traj-label {font-weight: 600;}
    .traj-bar-wrap {height: 12px; background: #e8edf2; border-radius: 999px; overflow: hidden;}
    .traj-bar {height: 12px; background: #ce3f31; border-radius: 999px;}
    .traj-value {text-align: right; font-variant-numeric: tabular-nums;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SFTS Dynamic Risk Monitor")
st.caption("Sequential in-hospital mortality risk updating from baseline and repeated laboratory measurements.")
st.caption(f"Build {APP_BUILD}")

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
    latest_label = st.selectbox("Latest available laboratory panel", landmark_options, index=0)
    latest_index = landmark_options.index(latest_label)
    active_landmarks = CFG["landmarks"][: latest_index + 1]

    matrix = {lab["key"]: {} for lab in CFG["labs"]}
    for landmark_index, landmark in enumerate(active_landmarks):
        with st.expander(landmark["label"], expanded=landmark_index == latest_index):
            lc1, lc2 = st.columns(2)
            for lab_index, lab in enumerate(CFG["labs"]):
                column = lc1 if lab_index % 2 == 0 else lc2
                matrix[lab["key"]][landmark["id"]] = column.number_input(
                    f'{LAB_LABELS.get(lab["key"], lab["label"])} ({lab["unit"]})',
                    min_value=0.0,
                    value=float(EXAMPLE[lab["key"]][landmark_index]),
                    step=0.1,
                    key=f'{lab["key"]}_{landmark["id"]}',
                )

    st.button("Update risk", type="primary")

results = [calculate_landmark(baseline, matrix, i) for i in range(latest_index + 1)]
current = results[-1]
trajectory_rows = [{"landmark": r["landmark"], "hour": r["landmark"]["hour"], "risk": r["risk"]} for r in results]
top_drivers = sorted(current["contributions"], key=lambda item: abs(item["contribution"]), reverse=True)[:10]

with right:
    st.subheader("Risk dashboard")
    m1, m2, m3 = st.columns(3)
    m1.metric("Latest update", current["landmark"]["label"])
    m2.metric("Mortality risk", f'{current["risk"] * 100:.1f}%')
    m3.metric("Risk category", risk_stratum(current["risk"]))

    st.subheader("Risk trajectory")
    render_trajectory(trajectory_rows)
    render_table(
        ["Landmark", "Hour", "Predicted mortality risk"],
        [[row["landmark"]["id"], row["hour"], f'{row["risk"] * 100:.1f}%'] for row in trajectory_rows],
    )

    st.subheader("Main risk drivers")
    render_table(
        ["Feature", "Current value", "Model contribution"],
        [
            [
                driver["label"],
                format_value(driver["raw"]),
                f'{driver["contribution"]:.4f}',
            ]
            for driver in top_drivers
        ],
    )
