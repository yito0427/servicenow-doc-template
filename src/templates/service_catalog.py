from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class ServiceCatalogTemplate(BaseDocumentTemplate):
    """サービスカタログ設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "service_catalog.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.SERVICE_CATALOG
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. サービスカタログ構造",
            "3. サービス分類",
            "4. リクエストプロセス",
            "5. 承認ワークフロー",
            "6. フルフィルメント",
            "7. ポータル設計",
            "8. 統合と自動化",
            "9. ガバナンスとライフサイクル",
            "10. KPIとメトリクス"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "catalog_overview": data.get("catalog_overview", {}),
            "service_categories": data.get("service_categories", []),
            "service_items": data.get("service_items", []),
            "request_process": data.get("request_process", {}),
            "approval_workflow": data.get("approval_workflow", {}),
            "fulfillment_process": data.get("fulfillment_process", {}),
            "portal_design": data.get("portal_design", {}),
            "integrations": data.get("integrations", []),
            "governance": data.get("governance", {}),
            "kpi_metrics": data.get("kpi_metrics", [])
        }
        
        # デフォルト値の設定
        if not context["catalog_overview"]:
            context["catalog_overview"] = self._get_default_catalog_overview()
        
        if not context["service_categories"]:
            context["service_categories"] = self._get_default_service_categories()
        
        if not context["service_items"]:
            context["service_items"] = self._get_default_service_items()
        
        if not context["request_process"]:
            context["request_process"] = self._get_default_request_process()
        
        if not context["approval_workflow"]:
            context["approval_workflow"] = self._get_default_approval_workflow()
        
        if not context["fulfillment_process"]:
            context["fulfillment_process"] = self._get_default_fulfillment_process()
        
        if not context["portal_design"]:
            context["portal_design"] = self._get_default_portal_design()
        
        if not context["kpi_metrics"]:
            context["kpi_metrics"] = self._get_default_kpi_metrics()
        
        return context
    
    def _get_default_catalog_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "標準化されたITサービスの提供を通じて、ユーザーエクスペリエンスの向上と運用効率化を実現する",
            "scope": "IT部門が提供するすべてのサービスとリクエストタイプ",
            "objectives": [
                "セルフサービス化による効率向上",
                "サービス提供の標準化と品質向上",
                "リクエスト処理時間の短縮",
                "透明性の高いサービス提供",
                "コスト管理の最適化"
            ],
            "benefits": [
                "ユーザー満足度の向上",
                "IT部門の作業負荷軽減",
                "サービス提供時間の短縮",
                "コンプライアンスの確保",
                "サービス利用状況の可視化"
            ]
        }
    
    def _get_default_service_categories(self) -> list:
        return [
            {
                "name": "エンドユーザーサービス",
                "description": "従業員の日常業務をサポートするサービス",
                "icon": "fas fa-user",
                "subcategories": [
                    "ハードウェアリクエスト",
                    "ソフトウェアリクエスト",
                    "アカウント管理",
                    "アクセス権限"
                ]
            },
            {
                "name": "インフラストラクチャサービス",
                "description": "ITインフラに関連するサービス",
                "icon": "fas fa-server",
                "subcategories": [
                    "サーバーリクエスト",
                    "ネットワークサービス",
                    "ストレージサービス",
                    "バックアップ・リストア"
                ]
            },
            {
                "name": "アプリケーションサービス",
                "description": "ビジネスアプリケーションに関するサービス",
                "icon": "fas fa-desktop",
                "subcategories": [
                    "新規アプリケーション導入",
                    "アプリケーション変更",
                    "ライセンス管理",
                    "アプリケーションサポート"
                ]
            },
            {
                "name": "セキュリティサービス",
                "description": "情報セキュリティに関するサービス",
                "icon": "fas fa-shield-alt",
                "subcategories": [
                    "セキュリティ評価",
                    "アクセス制御",
                    "証明書管理",
                    "セキュリティ例外申請"
                ]
            }
        ]
    
    def _get_default_service_items(self) -> list:
        return [
            {
                "name": "新規PCセットアップ",
                "category": "エンドユーザーサービス",
                "description": "新入社員または既存社員向けの新規PC環境のセットアップ",
                "sla": "5営業日",
                "cost": "部門負担",
                "approval_required": True,
                "fulfillment_group": "デスクトップサポートチーム"
            },
            {
                "name": "ソフトウェアライセンス申請",
                "category": "エンドユーザーサービス",
                "description": "業務に必要なソフトウェアライセンスの新規取得",
                "sla": "3営業日",
                "cost": "申請部門負担",
                "approval_required": True,
                "fulfillment_group": "ソフトウェア管理チーム"
            },
            {
                "name": "共有フォルダアクセス権限",
                "category": "エンドユーザーサービス",
                "description": "ファイルサーバー上の共有フォルダへのアクセス権限付与",
                "sla": "1営業日",
                "cost": "無料",
                "approval_required": True,
                "fulfillment_group": "アクセス管理チーム"
            },
            {
                "name": "仮想サーバー作成",
                "category": "インフラストラクチャサービス",
                "description": "開発・テスト・本番環境用の仮想サーバー新規作成",
                "sla": "3営業日",
                "cost": "リソース使用量に応じて課金",
                "approval_required": True,
                "fulfillment_group": "インフラチーム"
            }
        ]
    
    def _get_default_request_process(self) -> Dict[str, Any]:
        return {
            "stages": [
                {
                    "stage": "リクエスト作成",
                    "activities": [
                        "サービスカタログへのアクセス",
                        "サービスアイテムの選択",
                        "必要情報の入力",
                        "添付ファイルのアップロード"
                    ]
                },
                {
                    "stage": "初期検証",
                    "activities": [
                        "入力情報の完全性チェック",
                        "重複リクエストの確認",
                        "前提条件の確認",
                        "承認要否の判定"
                    ]
                },
                {
                    "stage": "承認プロセス",
                    "activities": [
                        "承認者への通知",
                        "承認/却下の判断",
                        "条件付き承認の処理",
                        "エスカレーション"
                    ]
                },
                {
                    "stage": "フルフィルメント",
                    "activities": [
                        "タスクの作成と割当",
                        "リソースの確保",
                        "実装作業の実施",
                        "品質チェック"
                    ]
                },
                {
                    "stage": "クローズ",
                    "activities": [
                        "完了通知",
                        "ユーザー確認",
                        "満足度調査",
                        "記録の更新"
                    ]
                }
            ],
            "request_types": [
                "標準リクエスト - 事前定義・自動承認",
                "一般リクエスト - 承認フロー必須",
                "複雑リクエスト - 複数承認・調整必要"
            ]
        }
    
    def _get_default_approval_workflow(self) -> Dict[str, Any]:
        return {
            "approval_rules": [
                {
                    "condition": "コスト > 10万円",
                    "approvers": ["直属上司", "部門長", "IT予算管理者"],
                    "type": "順次承認"
                },
                {
                    "condition": "セキュリティ関連",
                    "approvers": ["直属上司", "セキュリティ管理者"],
                    "type": "並列承認"
                },
                {
                    "condition": "標準サービス",
                    "approvers": ["直属上司"],
                    "type": "単一承認"
                }
            ],
            "escalation_rules": [
                {
                    "trigger": "承認待ち48時間",
                    "action": "リマインダー送信"
                },
                {
                    "trigger": "承認待ち72時間",
                    "action": "上位承認者へエスカレーション"
                }
            ],
            "delegation": {
                "enabled": True,
                "rules": "不在時の代理承認者設定可能"
            }
        }
    
    def _get_default_fulfillment_process(self) -> Dict[str, Any]:
        return {
            "fulfillment_models": [
                {
                    "model": "自動フルフィルメント",
                    "description": "システム連携による自動実行",
                    "examples": ["パスワードリセット", "メーリングリスト追加"],
                    "benefits": "即時完了、人的エラー削減"
                },
                {
                    "model": "半自動フルフィルメント",
                    "description": "一部手動確認を含む自動処理",
                    "examples": ["ソフトウェアインストール", "権限付与"],
                    "benefits": "効率性と品質のバランス"
                },
                {
                    "model": "手動フルフィルメント",
                    "description": "専門スタッフによる手動作業",
                    "examples": ["ハードウェア設置", "複雑な設定変更"],
                    "benefits": "柔軟な対応、品質確保"
                }
            ],
            "task_management": {
                "assignment_method": "スキルベース自動割当",
                "priority_rules": "SLA、ビジネス影響度、承認レベル",
                "tracking": "リアルタイムステータス更新"
            }
        }
    
    def _get_default_portal_design(self) -> Dict[str, Any]:
        return {
            "user_interface": {
                "design_principles": [
                    "直感的なナビゲーション",
                    "レスポンシブデザイン",
                    "アクセシビリティ準拠",
                    "多言語対応"
                ],
                "key_features": [
                    "サービス検索機能",
                    "人気サービスの表示",
                    "マイリクエストダッシュボード",
                    "ナレッジベース統合"
                ]
            },
            "personalization": {
                "user_profiles": "部門・役職別のカスタマイズビュー",
                "favorites": "よく使うサービスのお気に入り登録",
                "history": "過去のリクエスト履歴参照",
                "notifications": "プッシュ通知・メール通知設定"
            },
            "mobile_access": {
                "native_app": "iOS/Android対応ネイティブアプリ",
                "responsive_web": "モバイルブラウザ最適化",
                "offline_capability": "オフライン時の下書き保存"
            }
        }
    
    def _get_default_kpi_metrics(self) -> list:
        return [
            {
                "name": "カタログ利用率",
                "description": "全リクエストに占めるカタログ経由の割合",
                "target": "80%以上",
                "formula": "カタログリクエスト数 / 全リクエスト数 × 100"
            },
            {
                "name": "平均処理時間",
                "description": "リクエストから完了までの平均時間",
                "target": "SLA遵守率95%以上",
                "formula": "総処理時間 / 完了リクエスト数"
            },
            {
                "name": "ユーザー満足度",
                "description": "サービスカタログ利用者の満足度",
                "target": "4.0以上（5段階評価）",
                "formula": "満足度調査の平均スコア"
            },
            {
                "name": "自動化率",
                "description": "自動フルフィルメントの割合",
                "target": "60%以上",
                "formula": "自動処理リクエスト数 / 全リクエスト数 × 100"
            },
            {
                "name": "初回解決率",
                "description": "追加情報なしで完了したリクエストの割合",
                "target": "90%以上",
                "formula": "初回完了数 / 全リクエスト数 × 100"
            }
        ]