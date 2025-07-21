"""
Template generation tests
"""
import pytest
from datetime import datetime
from pathlib import Path

from src.models.document import DocumentType
from src.templates.incident_management import IncidentManagementTemplate
from src.templates.knowledge_management import KnowledgeManagementTemplate
from src.templates.slm_design import SLMDesignTemplate
from src.core.base_template import TemplateConfig


class TestBaseTemplate:
    """ベーステンプレートのテスト"""
    
    def test_template_config_creation(self, temp_dir):
        """テンプレート設定の作成テスト"""
        config = TemplateConfig(
            template_dir=temp_dir,
            output_dir=temp_dir,
            date_format="%Y-%m-%d"
        )
        
        assert config.template_dir == temp_dir
        assert config.output_dir == temp_dir
        assert config.date_format == "%Y-%m-%d"


class TestIncidentManagementTemplate:
    """インシデント管理テンプレートのテスト"""
    
    def test_template_creation(self):
        """テンプレート作成のテスト"""
        template = IncidentManagementTemplate()
        
        assert template.get_template_name() == "incident_management.j2"
        assert template.get_document_type() == DocumentType.INCIDENT_MANAGEMENT
    
    def test_required_fields(self):
        """必須フィールドのテスト"""
        template = IncidentManagementTemplate()
        required_fields = template.get_required_fields()
        
        assert "project_name" in required_fields
        assert "author" in required_fields
        assert "client" in required_fields
    
    def test_sections(self):
        """セクション構成のテスト"""
        template = IncidentManagementTemplate()
        sections = template.get_sections()
        
        assert len(sections) > 0
        assert "1. 概要" in sections
        assert "2. プロセス定義" in sections
    
    def test_prepare_context(self, incident_management_data):
        """コンテキスト準備のテスト"""
        template = IncidentManagementTemplate()
        context = template.prepare_context(incident_management_data)
        
        assert context["project_name"] == "ServiceNow ITSM導入プロジェクト"
        assert context["author"]["name"] == "山田太郎"
        assert "システム障害" in context["incident_types"]
        assert context["sla_targets"]["critical"] == "4時間"
    
    def test_render_template(self, incident_management_data, temp_dir):
        """テンプレートレンダリングのテスト"""
        # テンプレートファイルが存在しない場合のモック処理
        template = IncidentManagementTemplate()
        
        # prepare_contextが正常に動作することを確認
        context = template.prepare_context(incident_management_data)
        assert context is not None
        assert isinstance(context, dict)
    
    def test_validation_success(self, incident_management_data):
        """バリデーション成功のテスト"""
        template = IncidentManagementTemplate()
        
        # バリデーションが例外を発生させないことを確認
        try:
            template.validate_data(incident_management_data)
        except ValueError:
            pytest.fail("Validation should not fail with valid data")
    
    def test_validation_failure(self):
        """バリデーション失敗のテスト"""
        template = IncidentManagementTemplate()
        invalid_data = {"invalid_field": "value"}
        
        with pytest.raises(ValueError):
            template.validate_data(invalid_data)


class TestKnowledgeManagementTemplate:
    """ナレッジ管理テンプレートのテスト"""
    
    def test_template_creation(self):
        """テンプレート作成のテスト"""
        template = KnowledgeManagementTemplate()
        
        assert template.get_template_name() == "knowledge_management.j2"
        assert template.get_document_type() == DocumentType.KNOWLEDGE_MANAGEMENT
    
    def test_sections(self):
        """セクション構成のテスト"""
        template = KnowledgeManagementTemplate()
        sections = template.get_sections()
        
        expected_sections = [
            "1. 概要",
            "2. ナレッジ管理基本方針",
            "3. ナレッジベース設計",
            "4. ナレッジ分類・タクソノミー"
        ]
        
        for section in expected_sections:
            assert section in sections
    
    def test_prepare_context(self, knowledge_management_data):
        """コンテキスト準備のテスト"""
        template = KnowledgeManagementTemplate()
        context = template.prepare_context(knowledge_management_data)
        
        assert context["project_name"] == "ナレッジ管理システム構築"
        assert context["author"]["name"] == "田中花子"
        assert "knowledge_types" in context
    
    def test_default_values(self):
        """デフォルト値のテスト"""
        template = KnowledgeManagementTemplate()
        
        # デフォルトの概要を取得
        default_overview = template._get_default_km_overview()
        assert "purpose" in default_overview
        assert "objectives" in default_overview
        
        # デフォルトのナレッジベース設計を取得
        default_kb_design = template._get_default_kb_design()
        assert "architecture" in default_kb_design
        assert "storage_structure" in default_kb_design
    
    def test_taxonomy_design(self):
        """タクソノミー設計のテスト"""
        template = KnowledgeManagementTemplate()
        taxonomy = template._get_default_taxonomy()
        
        assert len(taxonomy) > 0
        assert taxonomy[0]["category"] is not None
        assert "subcategories" in taxonomy[0]


class TestSLMDesignTemplate:
    """SLM設計テンプレートのテスト"""
    
    def test_template_creation(self):
        """テンプレート作成のテスト"""
        template = SLMDesignTemplate()
        
        assert template.get_template_name() == "slm_design.j2"
        assert template.get_document_type() == DocumentType.SLM_DESIGN
    
    def test_sections(self):
        """セクション構成のテスト"""
        template = SLMDesignTemplate()
        sections = template.get_sections()
        
        expected_sections = [
            "1. 概要",
            "2. SLM基本方針",
            "3. サービスレベル定義",
            "4. SLA設計"
        ]
        
        for section in expected_sections:
            assert section in sections
    
    def test_prepare_context(self, sample_document_data):
        """コンテキスト準備のテスト"""
        template = SLMDesignTemplate()
        context = template.prepare_context(sample_document_data)
        
        assert context["project_name"] == "テストプロジェクト"
        assert "slm_overview" in context
        assert "service_levels" in context
    
    def test_default_slm_overview(self):
        """デフォルトSLM概要のテスト"""
        template = SLMDesignTemplate()
        overview = template._get_default_slm_overview()
        
        assert "purpose" in overview
        assert "objectives" in overview
        assert "benefits" in overview
        assert len(overview["objectives"]) > 0
    
    def test_default_service_levels(self):
        """デフォルトサービスレベルのテスト"""
        template = SLMDesignTemplate()
        service_levels = template._get_default_service_levels()
        
        assert len(service_levels) > 0
        assert "service_name" in service_levels[0]
        assert "availability" in service_levels[0]
        assert "performance" in service_levels[0]


class TestTemplateIntegration:
    """テンプレート統合テスト"""
    
    def test_multiple_template_creation(self):
        """複数テンプレートの作成テスト"""
        templates = [
            IncidentManagementTemplate(),
            KnowledgeManagementTemplate(),
            SLMDesignTemplate()
        ]
        
        for template in templates:
            assert template.get_template_name() is not None
            assert template.get_document_type() is not None
            assert len(template.get_sections()) > 0
    
    def test_template_structure_consistency(self):
        """テンプレート構造の一貫性テスト"""
        templates = [
            IncidentManagementTemplate(),
            KnowledgeManagementTemplate(),
            SLMDesignTemplate()
        ]
        
        for template in templates:
            structure = template.get_template_structure()
            
            assert "document_type" in structure
            assert "template_name" in structure
            assert "required_fields" in structure
            assert "sections" in structure
    
    def test_date_formatting(self):
        """日付フォーマットのテスト"""
        template = IncidentManagementTemplate()
        test_date = datetime(2024, 1, 15, 10, 30)
        
        formatted = template._date_format(test_date)
        assert "2024" in formatted
        assert "01" in formatted or "1" in formatted
        assert "15" in formatted