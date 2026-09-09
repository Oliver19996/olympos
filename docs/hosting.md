# 外部公開

画面とAPIを1つのサービスで公開できます。回答者にはそのURLだけ渡せば十分です。運営KPIは `?ops=1` です。

## おすすめ

1. **[Render](https://render.com/)** — このリポジトリを接続し、`render.yaml` のまま Web Service を作る。Phase 0 のアンケート公開に一番合う。
2. **[Railway](https://railway.app/)** — GitHub連携が速く、デプロイも簡単。無料枠の条件は変わりやすい。
3. **[Fly.io](https://fly.io/)** — 東京リージョンがあり、日本からの表示が速い。Dockerが必要。

GitHub Pages は静的ファイルだけなので、API（登録・アンケート）は動きません。画面だけ置きたい場合の補助です。

## Renderで必要なセットアップ

GitHub の https://github.com/Oliver19996/olympos を Render に繋ぎます。似顔絵は既定の `mock` なので **APIキーは不要** です。`backend/.env` も Render には上げません。

回答を再デプロイ後も残すには **Starter（有料）＋ Persistent Disk** が必要です。無料Webはディスクを付けられず、再起動・再デプロイで SQLite が消えます。

### 1. アカウントとGitHub連携

1. [Render](https://render.com/) にサインアップする
2. 支払い方法を登録する（Starter に必要）
3. Dashboard で GitHub を接続し、`Oliver19996/olympos` を許可する

### 2. 既存の無料サービスを残す場合

いま動いている `olympos` を無料のまま再デプロイすると、集計はまた空になります。Dashboard で次をこの順で行います。

1. サービス `olympos` を開く
2. インスタンスを **Starter** にする
3. **Disks** で Persistent Disk を追加する（Name `olympos-data`、Mount path `/data`、Size 1 GB）
4. Environment の `OLYMPOS_DB_PATH` を `/data/olympos_phase0.db` にする
5. **Manual Deploy** で再デプロイする

ディスクを付けたあとの回答は、以降のデプロイでは消えません。付ける前のコンテナ内データは移行されません。

### 3. 新規作成（Blueprint）

1. Dashboard → **New** → **Blueprint**
2. リポジトリ `olympos` を選ぶ
3. `render.yaml` が Starter と `/data` ディスクを設定する

手動作成する場合はランタイム **Docker** で、下記の環境変数とディスクを同じ内容にします。

### 4. 環境変数

| 変数 | 値 | 用途 |
| --- | --- | --- |
| `OLYMPOS_ENV` | `production` | 本番扱い |
| `OLYMPOS_CORS_ORIGINS` | `*` | 同一オリジン配信ならこれで足りる |
| `OLYMPOS_DB_PATH` | `/data/olympos_phase0.db` | ディスク上の SQLite |
| `PORTRAIT_PROVIDER` | `mock` | 外部似顔絵APIなし |

似顔絵を実接続する場合だけ `PORTRAIT_PROVIDER=http` と URL／キーを追加します。Phase 0 では不要です。

### 5. 公開後

1. 発行URL `https://xxxx.onrender.com` を回答者に配る
2. 運営は `https://xxxx.onrender.com/?ops=1`
3. Starter はスリープしません。ヘルスチェックは `/health` です。

## ローカル確認

API（8000）が `web/` も配信します。`http://localhost:8000` でも画面を開けます。ローカルの集計は `backend/data/olympos_phase0.db` です。
