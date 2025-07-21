from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class SecurityDesignTemplate(BaseDocumentTemplate):
    """セキュリティ設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "security_design.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.SECURITY_DESIGN
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        return base_fields + [
            "security_requirements",
            "access_control_model",
            "authentication_method",
            "encryption_strategy",
            "compliance_requirements"
        ]
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. セキュリティ要件",
            "3. アクセス制御設計",
            "4. 認証・認可設計",
            "5. データ暗号化設計",
            "6. ネットワークセキュリティ",
            "7. 監査・ログ設計",
            "8. コンプライアンス対応",
            "9. セキュリティ運用",
            "10. インシデント対応"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date"),
            "security_requirements": data.get("security_requirements", {}),
            "access_control_model": data.get("access_control_model", {}),
            "authentication_method": data.get("authentication_method", {}),
            "encryption_strategy": data.get("encryption_strategy", {}),
            "network_security": data.get("network_security", {}),
            "audit_logging": data.get("audit_logging", {}),
            "compliance_requirements": data.get("compliance_requirements", []),
            "security_operations": data.get("security_operations", {}),
            "incident_response": data.get("incident_response", {})
        }
        
        # デフォルト値の設定
        if not context["security_requirements"]:
            context["security_requirements"] = self._get_default_security_requirements()
        
        if not context["access_control_model"]:
            context["access_control_model"] = self._get_default_access_control()
        
        return context
    
    def _get_default_security_requirements(self) -> Dict[str, Any]:
        return {
            "objectives": [
                "機密データの保護",
                "不正アクセスの防止",
                "データの完全性確保",
                "サービスの可用性維持",
                "規制要件への準拠"
            ],
            "principles": [
                "最小権限の原則",
                "多層防御の実装",
                "ゼロトラストアプローチ",
                "継続的な監視と改善"
            ],
            "scope": {
                "in_scope": [
                    "ServiceNowプラットフォーム全体",
                    "統合される外部システム",
                    "ユーザーアクセス管理",
                    "データの保存・転送"
                ],
                "out_of_scope": [
                    "エンドポイントセキュリティ",
                    "物理セキュリティ"
                ]
            }
        }
    
    def _get_default_access_control(self) -> Dict[str, Any]:
        return {
            "model": "Role-Based Access Control (RBAC)",
            "principles": [
                "職務分離の原則",
                "Need-to-Know原則",
                "定期的な権限レビュー"
            ],
            "role_hierarchy": {
                "admin_roles": [
                    {"name": "admin", "description": "システム管理者"},
                    {"name": "security_admin", "description": "セキュリティ管理者"}
                ],
                "process_roles": [
                    {"name": "itil", "description": "ITIL基本ロール"},
                    {"name": "incident_manager", "description": "インシデント管理者"},
                    {"name": "change_manager", "description": "変更管理者"}
                ],
                "user_roles": [
                    {"name": "itil_user", "description": "ITILユーザー"},
                    {"name": "self_service_user", "description": "セルフサービスユーザー"}
                ]
            }
        }