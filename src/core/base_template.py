from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import BaseModel

from src.models.document import Document, DocumentType


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
    
    def validate_data(self, data: Dict[str, Any]) -> None:
        """入力データの検証"""
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in data:
                raise ValueError(f"必須フィールド '{field}' が見つかりません")
    
    def get_required_fields(self) -> list:
        """必須フィールドのリストを返す"""
        return ["project_name", "author", "version"]
    
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
        return ["概要", "詳細設計", "実装方針", "テスト計画", "リスク管理"]