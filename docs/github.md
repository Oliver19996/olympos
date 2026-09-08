# GitHub 公開手順

秘密情報（`backend/.env`）はコミットされません。テンプレートだけがリポジトリに入ります。

## 初回

```bash
git add -A
git status   # .env が含まれていないことを確認
git commit -m "Initial commit: OLYMPOS Phase 0"

gh repo create olympos-phase0 --private --source=. --remote=origin --push
```

公開リポジトリにする場合は `--public` を使います。APIキーを入れた `.env` は絶対に push しないでください。

## 以降

```bash
git add -A
git commit -m "変更内容"
git push origin HEAD
```

CI は `.github/workflows/ci.yml` が push / PR でバックエンドテストと JS 構文チェックを実行します。
