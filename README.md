# OLYMPOS Phase 0 Application

20〜39歳を対象に、コンセプト需要、支払意思、AI似顔絵、匿名編成成立率を検証するためのソースコードです。活動エリアは日本全国（47都道府県）から選択します。

> **Phase 0限定**：実課金、本番eKYC、実デート、App Store公開は行いません。

## 構成

```text
backend/     FastAPI + SQLite API
web/         レスポンシブ検証Web
flutter/     iPhone向けFlutter検証アプリ基盤
scripts/     デモデータ投入
```

## 実装済み

- 公開用Webは概要・体験・参加の3タブ。検証KPIは `?ops=1` のみ
- 参加と評価は同一フォーム。プロフィールと感想を一度に送信
- ユーザー向け呼称は主役／共演者（API・DBは `host` / `candidate`）
- 性自認・希望相手は男性／女性／それ以外
- ZEUS／APHRODITEの興味モード（複数可）
- 活動エリアは47都道府県
- 価格受容は共演者2,000円／主役6,000円と、共演者1,000円／主役9,000円
- 申込順を基本とする、主役1名＋共演者6〜7名の匿名編成
- 継続KPI：参加意向60%／支払意思40%／似顔絵承認80%／編成成立70%
- AI似顔絵Provider Adapter（既定はモック。同意は「アプリで使うことへの賛成」）
- 画面とAPIを同一サービスで配信可能（Render 等）

## バックエンド起動

Python 3.12推奨。

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

API仕様：`http://localhost:8000/docs`  
ヘルスチェック：`http://localhost:8000/health`

### テスト

```bash
cd backend
PYTHONPATH=. pytest -q
```

## Web起動

別ターミナルで：

```bash
cd web
python3 -m http.server 8080
```

`http://localhost:8080` または API と同じ `http://localhost:8000` を開きます。

- 回答者：`/`（KPIなし）
- 運営：`/?ops=1`
- 別APIを使う場合：`/?api=https://your-api.example.com`

## アンケートの集計先

送信内容は FastAPI 経由で SQLite に保存します。外部のフォームSaaSには送りません。

| データ | テーブル | 場所 |
| --- | --- | --- |
| 匿名プロフィール | `participants` | ローカル：`backend/data/olympos_phase0.db` |
| 参加意向・支払意思・価格・感想 | `survey_responses` | 同上 |
| 編成シミュレーション | `simulation_runs` | 同上 |

集計APIは `GET /v1/kpis`。画面では `/?ops=1` の検証KPIに出ます。Render では Persistent Disk 上の `/data/olympos_phase0.db`（再デプロイ後も残る。Starter が必要）。`.env` や Git には入りません。

## デモデータ

API起動後：

```bash
python3 scripts/seed_demo.py
```

ZEUS／APHRODITE各1グループ分の匿名データとアンケートを投入し、編成を実行します。

## Flutter起動

Flutter 3.24以降を推奨。

```bash
cd flutter
flutter create . --platforms=ios
flutter pub get
flutter run
```

iOS SimulatorからホストPCのAPIへ接続する場合は、`lib/api.dart`の`baseUrl`を環境に合わせて変更してください。本番化時は`--dart-define=API_BASE_URL=...`への移行を推奨します。

## AI似顔絵API

既定値は`PORTRAIT_PROVIDER=mock`で、顔画像を外部送信しません。契約・プライバシー確認後のみ以下を設定します。

```env
PORTRAIT_PROVIDER=http
PORTRAIT_API_URL=https://provider.example.com
PORTRAIT_API_KEY=replace-me
```

`HttpPortraitProvider`はProviderに次を要求する前提です。

- `retention: none`
- `training: false`
- 生成後の元画像削除API

Provider固有仕様に合わせて`backend/app/portrait.py`だけを差し替えてください。APIキーをGitへ保存しないでください。

## データ上の注意

- Phase 0では氏名・住所・電話番号を収集しません。
- 顔写真本体はSQLiteへ保存しません。
- 顔写真テストは希望者・個別同意に限定します。
- 本番eKYC・決済・通報処理として使用しないでください。
- Phase 0データを有料βへ自動移行しないでください。

## 未実装（Phase 0対象外）

- Sign in with Apple、SMS認証、eKYC
- Apple IAP／外部決済・返金
- Google Calendar OAuth
- デート当日限定チャット、連絡先遮断、場所カード
- 本番の写真配信・透かし・スクリーンショット監査
- 外部緊急窓口・管理者承認ワークフロー
- App Store配布・本番インフラ

## 検査状況

- Python：`py_compile`合格
- Web：管理ブラウザで描画・JavaScriptエラーなし
- pytest：テストコード同梱。依存関係導入後に実行
- Flutter：ソース同梱。Flutter SDK環境で`flutter analyze`と実機確認が必要

## Cursorで作業を始める

1. Cursorで `OLYMPOS.code-workspace` を開きます。
2. 推奨拡張機能のインストール通知を承認します。
3. コマンドパレットから **Tasks: Run Task** → `OLYMPOS: Setup backend` を実行します（`.env` が無ければ `.env.example` からコピーされます）。
4. `OLYMPOS: Start API` と `OLYMPOS: Start Web` をそれぞれ実行します。
5. ブラウザで `http://localhost:8080` を開きます。API仕様は `http://localhost:8000/docs` です。

### Cursor内の主な操作

- APIデバッグ：Run and Debug → `Debug OLYMPOS API`
- テスト：Tasks → `OLYMPOS: Run tests`
- デモ投入：Tasks → `OLYMPOS: Seed demo`
- Flutter：`flutter create . --platforms=ios`を`flutter/`で一度実行後、Run and Debug → `Flutter: OLYMPOS Phase 0`

### 秘密情報

`backend/.env.example` を `backend/.env` へコピーし、APIキーは `.env` だけに記載してください。`.env` は `.gitignore` 対象です。

```bash
cp backend/.env.example backend/.env
```

`make setup` でも `.env` が無い場合は自動コピーされます。

## GitHub

初回のリポジトリ作成・push 手順は [docs/github.md](docs/github.md) を参照してください。外部公開は [docs/hosting.md](docs/hosting.md)（Render 推奨）。
