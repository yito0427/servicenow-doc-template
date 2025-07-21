from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel

from src.models.document import Document, DocumentType
from src.config.settings import get_settings
from src.validators.validation_manager import ValidationManager, ValidationMode


class TemplateConfig(BaseModel):
    template_dir: Path = Path(__file__).parent.parent / "templates"
    output_dir: Path = Path("output")
    date_format: str = "%Y年%m月%d日"
    
    class Config:
        arbitrary_types_allowed = True


class BaseDocumentTemplate(ABC):
    """設計書テンプレートの基底クラス"""
    
    def __init__(self, config: Optional[TemplateConfig] = None):
        self.config = config or TemplateConfig()
        self.env = Environment(
            loader=FileSystemLoader(str(self.config.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False
        )
        self._setup_filters()
    
    def _setup_filters(self) -> None:
        """Jinja2カスタムフィルターの設定"""
        self.env.filters['date_format'] = self._date_format
        self.env.filters['number_format'] = self._number_format
    
    def _date_format(self, date: datetime, fmt: Optional[str] = None) -> str:
        """日付フォーマットフィルター"""
        if not date:
            return ""
        fmt = fmt or self.config.date_format
        return date.strftime(fmt)
    
    def _number_format(self, number: float) -> str:
        """数値フォーマットフィルター"""
        return f"{number:,.0f}"
    
    @abstractmethod
    def get_template_name(self) -> str:
        """テンプレートファイル名を返す"""
        pass
    
    @abstractmethod
    def get_document_type(self) -> DocumentType:
        """ドキュメントタイプを返す"""
        pass
    
    @abstractmethod
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """テンプレート用のコンテキストデータを準備"""
        pass
    
    def validate_data(self, data: Dict[str, Any], strict: bool = True) -> None:
        """入力データの検証"""
        # 基本的な必須フィールドチェック（後方互換性のため保持）
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in data:
                raise ValueError(f"必須フィールド '{field}' が見つかりません")
        
        # 高度なバリデーション
        validation_mode = ValidationMode.STRICT if strict else ValidationMode.PERMISSIVE
        validator_manager = ValidationManager(validation_mode)
        
        try:
            validation_report = validator_manager.validate_document(
                self.get_document_type(), data
            )
            
            # バリデーション結果をログに記録（将来的な拡張用）
            self._validation_report = validation_report
            
            # エラーがある場合は例外を発生
            if strict and not validation_report.is_valid:
                error_messages = [
                    result.message for result in validation_report.results 
                    if result.level.value == "error"
                ]
                raise ValueError(f"バリデーションエラー: {'; '.join(error_messages)}")
                
        except Exception as e:
            if strict:
                raise
            # 非strictモードではバリデーションエラーをログに記録して続行
            print(f"バリデーション警告: {e}")
    
    def get_required_fields(self) -> list:
        """必須フィールドのリストを返す"""
        settings = get_settings()
        doc_type = self.get_document_type()
        return settings.get_required_fields(doc_type.value)
    
    def render(self, data: Dict[str, Any]) -> str:
        """テンプレートをレンダリング"""
        self.validate_data(data)
        template = self.env.get_template(self.get_template_name())
        context = self.prepare_context(data)
        return template.render(**context)
    
    def save(self, data: Dict[str, Any], filename: Optional[str] = None) -> Path:
        """レンダリング結果をファイルに保存"""
        content = self.render(data)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            doc_type = self.get_document_type().value.replace("/", "_")
            filename = f"{doc_type}_{timestamp}.md"
        
        output_path = self.config.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return output_path
    
    def get_template_structure(self) -> Dict[str, Any]:
        """テンプレートの構造情報を返す"""
        return {
            "document_type": self.get_document_type().value,
            "template_name": self.get_template_name(),
            "required_fields": self.get_required_fields(),
            "sections": self.get_sections()
        }
    
    def get_sections(self) -> list:
        """ドキュメントのセクション構成を返す"""
        settings = get_settings()
        doc_type = self.get_document_type()
        return settings.get_template_sections(doc_type.value)
    
    def get_default_values(self) -> Dict[str, Any]:
        """テンプレートのデフォルト値を取得"""
        settings = get_settings()
        doc_type = self.get_document_type()
        return settings.get_default_values(doc_type.value)
    
    def get_validation_report(self):
        """最後のバリデーション結果を取得"""
        return getattr(self, '_validation_report', None)
    
    def validate_and_get_report(self, data: Dict[str, Any]) -> 'ValidationReport':
        """データをバリデーションしてレポートを返す"""
        from src.validators.validation_manager import ValidationManager, ValidationMode
        
        validator_manager = ValidationManager(ValidationMode.PERMISSIVE)
        validation_report = validator_manager.validate_document(
            self.get_document_type(), data
        )
        
        self._validation_report = validation_report
        return validation_report