# OLYMPOS Phase 0

Cursor 用のプロジェクトマップ。詳細は `README.md`。

| 場所 | 役割 |
| --- | --- |
| `backend/app/` | FastAPI API。設定は `config.py`、秘密情報は `backend/.env` |
| `backend/tests/` | pytest（`PYTHONPATH=backend`） |
| `web/` | 検証用静的 Web（`index.html` / `app.js`） |
| `flutter/lib/` | iPhone 向け検証アプリ |
| `scripts/seed_demo.py` | デモデータ投入 |
| `docs/api.http` | REST Client で API 手動実行 |
| `docs/github.md` | GitHub 初回 push 手順 |

起動: `make setup` → `make api` と `make web`。ワークスペースは `OLYMPOS.code-workspace` を開く。
