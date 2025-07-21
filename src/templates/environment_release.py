from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class EnvironmentReleaseTemplate(BaseDocumentTemplate):
    """環境・リリース管理設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "environment_release.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.ENVIRONMENT_STRATEGY
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        return base_fields + [
            "environment_strategy",
            "release_process",
            "update_set_strategy",
            "cicd_pipeline"
        ]
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. 環境戦略",
            "3. 環境構成",
            "4. リリース管理プロセス",
            "5. Update Set管理",
            "6. CI/CD・DevOps",
            "7. 環境同期・リフレッシュ",
            "8. 変更管理統合",
            "9. 品質保証",
            "10. 運用手順"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date"),
            "environment_strategy": data.get("environment_strategy", {}),
            "environments": data.get("environments", []),
            "release_process": data.get("release_process", {}),
            "update_set_strategy": data.get("update_set_strategy", {}),
            "cicd_pipeline": data.get("cicd_pipeline", {}),
            "sync_strategy": data.get("sync_strategy", {}),
            "change_integration": data.get("change_integration", {}),
            "quality_gates": data.get("quality_gates", []),
            "operational_procedures": data.get("operational_procedures", {})
        }
        
        # デフォルト値の設定
        if not context["environment_strategy"]:
            context["environment_strategy"] = self._get_default_environment_strategy()
        
        if not context["environments"]:
            context["environments"] = self._get_default_environments()
        
        if not context["release_process"]:
            context["release_process"] = self._get_default_release_process()
        
        return context
    
    def _get_default_environment_strategy(self) -> Dict[str, Any]:
        return {
            "approach": "4段階環境アプローチ（Dev → Test → UAT → Prod）",
            "principles": [
                "本番環境と同等の構成を維持",
                "環境間の自動化された昇格プロセス",
                "厳格な変更管理とトレーサビリティ",
                "定期的な環境リフレッシュ"
            ],
            "objectives": [
                "開発効率の向上",
                "品質の確保",
                "リスクの最小化",
                "迅速なデリバリー"
            ]
        }
    
    def _get_default_environments(self) -> list:
        return [
            {
                "name": "Development (Dev)",
                "purpose": "開発・単体テスト",
                "url": "https://dev.service-now.com",
                "refresh_cycle": "週次",
                "users": ["開発者", "設定担当者"]
            },
            {
                "name": "Test",
                "purpose": "統合テスト・システムテスト",
                "url": "https://test.service-now.com",
                "refresh_cycle": "月次",
                "users": ["テスター", "開発者"]
            },
            {
                "name": "UAT (User Acceptance Test)",
                "purpose": "ユーザー受入テスト",
                "url": "https://uat.service-now.com",
                "refresh_cycle": "リリース前",
                "users": ["ビジネスユーザー", "UAT担当者"]
            },
            {
                "name": "Production (Prod)",
                "purpose": "本番運用",
                "url": "https://prod.service-now.com",
                "refresh_cycle": "N/A",
                "users": ["エンドユーザー", "運用担当者"]
            }
        ]
    
    def _get_default_release_process(self) -> Dict[str, Any]:
        return {
            "phases": [
                {
                    "name": "計画",
                    "activities": [
                        "リリース内容の確定",
                        "影響分析",
                        "リリーススケジュール策定"
                    ]
                },
                {
                    "name": "準備",
                    "activities": [
                        "Update Set作成・レビュー",
                        "テスト計画作成",
                        "ロールバック計画作成"
                    ]
                },
                {
                    "name": "テスト",
                    "activities": [
                        "Test環境でのテスト実施",
                        "UAT環境での受入テスト",
                        "パフォーマンステスト"
                    ]
                },
                {
                    "name": "リリース",
                    "activities": [
                        "変更諮問委員会（CAB）承認",
                        "本番環境へのデプロイ",
                        "動作確認"
                    ]
                },
                {
                    "name": "事後対応",
                    "activities": [
                        "HyperCare対応",
                        "問題点の収集と対応",
                        "リリース完了報告"
                    ]
                }
            ],
            "release_types": [
                {
                    "type": "定期リリース",
                    "frequency": "月次",
                    "lead_time": "2週間"
                },
                {
                    "type": "緊急リリース",
                    "frequency": "随時",
                    "lead_time": "24時間"
                }
            ]
        }