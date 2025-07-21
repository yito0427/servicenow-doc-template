"""
Validation manager for coordinating document validation
"""
from typing import Dict, Any, Optional, Type
from enum import Enum

from src.validators.base_validator import BaseValidator, ValidationReport
from src.validators.document_validator import (
    DocumentValidator,
    IncidentManagementValidator,
    KnowledgeManagementValidator,
    SLMDesignValidator
)
from src.models.document import DocumentType


class ValidationMode(Enum):
    """バリデーションモード"""
    STRICT = "strict"      # エラーがあると処理を停止
    PERMISSIVE = "permissive"  # 警告は無視してエラーのみチェック
    INFO_ONLY = "info_only"    # 情報提供のみ、エラーでも処理続行


class ValidationManager:
    """バリデーション管理クラス"""
    
    # ドキュメントタイプ別バリデーターマッピング
    VALIDATOR_MAPPING: Dict[DocumentType, Type[BaseValidator]] = {
        DocumentType.INCIDENT_MANAGEMENT: IncidentManagementValidator,
        DocumentType.KNOWLEDGE_MANAGEMENT: KnowledgeManagementValidator,
        DocumentType.SLM_DESIGN: SLMDesignValidator,
        # 他のドキュメントタイプは汎用バリデーターを使用
    }
    
    def __init__(self, mode: ValidationMode = ValidationMode.PERMISSIVE):
        self.mode = mode
        self.validation_history: list[ValidationReport] = []
    
    def validate_document(self, document_type: DocumentType, data: Dict[str, Any]) -> ValidationReport:
        """ドキュメントタイプに応じたバリデーションを実行"""
        
        # 適切なバリデーターを取得
        validator_class = self.VALIDATOR_MAPPING.get(document_type, DocumentValidator)
        validator = validator_class()
        
        # バリデーション実行
        report = validator.validate(data)
        
        # 履歴に追加
        self.validation_history.append(report)
        
        # モードに応じた処理
        if self.mode == ValidationMode.STRICT and not report.is_valid:
            raise ValidationError(f"Validation failed for {document_type.value}", report)
        
        return report
    
    def validate_multiple_documents(self, documents: Dict[DocumentType, Dict[str, Any]]) -> Dict[DocumentType, ValidationReport]:
        """複数ドキュメントの一括バリデーション"""
        results = {}
        
        for doc_type, data in documents.items():
            try:
                results[doc_type] = self.validate_document(doc_type, data)
            except ValidationError as e:
                if self.mode == ValidationMode.STRICT:
                    raise
                # エラーを含むレポートを結果に含める
                results[doc_type] = e.report
        
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """バリデーション履歴のサマリーを取得"""
        if not self.validation_history:
            return {"total_validations": 0}
        
        total_validations = len(self.validation_history)
        total_errors = sum(report.errors for report in self.validation_history)
        total_warnings = sum(report.warnings for report in self.validation_history)
        total_checks = sum(report.total_checks for report in self.validation_history)
        
        success_rate = sum(1 for report in self.validation_history if report.is_valid) / total_validations
        
        return {
            "total_validations": total_validations,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "total_checks": total_checks,
            "success_rate": success_rate,
            "most_recent_validation": self.validation_history[-1].document_type if self.validation_history else None
        }
    
    def clear_history(self) -> None:
        """バリデーション履歴をクリア"""
        self.validation_history.clear()
    
    def export_validation_report(self, report: ValidationReport, format: str = "text") -> str:
        """バリデーションレポートを指定形式でエクスポート"""
        if format == "text":
            return self._export_text_report(report)
        elif format == "markdown":
            return self._export_markdown_report(report)
        elif format == "html":
            return self._export_html_report(report)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_text_report(self, report: ValidationReport) -> str:
        """テキスト形式のレポート生成"""
        lines = []
        lines.append(f"=== バリデーションレポート: {report.document_type} ===")
        lines.append(f"総チェック数: {report.total_checks}")
        lines.append(f"成功: {report.passed_checks}, 失敗: {report.failed_checks}")
        lines.append(f"エラー: {report.errors}, 警告: {report.warnings}")
        lines.append(f"全体結果: {'✅ 合格' if report.is_valid else '❌ 不合格'}")
        lines.append("")
        
        if report.results:
            lines.append("詳細結果:")
            for i, result in enumerate(report.results, 1):
                status = "✅" if result.is_valid else "❌"
                level_icon = {"error": "🚨", "warning": "⚠️", "info": "ℹ️"}.get(result.level.value, "")
                lines.append(f"{i:2d}. {status} {level_icon} [{result.field}] {result.message}")
                if result.suggestion:
                    lines.append(f"    💡 提案: {result.suggestion}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _export_markdown_report(self, report: ValidationReport) -> str:
        """Markdown形式のレポート生成"""
        lines = []
        lines.append(f"# バリデーションレポート: {report.document_type}")
        lines.append("")
        lines.append("## サマリー")
        lines.append(f"- **総チェック数**: {report.total_checks}")
        lines.append(f"- **成功**: {report.passed_checks}")
        lines.append(f"- **失敗**: {report.failed_checks}")
        lines.append(f"- **エラー**: {report.errors}")
        lines.append(f"- **警告**: {report.warnings}")
        lines.append(f"- **全体結果**: {'✅ 合格' if report.is_valid else '❌ 不合格'}")
        lines.append("")
        
        if report.results:
            lines.append("## 詳細結果")
            lines.append("")
            
            # エラー
            errors = [r for r in report.results if r.level.value == "error"]
            if errors:
                lines.append("### 🚨 エラー")
                for result in errors:
                    lines.append(f"- **{result.field}**: {result.message}")
                    if result.suggestion:
                        lines.append(f"  - 💡 **提案**: {result.suggestion}")
                lines.append("")
            
            # 警告
            warnings = [r for r in report.results if r.level.value == "warning"]
            if warnings:
                lines.append("### ⚠️ 警告")
                for result in warnings:
                    lines.append(f"- **{result.field}**: {result.message}")
                    if result.suggestion:
                        lines.append(f"  - 💡 **提案**: {result.suggestion}")
                lines.append("")
            
            # 情報
            infos = [r for r in report.results if r.level.value == "info"]
            if infos:
                lines.append("### ℹ️ 情報・推奨事項")
                for result in infos:
                    lines.append(f"- **{result.field}**: {result.message}")
                    if result.suggestion:
                        lines.append(f"  - 💡 **提案**: {result.suggestion}")
                lines.append("")
        
        return "\n".join(lines)
    
    def _export_html_report(self, report: ValidationReport) -> str:
        """HTML形式のレポート生成"""
        status_class = "success" if report.is_valid else "error"
        status_text = "✅ 合格" if report.is_valid else "❌ 不合格"
        
        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>バリデーションレポート: {report.document_type}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .metric {{ background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #0066cc; }}
        .metric-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        .status.success {{ color: #28a745; }}
        .status.error {{ color: #dc3545; }}
        .result-item {{ margin: 10px 0; padding: 15px; border-radius: 6px; }}
        .result-error {{ background: #fee; border-left: 4px solid #dc3545; }}
        .result-warning {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
        .result-info {{ background: #e7f3ff; border-left: 4px solid #0066cc; }}
        .suggestion {{ margin-top: 8px; font-style: italic; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>バリデーションレポート: {report.document_type}</h1>
        <p class="status {status_class}"><strong>{status_text}</strong></p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <div class="metric-value">{report.total_checks}</div>
            <div class="metric-label">総チェック数</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report.passed_checks}</div>
            <div class="metric-label">成功</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report.failed_checks}</div>
            <div class="metric-label">失敗</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report.errors}</div>
            <div class="metric-label">エラー</div>
        </div>
        <div class="metric">
            <div class="metric-value">{report.warnings}</div>
            <div class="metric-label">警告</div>
        </div>
    </div>
"""
        
        if report.results:
            html += "<h2>詳細結果</h2>\n"
            
            for result in report.results:
                level_class = f"result-{result.level.value}"
                level_icon = {"error": "🚨", "warning": "⚠️", "info": "ℹ️"}.get(result.level.value, "")
                
                html += f"""
    <div class="result-item {level_class}">
        <strong>{level_icon} {result.field}</strong>: {result.message}
"""
                if result.suggestion:
                    html += f'        <div class="suggestion">💡 提案: {result.suggestion}</div>\n'
                
                html += "    </div>\n"
        
        html += """
</body>
</html>
"""
        return html


class ValidationError(Exception):
    """バリデーションエラー"""
    
    def __init__(self, message: str, report: ValidationReport):
        super().__init__(message)
        self.report = report


# 便利関数
def validate_document_data(document_type: DocumentType, data: Dict[str, Any], 
                          mode: ValidationMode = ValidationMode.PERMISSIVE) -> ValidationReport:
    """ドキュメントデータの簡単なバリデーション"""
    manager = ValidationManager(mode)
    return manager.validate_document(document_type, data)


def get_validator_for_document_type(document_type: DocumentType) -> BaseValidator:
    """ドキュメントタイプに対応するバリデーターを取得"""
    validator_class = ValidationManager.VALIDATOR_MAPPING.get(document_type, DocumentValidator)
    return validator_class()