from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile


url = "https://zenodo.org/records/8196385/files/HDFS_v1.zip?download=1"
data_dir = Path(__file__).resolve().parents[1] / "data" / "loghub"
archive_path = data_dir / "HDFS_v1.zip"

data_dir.mkdir(parents=True, exist_ok=True)

if not archive_path.exists():
    print("Downloading HDFS_v1...", flush=True)
    urlretrieve(url, archive_path)

print("Extracting HDFS_v1...", flush=True)
with ZipFile(archive_path) as archive:
    archive.extractall(data_dir / "HDFS_v1")

print(f"Done: {data_dir / 'HDFS_v1'}")
