# ServiceNow Documentation Template Generator

ServiceNowをデリバリするために必要なドキュメント雛形を生成AIで作る実験リポジトリ

## 概要

このプロジェクトは、ServiceNow ITSM導入プロジェクトで必要となる各種設計書のテンプレートを自動生成するツールです。標準化されたテンプレートにより、品質の高い設計書を効率的に作成できます。

## 主な機能

### 🌐 Web インターフェース
- **Bootstrap 5 対応**: モダンで使いやすいWebUI
- **リアルタイムプレビュー**: テンプレートの即座確認
- **ドラッグ&ドロップ**: 直感的なファイル操作

### 📄 多様なテンプレート
- **インシデント管理設計書**: インシデント処理フロー、SLA設計
- **問題管理設計書**: 根本原因分析、問題解決プロセス
- **変更管理設計書**: 変更プロセス、承認フロー、リスク評価
- **サービスカタログ設計書**: カタログ構造、申請フォーム設計
- **CMDB設計書**: CI設計、関係性定義、データ品質管理
- **セキュリティ設計書**: アクセス制御、認証、暗号化
- **環境・リリース管理設計書**: 環境戦略、CI/CD設計
- **テスト設計書**: テスト計画、テストケース、品質保証
- **データ移行設計書**: 移行戦略、データマッピング
- **運用設計書**: 運用手順、監視設計、バックアップ戦略
- **SLM設計書**: サービスレベル管理、メトリクス定義
- **ナレッジ管理設計書**: ナレッジベース構造、品質管理

### 🔄 エクスポート機能
- **PDF**: プロフェッショナルな文書出力
- **Word (DOCX)**: 編集可能な文書形式
- **Markdown**: 元のテンプレート形式
- **テキスト**: プレーンテキスト形式

### ⚙️ 高度な機能
- **設定外部化**: YAML設定ファイルによるカスタマイズ
- **バリデーション**: 多段階検証とレポート生成
- **テスト**: 100+ のテストケースによる品質保証

## インストール

### 前提条件
- Python 3.9以上
- Poetry（Pythonパッケージマネージャー）

### セットアップ手順

```bash
# リポジトリのクローン
git clone https://github.com/your-org/servicenow-doc-template.git
cd servicenow-doc-template

# 依存関係のインストール
make install

# または直接Poetryを使用
poetry install
```

### 追加パッケージ（オプション）

```bash
# PDF生成用（WeasyPrint）
poetry install --extras pdf

# Word文書生成用
poetry install --extras docx
```

## 使い方

### 🌐 Web インターフェース（推奨）

```bash
# Webサーバーを起動
poetry run python -m src.web.main

# ブラウザで http://localhost:8000 にアクセス
```

Web インターフェースの機能：
- **テンプレート選択**: 利用可能なテンプレート一覧
- **プレビュー**: サンプルデータでのリアルタイム確認
- **ドキュメント生成**: フォーム入力による簡単生成
- **エクスポート**: 複数形式での出力
- **設定管理**: デフォルト値やテーマの設定
- **バリデーション**: データ検証とレポート表示

### 💻 CLIコマンド

#### 1. 利用可能なテンプレートの確認

```bash
poetry run servicenow-doc list-templates
```

#### 2. 設計書の生成

```bash
# インシデント管理設計書の生成
poetry run servicenow-doc generate \
  --type "incident_management" \
  --project "自社ITSM導入プロジェクト" \
  --author "山田太郎" \
  --email "yamada@example.com"

# 追加データを指定して生成
poetry run servicenow-doc generate \
  --type "security_design" \
  --project "自社ITSM導入プロジェクト" \
  --author "山田太郎" \
  --email "yamada@example.com" \
  --data custom_data.yaml
```

#### 3. サンプル設計書の生成

```bash
# サンプルデータで設計書を生成
poetry run servicenow-doc generate-sample --type "cmdb_design"
```

#### 4. テンプレート構造の確認

```bash
poetry run servicenow-doc show-template --type "change_management"
```

## 設定とカスタマイズ

### 設定ファイル

設定は `config/templates.yaml` で管理されます：

```yaml
# デフォルト値設定
defaults:
  author:
    name: "システムアナリスト"
    email: "analyst@company.com"
    role: "プロジェクトマネージャー"
  
  client:
    name: "株式会社サンプル"
    department: "IT部"
  
  document:
    version: "1.0.0"
    language: "ja"
    format: "markdown"

# エクスポート設定
export:
  pdf:
    page_size: "A4"
    margin: "20mm"
  
  word:
    font_size: 11

# Web設定
web:
  title: "ServiceNow Template Generator"
  theme: "light"
  items_per_page: 10
```

### カスタムデータの指定

YAMLまたはJSONファイルで追加データを指定できます：

```yaml
# custom_data.yaml
incident_management:
  incident_types:
    - "システム障害"
    - "パフォーマンス問題"
    - "ユーザーサポート"
  
  priority_levels:
    - "Critical"
    - "High"
    - "Medium"
    - "Low"
  
  sla_targets:
    critical: "4時間"
    high: "8時間"
    medium: "24時間"
    low: "72時間"
```

## バリデーション機能

### バリデーションモード

- **STRICT**: エラーで処理停止
- **PERMISSIVE**: 警告は無視、エラーのみチェック
- **INFO_ONLY**: 情報提供のみ、処理継続

### バリデーションレポート

```bash
# バリデーションレポートの生成
poetry run python -c "
from src.validators.validation_manager import ValidationManager, ValidationMode
from src.models.document import DocumentType

manager = ValidationManager(ValidationMode.PERMISSIVE)
data = {'project_name': 'テスト', 'author': {'name': 'テスト', 'email': 'test@example.com'}}
report = manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, data)

# テキスト形式でエクスポート
print(manager.export_validation_report(report, 'text'))
"
```

## 開発者向け情報

### プロジェクト構造

```
servicenow-doc-template/
├── src/
│   ├── core/                 # 基本クラス・ベーステンプレート
│   ├── templates/            # Jinja2テンプレートファイル
│   ├── templates_impl/       # テンプレート実装クラス
│   ├── generators/           # ドキュメント生成器
│   ├── models/              # データモデル・型定義
│   ├── exporters/           # エクスポート機能
│   ├── validators/          # バリデーション機能
│   ├── config/              # 設定管理
│   ├── web/                 # Webインターフェース
│   │   ├── templates/       # HTMLテンプレート
│   │   └── static/          # CSS/JS/画像
│   └── cli.py               # CLIインターフェース
├── tests/                   # テストコード
│   ├── test_templates.py    # テンプレートテスト
│   ├── test_generators.py   # 生成器テスト
│   ├── test_exporters.py    # エクスポートテスト
│   ├── test_validators.py   # バリデーションテスト
│   └── test_web.py          # Webインターフェーステスト
├── config/                  # 設定ファイル
├── docs/                    # ドキュメント
└── output/                  # 生成されたドキュメント
```

### テスト実行

```bash
# すべてのテストを実行
make test

# カバレッジレポート付きでテスト
poetry run pytest --cov=src --cov-report=html

# 特定のテストファイルを実行
poetry run pytest tests/test_validators.py -v

# テストレポート生成
poetry run python scripts/run_tests.py
```

### コード品質チェック

```bash
# リンターとフォーマッターを実行
make lint
make format

# 型チェック
poetry run mypy src/
```

### API開発

FastAPI ベースのWeb APIも提供：

```bash
# API ドキュメント
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)

# 主要エンドポイント
GET    /api/templates              # テンプレート一覧
POST   /api/generate               # ドキュメント生成
GET    /api/templates/{type}/preview  # プレビュー
POST   /api/export/{filename}      # エクスポート
POST   /api/validate               # バリデーション
GET    /api/settings               # 設定取得
PUT    /api/settings/defaults      # デフォルト値更新
```

## アーキテクチャ

### 設計原則

- **抽象化**: `BaseDocumentTemplate` による共通インターフェース
- **拡張性**: 新しいテンプレートの簡単追加
- **設定駆動**: YAML設定による柔軟なカスタマイズ
- **品質保証**: 包括的なテストとバリデーション
- **ユーザビリティ**: CLI・Web両対応

### 技術スタック

- **Backend**: Python 3.9+, FastAPI, Pydantic
- **Templates**: Jinja2
- **Export**: WeasyPrint (PDF), python-docx (Word)
- **Frontend**: Bootstrap 5, JavaScript
- **Testing**: pytest, coverage
- **Config**: YAML, 型安全な設定管理

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストを歓迎します。大きな変更を行う場合は、まずissueを作成して変更内容について議論してください。

### 開発手順

1. フォークする
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## サポート

問題や質問がある場合は、GitHubのissueを作成してください。

## 更新履歴

### v1.0.0 (2024)
- ✅ 初期リリース
- ✅ 12種類のテンプレート実装
- ✅ Web インターフェース追加
- ✅ 多形式エクスポート機能
- ✅ バリデーション機能
- ✅ 設定外部化
- ✅ 包括的テストスイート