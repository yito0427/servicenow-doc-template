from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class SLMDesignTemplate(BaseDocumentTemplate):
    """SLM（Service Level Management）設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "slm_design.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.SLM_DESIGN
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. SLM基本方針",
            "3. サービスレベル定義",
            "4. SLA設計",
            "5. OLA設計", 
            "6. UC設計",
            "7. 測定・監視設計",
            "8. レポート設計",
            "9. 改善プロセス",
            "10. 他プロセスとの連携"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 設定ファイルからデフォルト値を取得
        default_values = self.get_default_values()
        
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "slm_overview": data.get("slm_overview", {}),
            "service_levels": data.get("service_levels", []),
            "sla_definitions": data.get("sla_definitions", []),
            "ola_definitions": data.get("ola_definitions", []),
            "uc_definitions": data.get("uc_definitions", []),
            "monitoring_design": data.get("monitoring_design", {}),
            "reporting_design": data.get("reporting_design", []),
            "improvement_process": data.get("improvement_process", {}),
            "integration_points": data.get("integration_points", [])
        }
        
        # 設定ファイルからのデフォルト値を使用
        context.update({
            "service_categories": data.get("service_categories", default_values.get("service_categories", [])),
            "measurement_metrics": data.get("measurement_metrics", default_values.get("measurement_metrics", [])),
            "reporting_frequency": data.get("reporting_frequency", default_values.get("reporting_frequency", {})),
            "review_cycles": data.get("review_cycles", default_values.get("review_cycles", []))
        })
        
        # デフォルト値の設定
        if not context["slm_overview"]:
            context["slm_overview"] = self._get_default_slm_overview()
        
        if not context["service_levels"]:
            context["service_levels"] = self._get_default_service_levels()
        
        if not context["sla_definitions"]:
            context["sla_definitions"] = self._get_default_sla_definitions()
        
        if not context["monitoring_design"]:
            context["monitoring_design"] = self._get_default_monitoring_design()
        
        return context
    
    def _get_default_slm_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "ITサービスの品質を継続的に監視・測定し、合意されたサービスレベルの達成を確保する",
            "scope": "全てのITサービスに対するサービスレベルの定義、測定、レポート、改善",
            "objectives": [
                "サービスレベルの明確化",
                "サービス品質の可視化", 
                "継続的なサービス改善",
                "顧客満足度の向上",
                "コストパフォーマンスの最適化"
            ],
            "benefits": [
                "サービス品質の向上",
                "顧客との信頼関係構築",
                "リスクの早期発見",
                "投資対効果の明確化"
            ],
            "key_activities": [
                "SLA/OLA/UCの定義と合意",
                "サービスレベルの監視・測定",
                "定期的なレポート作成",
                "サービス改善計画の策定・実行"
            ]
        }
    
    def _get_default_service_levels(self) -> list:
        return [
            {
                "service_name": "メール・グループウェアサービス",
                "availability": "99.5%",
                "performance": "応答時間 < 3秒",
                "capacity": "同時接続数 1000ユーザー",
                "continuity": "RPO: 4時間, RTO: 8時間"
            },
            {
                "service_name": "ファイルサーバーサービス",
                "availability": "99.9%", 
                "performance": "データ転送速度 > 100Mbps",
                "capacity": "ストレージ容量 10TB",
                "continuity": "RPO: 1時間, RTO: 4時間"
            },
            {
                "service_name": "基幹業務システム",
                "availability": "99.9%",
                "performance": "応答時間 < 2秒",
                "capacity": "同時接続数 500ユーザー",
                "continuity": "RPO: 15分, RTO: 2時間"
            }
        ]
    
    def _get_default_sla_definitions(self) -> list:
        return [
            {
                "service": "インシデント対応サービス",
                "metrics": [
                    {"name": "初回応答時間", "target": "P1: 15分以内, P2: 30分以内, P3: 2時間以内, P4: 8時間以内"},
                    {"name": "解決時間", "target": "P1: 4時間以内, P2: 8時間以内, P3: 24時間以内, P4: 72時間以内"},
                    {"name": "顧客満足度", "target": "4.0以上 (5段階評価)"}
                ]
            },
            {
                "service": "変更要求対応サービス",
                "metrics": [
                    {"name": "変更成功率", "target": "95%以上"},
                    {"name": "計画変更の承認期間", "target": "標準変更: 3営業日, 通常変更: 5営業日"},
                    {"name": "緊急変更の対応時間", "target": "2時間以内"}
                ]
            },
            {
                "service": "問題管理サービス",
                "metrics": [
                    {"name": "問題解決率", "target": "月次90%以上"},
                    {"name": "根本原因分析完了期間", "target": "重要問題: 7日以内, 一般問題: 30日以内"},
                    {"name": "既知エラー登録期間", "target": "問題特定後24時間以内"}
                ]
            }
        ]
    
    def _get_default_monitoring_design(self) -> Dict[str, Any]:
        return {
            "monitoring_tools": [
                {"name": "ServiceNow Performance Analytics", "purpose": "SLA測定・レポート"},
                {"name": "System Center Operations Manager", "purpose": "インフラ監視"},
                {"name": "Application Performance Monitoring", "purpose": "アプリケーション監視"}
            ],
            "data_sources": [
                "ServiceNowインシデント管理",
                "ServiceNow変更管理",
                "ServiceNow問題管理",
                "インフラ監視システム",
                "ネットワーク監視システム"
            ],
            "measurement_frequency": {
                "real_time": ["可用性", "応答時間", "エラー率"],
                "daily": ["インシデント件数", "変更成功率"],
                "weekly": ["顧客満足度", "SLA達成率"],
                "monthly": ["トレンド分析", "改善計画立案"]
            },
            "alert_conditions": [
                {"metric": "可用性", "threshold": "SLA目標値を下回った場合"},
                {"metric": "応答時間", "threshold": "SLA目標値を上回った場合"},
                {"metric": "インシデント数", "threshold": "前月比150%を超えた場合"}
            ]
        }