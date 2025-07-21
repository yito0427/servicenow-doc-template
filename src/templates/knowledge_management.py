from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class KnowledgeManagementTemplate(BaseDocumentTemplate):
    """ナレッジ管理設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "knowledge_management.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.KNOWLEDGE_MANAGEMENT
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. ナレッジ管理基本方針",
            "3. ナレッジベース設計",
            "4. ナレッジ分類・タクソノミー",
            "5. ナレッジライフサイクル",
            "6. 品質管理・承認プロセス",
            "7. 検索・活用設計",
            "8. パフォーマンス・分析設計",
            "9. セキュリティ・アクセス制御",
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
            "km_overview": data.get("km_overview", {}),
            "knowledge_base_design": data.get("knowledge_base_design", {}),
            "taxonomy_design": data.get("taxonomy_design", []),
            "lifecycle_design": data.get("lifecycle_design", {}),
            "quality_process": data.get("quality_process", {}),
            "search_design": data.get("search_design", {}),
            "analytics_design": data.get("analytics_design", {}),
            "security_design": data.get("security_design", {}),
            "integration_points": data.get("integration_points", [])
        }
        
        # 設定ファイルからのデフォルト値を使用
        context.update({
            "knowledge_types": data.get("knowledge_types", default_values.get("knowledge_types", [])),
            "content_categories": data.get("content_categories", default_values.get("content_categories", [])),
            "approval_workflows": data.get("approval_workflows", default_values.get("approval_workflows", [])),
            "quality_metrics": data.get("quality_metrics", default_values.get("quality_metrics", [])),
            "search_features": data.get("search_features", default_values.get("search_features", [])),
            "analytics_reports": data.get("analytics_reports", default_values.get("analytics_reports", []))
        })
        
        # デフォルト値の設定
        if not context["km_overview"]:
            context["km_overview"] = self._get_default_km_overview()
        
        if not context["knowledge_base_design"]:
            context["knowledge_base_design"] = self._get_default_kb_design()
        
        if not context["taxonomy_design"]:
            context["taxonomy_design"] = self._get_default_taxonomy()
        
        if not context["lifecycle_design"]:
            context["lifecycle_design"] = self._get_default_lifecycle()
        
        if not context["quality_process"]:
            context["quality_process"] = self._get_default_quality_process()
        
        return context
    
    def _get_default_km_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "組織の知識・経験・ノウハウを体系的に管理し、効果的な知識共有と活用を促進する",
            "scope": "IT運用・保守に関するナレッジ、問題解決手順、ベストプラクティス、FAQ",
            "objectives": [
                "知識の体系的な蓄積・管理",
                "効率的な問題解決の実現",
                "ベストプラクティスの共有",
                "新人教育・スキル向上の支援",
                "重複作業の削減"
            ],
            "benefits": [
                "問題解決時間の短縮",
                "サービス品質の向上",
                "属人化の解消",
                "組織学習の促進",
                "顧客満足度の向上"
            ],
            "success_factors": [
                "経営層のコミットメント",
                "適切なインセンティブ設計",
                "使いやすいツール・インターフェース",
                "継続的な品質管理",
                "組織文化の醸成"
            ]
        }
    
    def _get_default_kb_design(self) -> Dict[str, Any]:
        return {
            "architecture": {
                "platform": "ServiceNow Knowledge Management",
                "knowledge_bases": [
                    {"name": "IT Support KB", "purpose": "ITサポート関連ナレッジ"},
                    {"name": "Employee Self-Service KB", "purpose": "従業員セルフサービス用FAQ"},
                    {"name": "Technical Documentation KB", "purpose": "技術文書・手順書"}
                ],
                "content_types": [
                    "How-to記事",
                    "トラブルシューティングガイド", 
                    "FAQ",
                    "ベストプラクティス",
                    "技術仕様書"
                ]
            },
            "storage_structure": {
                "primary_storage": "ServiceNow Knowledge Base",
                "backup_storage": "SharePoint/Teams",
                "versioning": "自動バージョン管理",
                "retention_policy": "3年間保持（定期レビュー）"
            },
            "access_channels": [
                "ServiceNow Service Portal",
                "Mobile App",
                "Teams Bot",
                "Email Integration"
            ]
        }
    
    def _get_default_taxonomy(self) -> list:
        return [
            {
                "category": "ITサービス",
                "subcategories": [
                    "インシデント対応",
                    "変更管理",
                    "問題管理",
                    "資産管理"
                ],
                "tags": ["urgent", "standard", "approved"]
            },
            {
                "category": "インフラストラクチャ",
                "subcategories": [
                    "サーバー",
                    "ネットワーク",
                    "ストレージ",
                    "セキュリティ"
                ],
                "tags": ["production", "development", "maintenance"]
            },
            {
                "category": "アプリケーション",
                "subcategories": [
                    "業務アプリケーション",
                    "オフィスアプリケーション",
                    "開発ツール",
                    "監視ツール"
                ],
                "tags": ["user-guide", "admin-guide", "troubleshooting"]
            },
            {
                "category": "プロセス・手順",
                "subcategories": [
                    "運用手順",
                    "保守手順",
                    "緊急時対応",
                    "品質管理"
                ],
                "tags": ["step-by-step", "checklist", "template"]
            }
        ]
    
    def _get_default_lifecycle(self) -> Dict[str, Any]:
        return {
            "stages": [
                {
                    "stage": "作成",
                    "description": "新規ナレッジの作成・登録",
                    "activities": [
                        "コンテンツ作成",
                        "メタデータ設定",
                        "カテゴリ分類",
                        "初期レビュー"
                    ],
                    "roles": ["Subject Matter Expert", "Knowledge Author"],
                    "duration": "3-5営業日"
                },
                {
                    "stage": "レビュー・承認",
                    "description": "コンテンツの品質確認と承認",
                    "activities": [
                        "技術的正確性確認",
                        "表記・体裁確認",
                        "分類適切性確認",
                        "承認・公開"
                    ],
                    "roles": ["Knowledge Manager", "Technical Reviewer"],
                    "duration": "2-3営業日"
                },
                {
                    "stage": "公開・活用",
                    "description": "ナレッジの公開と利用促進",
                    "activities": [
                        "公開設定",
                        "通知配信",
                        "利用状況監視",
                        "フィードバック収集"
                    ],
                    "roles": ["Knowledge Manager"],
                    "duration": "継続的"
                },
                {
                    "stage": "更新・保守",
                    "description": "コンテンツの定期的な見直しと更新",
                    "activities": [
                        "有効性確認",
                        "内容更新",
                        "メタデータ見直し",
                        "アーカイブ判定"
                    ],
                    "roles": ["Knowledge Owner", "Subject Matter Expert"],
                    "duration": "四半期毎"
                },
                {
                    "stage": "廃止・アーカイブ",
                    "description": "不要・古いナレッジの廃止処理",
                    "activities": [
                        "廃止判定",
                        "代替ナレッジ確認",
                        "アーカイブ移行",
                        "関連リンク更新"
                    ],
                    "roles": ["Knowledge Manager"],
                    "duration": "1営業日"
                }
            ],
            "review_schedule": {
                "high_priority": "月次",
                "medium_priority": "四半期毎",
                "low_priority": "年次"
            }
        }
    
    def _get_default_quality_process(self) -> Dict[str, Any]:
        return {
            "quality_criteria": [
                {
                    "criteria": "正確性",
                    "description": "技術的に正確で最新の情報であること",
                    "check_points": [
                        "事実確認済み",
                        "手順の動作確認済み",
                        "最新バージョン対応"
                    ]
                },
                {
                    "criteria": "完全性",
                    "description": "必要な情報が漏れなく含まれていること",
                    "check_points": [
                        "前提条件明記",
                        "手順の詳細記載",
                        "期待結果の明示"
                    ]
                },
                {
                    "criteria": "明確性",
                    "description": "読み手にとって理解しやすい表現であること",
                    "check_points": [
                        "専門用語の説明",
                        "図表の適切な使用",
                        "論理的な構成"
                    ]
                },
                {
                    "criteria": "有用性",
                    "description": "実際の業務で活用できる内容であること",
                    "check_points": [
                        "実用的な情報",
                        "適切な詳細レベル",
                        "関連情報への参照"
                    ]
                }
            ],
            "approval_workflow": [
                {
                    "step": 1,
                    "role": "作成者",
                    "action": "初期品質チェック",
                    "criteria": ["基本要件充足", "体裁確認"]
                },
                {
                    "step": 2,
                    "role": "ピアレビューア",
                    "action": "技術的レビュー",
                    "criteria": ["技術的正確性", "実用性"]
                },
                {
                    "step": 3,
                    "role": "ナレッジマネージャー",
                    "action": "最終承認",
                    "criteria": ["品質基準適合", "分類適切性"]
                }
            ],
            "feedback_mechanism": {
                "rating_system": "5段階評価（役立ち度）",
                "comment_collection": "具体的な改善提案の収集",
                "usage_analytics": "閲覧数・検索ヒット数の追跡",
                "review_trigger": "低評価時の自動レビュー依頼"
            }
        }