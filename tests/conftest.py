"""
pytest configuration and fixtures
"""
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any

from src.config.settings import Settings
from src.generators.document_generator import DocumentGenerator


@pytest.fixture
def temp_dir():
    """一時ディレクトリを作成するフィクスチャ"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def test_settings():
    """テスト用設定を作成するフィクスチャ"""
    return Settings(
        application={
            "name": "Test ServiceNow Document Generator",
            "version": "test-1.0.0",
            "description": "Test version"
        },
        templates={
            "test_template": {
                "name": "テストテンプレート",
                "description": "テスト用テンプレート",
                "template_file": "test.j2",
                "sections": ["概要", "詳細"],
                "required_fields": ["project_name", "author"],
                "default_values": {"test_value": "default"}
            }
        },
        defaults={
            "author": {"name": "テスト太郎", "email": "test@example.com", "role": "テスター"},
            "client": {"name": "テスト会社", "department": "テスト部"},
            "document": {"version": "1.0", "language": "ja", "format": "markdown"}
        }
    )


@pytest.fixture
def document_generator(temp_dir):
    """DocumentGeneratorのフィクスチャ"""
    return DocumentGenerator(output_dir=temp_dir)


@pytest.fixture
def sample_document_data():
    """サンプルドキュメントデータのフィクスチャ"""
    return {
        "project_name": "テストプロジェクト",
        "author": {
            "name": "テスト太郎",
            "email": "test@example.com",
            "role": "テスター"
        },
        "version": "1.0",
        "client": {
            "name": "テスト会社",
            "department": "テスト部"
        }
    }


@pytest.fixture
def incident_management_data():
    """インシデント管理テンプレート用のテストデータ"""
    return {
        "project_name": "ServiceNow ITSM導入プロジェクト",
        "author": {
            "name": "山田太郎",
            "email": "yamada@example.com",
            "role": "システムアナリスト"
        },
        "version": "1.0",
        "client": {
            "name": "株式会社サンプル",
            "department": "情報システム部"
        },
        "incident_types": ["システム障害", "パフォーマンス問題"],
        "priority_levels": ["重要", "高", "中", "低"],
        "escalation_rules": "30分以内に上位者へエスカレーション",
        "sla_targets": {
            "critical": "4時間",
            "high": "8時間",
            "medium": "24時間",
            "low": "72時間"
        }
    }


@pytest.fixture
def knowledge_management_data():
    """ナレッジ管理テンプレート用のテストデータ"""
    return {
        "project_name": "ナレッジ管理システム構築",
        "author": {
            "name": "田中花子",
            "email": "tanaka@example.com",
            "role": "ナレッジマネージャー"
        },
        "version": "1.0",
        "client": {
            "name": "株式会社テスト",
            "department": "IT部"
        },
        "knowledge_types": [
            {
                "name": "FAQ",
                "description": "よくある質問と回答",
                "format": "Q&A形式",
                "usage": "問い合わせ削減"
            }
        ]
    }


@pytest.fixture
def mock_yaml_config(tmp_path):
    """モックYAML設定ファイル"""
    config_content = """
application:
  name: "Test ServiceNow Document Generator"
  version: "test-1.0.0"
  description: "Test application"

templates:
  test_template:
    name: "テストテンプレート"
    description: "テスト用"
    template_file: "test.j2"
    sections: ["概要"]
    required_fields: ["project_name"]
    default_values:
      test_field: "test_value"

defaults:
  author:
    name: "テスト太郎"
    email: "test@example.com"
    role: "テスター"
  client:
    name: "テスト会社"
    department: "テスト部"
  document:
    version: "1.0"
    language: "ja"
    format: "markdown"

export:
  formats: ["md", "pdf", "docx"]
  pdf:
    page_size: "A4"
    margin: "20mm"
  word:
    font_size: "11pt"

web:
  title: "Test Generator"
  theme: "bootstrap"
  items_per_page: 10
"""
    
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(config_content, encoding='utf-8')
    return config_file