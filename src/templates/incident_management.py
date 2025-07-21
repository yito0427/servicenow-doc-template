from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class IncidentManagementTemplate(BaseDocumentTemplate):
    """インシデント管理設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "incident_management.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.INCIDENT_MANAGEMENT
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. プロセス定義",
            "3. インシデント分類",
            "4. 優先度マトリクス",
            "5. エスカレーション設計",
            "6. SLA定義",
            "7. 役割と責任",
            "8. ワークフロー設計",
            "9. 通知設計",
            "10. KPIとレポート",
            "11. 他プロセスとの連携"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 設定ファイルからデフォルト値を取得
        default_values = self.get_default_values()
        
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "process_overview": data.get("process_overview", {}),
            "incident_categories": data.get("incident_categories", []),
            "priority_matrix": data.get("priority_matrix", {}),
            "escalation_rules": data.get("escalation_rules", []),
            "sla_definitions": data.get("sla_definitions", []),
            "roles_responsibilities": data.get("roles_responsibilities", []),
            "workflow_design": data.get("workflow_design", {}),
            "notification_rules": data.get("notification_rules", []),
            "kpi_metrics": data.get("kpi_metrics", []),
            "integration_points": data.get("integration_points", [])
        }
        
        # 設定ファイルからのデフォルト値を使用
        context.update({
            "incident_types": data.get("incident_types", default_values.get("incident_types", ["システム障害", "パフォーマンス問題"])),
            "priority_levels": data.get("priority_levels", default_values.get("priority_levels", ["重要", "高", "中", "低"])),
            "escalation_rules": data.get("escalation_rules", default_values.get("escalation_rules", "30分以内に上位者へエスカレーション")),
            "sla_targets": data.get("sla_targets", default_values.get("sla_targets", {}))
        })
        
        # デフォルト値の設定（既存のメソッドも継続使用）
        if not context["process_overview"]:
            context["process_overview"] = self._get_default_process_overview()
        
        if not context["incident_categories"]:
            context["incident_categories"] = self._get_default_categories()
        
        if not context["priority_matrix"]:
            context["priority_matrix"] = self._get_default_priority_matrix()
        
        if not context["sla_definitions"]:
            context["sla_definitions"] = self._get_default_sla()
        
        return context
    
    def _get_default_process_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "ITサービスの正常な運用を迅速に回復し、ビジネスへの影響を最小限に抑える",
            "scope": "すべてのITサービスに関するインシデントの記録、分類、調査、解決、クローズ",
            "objectives": [
                "インシデントの迅速な解決",
                "ビジネスへの影響の最小化",
                "インシデントの可視化と追跡",
                "サービスレベルの維持",
                "ユーザー満足度の向上"
            ],
            "benefits": [
                "ダウンタイムの削減",
                "生産性の向上",
                "インシデント対応の標準化",
                "ナレッジの蓄積と活用"
            ]
        }
    
    def _get_default_categories(self) -> list:
        return [
            {
                "category": "ハードウェア",
                "subcategories": ["サーバー", "ネットワーク機器", "ストレージ", "PC・周辺機器"],
                "assignment_group": "インフラチーム"
            },
            {
                "category": "ソフトウェア",
                "subcategories": ["OS", "ミドルウェア", "アプリケーション", "データベース"],
                "assignment_group": "アプリケーションチーム"
            },
            {
                "category": "ネットワーク",
                "subcategories": ["LAN", "WAN", "インターネット接続", "VPN"],
                "assignment_group": "ネットワークチーム"
            },
            {
                "category": "サービス要求",
                "subcategories": ["アカウント", "アクセス権限", "ソフトウェアインストール"],
                "assignment_group": "サービスデスク"
            }
        ]
    
    def _get_default_priority_matrix(self) -> Dict[str, Any]:
        return {
            "factors": {
                "impact": [
                    {"level": "高", "description": "多数のユーザー/重要業務に影響", "score": 3},
                    {"level": "中", "description": "一部のユーザー/業務に影響", "score": 2},
                    {"level": "低", "description": "個人ユーザーに影響", "score": 1}
                ],
                "urgency": [
                    {"level": "高", "description": "即時対応が必要", "score": 3},
                    {"level": "中", "description": "業務時間内の対応で可", "score": 2},
                    {"level": "低", "description": "計画的な対応で可", "score": 1}
                ]
            },
            "matrix": [
                {"impact": "高", "urgency": "高", "priority": "P1 - Critical"},
                {"impact": "高", "urgency": "中", "priority": "P2 - High"},
                {"impact": "高", "urgency": "低", "priority": "P3 - Medium"},
                {"impact": "中", "urgency": "高", "priority": "P2 - High"},
                {"impact": "中", "urgency": "中", "priority": "P3 - Medium"},
                {"impact": "中", "urgency": "低", "priority": "P4 - Low"},
                {"impact": "低", "urgency": "高", "priority": "P3 - Medium"},
                {"impact": "低", "urgency": "中", "priority": "P4 - Low"},
                {"impact": "低", "urgency": "低", "priority": "P5 - Planning"}
            ]
        }
    
    def _get_default_sla(self) -> list:
        return [
            {
                "priority": "P1 - Critical",
                "response_time": "15分",
                "resolution_time": "4時間",
                "escalation_time": "1時間"
            },
            {
                "priority": "P2 - High",
                "response_time": "30分",
                "resolution_time": "8時間",
                "escalation_time": "2時間"
            },
            {
                "priority": "P3 - Medium",
                "response_time": "2時間",
                "resolution_time": "24時間",
                "escalation_time": "8時間"
            },
            {
                "priority": "P4 - Low",
                "response_time": "8時間",
                "resolution_time": "72時間",
                "escalation_time": "24時間"
            },
            {
                "priority": "P5 - Planning",
                "response_time": "24時間",
                "resolution_time": "計画に従う",
                "escalation_time": "N/A"
            }
        ]