import csv
import logging
import re
from pathlib import Path

from drain3 import TemplateMiner
from drain3.masking import MaskingInstruction
from drain3.template_miner_config import TemplateMinerConfig

logger = logging.getLogger(__name__)

BLOCK_ID_REGEX = r"\bblk_-?\d+\b"


class LogEntry:
    def __init__(self, line: str, line_no: int):
        self.line_no = line_no
        self.raw_line = line.rstrip("\r\n")

        (
            self.date,
            self.time,
            self.pid,
            self.level,
            self.component,
            self.message,
        ) = self.raw_line.split(maxsplit=5)

        self.block_id = re.search(BLOCK_ID_REGEX, self.message).group(0)

        self.prepared_message = self.message.replace(
            ":Transmitted",
            ": Transmitted",
        )

        self.masked_message = None
        self.cluster_id = None


def create_miner() -> TemplateMiner:
    config = TemplateMinerConfig()

    config.masking_instructions = [
        # ID блока HDFS: blk_123 или blk_-123; знак минус необязателен.
        MaskingInstruction(BLOCK_ID_REGEX, "BLOCK"),
        # IPv4-адрес с необязательным портом: 10.20.30.40 или 10.20.30.40:50010.
        MaskingInstruction(r"\b(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?\b", "ADDR"),
    ]

    config.drain_sim_th = 0.6

    return TemplateMiner(config=config)


def process_log(log_path: Path, events_path: Path, miner: TemplateMiner) -> None:
    event_fields = [
        "line_no",
        "raw_line",
        "date",
        "time",
        "pid",
        "level",
        "component",
        "message",
        "block_id",
        "prepared_message",
        "masked_message",
        "cluster_id",
    ]

    with events_path.open("w", encoding="utf-8", newline="") as events_file:
        events_writer = csv.DictWriter(events_file, fieldnames=event_fields)
        events_writer.writeheader()

        with log_path.open(encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                entry = LogEntry(line, line_no)

                result = miner.add_log_message(entry.prepared_message)

                entry.masked_message = miner.masker.mask(entry.prepared_message)
                entry.cluster_id = result["cluster_id"]

                events_writer.writerow(vars(entry))
                if line_no % 1_000_000 == 0:
                    logger.info(
                        "Обработано строк: %s; шаблонов: %s",
                        line_no,
                        len(miner.drain.clusters),
                    )


def save_templates(miner: TemplateMiner, templates_path: Path) -> None:
    clusters = sorted(miner.drain.clusters, key=lambda cluster: cluster.size, reverse=True)

    rows = []

    for cluster in clusters:
        row = {
            "cluster_id": cluster.cluster_id,
            "template": cluster.get_template(),
            "count": cluster.size,
        }
        rows.append(row)

    fieldnames = ["cluster_id", "template", "count"]

    with templates_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    project_dir = Path(__file__).resolve().parents[2]
    log_path = project_dir / "data/loghub/HDFS_v1/HDFS.log"

    output_dir = project_dir / "data/processed/drain3"
    output_dir.mkdir(parents=True, exist_ok=True)

    events_path = output_dir / "events.csv"
    templates_path = output_dir / "HDFS.log_templates.csv"

    logger.info("Начинаю обработку: %s", log_path)

    miner = create_miner()

    process_log(log_path, events_path, miner)
    save_templates(miner, templates_path)
    logger.info(
        "Готово: %s событий, %s шаблонов. Результаты: %s",
        sum(cluster.size for cluster in miner.drain.clusters),
        len(miner.drain.clusters),
        output_dir,
    )


if __name__ == "__main__":
    main()
