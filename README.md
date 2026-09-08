# OLYMPOS Phase 0 Application

東京23区の20〜39歳・男女各50人を対象に、コンセプト需要、操作性、AI似顔絵、匿名編成成立率を検証するためのソースコードです。

> **Phase 0限定**：実課金、本番eKYC、実デート、App Store公開は行いません。

## 構成

```text
backend/     FastAPI + SQLite API
web/         レスポンシブ検証Web
flutter/     iPhone向けFlutter検証アプリ基盤
scripts/     デモデータ投入
```

## 実装済み

- 同意済み匿名プロフィール登録
- 性自認・希望対象、5歳帯、東京23区、必須／希望条件、日程枠
- 申込順を基本とする、ホスト1名＋候補者6〜7名の匿名編成
- ZEUS／APHRODITEのクール種別表示
- 参加意向、支払意思、操作性アンケート
- 4つの継続KPI（60%／40%／80%／70%）
- AI似顔絵Provider Adapter
  - 既定はモック
  - 最大2回（初回＋無料再生成1回）
  - 本人同意必須
  - 外部Provider接続口は保存・学習禁止パラメータを送信
- 黒＋ルビー＋ゴールドのレスポンシブWeb
- Flutterの概要・匿名登録・KPI画面

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

`http://localhost:8080`を開きます。API URLを変更する場合：

```text
http://localhost:8080/?api=https://your-api.example.com
```

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

初回のリポジトリ作成・push 手順は [docs/github.md](docs/github.md) を参照してください。
