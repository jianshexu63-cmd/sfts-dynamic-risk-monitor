const MODEL3_CONFIG = {
  "modelName": "SFTS Dynamic Risk Monitor - Model 3",
  "modelRole": "Research prototype only; not for clinical decision-making.",
  "intercept": -2.348907715220354,
  "coefficients": [
    {
      "feature": "age",
      "coefficient": 0.22947525180494754,
      "selected": 1
    },
    {
      "feature": "apache2",
      "coefficient": 0.37407197451439356,
      "selected": 1
    },
    {
      "feature": "temperature",
      "coefficient": 0.03360340634317326,
      "selected": 1
    },
    {
      "feature": "pulse_rate",
      "coefficient": 0.122843890718828,
      "selected": 1
    },
    {
      "feature": "hypertension",
      "coefficient": -0.07050623609929786,
      "selected": 1
    },
    {
      "feature": "PLT_latest",
      "coefficient": -0.26345539561527576,
      "selected": 1
    },
    {
      "feature": "WBC_latest",
      "coefficient": -0.0027880608016132096,
      "selected": 1
    },
    {
      "feature": "LYMPH_ABS_latest",
      "coefficient": -0.03519346622858174,
      "selected": 1
    },
    {
      "feature": "AST_latest",
      "coefficient": 0.3009815543360751,
      "selected": 1
    },
    {
      "feature": "LDH_latest",
      "coefficient": 0.4938822087545455,
      "selected": 1
    },
    {
      "feature": "CREA_latest",
      "coefficient": 0.10917467148795168,
      "selected": 1
    },
    {
      "feature": "UREA_latest",
      "coefficient": 0.2356574777414144,
      "selected": 1
    },
    {
      "feature": "LDH_change_from_first",
      "coefficient": 0.18606149538140032,
      "selected": 1
    },
    {
      "feature": "PLT_measure_n_so_far",
      "coefficient": -0.0004934649351939795,
      "selected": 1
    },
    {
      "feature": "WBC_measure_n_so_far",
      "coefficient": -0.006985387586249767,
      "selected": 1
    },
    {
      "feature": "LYMPH_ABS_measure_n_so_far",
      "coefficient": -0.010275117800194283,
      "selected": 1
    },
    {
      "feature": "CREA_measure_n_so_far",
      "coefficient": -0.08552748356819684,
      "selected": 1
    },
    {
      "feature": "UREA_measure_n_so_far",
      "coefficient": -0.0939688240736342,
      "selected": 1
    },
    {
      "feature": "CREA_time_since_last",
      "coefficient": -0.06108803562259434,
      "selected": 1
    },
    {
      "feature": "UREA_time_since_last",
      "coefficient": -0.05944747171792247,
      "selected": 1
    }
  ],
  "preprocessing": {
    "age": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 67.0,
      "center": 64.89917254060681,
      "scale": 10.480629818847369,
      "missingIndicatorCreated": false,
      "missingIndicatorName": null
    },
    "male": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 0.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": false,
      "missingIndicatorName": null
    },
    "apache2": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 11.0,
      "center": 10.991112473184202,
      "scale": 2.6830726196505568,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_apache2"
    },
    "map": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 86.3,
      "center": 87.00006129328838,
      "scale": 16.66379544028624,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_map"
    },
    "temperature": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 37.0,
      "center": 37.31700888752682,
      "scale": 0.8834721241195717,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_temperature"
    },
    "pulse_rate": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 80.0,
      "center": 81.19889672080907,
      "scale": 14.358785243927784,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_pulse_rate"
    },
    "respiratory_rate": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 20.0,
      "center": 20.208703646950664,
      "scale": 5.821029783691221,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_respiratory_rate"
    },
    "admission_condition_yes": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 1.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": false,
      "missingIndicatorName": null
    },
    "hypertension": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 0.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_hypertension"
    },
    "diabetes": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 0.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_diabetes"
    },
    "heart_disease": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 0.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_heart_disease"
    },
    "hepatitis": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 0.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_hepatitis"
    },
    "tuberculosis": {
      "variableType": "binary",
      "log1pTransform": false,
      "imputationMethod": "mode",
      "imputationValue": 0.0,
      "center": null,
      "scale": null,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_tuberculosis"
    },
    "PLT_latest": {
      "variableType": "continuous",
      "log1pTransform": true,
      "imputationMethod": "median",
      "imputationValue": 4.060443010546419,
      "center": 4.099685134566225,
      "scale": 0.5901388656329027,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_PLT_latest"
    },
    "WBC_latest": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 4.74,
      "center": 5.70589334967821,
      "scale": 3.754513081168631,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_WBC_latest"
    },
    "LYMPH_ABS_latest": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.94,
      "center": 1.0933741955255898,
      "scale": 0.7268450064694474,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LYMPH_ABS_latest"
    },
    "AST_latest": {
      "variableType": "continuous",
      "log1pTransform": true,
      "imputationMethod": "median",
      "imputationValue": 4.77912349311153,
      "center": 4.848374399645928,
      "scale": 0.9095448325417427,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_AST_latest"
    },
    "LDH_latest": {
      "variableType": "continuous",
      "log1pTransform": true,
      "imputationMethod": "median",
      "imputationValue": 6.29156913955832,
      "center": 6.393085362805325,
      "scale": 0.6746607375455426,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LDH_latest"
    },
    "CREA_latest": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 70.0,
      "center": 79.92418020226788,
      "scale": 48.433232538801136,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_CREA_latest"
    },
    "UREA_latest": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 5.03,
      "center": 6.096064970885688,
      "scale": 4.085560532706491,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_UREA_latest"
    },
    "PLT_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.0,
      "center": 14.430891817345977,
      "scale": 45.06687641173946,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_PLT_change_from_first"
    },
    "WBC_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.5750000000000002,
      "center": 1.6189871284094393,
      "scale": 4.193670004996745,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_WBC_change_from_first"
    },
    "LYMPH_ABS_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.16999999999999996,
      "center": 0.32505363162733675,
      "scale": 0.7190996323905636,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LYMPH_ABS_change_from_first"
    },
    "AST_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.0,
      "center": 4.694759423843169,
      "scale": 239.05111224890686,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_AST_change_from_first"
    },
    "LDH_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.0,
      "center": 77.23812442537596,
      "scale": 640.9801966525253,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LDH_change_from_first"
    },
    "CREA_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.0,
      "center": -4.218449279803835,
      "scale": 29.655963289025976,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_CREA_change_from_first"
    },
    "UREA_change_from_first": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 0.0,
      "center": -0.2694391664112738,
      "scale": 2.9063422726489594,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_UREA_change_from_first"
    },
    "PLT_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 3.0,
      "center": 2.943916641127815,
      "scale": 1.7465685675888825,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_PLT_measure_n_so_far"
    },
    "WBC_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 3.0,
      "center": 2.9448360404535676,
      "scale": 1.747738355262445,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_WBC_measure_n_so_far"
    },
    "LYMPH_ABS_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 3.0,
      "center": 2.9445295740116393,
      "scale": 1.7469391514312314,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LYMPH_ABS_measure_n_so_far"
    },
    "AST_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 2.0,
      "center": 2.6484829911124725,
      "scale": 1.5666091574606977,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_AST_measure_n_so_far"
    },
    "LDH_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 2.0,
      "center": 2.483910511798958,
      "scale": 1.4884498396517458,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LDH_measure_n_so_far"
    },
    "CREA_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 2.0,
      "center": 2.342016549187867,
      "scale": 1.4254743669343077,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_CREA_measure_n_so_far"
    },
    "UREA_measure_n_so_far": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 2.0,
      "center": 2.3435488813974774,
      "scale": 1.4271478487546776,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_UREA_measure_n_so_far"
    },
    "PLT_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 10.233333333333334,
      "center": 17.18040147103892,
      "scale": 17.240785120082908,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_PLT_time_since_last"
    },
    "WBC_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 10.233333333333334,
      "center": 17.18040147103892,
      "scale": 17.240785120082908,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_WBC_time_since_last"
    },
    "LYMPH_ABS_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 10.233333333333334,
      "center": 17.18040147103892,
      "scale": 17.240785120082908,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LYMPH_ABS_time_since_last"
    },
    "AST_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 19.575000000000003,
      "center": 22.601305036265188,
      "scale": 22.109104874956067,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_AST_time_since_last"
    },
    "LDH_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 19.516666666666666,
      "center": 22.669654714475442,
      "scale": 22.20483752320203,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_LDH_time_since_last"
    },
    "CREA_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 21.141666666666666,
      "center": 25.88427060986821,
      "scale": 25.48520462289517,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_CREA_time_since_last"
    },
    "UREA_time_since_last": {
      "variableType": "continuous",
      "log1pTransform": false,
      "imputationMethod": "median",
      "imputationValue": 21.141666666666666,
      "center": 25.88427060986821,
      "scale": 25.48520462289517,
      "missingIndicatorCreated": true,
      "missingIndicatorName": "miss_UREA_time_since_last"
    }
  },
  "landmarks": [
    {
      "id": "L0",
      "hour": 24,
      "label": "L0 / 0-24 h"
    },
    {
      "id": "L48",
      "hour": 48,
      "label": "L48 / 48 h"
    },
    {
      "id": "L72",
      "hour": 72,
      "label": "L72 / 72 h"
    },
    {
      "id": "L120",
      "hour": 120,
      "label": "L120 / 120 h"
    },
    {
      "id": "L168",
      "hour": 168,
      "label": "L168 / 168 h"
    }
  ],
  "labs": [
    {
      "key": "PLT",
      "label": "PLT 血小板",
      "unit": "10^9/L"
    },
    {
      "key": "WBC",
      "label": "WBC 白细胞",
      "unit": "10^9/L"
    },
    {
      "key": "LYMPH_ABS",
      "label": "LYMPH 淋巴细胞绝对值",
      "unit": "10^9/L"
    },
    {
      "key": "AST",
      "label": "AST",
      "unit": "U/L"
    },
    {
      "key": "LDH",
      "label": "LDH",
      "unit": "U/L"
    },
    {
      "key": "CREA",
      "label": "肌酐 CREA",
      "unit": "umol/L"
    },
    {
      "key": "UREA",
      "label": "尿素 UREA",
      "unit": "mmol/L"
    }
  ],
  "riskStrata": [
    {
      "name": "Low",
      "label": "低风险",
      "min": 0,
      "max": 0.1,
      "color": "#2f7d5c"
    },
    {
      "name": "Intermediate",
      "label": "中风险",
      "min": 0.1,
      "max": 0.3,
      "color": "#b7831f"
    },
    {
      "name": "High",
      "label": "高风险",
      "min": 0.3,
      "max": 1.01,
      "color": "#b83232"
    }
  ],
  "thresholds": [
    {
      "threshold": 0.05,
      "tp": 441,
      "fp": 1520,
      "tn": 1281,
      "fn": 21,
      "sensitivity": 0.9545454545454546,
      "specificity": 0.4573366654766155,
      "ppv": 0.22488526262111166,
      "npv": 0.9838709677419355,
      "youden": 0.41188212002207014,
      "flagged_pct": 0.6009806926141588,
      "event_rate_above_threshold": 0.22488526262111166
    },
    {
      "threshold": 0.1,
      "tp": 408,
      "fp": 902,
      "tn": 1899,
      "fn": 54,
      "sensitivity": 0.8831168831168831,
      "specificity": 0.6779721528025705,
      "ppv": 0.3114503816793893,
      "npv": 0.9723502304147466,
      "youden": 0.5610890359194536,
      "flagged_pct": 0.40147103892123814,
      "event_rate_above_threshold": 0.3114503816793893
    },
    {
      "threshold": 0.15000000000000002,
      "tp": 368,
      "fp": 590,
      "tn": 2211,
      "fn": 94,
      "sensitivity": 0.7965367965367965,
      "specificity": 0.7893609425205284,
      "ppv": 0.38413361169102295,
      "npv": 0.9592190889370933,
      "youden": 0.5858977390573248,
      "flagged_pct": 0.29359485136377567,
      "event_rate_above_threshold": 0.38413361169102295
    },
    {
      "threshold": 0.2,
      "tp": 322,
      "fp": 398,
      "tn": 2403,
      "fn": 140,
      "sensitivity": 0.696969696969697,
      "specificity": 0.8579078900392717,
      "ppv": 0.44722222222222224,
      "npv": 0.94494691309477,
      "youden": 0.5548775870089688,
      "flagged_pct": 0.22065583818571866,
      "event_rate_above_threshold": 0.44722222222222224
    },
    {
      "threshold": 0.25,
      "tp": 281,
      "fp": 270,
      "tn": 2531,
      "fn": 181,
      "sensitivity": 0.6082251082251082,
      "specificity": 0.9036058550517673,
      "ppv": 0.5099818511796733,
      "npv": 0.9332595870206489,
      "youden": 0.5118309632768754,
      "flagged_pct": 0.1688630095004597,
      "event_rate_above_threshold": 0.5099818511796733
    },
    {
      "threshold": 0.3,
      "tp": 241,
      "fp": 197,
      "tn": 2604,
      "fn": 221,
      "sensitivity": 0.5216450216450217,
      "specificity": 0.9296679757229561,
      "ppv": 0.5502283105022832,
      "npv": 0.9217699115044248,
      "youden": 0.4513129973679777,
      "flagged_pct": 0.13423230156297886,
      "event_rate_above_threshold": 0.5502283105022832
    },
    {
      "threshold": 0.35000000000000003,
      "tp": 204,
      "fp": 150,
      "tn": 2651,
      "fn": 258,
      "sensitivity": 0.44155844155844154,
      "specificity": 0.9464476972509818,
      "ppv": 0.576271186440678,
      "npv": 0.9113097284290134,
      "youden": 0.38800613880942336,
      "flagged_pct": 0.10848912044131168,
      "event_rate_above_threshold": 0.576271186440678
    },
    {
      "threshold": 0.4,
      "tp": 175,
      "fp": 109,
      "tn": 2692,
      "fn": 287,
      "sensitivity": 0.3787878787878788,
      "specificity": 0.9610853266690468,
      "ppv": 0.6161971830985915,
      "npv": 0.9036589459550185,
      "youden": 0.33987320545692556,
      "flagged_pct": 0.08703646950658903,
      "event_rate_above_threshold": 0.6161971830985915
    },
    {
      "threshold": 0.45,
      "tp": 152,
      "fp": 80,
      "tn": 2721,
      "fn": 310,
      "sensitivity": 0.329004329004329,
      "specificity": 0.9714387718671903,
      "ppv": 0.6551724137931034,
      "npv": 0.8977235235895744,
      "youden": 0.3004431008715194,
      "flagged_pct": 0.07110021452650934,
      "event_rate_above_threshold": 0.6551724137931034
    },
    {
      "threshold": 0.5,
      "tp": 132,
      "fp": 63,
      "tn": 2738,
      "fn": 330,
      "sensitivity": 0.2857142857142857,
      "specificity": 0.9775080328454123,
      "ppv": 0.676923076923077,
      "npv": 0.8924380704041721,
      "youden": 0.263222318559698,
      "flagged_pct": 0.05976095617529881,
      "event_rate_above_threshold": 0.676923076923077
    },
    {
      "threshold": 0.55,
      "tp": 115,
      "fp": 49,
      "tn": 2752,
      "fn": 347,
      "sensitivity": 0.24891774891774893,
      "specificity": 0.982506247768654,
      "ppv": 0.7012195121951219,
      "npv": 0.888028396256857,
      "youden": 0.2314239966864029,
      "flagged_pct": 0.05026049647563592,
      "event_rate_above_threshold": 0.7012195121951219
    },
    {
      "threshold": 0.6000000000000001,
      "tp": 105,
      "fp": 34,
      "tn": 2767,
      "fn": 357,
      "sensitivity": 0.22727272727272727,
      "specificity": 0.9878614780435558,
      "ppv": 0.7553956834532374,
      "npv": 0.8857234314980794,
      "youden": 0.21513420531628302,
      "flagged_pct": 0.04259883542752069,
      "event_rate_above_threshold": 0.7553956834532374
    },
    {
      "threshold": 0.6500000000000001,
      "tp": 91,
      "fp": 23,
      "tn": 2778,
      "fn": 371,
      "sensitivity": 0.19696969696969696,
      "specificity": 0.9917886469118172,
      "ppv": 0.7982456140350878,
      "npv": 0.8821848205779612,
      "youden": 0.18875834388151413,
      "flagged_pct": 0.03493717437940545,
      "event_rate_above_threshold": 0.7982456140350878
    },
    {
      "threshold": 0.7000000000000001,
      "tp": 74,
      "fp": 18,
      "tn": 2783,
      "fn": 388,
      "sensitivity": 0.16017316017316016,
      "specificity": 0.9935737236701179,
      "ppv": 0.8043478260869565,
      "npv": 0.8776411226742352,
      "youden": 0.15374688384327806,
      "flagged_pct": 0.02819491265706405,
      "event_rate_above_threshold": 0.8043478260869565
    },
    {
      "threshold": 0.7500000000000001,
      "tp": 58,
      "fp": 12,
      "tn": 2789,
      "fn": 404,
      "sensitivity": 0.12554112554112554,
      "specificity": 0.9957158157800785,
      "ppv": 0.8285714285714286,
      "npv": 0.8734732226746007,
      "youden": 0.12125694132120413,
      "flagged_pct": 0.021452650934722647,
      "event_rate_above_threshold": 0.8285714285714286
    },
    {
      "threshold": 0.8,
      "tp": 43,
      "fp": 6,
      "tn": 2795,
      "fn": 419,
      "sensitivity": 0.09307359307359307,
      "specificity": 0.9978579078900393,
      "ppv": 0.8775510204081632,
      "npv": 0.8696328562538892,
      "youden": 0.09093150096363223,
      "flagged_pct": 0.015016855654305853,
      "event_rate_above_threshold": 0.8775510204081632
    }
  ]
};
