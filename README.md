# ServiceNow Documentation Template Generator

ServiceNowをデリバリするために必要なドキュメント雛形を生成AIで作る実験リポジトリ

## 概要

このプロジェクトは、ServiceNow ITSM導入プロジェクトで必要となる各種設計書のテンプレートを自動生成するツールです。標準化されたテンプレートにより、品質の高い設計書を効率的に作成できます。

## 主な機能

- **CMDB設計書**: Configuration Management Database の設計ドキュメント生成
- **セキュリティ設計書**: アクセス制御、認証、暗号化などのセキュリティ設計
- **環境・リリース管理設計書**: 環境戦略、CI/CD、リリースプロセスの設計

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

## 使い方

### CLIコマンド

#### 1. 利用可能なテンプレートの確認

```bash
poetry run servicenow-doc list-templates
```

#### 2. 設計書の生成

```bash
# CMDB設計書の生成
poetry run servicenow-doc generate \
  --type "CMDB設計書" \
  --project "自社ITSM導入プロジェクト" \
  --author "山田太郎" \
  --email "yamada@example.com"

# 追加データを指定して生成
poetry run servicenow-doc generate \
  --type "セキュリティ設計書" \
  --project "自社ITSM導入プロジェクト" \
  --author "山田太郎" \
  --email "yamada@example.com" \
  --data custom_data.yaml
```

#### 3. サンプル設計書の生成

```bash
# サンプルデータで設計書を生成
poetry run servicenow-doc generate-sample --type "CMDB設計書"
```

#### 4. テンプレート構造の確認

```bash
poetry run servicenow-doc show-template --type "環境戦略設計書"
```

## 設計書テンプレート

### CMDB設計書
- CMDB設計方針
- CIクラス設計
- CI識別・正規化ルール
- 関係性設計
- Discovery戦略
- データ品質管理

### セキュリティ設計書
- セキュリティ要件
- アクセス制御設計（RBAC）
- 認証・認可設計
- データ暗号化設計
- 監査・ログ設計
- コンプライアンス対応

### 環境・リリース管理設計書
- 環境戦略（Dev/Test/UAT/Prod）
- リリース管理プロセス
- Update Set管理
- CI/CD・DevOps設計
- 環境同期・リフレッシュ戦略

## カスタマイズ

### 追加データの指定

YAMLまたはJSONファイルで追加データを指定できます：

```yaml
# custom_data.yaml
cmdb_scope:
  description: "カスタムCMDB実装"
  objectives:
    - "ビジネスサービスの可視化"
    - "変更影響分析の高度化"
  
ci_classes:
  - name: "cmdb_ci_custom_app"
    label: "カスタムアプリケーション"
    parent: "cmdb_ci_appl"
    attributes:
      - name: "custom_field"
        type: "string"
        mandatory: true
```

## 開発者向け情報

### プロジェクト構造

```
servicenow-doc-template/
├── src/
│   ├── core/              # 基本クラス
│   ├── templates/         # テンプレート実装
│   ├── generators/        # ドキュメント生成器
│   ├── models/           # データモデル
│   └── cli.py            # CLIインターフェース
├── tests/                # テストコード
├── docs/                 # ドキュメント
└── output/              # 生成されたドキュメント
```

### テスト実行

```bash
# すべてのテストを実行
make test

# カバレッジレポート付きでテスト
poetry run pytest --cov=src --cov-report=html
```

### コード品質チェック

```bash
# リンターとフォーマッターを実行
make lint
make format
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

プルリクエストを歓迎します。大きな変更を行う場合は、まずissueを作成して変更内容について議論してください。

## サポート

問題や質問がある場合は、GitHubのissueを作成してください。
