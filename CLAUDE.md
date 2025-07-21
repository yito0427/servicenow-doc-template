# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ServiceNow ITSM導入プロジェクト向けの設計書テンプレート自動生成ツールです。Jinja2テンプレートエンジンを使用して、標準化された高品質な設計書を効率的に作成できます。

## Repository Status

- **Project Type**: ServiceNow documentation template generator
- **Technology Stack**: Python 3.9+, Jinja2, Click CLI, Pydantic
- **Current State**: 実装完了、3つの主要テンプレート利用可能
- **Purpose**: ServiceNow ITSM導入に必要な設計書の自動生成

## Development Setup

### インストール手順（Poetryが利用できない場合）
```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 依存関係のインストール
pip install -r requirements.txt

# CLIツールの実行
python setup.py --help
```

### インストール手順（Poetryが利用可能な場合）
```bash
# 依存関係のインストール
make install
# または
poetry install

# CLIツールの実行
poetry run servicenow-doc --help
```

## Common Development Commands

### テンプレート関連
```bash
# 利用可能なテンプレートの確認
python setup.py list-templates

# 設計書の生成
python setup.py generate --type "CMDB設計書" --project "プロジェクト名" --author "作成者" --email "email@example.com"

# サンプル設計書の生成
python setup.py generate-sample --type "CMDB設計書"

# テンプレート構造の確認
python setup.py show-template --type "セキュリティ設計書"
```

### 開発・テスト
```bash
# テストの実行（Poetryが必要）
make test

# コードフォーマット（Poetryが必要）
make format

# リンターの実行（Poetryが必要）
make lint
```

## Project Structure

```
servicenow-doc-template/
├── src/
│   ├── core/
│   │   └── base_template.py      # テンプレート基底クラス
│   ├── templates/
│   │   ├── cmdb_design.py        # CMDB設計書テンプレートクラス
│   │   ├── cmdb_design.j2        # CMDB設計書Jinja2テンプレート
│   │   ├── security_design.py    # セキュリティ設計書クラス
│   │   ├── security_design.j2    # セキュリティ設計書テンプレート
│   │   ├── environment_release.py # 環境・リリース管理設計書クラス
│   │   └── environment_release.j2 # 環境・リリース管理テンプレート
│   ├── generators/
│   │   └── document_generator.py  # ドキュメント生成エンジン
│   ├── models/
│   │   └── document.py           # データモデル定義
│   └── cli.py                    # CLIインターフェース
├── docs/
│   └── samples/                  # サンプル出力
├── output/                       # 生成された設計書の出力先
├── pyproject.toml               # Poetry設定
├── requirements.txt             # pip用依存関係
├── setup.py                     # 直接実行用スクリプト
└── Makefile                     # ビルドコマンド
```

## Available Templates

### 1. CMDB設計書
- CIクラス階層設計
- CI識別・正規化ルール
- Discovery戦略とMIDサーバー配置
- サービスマッピング設計
- データ品質管理

### 2. セキュリティ設計書
- アクセス制御（RBAC）設計
- 認証・認可（SSO/MFA）設計
- データ暗号化設計
- 監査ログ設計
- コンプライアンス対応

### 3. 環境・リリース管理設計書
- 4段階環境戦略（Dev/Test/UAT/Prod）
- リリース管理プロセス
- Update Set管理戦略
- CI/CD・DevOpsパイプライン
- 環境同期・リフレッシュ戦略

## Key Design Patterns

### テンプレートクラス設計
- 抽象基底クラス `BaseDocumentTemplate` を継承
- 各テンプレートは以下を実装:
  - `get_template_name()`: Jinja2テンプレートファイル名
  - `get_document_type()`: ドキュメントタイプ
  - `prepare_context()`: テンプレート用データ準備
  - `get_required_fields()`: 必須フィールド定義

### Jinja2テンプレート
- Markdownフォーマットで設計書を生成
- 条件分岐でデフォルト値を提供
- ループで動的なセクション生成
- カスタムフィルター（日付、数値フォーマット）

## ServiceNow Context

このツールは以下のServiceNow導入フェーズをサポート:
- **設計フェーズ**: 詳細な技術設計書の作成
- **実装フェーズ**: 設定・開発ガイドライン
- **テストフェーズ**: テスト計画とシナリオ
- **運用フェーズ**: 運用手順と保守ガイド