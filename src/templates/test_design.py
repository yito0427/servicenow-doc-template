from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class TestDesignTemplate(BaseDocumentTemplate):
    """テスト設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "test_design.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.TEST_DESIGN
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. テスト戦略",
            "3. テスト計画",
            "4. テストケース設計",
            "5. テスト環境",
            "6. テストデータ",
            "7. 自動化戦略",
            "8. 欠陥管理",
            "9. テスト報告",
            "10. リスクと対策"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "test_overview": data.get("test_overview", {}),
            "test_strategy": data.get("test_strategy", {}),
            "test_phases": data.get("test_phases", []),
            "test_types": data.get("test_types", []),
            "test_environments": data.get("test_environments", []),
            "test_data_strategy": data.get("test_data_strategy", {}),
            "automation_strategy": data.get("automation_strategy", {}),
            "defect_management": data.get("defect_management", {}),
            "test_metrics": data.get("test_metrics", []),
            "risk_mitigation": data.get("risk_mitigation", [])
        }
        
        # デフォルト値の設定
        if not context["test_overview"]:
            context["test_overview"] = self._get_default_test_overview()
        
        if not context["test_strategy"]:
            context["test_strategy"] = self._get_default_test_strategy()
        
        if not context["test_phases"]:
            context["test_phases"] = self._get_default_test_phases()
        
        if not context["test_types"]:
            context["test_types"] = self._get_default_test_types()
        
        if not context["test_environments"]:
            context["test_environments"] = self._get_default_test_environments()
        
        if not context["test_data_strategy"]:
            context["test_data_strategy"] = self._get_default_test_data_strategy()
        
        if not context["automation_strategy"]:
            context["automation_strategy"] = self._get_default_automation_strategy()
        
        if not context["defect_management"]:
            context["defect_management"] = self._get_default_defect_management()
        
        if not context["test_metrics"]:
            context["test_metrics"] = self._get_default_test_metrics()
        
        if not context["risk_mitigation"]:
            context["risk_mitigation"] = self._get_default_risk_mitigation()
        
        return context
    
    def _get_default_test_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "ServiceNow実装の品質を保証し、要件を満たすシステムの提供を確実にする",
            "scope": "すべてのServiceNowモジュール、カスタマイズ、統合、データ移行の検証",
            "objectives": [
                "機能要件の充足確認",
                "非機能要件（パフォーマンス、セキュリティ）の検証",
                "既存システムとの統合動作確認",
                "ユーザビリティとアクセシビリティの確保",
                "本番環境での安定稼働の保証"
            ],
            "deliverables": [
                "テスト計画書",
                "テストケース",
                "テスト実行結果",
                "欠陥レポート",
                "テスト完了報告書"
            ]
        }
    
    def _get_default_test_strategy(self) -> Dict[str, Any]:
        return {
            "approach": "リスクベーステスト＋段階的テスト実施",
            "test_levels": [
                "単体テスト（UT）",
                "結合テスト（IT）",
                "システムテスト（ST）",
                "受入テスト（UAT）"
            ],
            "entry_criteria": [
                "開発完了",
                "コードレビュー完了",
                "テスト環境準備完了",
                "テストデータ準備完了"
            ],
            "exit_criteria": [
                "全テストケース実行完了",
                "重大欠陥ゼロ",
                "中程度欠陥の90%以上解決",
                "ステークホルダー承認"
            ],
            "suspension_criteria": [
                "環境の重大な障害",
                "テストブロッカーの発生",
                "要件の大幅な変更"
            ]
        }
    
    def _get_default_test_phases(self) -> list:
        return [
            {
                "phase": "単体テスト（UT）",
                "duration": "2週間",
                "responsible": "開発チーム",
                "scope": "個別機能、スクリプト、ワークフロー",
                "tools": "ServiceNow ATF, スクリプトデバッガー"
            },
            {
                "phase": "結合テスト（IT）",
                "duration": "3週間",
                "responsible": "開発チーム + テストチーム",
                "scope": "モジュール間連携、API統合、データフロー",
                "tools": "ServiceNow ATF, Postman, SoapUI"
            },
            {
                "phase": "システムテスト（ST）",
                "duration": "4週間",
                "responsible": "テストチーム",
                "scope": "E2Eシナリオ、性能、セキュリティ",
                "tools": "ServiceNow ATF, JMeter, セキュリティスキャナー"
            },
            {
                "phase": "受入テスト（UAT）",
                "duration": "3週間",
                "responsible": "ビジネスユーザー",
                "scope": "ビジネスシナリオ、ユーザビリティ",
                "tools": "手動テスト、ServiceNowポータル"
            }
        ]
    
    def _get_default_test_types(self) -> list:
        return [
            {
                "type": "機能テスト",
                "description": "要件に基づく機能の動作確認",
                "coverage": "全機能要件",
                "method": "手動 + 自動",
                "priority": "高"
            },
            {
                "type": "統合テスト",
                "description": "外部システムとの連携確認",
                "coverage": "すべての統合ポイント",
                "method": "自動化推奨",
                "priority": "高"
            },
            {
                "type": "パフォーマンステスト",
                "description": "応答時間、同時接続数、処理能力の検証",
                "coverage": "主要トランザクション",
                "method": "自動（負荷テストツール）",
                "priority": "高"
            },
            {
                "type": "セキュリティテスト",
                "description": "脆弱性、アクセス制御、データ保護の検証",
                "coverage": "全モジュール",
                "method": "手動 + ツール",
                "priority": "高"
            },
            {
                "type": "ユーザビリティテスト",
                "description": "UI/UX、操作性の確認",
                "coverage": "主要画面・操作フロー",
                "method": "手動（ユーザー参加）",
                "priority": "中"
            },
            {
                "type": "回帰テスト",
                "description": "変更による既存機能への影響確認",
                "coverage": "重要機能",
                "method": "自動化必須",
                "priority": "高"
            }
        ]
    
    def _get_default_test_environments(self) -> list:
        return [
            {
                "name": "開発環境（DEV）",
                "purpose": "単体テスト、初期結合テスト",
                "configuration": "最小構成",
                "data": "テストデータ（匿名化）",
                "access": "開発チーム"
            },
            {
                "name": "テスト環境（TEST）",
                "purpose": "結合テスト、システムテスト",
                "configuration": "本番相当（縮小版）",
                "data": "本番相当データ（マスキング済）",
                "access": "テストチーム、開発チーム"
            },
            {
                "name": "ステージング環境（STG）",
                "purpose": "受入テスト、性能テスト",
                "configuration": "本番同等",
                "data": "本番データコピー（最新）",
                "access": "全プロジェクトメンバー"
            },
            {
                "name": "性能テスト環境（PERF）",
                "purpose": "負荷テスト、ストレステスト",
                "configuration": "本番同等以上",
                "data": "大量テストデータ",
                "access": "性能テストチーム"
            }
        ]
    
    def _get_default_test_data_strategy(self) -> Dict[str, Any]:
        return {
            "data_categories": [
                {
                    "category": "マスターデータ",
                    "source": "本番データ抽出",
                    "preparation": "個人情報マスキング",
                    "volume": "全件"
                },
                {
                    "category": "トランザクションデータ",
                    "source": "本番データサンプリング",
                    "preparation": "日付調整、匿名化",
                    "volume": "過去3ヶ月分"
                },
                {
                    "category": "テスト専用データ",
                    "source": "新規作成",
                    "preparation": "境界値、異常系データ作成",
                    "volume": "シナリオ別"
                }
            ],
            "data_management": {
                "refresh_cycle": "フェーズごと",
                "backup_strategy": "日次バックアップ",
                "cleanup_policy": "テスト完了後1週間保持"
            },
            "compliance": {
                "gdpr": "個人情報完全マスキング",
                "data_retention": "テスト期間のみ保持",
                "access_control": "役割ベースアクセス制御"
            }
        }
    
    def _get_default_automation_strategy(self) -> Dict[str, Any]:
        return {
            "automation_scope": {
                "target_coverage": "70%以上",
                "priority_areas": [
                    "回帰テスト",
                    "スモークテスト",
                    "APIテスト",
                    "基本的な機能テスト"
                ]
            },
            "tools": [
                {
                    "tool": "ServiceNow ATF",
                    "purpose": "UI自動テスト、E2Eテスト",
                    "coverage": "ServiceNow内機能"
                },
                {
                    "tool": "Postman/Newman",
                    "purpose": "REST API自動テスト",
                    "coverage": "統合API"
                },
                {
                    "tool": "JMeter",
                    "purpose": "性能テスト自動化",
                    "coverage": "負荷テスト"
                },
                {
                    "tool": "Jenkins",
                    "purpose": "CI/CDパイプライン",
                    "coverage": "継続的テスト実行"
                }
            ],
            "framework": {
                "design_pattern": "Page Object Model",
                "test_data": "データ駆動型テスト",
                "reporting": "Allure Report統合",
                "version_control": "Git管理"
            }
        }
    
    def _get_default_defect_management(self) -> Dict[str, Any]:
        return {
            "defect_lifecycle": [
                "新規",
                "割当済",
                "調査中",
                "修正中",
                "修正済",
                "再テスト中",
                "検証済",
                "クローズ"
            ],
            "severity_levels": [
                {
                    "level": "Critical",
                    "description": "システム停止、データ損失",
                    "sla": "4時間以内対応",
                    "escalation": "即時"
                },
                {
                    "level": "High",
                    "description": "主要機能の障害",
                    "sla": "24時間以内対応",
                    "escalation": "翌営業日"
                },
                {
                    "level": "Medium",
                    "description": "機能の部分的障害",
                    "sla": "3営業日以内",
                    "escalation": "週次"
                },
                {
                    "level": "Low",
                    "description": "軽微な問題、改善要望",
                    "sla": "次リリース検討",
                    "escalation": "月次"
                }
            ],
            "defect_fields": [
                "欠陥ID",
                "発見日時",
                "発見者",
                "発見フェーズ",
                "機能エリア",
                "再現手順",
                "期待結果",
                "実際の結果",
                "証拠（スクリーンショット）",
                "環境情報",
                "優先度",
                "重要度"
            ]
        }
    
    def _get_default_test_metrics(self) -> list:
        return [
            {
                "metric": "テスト進捗率",
                "formula": "実行済テストケース数 / 全テストケース数 × 100",
                "target": "計画通り",
                "frequency": "日次"
            },
            {
                "metric": "テスト合格率",
                "formula": "合格テストケース数 / 実行済テストケース数 × 100",
                "target": "95%以上",
                "frequency": "日次"
            },
            {
                "metric": "欠陥密度",
                "formula": "欠陥数 / テストケース数",
                "target": "0.05以下",
                "frequency": "週次"
            },
            {
                "metric": "欠陥除去率",
                "formula": "解決済欠陥数 / 発見欠陥数 × 100",
                "target": "90%以上",
                "frequency": "週次"
            },
            {
                "metric": "テスト自動化率",
                "formula": "自動化テストケース数 / 全テストケース数 × 100",
                "target": "70%以上",
                "frequency": "フェーズ終了時"
            },
            {
                "metric": "要件カバレッジ",
                "formula": "テスト済要件数 / 全要件数 × 100",
                "target": "100%",
                "frequency": "フェーズ終了時"
            }
        ]
    
    def _get_default_risk_mitigation(self) -> list:
        return [
            {
                "risk": "テスト環境の不安定性",
                "impact": "高",
                "probability": "中",
                "mitigation": "環境の冗長化、定期メンテナンス、バックアップ環境準備"
            },
            {
                "risk": "テストデータの不足・不整合",
                "impact": "高",
                "probability": "中",
                "mitigation": "早期データ準備、データ生成ツール活用、本番データ活用"
            },
            {
                "risk": "キーリソースの不在",
                "impact": "高",
                "probability": "低",
                "mitigation": "知識共有、バックアップ要員確保、ドキュメント整備"
            },
            {
                "risk": "要件変更によるテスト手戻り",
                "impact": "中",
                "probability": "高",
                "mitigation": "変更管理プロセス確立、影響分析実施、柔軟なテスト計画"
            },
            {
                "risk": "統合先システムの遅延",
                "impact": "高",
                "probability": "中",
                "mitigation": "モックサービス準備、段階的統合、早期調整"
            }
        ]