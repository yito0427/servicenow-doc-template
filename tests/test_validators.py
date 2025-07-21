"""
Validation tests
"""
import pytest
from typing import Dict, Any

from src.validators.base_validator import (
    BaseValidator, ValidationLevel, ValidationResult, ValidationReport
)
from src.validators.document_validator import (
    DocumentValidator, IncidentManagementValidator, 
    KnowledgeManagementValidator, SLMDesignValidator
)
from src.validators.validation_manager import (
    ValidationManager, ValidationMode, ValidationError
)
from src.models.document import DocumentType


class TestBaseValidator:
    """基底バリデーターのテスト"""
    
    def test_validation_result_creation(self):
        """バリデーション結果作成のテスト"""
        result = ValidationResult(
            is_valid=True,
            level=ValidationLevel.INFO,
            field="test_field",
            message="テストメッセージ",
            suggestion="テスト提案"
        )
        
        assert result.is_valid is True
        assert result.level == ValidationLevel.INFO
        assert result.field == "test_field"
        assert result.message == "テストメッセージ"
        assert result.suggestion == "テスト提案"
    
    def test_validation_report_creation(self):
        """バリデーションレポート作成のテスト"""
        results = [
            ValidationResult(
                is_valid=True, level=ValidationLevel.INFO,
                field="field1", message="OK"
            ),
            ValidationResult(
                is_valid=False, level=ValidationLevel.ERROR,
                field="field2", message="Error"
            )
        ]
        
        report = ValidationReport(
            document_type="test",
            total_checks=2,
            passed_checks=1,
            failed_checks=1,
            warnings=0,
            errors=1,
            results=results
        )
        
        assert report.document_type == "test"
        assert report.total_checks == 2
        assert report.errors == 1
        assert report.is_valid is False  # エラーがあるので無効
    
    def test_base_validator_required_field_validation(self):
        """必須フィールドバリデーションのテスト"""
        class TestValidator(BaseValidator):
            def validate(self, data: Dict[str, Any]) -> ValidationReport:
                self.reset()
                self.validate_required_field(data, "required_field", str)
                return self.generate_report("test")
        
        validator = TestValidator()
        
        # 必須フィールドが存在する場合
        valid_data = {"required_field": "value"}
        report = validator.validate(valid_data)
        assert report.is_valid is True
        
        # 必須フィールドが存在しない場合
        validator.reset()
        invalid_data = {}
        report = validator.validate(invalid_data)
        assert report.is_valid is False
        assert report.errors == 1
    
    def test_email_validation(self):
        """メールアドレスバリデーションのテスト"""
        class TestValidator(BaseValidator):
            def validate(self, data: Dict[str, Any]) -> ValidationReport:
                self.reset()
                if "email" in data:
                    self.validate_email(data["email"], "email")
                return self.generate_report("test")
        
        validator = TestValidator()
        
        # 有効なメールアドレス
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.jp",
            "admin+tag@company.org"
        ]
        
        for email in valid_emails:
            validator.reset()
            report = validator.validate({"email": email})
            assert report.is_valid is True, f"Valid email failed: {email}"
        
        # 無効なメールアドレス
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user..name@domain.com"
        ]
        
        for email in invalid_emails:
            validator.reset()
            report = validator.validate({"email": email})
            assert report.is_valid is False, f"Invalid email passed: {email}"
    
    def test_project_name_validation(self):
        """プロジェクト名バリデーションのテスト"""
        class TestValidator(BaseValidator):
            def validate(self, data: Dict[str, Any]) -> ValidationReport:
                self.reset()
                if "project_name" in data:
                    self.validate_project_name(data["project_name"])
                return self.generate_report("test")
        
        validator = TestValidator()
        
        # 有効なプロジェクト名
        valid_names = [
            "ServiceNow ITSM Project",
            "システム構築プロジェクト",
            "Project ABC-123"
        ]
        
        for name in valid_names:
            validator.reset()
            report = validator.validate({"project_name": name})
            # 警告があっても有効とする（警告レベルのため）
            error_count = len([r for r in report.results if r.level == ValidationLevel.ERROR])
            assert error_count == 0, f"Valid project name failed: {name}"
        
        # 無効なプロジェクト名（短すぎる）
        validator.reset()
        report = validator.validate({"project_name": "AB"})
        warning_count = len([r for r in report.results if r.level == ValidationLevel.WARNING])
        assert warning_count > 0


class TestDocumentValidator:
    """ドキュメントバリデーターのテスト"""
    
    def test_valid_document_data(self):
        """有効なドキュメントデータのテスト"""
        validator = DocumentValidator()
        
        valid_data = {
            "project_name": "テストプロジェクト",
            "author": {
                "name": "山田太郎",
                "email": "yamada@example.com",
                "role": "システムアナリスト"
            },
            "version": "1.0.0",
            "client": {
                "name": "株式会社テスト",
                "department": "IT部"
            }
        }
        
        report = validator.validate(valid_data)
        assert report.is_valid is True
        assert report.errors == 0
    
    def test_missing_required_fields(self):
        """必須フィールド不足のテスト"""
        validator = DocumentValidator()
        
        invalid_data = {
            "project_name": "テストプロジェクト"
            # author フィールドが不足
        }
        
        report = validator.validate(invalid_data)
        assert report.is_valid is False
        assert report.errors > 0
        
        # authorフィールドのエラーがあることを確認
        author_errors = [r for r in report.results if "author" in r.field and r.level == ValidationLevel.ERROR]
        assert len(author_errors) > 0
    
    def test_invalid_email_in_author(self):
        """作成者の無効なメールアドレステスト"""
        validator = DocumentValidator()
        
        invalid_data = {
            "project_name": "テストプロジェクト",
            "author": {
                "name": "山田太郎",
                "email": "invalid-email"  # 無効なメールアドレス
            }
        }
        
        report = validator.validate(invalid_data)
        assert report.is_valid is False
        
        # メールアドレスエラーがあることを確認
        email_errors = [r for r in report.results if "email" in r.field and r.level == ValidationLevel.ERROR]
        assert len(email_errors) > 0


class TestIncidentManagementValidator:
    """インシデント管理バリデーターのテスト"""
    
    def test_valid_incident_management_data(self):
        """有効なインシデント管理データのテスト"""
        validator = IncidentManagementValidator()
        
        valid_data = {
            "project_name": "インシデント管理プロジェクト",
            "author": {
                "name": "山田太郎",
                "email": "yamada@example.com"
            },
            "incident_types": ["システム障害", "パフォーマンス問題", "ユーザーサポート"],
            "priority_levels": ["重要", "高", "中", "低"],
            "sla_targets": {
                "critical": "4時間",
                "high": "8時間",
                "medium": "24時間",
                "low": "72時間"
            },
            "escalation_rules": "30分以内に上位者へエスカレーション"
        }
        
        report = validator.validate(valid_data)
        assert report.document_type == "Incident Management"
        # エラーがないことを確認（警告は許容）
        assert report.errors == 0
    
    def test_insufficient_incident_types(self):
        """インシデントタイプ不足のテスト"""
        validator = IncidentManagementValidator()
        
        data_with_few_types = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"},
            "incident_types": ["システム障害"]  # 3つ未満
        }
        
        report = validator.validate(data_with_few_types)
        
        # 警告があることを確認
        incident_warnings = [r for r in report.results if "incident_types" in r.field]
        assert len(incident_warnings) > 0
    
    def test_sla_targets_validation(self):
        """SLA目標バリデーションのテスト"""
        validator = IncidentManagementValidator()
        
        data_with_sla = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"},
            "sla_targets": {
                "critical": "4時間",
                "high": "8時間"
                # medium, low が不足
            }
        }
        
        report = validator.validate(data_with_sla)
        
        # SLA関連の情報レベルメッセージがあることを確認
        sla_info = [r for r in report.results if "sla_targets" in r.field and r.level == ValidationLevel.INFO]
        assert len(sla_info) > 0


class TestKnowledgeManagementValidator:
    """ナレッジ管理バリデーターのテスト"""
    
    def test_valid_knowledge_management_data(self):
        """有効なナレッジ管理データのテスト"""
        validator = KnowledgeManagementValidator()
        
        valid_data = {
            "project_name": "ナレッジ管理プロジェクト",
            "author": {
                "name": "田中花子",
                "email": "tanaka@example.com"
            },
            "knowledge_types": [
                {"name": "How-to記事", "description": "手順説明"},
                {"name": "FAQ", "description": "よくある質問"},
                {"name": "トラブルシューティングガイド", "description": "問題解決"}
            ],
            "content_categories": [
                {"name": "基本操作", "description": "基本的な操作方法", "audience": "全ユーザー"},
                {"name": "管理者向け", "description": "システム管理", "audience": "管理者"},
                {"name": "トラブルシューティング", "description": "問題解決", "audience": "サポート"}
            ]
        }
        
        report = validator.validate(valid_data)
        assert report.document_type == "Knowledge Management"
        assert report.errors == 0
    
    def test_insufficient_knowledge_types(self):
        """ナレッジタイプ不足のテスト"""
        validator = KnowledgeManagementValidator()
        
        data_with_few_types = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"},
            "knowledge_types": ["FAQ"]  # 2つ未満
        }
        
        report = validator.validate(data_with_few_types)
        
        # 警告があることを確認
        knowledge_warnings = [r for r in report.results if "knowledge_types" in r.field]
        assert len(knowledge_warnings) > 0


class TestSLMDesignValidator:
    """SLM設計バリデーターのテスト"""
    
    def test_valid_slm_design_data(self):
        """有効なSLM設計データのテスト"""
        validator = SLMDesignValidator()
        
        valid_data = {
            "project_name": "SLM設計プロジェクト",
            "author": {
                "name": "佐藤次郎",
                "email": "sato@example.com"
            },
            "service_categories": ["基幹業務システム", "インフラサービス", "オフィス系システム"],
            "measurement_metrics": [
                {"name": "可用性", "definition": "システム稼働率", "formula": "稼働時間/総時間*100"},
                {"name": "応答時間", "definition": "レスポンス時間", "formula": "平均応答時間"},
                {"name": "顧客満足度", "definition": "満足度評価", "formula": "アンケート平均値"}
            ],
            "reporting_frequency": {
                "daily": "日次レポート",
                "weekly": "週次レポート",
                "monthly": "月次レポート",
                "quarterly": "四半期レポート"
            }
        }
        
        report = validator.validate(valid_data)
        assert report.document_type == "SLM Design"
        assert report.errors == 0
    
    def test_missing_critical_metrics(self):
        """重要メトリクス不足のテスト"""
        validator = SLMDesignValidator()
        
        data_missing_metrics = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"},
            "measurement_metrics": [
                {"name": "その他メトリクス", "definition": "その他", "formula": "計算式"}
                # 可用性、応答時間、顧客満足度が不足
            ]
        }
        
        report = validator.validate(data_missing_metrics)
        
        # 重要メトリクス不足の警告があることを確認
        metric_warnings = [r for r in report.results if "measurement_metrics" in r.field and r.level == ValidationLevel.WARNING]
        assert len(metric_warnings) > 0


class TestValidationManager:
    """バリデーション管理のテスト"""
    
    def test_validation_manager_creation(self):
        """バリデーション管理作成のテスト"""
        manager = ValidationManager(ValidationMode.PERMISSIVE)
        assert manager.mode == ValidationMode.PERMISSIVE
        assert len(manager.validation_history) == 0
    
    def test_document_validation_with_manager(self):
        """管理機能を使ったドキュメントバリデーションのテスト"""
        manager = ValidationManager(ValidationMode.PERMISSIVE)
        
        valid_data = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"}
        }
        
        report = manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, valid_data)
        
        assert len(manager.validation_history) == 1
        assert report.document_type == "Incident Management"
    
    def test_strict_mode_validation_error(self):
        """Strictモードでのバリデーションエラーテスト"""
        manager = ValidationManager(ValidationMode.STRICT)
        
        invalid_data = {
            "project_name": "テストプロジェクト"
            # author フィールドが不足
        }
        
        with pytest.raises(ValidationError):
            manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, invalid_data)
    
    def test_permissive_mode_validation(self):
        """Permissiveモードでのバリデーションテスト"""
        manager = ValidationManager(ValidationMode.PERMISSIVE)
        
        invalid_data = {
            "project_name": "テストプロジェクト"
            # author フィールドが不足
        }
        
        # 例外は発生せず、レポートが返される
        report = manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, invalid_data)
        assert report.is_valid is False
        assert report.errors > 0
    
    def test_validation_summary(self):
        """バリデーションサマリーのテスト"""
        manager = ValidationManager(ValidationMode.PERMISSIVE)
        
        # 複数のバリデーションを実行
        valid_data = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"}
        }
        
        manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, valid_data)
        manager.validate_document(DocumentType.KNOWLEDGE_MANAGEMENT, valid_data)
        
        summary = manager.get_validation_summary()
        assert summary["total_validations"] == 2
        assert "success_rate" in summary
        assert "total_checks" in summary
    
    def test_report_export_formats(self):
        """レポートエクスポート形式のテスト"""
        manager = ValidationManager(ValidationMode.PERMISSIVE)
        
        data = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"}
        }
        
        report = manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, data)
        
        # 各形式でエクスポートできることを確認
        text_report = manager.export_validation_report(report, "text")
        assert isinstance(text_report, str)
        assert "バリデーションレポート" in text_report
        
        markdown_report = manager.export_validation_report(report, "markdown")
        assert isinstance(markdown_report, str)
        assert "# バリデーションレポート" in markdown_report
        
        html_report = manager.export_validation_report(report, "html")
        assert isinstance(html_report, str)
        assert "<html" in html_report
        assert "</html>" in html_report
    
    def test_unsupported_export_format(self):
        """サポートされていないエクスポート形式のテスト"""
        manager = ValidationManager(ValidationMode.PERMISSIVE)
        
        data = {
            "project_name": "テストプロジェクト",
            "author": {"name": "テスト", "email": "test@example.com"}
        }
        
        report = manager.validate_document(DocumentType.INCIDENT_MANAGEMENT, data)
        
        with pytest.raises(ValueError):
            manager.export_validation_report(report, "unsupported_format")