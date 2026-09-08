# 外部公開

画面とAPIを1つのサービスで公開できます。回答者にはそのURLだけ渡せば十分です。運営KPIは `?ops=1` です。

## おすすめ

1. **[Render](https://render.com/)** — このリポジトリを接続し、`render.yaml` のまま Web Service を作る。無料枠あり。Phase 0 のアンケート公開に一番合う。
2. **[Railway](https://railway.app/)** — GitHub連携が速く、デプロイも簡単。無料枠は制限が変わりやすい。
3. **[Fly.io](https://fly.io/)** — 東京リージョンがあり、日本からの表示が速い。Dockerが必要。

GitHub Pages は静的ファイルだけなので、API（登録・アンケート）は動きません。画面だけ置きたい場合の補助です。

## Renderで必要なセットアップ

GitHub の https://github.com/Oliver19996/olympos を Render に繋ぐだけで動きます。似顔絵は既定の `mock` なので **APIキーは不要** です。`backend/.env` も Render には上げません。

### 1. アカウントとGitHub連携

1. [Render](https://render.com/) にサインアップする
2. Dashboard で GitHub を接続し、`Oliver19996/olympos` を許可する

### 2. サービスの作り方（どちらか）

**A. Blueprint（推奨）**

1. Dashboard → **New** → **Blueprint**
2. リポジトリ `olympos` を選ぶ
3. `render.yaml` を読み取り、Web Service `olympos` が作られる

**B. 手動**

1. **New** → **Web Service**
2. リポジトリ `olympos`、ランタイム **Docker**
3. 下記の環境変数を設定する。ディスクは付けない（無料枠では不可）

### 3. 環境変数

`render.yaml` に入っている値です。手動作成時は同じものを入れます。

| 変数 | 値 | 用途 |
| --- | --- | --- |
| `OLYMPOS_ENV` | `production` | 本番扱い |
| `OLYMPOS_CORS_ORIGINS` | `*` | 同一オリジン配信ならこれで足りる |
| `OLYMPOS_DB_PATH` | `./data/olympos_phase0.db` | SQLite の保存先（コンテナ内） |
| `PORTRAIT_PROVIDER` | `mock` | 外部似顔絵APIなし |

似顔絵を実接続する場合だけ `PORTRAIT_PROVIDER=http` と URL／キーを追加します。Phase 0 では不要です。

### 4. ディスクは無料では付けない

`render.yaml` は無料枠向けで、Persistent Disk は入れていません。無料で Blueprint を再実行してください。

SQLite はコンテナ内の `./data/olympos_phase0.db` に保存されます。無料Webは再起動・スリープ・再デプロイでファイルが消えます。

回答を残したいときだけ、デプロイ成功後に：

1. プランを **Starter**（有料）へ上げる
2. Persistent Disk を付ける（mount `/data`、1GB）
3. 環境変数 `OLYMPOS_DB_PATH` を `/data/olympos_phase0.db` に変える

### 5. 公開後

1. 発行URL `https://xxxx.onrender.com` を回答者に配る
2. 運営は `https://xxxx.onrender.com/?ops=1`
3. 初回アクセスはスリープ解除で数十秒かかることがある（無料枠）

ヘルスチェックは `/health` です。

## ローカル確認

API（8000）が `web/` も配信します。`http://localhost:8000` でも画面を開けます。
