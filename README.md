# SFTS Dynamic Risk Monitor

This folder contains a research prototype for demonstrating the locked Model 3 dynamic landmark mortality-risk framework.

## Streamlit Cloud deployment

Deploy these files to Streamlit Cloud:

- `streamlit_app.py`
- `requirements.txt`
- `model3_config.js`

Recommended Streamlit settings:

- Main file path: `streamlit_app.py`
- Python version: any current Streamlit-supported Python 3 version
- Visibility: public, if the URL is intended for open demonstration

## Local use

Run:

```bash
streamlit run streamlit_app.py
```

The original static prototype can also be opened through `index.html`.
No patient data are uploaded or saved by the local prototype.

## Boundary

This is a manuscript and research demonstration prototype only. It is not a validated clinical decision-support system and must not be used as a standalone clinical decision tool.

## Model

The page uses the exported Model 3 intercept, non-zero coefficients, preprocessing parameters, landmark definitions and candidate risk thresholds from the formal analysis outputs.
