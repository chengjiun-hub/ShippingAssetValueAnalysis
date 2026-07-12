from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

CLARKSONS_DATA = RAW_DATA / "clarksons"

PUBLIC_DATA = PROCESSED_DATA / "public"
PRIVATE_DATA = PROCESSED_DATA / "private"