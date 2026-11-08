# Скрипты

## download_hdfs_v1.py

Скачивает архив HDFS_v1 с [Zenodo](https://zenodo.org/records/8196385), сохраняет
его в `data/loghub/HDFS_v1.zip` и распаковывает в `data/loghub/HDFS_v1/`.
Если архив уже есть, повторное скачивание пропускается.

Запуск из корня проекта:

```bash
python scripts/download_hdfs_v1.py
```
