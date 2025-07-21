"""
Base validation framework for ServiceNow document templates
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import re
from enum import Enum

from pydantic import BaseModel, ValidationError


class ValidationLevel(Enum):
    """バリデーションレベル"""
    ERROR = "error"     # 必須項目の欠如、形式エラー
    WARNING = "warning" # 推奨項目の欠如、品質改善提案
    INFO = "info"       # 情報提供、ベストプラクティス提案


class ValidationResult(BaseModel):
    """バリデーション結果"""
    is_valid: bool
    level: ValidationLevel
    field: str
    message: str
    suggestion: Optional[str] = None
    value: Optional[Any] = None


class ValidationReport(BaseModel):
    """バリデーションレポート"""
    document_type: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    warnings: int
    errors: int
    results: List[ValidationResult]
    is_valid: bool = True
    
    def __init__(self, **data):
        super().__init__(**data)
        self.is_valid = self.errors == 0


class BaseValidator(ABC):
    """バリデーターの基底クラス"""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ValidationReport:
        """データをバリデーションする"""
        pass
    
    def add_result(self, level: ValidationLevel, field: str, message: str, 
                  suggestion: str = None, value: Any = None) -> None:
        """バリデーション結果を追加"""
        result = ValidationResult(
            is_valid=(level != ValidationLevel.ERROR),
            level=level,
            field=field,
            message=message,
            suggestion=suggestion,
            value=value
        )
        self.results.append(result)
    
    def validate_required_field(self, data: Dict[str, Any], field: str, 
                               field_type: type = str) -> bool:
        """必須フィールドの検証"""
        if field not in data:
            self.add_result(
                ValidationLevel.ERROR,
                field,
                f"必須フィールド '{field}' が見つかりません",
                f"フィールド '{field}' を追加してください"
            )
            return False
        
        value = data[field]
        if value is None or (isinstance(value, str) and not value.strip()):
            self.add_result(
                ValidationLevel.ERROR,
                field,
                f"必須フィールド '{field}' が空です",
                f"フィールド '{field}' に有効な値を設定してください"
            )
            return False
        
        if not isinstance(value, field_type):
            self.add_result(
                ValidationLevel.ERROR,
                field,
                f"フィールド '{field}' の型が正しくありません。期待値: {field_type.__name__}, 実際値: {type(value).__name__}",
                f"フィールド '{field}' を {field_type.__name__} 型で設定してください"
            )
            return False
        
        return True
    
    def validate_email(self, email: str, field: str) -> bool:
        """メールアドレスの検証"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            self.add_result(
                ValidationLevel.ERROR,
                field,
                f"無効なメールアドレス形式: {email}",
                "有効なメールアドレス形式で入力してください（例: user@example.com）"
            )
            return False
        return True
    
    def validate_project_name(self, project_name: str) -> bool:
        """プロジェクト名の検証"""
        if len(project_name.strip()) < 3:
            self.add_result(
                ValidationLevel.WARNING,
                "project_name",
                "プロジェクト名が短すぎます（3文字未満）",
                "より具体的なプロジェクト名を設定することを推奨します"
            )
            return False
        
        if len(project_name) > 100:
            self.add_result(
                ValidationLevel.WARNING,
                "project_name",
                "プロジェクト名が長すぎます（100文字超）",
                "より簡潔なプロジェクト名を設定することを推奨します"
            )
            return False
        
        # 特殊文字のチェック
        if re.search(r'[<>:"/\\|?*]', project_name):
            self.add_result(
                ValidationLevel.WARNING,
                "project_name",
                "プロジェクト名にファイルシステムで使用できない文字が含まれています",
                "特殊文字（< > : \" / \\ | ? *）の使用を避けてください"
            )
            return False
        
        return True
    
    def validate_version_format(self, version: str) -> bool:
        """バージョン形式の検証"""
        version_pattern = r'^\d+\.\d+(\.\d+)?(-[a-zA-Z0-9]+)?$'
        if not re.match(version_pattern, version):
            self.add_result(
                ValidationLevel.WARNING,
                "version",
                f"バージョン形式が推奨形式と異なります: {version}",
                "推奨形式: X.Y.Z または X.Y （例: 1.0.0, 2.1）"
            )
            return False
        return True
    
    def validate_date_format(self, date_str: str, field: str) -> bool:
        """日付形式の検証"""
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
            r'^\d{4}年\d{1,2}月\d{1,2}日$'  # YYYY年MM月DD日
        ]
        
        if not any(re.match(pattern, date_str) for pattern in date_patterns):
            self.add_result(
                ValidationLevel.WARNING,
                field,
                f"日付形式が推奨形式と異なります: {date_str}",
                "推奨形式: YYYY-MM-DD, YYYY/MM/DD, YYYY年MM月DD日"
            )
            return False
        return True
    
    def validate_text_length(self, text: str, field: str, min_length: int = 1, 
                           max_length: int = 1000) -> bool:
        """テキスト長の検証"""
        if len(text) < min_length:
            self.add_result(
                ValidationLevel.WARNING,
                field,
                f"フィールド '{field}' のテキストが短すぎます（{len(text)}文字、最小{min_length}文字）",
                f"最低{min_length}文字以上のテキストを入力してください"
            )
            return False
        
        if len(text) > max_length:
            self.add_result(
                ValidationLevel.WARNING,
                field,
                f"フィールド '{field}' のテキストが長すぎます（{len(text)}文字、最大{max_length}文字）",
                f"テキストを{max_length}文字以内に収めてください"
            )
            return False
        
        return True
    
    def validate_list_field(self, data: Dict[str, Any], field: str, 
                          min_items: int = 1, max_items: int = 100) -> bool:
        """リストフィールドの検証"""
        if field not in data:
            return True  # オプショナルフィールドとして扱う
        
        value = data[field]
        if not isinstance(value, list):
            self.add_result(
                ValidationLevel.ERROR,
                field,
                f"フィールド '{field}' はリスト形式である必要があります",
                f"フィールド '{field}' を配列形式で設定してください"
            )
            return False
        
        if len(value) < min_items:
            self.add_result(
                ValidationLevel.WARNING,
                field,
                f"フィールド '{field}' の項目数が少なすぎます（{len(value)}項目、最小{min_items}項目）",
                f"最低{min_items}項目以上設定することを推奨します"
            )
            return False
        
        if len(value) > max_items:
            self.add_result(
                ValidationLevel.WARNING,
                field,
                f"フィールド '{field}' の項目数が多すぎます（{len(value)}項目、最大{max_items}項目）",
                f"項目数を{max_items}項目以内に収めることを推奨します"
            )
            return False
        
        return True
    
    def generate_report(self, document_type: str) -> ValidationReport:
        """バリデーションレポートを生成"""
        errors = len([r for r in self.results if r.level == ValidationLevel.ERROR])
        warnings = len([r for r in self.results if r.level == ValidationLevel.WARNING])
        passed = len([r for r in self.results if r.is_valid])
        failed = len([r for r in self.results if not r.is_valid])
        
        return ValidationReport(
            document_type=document_type,
            total_checks=len(self.results),
            passed_checks=passed,
            failed_checks=failed,
            warnings=warnings,
            errors=errors,
            results=self.results
        )
    
    def reset(self) -> None:
        """バリデーション結果をリセット"""
        self.results.clear()