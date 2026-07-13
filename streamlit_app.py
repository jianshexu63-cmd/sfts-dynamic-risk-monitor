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
    "LDH_latest": "LDH 最新值",
    "apache2": "APACHE II",
    "AST_latest": "AST 最新值",
    "PLT_latest": "PLT 最新值",
    "UREA_latest": "尿素最新值",
    "age": "年龄",
    "LDH_change_from_first": "LDH 较首次变化",
    "pulse_rate": "脉搏",
    "CREA_latest": "肌酐最新值",
    "UREA_measure_n_so_far": "尿素检测次数",
    "CREA_measure_n_so_far": "肌酐检测次数",
    "hypertension": "高血压",
    "CREA_time_since_last": "距上次肌酐检测时间",
    "UREA_time_since_last": "距上次尿素检测时间",
    "LYMPH_ABS_latest": "淋巴细胞最新值",
    "temperature": "体温",
    "LYMPH_ABS_measure_n_so_far": "淋巴细胞检测次数",
    "WBC_measure_n_so_far": "白细胞检测次数",
    "WBC_latest": "WBC 最新值",
    "PLT_measure_n_so_far": "血小板检测次数",
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
            return item["label"]
    return CFG["riskStrata"][-1]["label"]


st.set_page_config(page_title="SFTS Dynamic Risk Monitor", layout="wide")
st.title("SFTS Dynamic Risk Monitor")
st.caption("Research prototype only. Not for clinical decision-making.")

left, right = st.columns([1.05, 1])

with left:
    st.subheader("Baseline")
    c1, c2 = st.columns(2)
    age = c1.number_input("年龄", min_value=0, max_value=120, value=EXAMPLE["age"], step=1)
    apache2 = c2.number_input("APACHE II", min_value=0, max_value=71, value=EXAMPLE["apache2"], step=1)
    temperature = c1.number_input("体温, deg C", min_value=30.0, max_value=45.0, value=float(EXAMPLE["temperature"]), step=0.1)
    pulse_rate = c2.number_input("脉搏, 次/min", min_value=20, max_value=240, value=EXAMPLE["pulse_rate"], step=1)
    hypertension_label = c1.selectbox("高血压", ["无", "有"], index=int(EXAMPLE["hypertension"]))
    hypertension = 1 if hypertension_label == "有" else 0

    st.subheader("Laboratory timeline")
    lab_table = pd.DataFrame(
        {landmark["id"]: [EXAMPLE[lab["key"]][i] for lab in CFG["labs"]] for i, landmark in enumerate(CFG["landmarks"])},
        index=[f'{lab["label"]} ({lab["unit"]})' for lab in CFG["labs"]],
    )
    edited = st.data_editor(lab_table, use_container_width=True, num_rows="fixed")

baseline = {
    "age": age,
    "apache2": apache2,
    "temperature": temperature,
    "pulse_rate": pulse_rate,
    "hypertension": hypertension,
}

matrix = {}
for row_label, lab in zip(edited.index, CFG["labs"]):
    matrix[lab["key"]] = {}
    for landmark in CFG["landmarks"]:
        matrix[lab["key"]][landmark["id"]] = edited.loc[row_label, landmark["id"]]

results = [calculate_landmark(baseline, matrix, i) for i in range(len(CFG["landmarks"]))]
trajectory = pd.DataFrame(
    {
        "Landmark": [r["landmark"]["id"] for r in results],
        "Predicted mortality risk": [r["risk"] for r in results],
    }
)
current = results[-1]
top_drivers = (
    pd.DataFrame(current["contributions"])
    .assign(abs_contribution=lambda x: x["contribution"].abs())
    .sort_values("abs_contribution", ascending=False)
    .head(10)
)

with right:
    st.subheader("Risk update")
    m1, m2, m3 = st.columns(3)
    m1.metric("当前 landmark", current["landmark"]["label"])
    m2.metric("预测死亡风险", f'{current["risk"] * 100:.1f}%')
    m3.metric("风险分层", risk_stratum(current["risk"]))
    st.line_chart(trajectory, x="Landmark", y="Predicted mortality risk", height=260)
    st.subheader("主要风险贡献")
    st.bar_chart(top_drivers.set_index("label")["contribution"], height=320)

st.warning(
    "本网页仅用于论文研究演示，复现已锁定的 Model 3 计算流程。"
    "模型尚未完成前瞻性临床验证，不能作为独立临床决策工具。"
)
