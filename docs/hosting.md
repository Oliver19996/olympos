# 外部公開

画面とAPIを1つのサービスで公開できます。回答者にはそのURLだけ渡せば十分です。運営KPIは `?ops=1` です。

## おすすめ

1. **[Render](https://render.com/)** — このリポジトリを接続し、`render.yaml` のまま Web Service を作る。無料枠あり。Phase 0 のアンケート公開に一番合う。
2. **[Railway](https://railway.app/)** — GitHub連携が速く、デプロイも簡単。無料枠は制限が変わりやすい。
3. **[Fly.io](https://fly.io/)** — 東京リージョンがあり、日本からの表示が速い。Dockerが必要。

GitHub Pages は静的ファイルだけなので、API（登録・アンケート）は動きません。画面だけ置きたい場合の補助です。

## Renderでの手順

1. https://github.com/Oliver19996/olympos を Render に接続する
2. Docker ランタイムでデプロイする（`render.yaml` を使う）
3. 発行された `https://xxxx.onrender.com` を回答者に配る
4. 運営は `https://xxxx.onrender.com/?ops=1`

無料枠はスリープすることがあります。最初のアクセスで数十秒かかることがあります。

## ローカル確認

API（8000）が `web/` も配信します。`http://localhost:8000` でも画面を開けます。
