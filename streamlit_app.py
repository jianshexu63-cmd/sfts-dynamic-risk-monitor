import html
import json
import math
import re
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).parent
APP_BUILD = "2026-07-13-1415"


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


def input_default(value):
    if not st.session_state.example_mode:
        return ""
    return str(value)


def parse_optional_float(label, text, errors):
    text = str(text).strip()
    if text == "":
        return None
    try:
        value = float(text)
    except ValueError:
        errors.append(f"{label} must be a number.")
        return None
    if value < 0:
        errors.append(f"{label} cannot be negative.")
        return None
    return value


def number_text_input(container, label, key, default_value):
    return container.text_input(label, value=input_default(default_value), key=key)


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


def render_curve(rows):
    if len(rows) == 0:
        st.info("Enter the first laboratory panel to generate the initial risk estimate.")
        return

    width, height = 520, 240
    left, right, top, bottom = 48, 18, 22, 38
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_hour = max(row["hour"] for row in rows) or 24
    max_risk = max(max(row["risk"] for row in rows), 0.05)
    y_max = min(1.0, max(0.3, math.ceil(max_risk * 10) / 10))

    points = []
    dots = []
    labels = []
    for row in rows:
        x = left + (row["hour"] / max_hour) * plot_w
        y = top + (1 - row["risk"] / y_max) * plot_h
        points.append(f"{x:.1f},{y:.1f}")
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#ce3f31" />')
        labels.append(
            f'<text x="{x:.1f}" y="{y - 10:.1f}" text-anchor="middle" class="curve-label">'
            f'{row["risk"] * 100:.1f}%</text>'
        )

    x_axis = f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="axis" />'
    y_axis = f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" class="axis" />'
    grid = ""
    y_ticks = []
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        y = top + (1 - frac) * plot_h
        value = frac * y_max
        grid += f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" class="grid" />'
        y_ticks.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" class="tick">{value * 100:.0f}%</text>')

    x_labels = ""
    for row in rows:
        x = left + (row["hour"] / max_hour) * plot_w
        x_labels += f'<text x="{x:.1f}" y="{top + plot_h + 24}" text-anchor="middle" class="tick">{html.escape(row["landmark"]["id"])}</text>'

    st.markdown(
        f"""
        <svg class="risk-curve" viewBox="0 0 {width} {height}" role="img" aria-label="Risk trajectory">
            {grid}
            {x_axis}
            {y_axis}
            {''.join(y_ticks)}
            {x_labels}
            <polyline points="{' '.join(points)}" fill="none" stroke="#ce3f31" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" />
            {''.join(dots)}
            {''.join(labels)}
        </svg>
        """,
        unsafe_allow_html=True,
    )


def render_driver_chart(drivers):
    if not drivers:
        st.info("Risk drivers will appear after the first laboratory panel is saved.")
        return

    max_abs = max(max(abs(driver["contribution"]) for driver in drivers), 0.001)
    rows = ""
    for driver in drivers:
        contribution = driver["contribution"]
        width = max(3, abs(contribution) / max_abs * 100)
        direction = "risk-up" if contribution >= 0 else "risk-down"
        direction_text = "Raises risk" if contribution >= 0 else "Lowers risk"
        rows += (
            '<div class="driver-row">'
            '<div class="driver-label">'
            f'<div class="driver-name">{html.escape(driver["label"])}</div>'
            f'<div class="driver-value">Current value: {html.escape(format_value(driver["raw"]))}</div>'
            '</div>'
            '<div class="driver-track">'
            f'<div class="driver-bar {direction}" style="width:{width:.1f}%"></div>'
            '</div>'
            '<div class="driver-score">'
            f'<span>{direction_text}</span>'
            f'<strong>{contribution:+.3f}</strong>'
            '</div>'
            '</div>'
        )
    st.markdown(f"<div class='driver-chart'>{rows}</div>", unsafe_allow_html=True)


def blank_panel_values(panel_index):
    values = {}
    for lab in CFG["labs"]:
        values[lab["key"]] = float(EXAMPLE[lab["key"]][panel_index])
    return values


def build_matrix_from_panels(panels):
    matrix = {lab["key"]: {} for lab in CFG["labs"]}
    for panel in panels:
        for lab in CFG["labs"]:
            matrix[lab["key"]][panel["landmark_id"]] = panel["values"].get(lab["key"])
    return matrix


def saved_panel_rows(panels):
    rows = []
    for panel in panels:
        values = panel["values"]
        rows.append(
            [
                panel["landmark_id"],
                panel["label"],
                format_value(values.get("PLT")),
                format_value(values.get("WBC")),
                format_value(values.get("LYMPH_ABS")),
                format_value(values.get("AST")),
                format_value(values.get("LDH")),
                format_value(values.get("CREA")),
                format_value(values.get("UREA")),
            ]
        )
    return rows


st.set_page_config(page_title="SFTS Dynamic Risk Monitor", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1180px;}
    div[data-testid="stMetric"] {background: #f7f8fa; border: 1px solid #e3e7eb; border-radius: 8px; padding: 0.85rem 1rem;}
    div[data-testid="stMetricValue"] {font-size: 2rem;}
    .step-chip {display: inline-block; padding: 0.28rem 0.62rem; border: 1px solid #d0d7de; border-radius: 999px; background: #f6f8fa; font-size: 0.86rem; font-weight: 700; color: #24292f; margin-bottom: 0.45rem;}
    .step-title {font-size: 1.05rem; font-weight: 700; margin: 0.2rem 0 0.6rem;}
    .hint-text {font-size: 0.9rem; color: #57606a; margin-bottom: 0.75rem;}
    .risk-table {width: 100%; border-collapse: collapse; font-size: 0.92rem;}
    .risk-table th {text-align: left; border-bottom: 2px solid #222; padding: 0.45rem 0.55rem;}
    .risk-table td {border-bottom: 1px solid #ddd; padding: 0.42rem 0.55rem;}
    .risk-curve {width: 100%; height: auto; margin: 0.5rem 0 1rem;}
    .risk-curve .axis {stroke: #333; stroke-width: 1.2;}
    .risk-curve .grid {stroke: #e3e7eb; stroke-width: 1;}
    .risk-curve .tick {font-size: 12px; fill: #4b5563;}
    .risk-curve .curve-label {font-size: 12px; font-weight: 700; fill: #333;}
    .driver-chart {margin-top: 0.35rem;}
    .driver-row {display: grid; grid-template-columns: minmax(150px, 1.15fr) minmax(120px, 1.1fr) 96px; gap: 12px; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #eef1f4;}
    .driver-name {font-weight: 700; line-height: 1.2;}
    .driver-value {font-size: 0.82rem; color: #57606a; margin-top: 0.12rem;}
    .driver-track {height: 12px; background: #edf1f5; border-radius: 999px; overflow: hidden;}
    .driver-bar {height: 12px; border-radius: 999px;}
    .driver-bar.risk-up {background: #ce3f31;}
    .driver-bar.risk-down {background: #4f7cac;}
    .driver-score {font-size: 0.78rem; color: #57606a; text-align: right;}
    .driver-score strong {display: block; color: #24292f; font-size: 0.92rem; font-variant-numeric: tabular-nums;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SFTS Dynamic Risk Monitor")
st.caption("Enter each newly available laboratory panel to update the in-hospital mortality risk in real time.")
st.caption(f"Build {APP_BUILD}")

if "panels" not in st.session_state:
    st.session_state.panels = []
if "example_mode" not in st.session_state:
    st.session_state.example_mode = False
if "input_version" not in st.session_state:
    st.session_state.input_version = 0

left, right = st.columns([1.05, 1])

with left:
    st.subheader("1. Patient profile")
    tools1, tools2 = st.columns(2)
    if tools1.button("Load example patient", use_container_width=True):
        st.session_state.example_mode = True
        st.session_state.panels = []
        st.session_state.input_version += 1
        st.rerun()
    if tools2.button("Clear inputs", use_container_width=True):
        st.session_state.example_mode = False
        st.session_state.panels = []
        st.session_state.input_version += 1
        st.rerun()
    st.caption("Enter real patient values. Leave unavailable values blank.")

    input_errors = []
    version = st.session_state.input_version
    c1, c2 = st.columns(2)
    age_text = number_text_input(c1, "Age, years", f"age_{version}", EXAMPLE["age"])
    apache2_text = number_text_input(c2, "APACHE II score", f"apache2_{version}", EXAMPLE["apache2"])
    temperature_text = number_text_input(c1, "Temperature, deg C", f"temperature_{version}", EXAMPLE["temperature"])
    pulse_rate_text = number_text_input(c2, "Pulse rate, beats/min", f"pulse_rate_{version}", EXAMPLE["pulse_rate"])
    hypertension_label = c1.selectbox("Hypertension", ["No", "Yes"], index=int(EXAMPLE["hypertension"]))
    hypertension = 1 if hypertension_label == "Yes" else 0
    age = parse_optional_float("Age", age_text, input_errors)
    apache2 = parse_optional_float("APACHE II score", apache2_text, input_errors)
    temperature = parse_optional_float("Temperature", temperature_text, input_errors)
    pulse_rate = parse_optional_float("Pulse rate", pulse_rate_text, input_errors)
    for message in input_errors:
        st.error(message)

    baseline = {
        "age": age,
        "apache2": apache2,
        "temperature": temperature,
        "pulse_rate": pulse_rate,
        "hypertension": hypertension,
    }

    st.subheader("2. Enter current laboratory panel")
    next_index = min(len(st.session_state.panels), len(CFG["landmarks"]) - 1)
    all_entered = len(st.session_state.panels) >= len(CFG["landmarks"])

    if all_entered:
        st.success("All scheduled laboratory panels have been entered.")
    else:
        next_landmark = CFG["landmarks"][next_index]
        step_number = len(st.session_state.panels) + 1
        st.markdown(
            f"""
            <div class="step-chip">Step {step_number}</div>
            <div class="step-title">Enter {html.escape(next_landmark['label'])} laboratory values</div>
            <div class="hint-text">Click the update button after this panel is available. The next panel will open automatically.</div>
            """,
            unsafe_allow_html=True,
        )
        with st.form(key=f"panel_form_{next_landmark['id']}_{version}"):
            lc1, lc2 = st.columns(2)
            input_values = {}
            lab_errors = []
            defaults = blank_panel_values(next_index)
            for lab_index, lab in enumerate(CFG["labs"]):
                column = lc1 if lab_index % 2 == 0 else lc2
                text_value = number_text_input(
                    column,
                    f'{LAB_LABELS.get(lab["key"], lab["label"])} ({lab["unit"]})',
                    key=f'input_{next_landmark["id"]}_{lab["key"]}_{version}',
                    default_value=defaults[lab["key"]],
                )
                input_values[lab["key"]] = parse_optional_float(LAB_LABELS.get(lab["key"], lab["label"]), text_value, lab_errors)
            submitted = st.form_submit_button("Update risk with this panel", type="primary")
            if submitted:
                if lab_errors:
                    for message in lab_errors:
                        st.error(message)
                elif all(is_missing(value) for value in input_values.values()):
                    st.warning("Enter at least one laboratory value before updating risk.")
                else:
                    st.session_state.panels.append(
                        {
                            "index": next_index,
                            "landmark_id": next_landmark["id"],
                            "label": next_landmark["label"],
                            "hour": next_landmark["hour"],
                            "values": input_values,
                        }
                    )
                    st.rerun()

    rc1, rc2 = st.columns(2)
    if rc1.button("Start over", use_container_width=True):
        st.session_state.panels = []
        st.rerun()
    if rc2.button("Remove last panel", use_container_width=True, disabled=len(st.session_state.panels) == 0):
        st.session_state.panels = st.session_state.panels[:-1]
        st.rerun()

    if st.session_state.panels:
        st.subheader("Saved laboratory panels")
        render_table(
            ["Panel", "Time", "PLT", "WBC", "LYMPH", "AST", "LDH", "Creatinine", "Urea"],
            saved_panel_rows(st.session_state.panels),
        )

results = []
trajectory_rows = []
top_drivers = []
current = None
if st.session_state.panels:
    matrix = build_matrix_from_panels(st.session_state.panels)
    for panel in st.session_state.panels:
        result = calculate_landmark(baseline, matrix, panel["index"])
        results.append(result)
    current = results[-1]
    trajectory_rows = [{"landmark": r["landmark"], "hour": r["landmark"]["hour"], "risk": r["risk"]} for r in results]
    top_drivers = sorted(current["contributions"], key=lambda item: abs(item["contribution"]), reverse=True)[:10]

with right:
    st.subheader("3. Current risk")
    if current is None:
        st.info("No risk estimate yet. Enter the first laboratory panel and click the update button.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Latest update", current["landmark"]["label"])
        m2.metric("Mortality risk", f'{current["risk"] * 100:.1f}%')
        m3.metric("Risk category", risk_stratum(current["risk"]))

    st.subheader("Risk trend")
    render_curve(trajectory_rows)
    if trajectory_rows:
        render_table(
            ["Panel", "Hour", "Predicted mortality risk"],
            [[row["landmark"]["id"], row["hour"], f'{row["risk"] * 100:.1f}%'] for row in trajectory_rows],
        )

    st.subheader("Why is the risk changing?")
    render_driver_chart(top_drivers[:8])
    if top_drivers:
        with st.expander("Show numeric contribution details"):
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
