from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class ChangeManagementTemplate(BaseDocumentTemplate):
    """変更管理設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "change_management.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.CHANGE_MANAGEMENT
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. 変更管理プロセス",
            "3. 変更タイプと分類",
            "4. 変更諮問委員会（CAB）",
            "5. 変更評価とリスク分析",
            "6. 変更実装プロセス",
            "7. 役割と責任",
            "8. ワークフロー設計",
            "9. 変更カレンダー",
            "10. KPIとメトリクス",
            "11. 他プロセスとの連携"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "process_overview": data.get("process_overview", {}),
            "change_types": data.get("change_types", []),
            "cab_structure": data.get("cab_structure", {}),
            "risk_assessment": data.get("risk_assessment", {}),
            "implementation_process": data.get("implementation_process", {}),
            "roles_responsibilities": data.get("roles_responsibilities", []),
            "workflow_design": data.get("workflow_design", {}),
            "change_windows": data.get("change_windows", []),
            "kpi_metrics": data.get("kpi_metrics", []),
            "integration_points": data.get("integration_points", [])
        }
        
        # デフォルト値の設定
        if not context["process_overview"]:
            context["process_overview"] = self._get_default_process_overview()
        
        if not context["change_types"]:
            context["change_types"] = self._get_default_change_types()
        
        if not context["cab_structure"]:
            context["cab_structure"] = self._get_default_cab_structure()
        
        if not context["risk_assessment"]:
            context["risk_assessment"] = self._get_default_risk_assessment()
        
        if not context["change_windows"]:
            context["change_windows"] = self._get_default_change_windows()
        
        if not context["kpi_metrics"]:
            context["kpi_metrics"] = self._get_default_kpi_metrics()
        
        return context
    
    def _get_default_process_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "ITサービスへの変更を制御し、変更に伴うリスクを最小化しながら、ビジネス価値を最大化する",
            "scope": "ITインフラストラクチャ、アプリケーション、プロセス、ドキュメントへのすべての変更",
            "objectives": [
                "変更に伴うサービス中断の最小化",
                "変更の成功率向上",
                "無許可変更の防止",
                "変更影響の適切な評価",
                "効率的な変更実装"
            ],
            "benefits": [
                "サービス可用性の向上",
                "変更失敗によるインシデント削減",
                "コンプライアンスの確保",
                "リソースの最適活用",
                "ビジネスとITの連携強化"
            ]
        }
    
    def _get_default_change_types(self) -> list:
        return [
            {
                "type": "標準変更",
                "description": "事前承認済み、低リスク、手順が確立された変更",
                "approval": "事前承認（自動承認）",
                "lead_time": "即時",
                "examples": ["パスワードリセット", "標準的なソフトウェアインストール", "ユーザーアクセス権限付与"]
            },
            {
                "type": "通常変更",
                "description": "標準的なCABプロセスに従う変更",
                "approval": "CAB承認",
                "lead_time": "5営業日",
                "examples": ["サーバーパッチ適用", "アプリケーション更新", "ネットワーク設定変更"]
            },
            {
                "type": "緊急変更",
                "description": "重大なインシデント対応や緊急修正が必要な変更",
                "approval": "ECAB（緊急CAB）承認",
                "lead_time": "2時間以内",
                "examples": ["セキュリティパッチ", "サービス復旧のための変更", "重大バグ修正"]
            },
            {
                "type": "重大変更",
                "description": "大規模、高リスク、高コストの変更",
                "approval": "CAB + 経営層承認",
                "lead_time": "20営業日",
                "examples": ["新システム導入", "データセンター移行", "主要アップグレード"]
            }
        ]
    
    def _get_default_cab_structure(self) -> Dict[str, Any]:
        return {
            "regular_cab": {
                "purpose": "通常変更と重大変更の評価・承認",
                "frequency": "週次（毎週木曜日 14:00-15:00）",
                "chair": "変更マネージャー",
                "core_members": [
                    "ITサービスマネージャー",
                    "インフラリーダー",
                    "アプリケーションリーダー",
                    "セキュリティ担当者",
                    "ビジネス代表者"
                ],
                "optional_members": [
                    "影響を受けるサービスオーナー",
                    "技術専門家（SME）",
                    "ベンダー代表"
                ]
            },
            "emergency_cab": {
                "purpose": "緊急変更の迅速な評価・承認",
                "frequency": "必要に応じて（30分以内に招集）",
                "chair": "変更マネージャーまたは代理",
                "minimum_members": [
                    "変更マネージャー",
                    "技術リーダー",
                    "影響を受けるサービスオーナー"
                ]
            },
            "cab_agenda": [
                "前回のCABアクションレビュー",
                "変更失敗のレビュー",
                "今週の変更要求レビュー",
                "変更カレンダー確認",
                "リスクと競合の評価",
                "承認決定"
            ]
        }
    
    def _get_default_risk_assessment(self) -> Dict[str, Any]:
        return {
            "risk_factors": [
                {
                    "factor": "技術的複雑性",
                    "weight": 25,
                    "levels": ["低（既知技術）", "中（一部新技術）", "高（新技術・未検証）"]
                },
                {
                    "factor": "ビジネス影響",
                    "weight": 30,
                    "levels": ["低（限定的）", "中（部門レベル）", "高（全社レベル）"]
                },
                {
                    "factor": "変更規模",
                    "weight": 20,
                    "levels": ["小（単一システム）", "中（複数システム）", "大（基盤全体）"]
                },
                {
                    "factor": "ロールバック可能性",
                    "weight": 25,
                    "levels": ["容易（自動化済）", "可能（手動手順）", "困難（データ変更含む）"]
                }
            ],
            "risk_matrix": {
                "low": {"score": "0-30", "color": "green", "action": "標準手順で実施"},
                "medium": {"score": "31-60", "color": "yellow", "action": "追加レビューと対策"},
                "high": {"score": "61-80", "color": "orange", "action": "詳細計画と承認"},
                "critical": {"score": "81-100", "color": "red", "action": "経営層承認必須"}
            }
        }
    
    def _get_default_change_windows(self) -> list:
        return [
            {
                "window_type": "標準保守ウィンドウ",
                "schedule": "毎週土曜日 22:00-06:00",
                "allowed_changes": ["パッチ適用", "定期メンテナンス", "設定変更"],
                "approval_required": "通常CAB"
            },
            {
                "window_type": "月次保守ウィンドウ",
                "schedule": "第3土曜日 20:00-08:00",
                "allowed_changes": ["大規模更新", "インフラ変更", "移行作業"],
                "approval_required": "CAB + サービスオーナー"
            },
            {
                "window_type": "緊急保守ウィンドウ",
                "schedule": "随時（ECAB承認後）",
                "allowed_changes": ["緊急修正", "セキュリティパッチ"],
                "approval_required": "ECAB"
            },
            {
                "window_type": "ブラックアウト期間",
                "schedule": "年末年始、会計年度末、重要イベント期間",
                "allowed_changes": ["緊急変更のみ"],
                "approval_required": "経営層承認"
            }
        ]
    
    def _get_default_kpi_metrics(self) -> list:
        return [
            {
                "name": "変更成功率",
                "description": "計画通りに完了した変更の割合",
                "target": "95%以上",
                "formula": "成功変更数 / 実施変更総数 × 100"
            },
            {
                "name": "緊急変更率",
                "description": "全変更に占める緊急変更の割合",
                "target": "10%以下",
                "formula": "緊急変更数 / 変更総数 × 100"
            },
            {
                "name": "変更起因インシデント",
                "description": "変更が原因で発生したインシデント数",
                "target": "変更あたり0.1件以下",
                "formula": "変更起因インシデント数 / 実施変更数"
            },
            {
                "name": "未承認変更検出数",
                "description": "承認なしに実施された変更の数",
                "target": "0件",
                "formula": "検出された未承認変更数"
            },
            {
                "name": "変更リードタイム",
                "description": "RFC提出から実装までの平均日数",
                "target": "タイプ別目標値",
                "formula": "合計リードタイム / 変更数"
            }
        ]