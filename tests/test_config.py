"""
Configuration management tests
"""
import pytest
from pathlib import Path

from src.config.settings import Settings, get_settings, reload_settings


class TestSettings:
    """設定管理のテスト"""
    
    def test_default_settings_creation(self):
        """デフォルト設定の作成テスト"""
        settings = Settings()
        
        assert settings.application.name == "ServiceNow Document Template Generator"
        assert settings.application.version == "1.0.0"
        assert settings.defaults.author.name == "プロジェクトマネージャー"
        assert settings.defaults.document.language == "ja"
        assert "md" in settings.export.formats
    
    def test_settings_from_yaml(self, mock_yaml_config):
        """YAML設定ファイルからの読み込みテスト"""
        settings = Settings.from_yaml(mock_yaml_config)
        
        assert settings.application.name == "Test ServiceNow Document Generator"
        assert settings.application.version == "test-1.0.0"
        assert settings.defaults.author.name == "テスト太郎"
        assert settings.defaults.author.email == "test@example.com"
    
    def test_settings_from_nonexistent_yaml(self):
        """存在しないYAMLファイルの処理テスト"""
        nonexistent_path = Path("nonexistent_config.yaml")
        settings = Settings.from_yaml(nonexistent_path)
        
        # デフォルト設定が使用されることを確認
        assert settings.application.name == "ServiceNow Document Template Generator"
    
    def test_get_template_config(self, test_settings):
        """テンプレート設定取得のテスト"""
        template_config = test_settings.get_template_config("test_template")
        
        assert template_config is not None
        assert template_config.name == "テストテンプレート"
        assert "概要" in template_config.sections
    
    def test_get_template_config_nonexistent(self, test_settings):
        """存在しないテンプレート設定の取得テスト"""
        template_config = test_settings.get_template_config("nonexistent_template")
        assert template_config is None
    
    def test_get_default_values(self, test_settings):
        """デフォルト値取得のテスト"""
        default_values = test_settings.get_default_values("test_template")
        
        assert "test_value" in default_values
        assert default_values["test_value"] == "default"
    
    def test_get_template_sections(self, test_settings):
        """テンプレートセクション取得のテスト"""
        sections = test_settings.get_template_sections("test_template")
        
        assert len(sections) == 2
        assert "概要" in sections
        assert "詳細" in sections
    
    def test_get_required_fields(self, test_settings):
        """必須フィールド取得のテスト"""
        required_fields = test_settings.get_required_fields("test_template")
        
        assert "project_name" in required_fields
        assert "author" in required_fields
    
    def test_to_yaml(self, test_settings, temp_dir):
        """YAML出力のテスト"""
        output_path = temp_dir / "output_config.yaml"
        test_settings.to_yaml(output_path)
        
        assert output_path.exists()
        
        # 出力されたYAMLを再読み込みして確認
        reloaded_settings = Settings.from_yaml(output_path)
        assert reloaded_settings.application.name == test_settings.application.name
    
    def test_singleton_pattern(self):
        """シングルトンパターンのテスト"""
        settings1 = get_settings()
        settings2 = get_settings()
        
        # 同一インスタンスであることを確認
        assert settings1 is settings2
    
    def test_reload_settings(self, mock_yaml_config):
        """設定再読み込みのテスト"""
        # 初期設定を取得
        initial_settings = get_settings()
        
        # 設定を再読み込み
        reloaded_settings = reload_settings(mock_yaml_config)
        
        # 設定が更新されていることを確認
        assert reloaded_settings.application.name == "Test ServiceNow Document Generator"
        assert get_settings() is reloaded_settings


class TestConfigIntegration:
    """設定ファイル統合テスト"""
    
    def test_template_config_usage(self, test_settings):
        """テンプレート設定の使用テスト"""
        # テンプレート設定を取得
        template_config = test_settings.get_template_config("test_template")
        
        # 設定が正しく取得できることを確認
        assert template_config.name == "テストテンプレート"
        assert template_config.description == "テスト用テンプレート"
        assert template_config.template_file == "test.j2"
        
        # デフォルト値が設定されていることを確認
        assert template_config.default_values["test_value"] == "default"
    
    def test_export_config_usage(self, test_settings):
        """エクスポート設定の使用テスト"""
        export_config = test_settings.export
        
        assert "md" in export_config.formats
        assert export_config.pdf.page_size == "A4"
        assert export_config.word.font_size == "11pt"
    
    def test_web_config_usage(self, test_settings):
        """Web設定の使用テスト"""
        web_config = test_settings.web
        
        assert web_config.title == "ServiceNow Document Generator"
        assert web_config.theme == "bootstrap"
        assert web_config.items_per_page == 10