<div align="center">

# Anomaly Detection in Distributed System Logs

**Year-long project, MSc programme "Artificial Intelligence", Faculty of Computer Science, HSE University, 2026/27**

Topic 85 "Anomaly detection in distributed cloud data"

![Stage](https://img.shields.io/badge/stage-CP1-2ea44f)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Data](https://img.shields.io/badge/data-loghub%20HDFS__v1-orange)

[Русский](README.md) | **English**

[Problem](#problem) | [Team](#team) | [Plan](#checkpoint-plan) | [Data](#data) | [References](#references)

</div>

---

## Problem

Nodes of a distributed system write logs, text journals of events. Failures in a
cluster are frequent and diverse, while labelled data is scarce. The goal of the
project is to build a model that learns the **normal** behaviour of the system
from its logs and flags sessions that do not look like it.

### Principles agreed with the supervisor

| Aspect | Agreement |
| --- | --- |
| **Training** | models are trained on normal data; labels are used only for evaluation |
| **Metric** | the main one is **recall**: a missed failure costs more than a false alarm |
| **Threshold** | chosen for a target recall, not for maximum F1 |
| **Methods** | from simple ones (PCA, Isolation Forest) to neural ones (DeepLog, LogAnomaly, transformers) |

## Team

| Member | GitHub | Telegram |
| --- | --- | --- |
| Artem Pogosian | [@iamartempn](https://github.com/iamartempn) | [@iamartempn](https://t.me/iamartempn) |
| Stepan Polyakov | [@Spake4](https://github.com/Spake4) | [@kurulltyrbina](https://t.me/kurulltyrbina) |
| Arkadiy Shevyrov | [@ArkadiyShevyrov](https://github.com/ArkadiyShevyrov) | [@ArkadiyShevyrov](https://t.me/ArkadiyShevyrov) |
| Tabriz Musaev | [@tamumusaev](https://github.com/tamumusaev) | [@musatab89](https://t.me/musatab89) |

**Supervisor:** Dmitrii Kachkin, Telegram [@KachkinDmitrii](https://t.me/KachkinDmitrii)

## Checkpoint plan

Deadlines follow the programme's checkpoint schedule for 2026/27. The CP1
deadline is final; the others are announced as tentative.

| Stage | Deadline | Content | Status |
| --- | --- | --- | :---: |
| **CP1** | 06.10.2026 | meeting the supervisor, final topic, year plan, repository | ✅ |
| **CP2** | 27.10.2026 | exploratory analysis of HDFS_v1 (loghub): log parsing, session assembly, features, distributions and relationships, visualisation, conclusions | ⏳ |
| **CP3** | 27.11.2026 | first ML models: choice of metric; baselines — a rule and PCA; Isolation Forest, next-event model on n-grams; logistic regression as an upper bound; hyperparameter and threshold tuning for recall | ⏳ |
| **CP4** | 15.12.2026 | ML service on FastAPI: input — log lines of a session, output — a score and a decision; also counts as homework for the "Development Tools" course | ⏳ |
| **Pre-defence** | 10–15.01.2027 | talk on the semester's work and the plan for the second semester | ⏳ |
| **CP5** | 15.03.2027 | model improvement: windows instead of sessions, time features, data cleaning and extension — a second dataset (BGL or HDFS_v3), possibly our own logs with injected anomalies | ⏳ |
| **CP6** | 05.05.2027 | neural networks, one approach per member: DeepLog, LogAnomaly, a transformer, a fourth of choice; comparison with the ML models | ⏳ |
| **CP7** | before the defence, date TBA | MLflow and reproducibility, retraining and logging the best model, analysis of missed anomalies and robustness, threshold study | ⏳ |
| **Defence** | 13–20.06.2027 | talk on the year's results and a service demo | ⏳ |

## Data

The main dataset is **HDFS_v1** from [loghub](https://github.com/logpai/loghub):
logs of the Hadoop Distributed File System.

| Log lines | Sessions (blocks) | Anomalous share | Labels |
| ---: | ---: | ---: | --- |
| ~11 M | 575,061 | 2.93% | per block |

Data is not stored in the repository.

## References

1. He et al., 2016. *Experience Report: System Log Analysis for Anomaly Detection.* ISSRE
2. Xu et al., 2009. *Detecting Large-Scale System Problems by Mining Console Logs.* SOSP
3. Du et al., 2017. *DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning.* CCS
4. Meng et al., 2019. *LogAnomaly: Unsupervised Detection of Sequential and Quantitative Anomalies in Unstructured Logs.* IJCAI
5. Zhu et al., 2023. *Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics.* ISSRE

Baseline code: [loglizer](https://github.com/logpai/loglizer), [deep-loglizer](https://github.com/logpai/deep-loglizer).
