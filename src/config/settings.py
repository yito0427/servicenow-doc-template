"""
Configuration management for ServiceNow Document Template Generator
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AuthorConfig(BaseModel):
    """作成者設定"""
    name: str = "プロジェクトマネージャー"
    email: str = "pm@example.com"
    role: str = "システムアナリスト"


class ClientConfig(BaseModel):
    """クライアント設定"""
    name: str = "お客様会社名"
    department: str = "情報システム部"


class ProjectConfig(BaseModel):
    """プロジェクト設定"""
    phase: str = "設計フェーズ"
    methodology: str = "Agile"


class DocumentConfig(BaseModel):
    """ドキュメント設定"""
    version: str = "1.0"
    language: str = "ja"
    format: str = "markdown"


class DefaultsConfig(BaseModel):
    """デフォルト設定"""
    author: AuthorConfig = Field(default_factory=AuthorConfig)
    client: ClientConfig = Field(default_factory=ClientConfig)
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    document: DocumentConfig = Field(default_factory=DocumentConfig)


class PDFExportConfig(BaseModel):
    """PDF出力設定"""
    page_size: str = "A4"
    margin: str = "20mm"
    font_family: str = "Noto Sans CJK JP"


class WordExportConfig(BaseModel):
    """Word出力設定"""
    template_style: str = "Standard"
    font_size: str = "11pt"


class ExportConfig(BaseModel):
    """エクスポート設定"""
    formats: List[str] = ["md", "pdf", "docx", "txt"]
    pdf: PDFExportConfig = Field(default_factory=PDFExportConfig)
    word: WordExportConfig = Field(default_factory=WordExportConfig)


class WebConfig(BaseModel):
    """Webインターフェース設定"""
    title: str = "ServiceNow Document Generator"
    theme: str = "bootstrap"
    items_per_page: int = 10
    max_upload_size: str = "10MB"


class ApplicationConfig(BaseModel):
    """アプリケーション設定"""
    name: str = "ServiceNow Document Template Generator"
    version: str = "1.0.0"
    description: str = "ServiceNowデリバリプロジェクトに必要な設計書を簡単に生成"


class TemplateConfig(BaseModel):
    """個別テンプレート設定"""
    name: str
    description: str
    template_file: str
    sections: List[str]
    required_fields: List[str]
    default_values: Dict[str, Any] = Field(default_factory=dict)


class Settings(BaseModel):
    """メイン設定クラス"""
    application: ApplicationConfig = Field(default_factory=ApplicationConfig)
    templates: Dict[str, TemplateConfig] = Field(default_factory=dict)
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    export: ExportConfig = Field(default_factory=ExportConfig)
    web: WebConfig = Field(default_factory=WebConfig)

    @classmethod
    def from_yaml(cls, config_path: Optional[Path] = None) -> "Settings":
        """YAMLファイルから設定を読み込み"""
        if config_path is None:
            # デフォルトの設定ファイルパスを探索
            config_path = cls._find_config_file()
        
        if not config_path or not config_path.exists():
            # 設定ファイルがない場合はデフォルト設定を使用
            return cls()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            return cls(**config_data)
        except Exception as e:
            print(f"Warning: Failed to load config file {config_path}: {e}")
            print("Using default configuration.")
            return cls()

    @staticmethod
    def _find_config_file() -> Optional[Path]:
        """設定ファイルを探索"""
        possible_paths = [
            Path("config/templates.yaml"),
            Path("templates.yaml"),
            Path("config.yaml"),
            Path.home() / ".servicenow-doc-gen" / "config.yaml"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None

    def get_template_config(self, template_type: str) -> Optional[TemplateConfig]:
        """指定されたテンプレートタイプの設定を取得"""
        return self.templates.get(template_type)

    def get_default_values(self, template_type: str) -> Dict[str, Any]:
        """テンプレートのデフォルト値を取得"""
        template_config = self.get_template_config(template_type)
        if template_config:
            return template_config.default_values
        return {}

    def get_template_sections(self, template_type: str) -> List[str]:
        """テンプレートのセクション一覧を取得"""
        template_config = self.get_template_config(template_type)
        if template_config:
            return template_config.sections
        return []

    def get_required_fields(self, template_type: str) -> List[str]:
        """テンプレートの必須フィールドを取得"""
        template_config = self.get_template_config(template_type)
        if template_config:
            return template_config.required_fields
        return ["project_name", "author", "client"]

    def to_yaml(self, output_path: Path) -> None:
        """設定をYAMLファイルに出力"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = self.model_dump()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, 
                     allow_unicode=True, sort_keys=False)


# グローバル設定インスタンス
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """設定インスタンスを取得（シングルトンパターン）"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings.from_yaml()
    return _settings_instance


def reload_settings(config_path: Optional[Path] = None) -> Settings:
    """設定を再読み込み"""
    global _settings_instance
    _settings_instance = Settings.from_yaml(config_path)
    return _settings_instance


# 便利関数
def get_template_defaults(template_type: str) -> Dict[str, Any]:
    """テンプレートのデフォルト値を取得"""
    return get_settings().get_default_values(template_type)


def get_export_formats() -> List[str]:
    """利用可能なエクスポート形式を取得"""
    return get_settings().export.formats


def get_web_config() -> WebConfig:
    """Web設定を取得"""
    return get_settings().web