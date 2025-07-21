from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class ProblemManagementTemplate(BaseDocumentTemplate):
    """問題管理設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "problem_management.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.PROBLEM_MANAGEMENT
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. プロセス定義",
            "3. 問題の分類と優先度",
            "4. 根本原因分析（RCA）",
            "5. 既知エラーデータベース（KEDB）",
            "6. 役割と責任",
            "7. ワークフロー設計",
            "8. エスカレーション",
            "9. KPIとメトリクス",
            "10. 他プロセスとの連携"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "process_overview": data.get("process_overview", {}),
            "problem_categories": data.get("problem_categories", []),
            "priority_criteria": data.get("priority_criteria", {}),
            "rca_methodology": data.get("rca_methodology", {}),
            "kedb_structure": data.get("kedb_structure", {}),
            "roles_responsibilities": data.get("roles_responsibilities", []),
            "workflow_stages": data.get("workflow_stages", []),
            "escalation_matrix": data.get("escalation_matrix", {}),
            "kpi_metrics": data.get("kpi_metrics", []),
            "integration_points": data.get("integration_points", [])
        }
        
        # デフォルト値の設定
        if not context["process_overview"]:
            context["process_overview"] = self._get_default_process_overview()
        
        if not context["problem_categories"]:
            context["problem_categories"] = self._get_default_categories()
        
        if not context["rca_methodology"]:
            context["rca_methodology"] = self._get_default_rca_methodology()
        
        if not context["workflow_stages"]:
            context["workflow_stages"] = self._get_default_workflow_stages()
        
        if not context["kpi_metrics"]:
            context["kpi_metrics"] = self._get_default_kpi_metrics()
        
        return context
    
    def _get_default_process_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "インシデントの根本原因を特定し、恒久的な解決策を実装することで、インシデントの再発を防止する",
            "scope": "繰り返し発生するインシデント、重大インシデント、および潜在的な問題の分析と解決",
            "objectives": [
                "インシデントの根本原因の特定",
                "恒久的解決策の開発と実装",
                "インシデント再発の防止",
                "既知エラーの文書化と管理",
                "サービス品質の継続的改善"
            ],
            "benefits": [
                "インシデント発生数の削減",
                "サービス可用性の向上",
                "問題解決時間の短縮",
                "ナレッジの蓄積と活用",
                "IT運用コストの削減"
            ]
        }
    
    def _get_default_categories(self) -> list:
        return [
            {
                "category": "インフラストラクチャ",
                "description": "ハードウェア、ネットワーク、データセンター関連",
                "examples": ["サーバー障害", "ネットワーク輻輳", "ストレージ容量不足"]
            },
            {
                "category": "アプリケーション",
                "description": "ソフトウェア、アプリケーション関連",
                "examples": ["バグ", "パフォーマンス問題", "互換性問題"]
            },
            {
                "category": "プロセス",
                "description": "運用プロセス、手順関連",
                "examples": ["手順の欠陥", "コミュニケーション不足", "スキル不足"]
            },
            {
                "category": "外部要因",
                "description": "サードパーティ、環境要因",
                "examples": ["ベンダー問題", "自然災害", "規制変更"]
            }
        ]
    
    def _get_default_rca_methodology(self) -> Dict[str, Any]:
        return {
            "methods": [
                {
                    "name": "5 Whys（なぜなぜ分析）",
                    "description": "問題に対して「なぜ」を5回繰り返し、根本原因を特定",
                    "use_case": "比較的単純な問題、単一の原因が疑われる場合"
                },
                {
                    "name": "フィッシュボーン図（特性要因図）",
                    "description": "問題の要因を人、方法、機械、材料、測定、環境の観点から分析",
                    "use_case": "複雑な問題、複数の要因が関連する場合"
                },
                {
                    "name": "タイムライン分析",
                    "description": "問題発生前後の時系列イベントを分析",
                    "use_case": "時系列で発生した複雑な問題"
                },
                {
                    "name": "Kepner-Tregoe法",
                    "description": "問題の記述、原因分析、解決策選定、潜在問題分析の体系的アプローチ",
                    "use_case": "重大な問題、体系的な分析が必要な場合"
                }
            ],
            "process": [
                "問題の明確な定義",
                "データ収集と証拠の確保",
                "時系列での事象の整理",
                "分析手法の選定と実施",
                "根本原因の特定と検証",
                "解決策の開発",
                "効果の測定と文書化"
            ]
        }
    
    def _get_default_workflow_stages(self) -> list:
        return [
            {
                "stage": "問題検出",
                "activities": ["トレンド分析", "重大インシデントレビュー", "プロアクティブ問題識別"],
                "outputs": ["問題レコード作成"]
            },
            {
                "stage": "問題分類",
                "activities": ["カテゴリ割当", "優先度設定", "影響分析"],
                "outputs": ["分類済み問題レコード"]
            },
            {
                "stage": "調査・診断",
                "activities": ["データ収集", "根本原因分析", "再現テスト"],
                "outputs": ["RCA報告書"]
            },
            {
                "stage": "回避策の特定",
                "activities": ["一時的解決策の開発", "影響評価", "実装計画"],
                "outputs": ["回避策文書", "KEDB登録"]
            },
            {
                "stage": "解決策の開発",
                "activities": ["恒久対策の設計", "テスト計画", "変更要求作成"],
                "outputs": ["解決策設計書", "RFC"]
            },
            {
                "stage": "問題クローズ",
                "activities": ["解決確認", "文書更新", "レッスンラーンド"],
                "outputs": ["クローズ報告書", "ナレッジ記事"]
            }
        ]
    
    def _get_default_kpi_metrics(self) -> list:
        return [
            {
                "name": "問題解決時間",
                "description": "問題の記録から解決までの平均時間",
                "target": "30日以内",
                "measurement": "月次"
            },
            {
                "name": "再発防止率",
                "description": "解決後30日以内に関連インシデントが発生しなかった割合",
                "target": "95%以上",
                "measurement": "月次"
            },
            {
                "name": "KEDB利用率",
                "description": "インシデント解決時のKEDB参照率",
                "target": "60%以上",
                "measurement": "週次"
            },
            {
                "name": "プロアクティブ問題比率",
                "description": "インシデント発生前に特定された問題の割合",
                "target": "20%以上",
                "measurement": "四半期"
            },
            {
                "name": "根本原因特定率",
                "description": "根本原因が特定された問題の割合",
                "target": "80%以上",
                "measurement": "月次"
            }
        ]