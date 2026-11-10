from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile, is_zipfile

from tqdm import tqdm


url = "https://zenodo.org/records/8196385/files/HDFS_v1.zip?download=1"
data_dir = Path(__file__).resolve().parents[1] / "data" / "loghub"
archive_path = data_dir / "HDFS_v1.zip"

data_dir.mkdir(parents=True, exist_ok=True)


def progress_hook(block_num, block_size, total_size):
    if total_size > 0:
        progress.total = total_size

    progress.update(
        max(0, block_num * block_size - progress.n)
    )


if not archive_path.exists() or not is_zipfile(archive_path):
    archive_path.unlink(missing_ok=True)

    print("Downloading HDFS_v1...")

    with tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc="HDFS_v1.zip",
    ) as progress:
        try:
            urlretrieve(url, archive_path, reporthook=progress_hook)
        except Exception:
            archive_path.unlink(missing_ok=True)
            raise

if not is_zipfile(archive_path):
    archive_path.unlink(missing_ok=True)
    raise RuntimeError("Downloaded file is not a valid ZIP archive")

print("Extracting HDFS_v1...")

with ZipFile(archive_path) as archive:
    archive.extractall(data_dir / "HDFS_v1")

print(f"Done: {data_dir / 'HDFS_v1'}")