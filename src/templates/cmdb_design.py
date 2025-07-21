from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class CMDBDesignTemplate(BaseDocumentTemplate):
    """CMDB設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "cmdb_design.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.CMDB_DESIGN
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        return base_fields + [
            "cmdb_scope",
            "ci_classes",
            "identification_rules",
            "relationships",
            "discovery_strategy"
        ]
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. CMDB設計方針",
            "3. CIクラス設計",
            "4. CI識別・正規化ルール",
            "5. 関係性設計",
            "6. Discovery戦略",
            "7. データ品質管理",
            "8. 実装計画",
            "9. テスト計画",
            "10. リスクと対策"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date"),
            "cmdb_scope": data.get("cmdb_scope", {}),
            "ci_classes": data.get("ci_classes", []),
            "identification_rules": data.get("identification_rules", []),
            "relationships": data.get("relationships", []),
            "discovery_strategy": data.get("discovery_strategy", {}),
            "data_quality": data.get("data_quality", {}),
            "implementation_plan": data.get("implementation_plan", {}),
            "test_plan": data.get("test_plan", {}),
            "risks": data.get("risks", [])
        }
        
        # デフォルト値の設定
        if not context["cmdb_scope"]:
            context["cmdb_scope"] = self._get_default_cmdb_scope()
        
        if not context["ci_classes"]:
            context["ci_classes"] = self._get_default_ci_classes()
        
        return context
    
    def _get_default_cmdb_scope(self) -> Dict[str, Any]:
        return {
            "description": "本CMDBは、ITサービス管理に必要なすべての構成アイテムとその関係性を管理します。",
            "objectives": [
                "ITサービスとビジネスサービスの関係性の可視化",
                "インシデント・問題・変更管理プロセスの効率化",
                "正確な影響分析の実現",
                "IT資産の適切な管理"
            ],
            "in_scope": [
                "本番環境のすべてのサーバー、ネットワーク機器",
                "ビジネスクリティカルなアプリケーション",
                "データベースとミドルウェア",
                "仮想化基盤とクラウドリソース"
            ],
            "out_of_scope": [
                "開発・テスト環境の一時的なリソース",
                "エンドユーザーのPC・モバイルデバイス（初期フェーズ）",
                "オフィス機器（プリンター等）"
            ]
        }
    
    def _get_default_ci_classes(self) -> list:
        return [
            {
                "name": "cmdb_ci_server",
                "label": "サーバー",
                "parent": "cmdb_ci_computer",
                "attributes": [
                    {"name": "host_name", "type": "string", "mandatory": True},
                    {"name": "ip_address", "type": "string", "mandatory": True},
                    {"name": "os", "type": "reference", "mandatory": True},
                    {"name": "cpu_count", "type": "integer", "mandatory": False},
                    {"name": "ram", "type": "integer", "mandatory": False}
                ]
            },
            {
                "name": "cmdb_ci_business_app",
                "label": "ビジネスアプリケーション",
                "parent": "cmdb_ci_appl",
                "attributes": [
                    {"name": "name", "type": "string", "mandatory": True},
                    {"name": "version", "type": "string", "mandatory": True},
                    {"name": "business_criticality", "type": "choice", "mandatory": True},
                    {"name": "support_group", "type": "reference", "mandatory": True}
                ]
            }
        ]