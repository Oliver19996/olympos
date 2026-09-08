"""環境変数と秘密情報の読み込み。APIキーは backend/.env に置く。"""
import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_ROOT / ".env")


def _csv(name: str, default: str) -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


OLYMPOS_ENV = os.getenv("OLYMPOS_ENV", "development")
DB_PATH = Path(os.getenv("OLYMPOS_DB_PATH", "./data/olympos_phase0.db"))
CORS_ORIGINS = _csv("OLYMPOS_CORS_ORIGINS", "http://localhost:8080")
PORTRAIT_PROVIDER = os.getenv("PORTRAIT_PROVIDER", "mock")
PORTRAIT_API_URL = os.getenv("PORTRAIT_API_URL", "")
PORTRAIT_API_KEY = os.getenv("PORTRAIT_API_KEY", "")
PORTRAIT_DELETE_AFTER_SECONDS = int(os.getenv("PORTRAIT_DELETE_AFTER_SECONDS", "3600"))
