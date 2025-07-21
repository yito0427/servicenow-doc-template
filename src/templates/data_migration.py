from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class DataMigrationTemplate(BaseDocumentTemplate):
    """データ移行計画書テンプレート"""
    
    def get_template_name(self) -> str:
        return "data_migration.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.DATA_MIGRATION
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. 移行戦略",
            "3. データ分析",
            "4. 移行設計",
            "5. データ変換",
            "6. 移行手順",
            "7. データ検証",
            "8. ロールバック計画",
            "9. リスク管理",
            "10. 運用移行"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "migration_overview": data.get("migration_overview", {}),
            "migration_strategy": data.get("migration_strategy", {}),
            "source_systems": data.get("source_systems", []),
            "data_entities": data.get("data_entities", []),
            "migration_phases": data.get("migration_phases", []),
            "data_transformation": data.get("data_transformation", {}),
            "validation_strategy": data.get("validation_strategy", {}),
            "rollback_plan": data.get("rollback_plan", {}),
            "migration_tools": data.get("migration_tools", []),
            "risk_assessment": data.get("risk_assessment", [])
        }
        
        # デフォルト値の設定
        if not context["migration_overview"]:
            context["migration_overview"] = self._get_default_migration_overview()
        
        if not context["migration_strategy"]:
            context["migration_strategy"] = self._get_default_migration_strategy()
        
        if not context["source_systems"]:
            context["source_systems"] = self._get_default_source_systems()
        
        if not context["data_entities"]:
            context["data_entities"] = self._get_default_data_entities()
        
        if not context["migration_phases"]:
            context["migration_phases"] = self._get_default_migration_phases()
        
        if not context["data_transformation"]:
            context["data_transformation"] = self._get_default_data_transformation()
        
        if not context["validation_strategy"]:
            context["validation_strategy"] = self._get_default_validation_strategy()
        
        if not context["rollback_plan"]:
            context["rollback_plan"] = self._get_default_rollback_plan()
        
        if not context["migration_tools"]:
            context["migration_tools"] = self._get_default_migration_tools()
        
        if not context["risk_assessment"]:
            context["risk_assessment"] = self._get_default_risk_assessment()
        
        return context
    
    def _get_default_migration_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "既存システムから ServiceNow への安全で効率的なデータ移行を実現する",
            "scope": "すべての業務データ、マスターデータ、履歴データの移行",
            "objectives": [
                "データの完全性と整合性の確保",
                "業務継続性の維持",
                "移行期間の最小化",
                "データ品質の向上",
                "法的要件・コンプライアンスの遵守"
            ],
            "constraints": [
                "営業時間外での実行",
                "システム停止時間の制限",
                "データ保護法規制の遵守",
                "既存システムとの並行稼働期間"
            ]
        }
    
    def _get_default_migration_strategy(self) -> Dict[str, Any]:
        return {
            "approach": "段階的移行（Big Bang + Phased Approach）",
            "migration_types": [
                {
                    "type": "一括移行",
                    "target": "マスターデータ",
                    "timing": "カットオーバー前",
                    "rationale": "参照データで影響範囲が限定的"
                },
                {
                    "type": "段階移行",
                    "target": "トランザクションデータ",
                    "timing": "システム別順次",
                    "rationale": "リスク分散と業務影響最小化"
                }
            ],
            "cutover_strategy": {
                "duration": "週末72時間",
                "fallback_window": "24時間",
                "validation_time": "48時間"
            },
            "parallel_run": {
                "duration": "4週間",
                "purpose": "データ整合性確認、業務プロセス検証",
                "scope": "重要業務プロセス"
            }
        }
    
    def _get_default_source_systems(self) -> list:
        return [
            {
                "system_name": "既存ITSM（Remedy）",
                "system_type": "インシデント・問題管理",
                "database_type": "Oracle 19c",
                "data_volume": "500万件（過去5年分）",
                "complexity": "高",
                "migration_priority": "1"
            },
            {
                "system_name": "資産管理システム",
                "system_type": "CMDB・資産管理",
                "database_type": "SQL Server 2019",
                "data_volume": "10万件（現行資産）",
                "complexity": "中",
                "migration_priority": "2"
            },
            {
                "system_name": "Excel・Spreadsheet",
                "system_type": "各種マスター",
                "database_type": "ファイル",
                "data_volume": "5万件",
                "complexity": "低",
                "migration_priority": "3"
            },
            {
                "system_name": "Active Directory",
                "system_type": "ユーザー・組織情報",
                "database_type": "LDAP",
                "data_volume": "1万ユーザー",
                "complexity": "中",
                "migration_priority": "1"
            }
        ]
    
    def _get_default_data_entities(self) -> list:
        return [
            {
                "entity_name": "インシデントレコード",
                "source_table": "HPD_Help_Desk",
                "target_table": "incident",
                "record_count": "3,000,000",
                "migration_type": "履歴込み移行",
                "priority": "高",
                "complexity": "高"
            },
            {
                "entity_name": "ユーザーマスター",
                "source_table": "CTM_People",
                "target_table": "sys_user",
                "record_count": "10,000",
                "migration_type": "現行のみ",
                "priority": "高",
                "complexity": "中"
            },
            {
                "entity_name": "構成アイテム",
                "source_table": "BMC_CORE_BMC_BaseElement",
                "target_table": "cmdb_ci",
                "record_count": "50,000",
                "migration_type": "現行のみ",
                "priority": "高",
                "complexity": "高"
            },
            {
                "entity_name": "組織情報",
                "source_table": "CTM_Department", 
                "target_table": "cmn_department",
                "record_count": "500",
                "migration_type": "現行のみ",
                "priority": "中",
                "complexity": "低"
            },
            {
                "entity_name": "変更要求",
                "source_table": "CHG_Infrastructure_Change",
                "target_table": "change_request",
                "record_count": "100,000",
                "migration_type": "過去2年分",
                "priority": "中",
                "complexity": "高"
            }
        ]
    
    def _get_default_migration_phases(self) -> list:
        return [
            {
                "phase": "Phase 0: 準備フェーズ",
                "duration": "4週間",
                "activities": [
                    "移行環境構築",
                    "移行ツール設定",
                    "データ抽出・分析",
                    "マッピング設計完了"
                ],
                "deliverables": [
                    "移行環境",
                    "データ分析レポート",
                    "マッピング仕様書"
                ]
            },
            {
                "phase": "Phase 1: マスターデータ移行",
                "duration": "2週間",
                "activities": [
                    "ユーザー・組織マスター移行",
                    "CI分類・カテゴリ移行",
                    "基本設定データ移行",
                    "参照データ検証"
                ],
                "deliverables": [
                    "マスターデータ移行完了",
                    "検証レポート"
                ]
            },
            {
                "phase": "Phase 2: 履歴データ移行",
                "duration": "1週間",
                "activities": [
                    "インシデント履歴移行",
                    "変更要求履歴移行",
                    "CI履歴移行",
                    "データ整合性検証"
                ],
                "deliverables": [
                    "履歴データ移行完了",
                    "整合性確認レポート"
                ]
            },
            {
                "phase": "Phase 3: 最終カットオーバー",
                "duration": "72時間",
                "activities": [
                    "最終差分データ移行",
                    "本番システム切替",
                    "システム間連携確認",
                    "業務開始準備"
                ],
                "deliverables": [
                    "本番システム稼働開始",
                    "カットオーバー完了報告"
                ]
            }
        ]
    
    def _get_default_data_transformation(self) -> Dict[str, Any]:
        return {
            "transformation_rules": [
                {
                    "rule_type": "データクレンジング",
                    "description": "重複データの除去、NULL値の処理",
                    "examples": "同一人物の重複ユーザー統合"
                },
                {
                    "rule_type": "フォーマット変換",
                    "description": "日付、数値、テキストフォーマットの統一",
                    "examples": "日付形式をYYYY-MM-DD HH:mm:ssに統一"
                },
                {
                    "rule_type": "コード変換",
                    "description": "マスターコード、分類コードのマッピング",
                    "examples": "優先度（1,2,3,4）→（Critical,High,Medium,Low）"
                },
                {
                    "rule_type": "データ補完",
                    "description": "必須項目の欠損値補完",
                    "examples": "カテゴリ未設定データにデフォルト値設定"
                }
            ],
            "mapping_examples": [
                {
                    "source_field": "Status_Reason",
                    "source_values": "New, Assigned, In Progress, Resolved",
                    "target_field": "state",
                    "target_values": "1, 2, 6, 6",
                    "mapping_logic": "ServiceNow標準ステート値にマッピング"
                },
                {
                    "source_field": "Priority_Weight",
                    "source_values": "1000, 2000, 3000, 4000",
                    "target_field": "priority", 
                    "target_values": "1, 2, 3, 4",
                    "mapping_logic": "数値範囲を優先度レベルに変換"
                }
            ]
        }
    
    def _get_default_validation_strategy(self) -> Dict[str, Any]:
        return {
            "validation_types": [
                {
                    "type": "データ件数検証",
                    "description": "移行前後のレコード数一致確認",
                    "automation": "自動",
                    "tolerance": "100%一致"
                },
                {
                    "type": "データ品質検証",
                    "description": "必須項目、フォーマット、制約違反チェック",
                    "automation": "自動",
                    "tolerance": "エラー率1%以下"
                },
                {
                    "type": "ビジネスロジック検証",
                    "description": "業務ルール、計算値の正当性確認",
                    "automation": "手動＋自動",
                    "tolerance": "サンプル100%一致"
                },
                {
                    "type": "関連性検証",
                    "description": "外部キー、参照整合性の確認",
                    "automation": "自動",
                    "tolerance": "100%一致"
                }
            ],
            "validation_phases": [
                "単体移行後検証",
                "結合移行後検証", 
                "本番移行後検証",
                "稼働後定期検証"
            ],
            "validation_tools": [
                "ServiceNow Import Set Preview",
                "SQL比較クエリ",
                "ETLツール検証機能",
                "カスタム検証スクリプト"
            ]
        }
    
    def _get_default_rollback_plan(self) -> Dict[str, Any]:
        return {
            "rollback_triggers": [
                "データ整合性エラー率が5%超過",
                "重大なビジネス機能停止",
                "システム性能の著しい劣化",
                "セキュリティインシデント発生"
            ],
            "rollback_procedures": [
                {
                    "step": "1. 緊急停止",
                    "action": "新システムへのアクセス停止、旧システム復旧",
                    "time_required": "30分",
                    "responsible": "システム管理者"
                },
                {
                    "step": "2. データベース復旧",
                    "action": "バックアップからのデータ復旧",
                    "time_required": "2時間",
                    "responsible": "DBA"
                },
                {
                    "step": "3. システム切戻し",
                    "action": "DNS、ロードバランサー設定変更",
                    "time_required": "1時間",
                    "responsible": "インフラチーム"
                },
                {
                    "step": "4. 業務再開",
                    "action": "ユーザー通知、業務プロセス復旧",
                    "time_required": "1時間",
                    "responsible": "業務部門"
                }
            ],
            "backup_strategy": {
                "full_backup": "移行開始前に完全バックアップ",
                "incremental_backup": "各フェーズ完了時点でバックアップ",
                "retention": "移行完了後3ヶ月間保持"
            }
        }
    
    def _get_default_migration_tools(self) -> list:
        return [
            {
                "tool_name": "ServiceNow Import Set",
                "purpose": "標準データ取り込み機能",
                "use_case": "構造化データの一括インポート",
                "advantages": "ServiceNow標準、変換ルール設定可能",
                "limitations": "大容量データの処理速度"
            },
            {
                "tool_name": "Integration Hub ETL",
                "purpose": "データ変換・統合処理",
                "use_case": "複雑なデータ変換、システム間連携",
                "advantages": "リアルタイム処理、エラーハンドリング",
                "limitations": "ライセンス費用"
            },
            {
                "tool_name": "REST API",
                "purpose": "プログラマティックデータ移行",
                "use_case": "カスタムデータ処理、大容量データ",
                "advantages": "柔軟性、処理速度",
                "limitations": "開発工数"
            },
            {
                "tool_name": "CSV Import",
                "purpose": "シンプルなファイルベース移行",
                "use_case": "Excel、CSVファイルからの移行",
                "advantages": "簡単、コスト効率",
                "limitations": "大容量データ、複雑な変換に不向き"
            }
        ]
    
    def _get_default_risk_assessment(self) -> list:
        return [
            {
                "risk": "データ変換エラー",
                "probability": "中",
                "impact": "高",
                "mitigation": "十分なテスト実施、段階的移行、データ検証の強化"
            },
            {
                "risk": "移行時間超過",
                "probability": "中",
                "impact": "高", 
                "mitigation": "性能テスト実施、並列処理の活用、バッファ時間確保"
            },
            {
                "risk": "システム間連携障害",
                "probability": "低",
                "impact": "高",
                "mitigation": "統合テスト強化、モックサービス準備、段階的切替"
            },
            {
                "risk": "データ破損・消失",
                "probability": "低",
                "impact": "最高",
                "mitigation": "完全バックアップ、検証プロセス強化、復旧手順確立"
            },
            {
                "risk": "ユーザー習熟不足",
                "probability": "高",
                "impact": "中",
                "mitigation": "事前トレーニング、マニュアル整備、サポート体制確立"
            },
            {
                "risk": "性能劣化",
                "probability": "中",
                "impact": "中",
                "mitigation": "性能要件定義、負荷テスト、チューニング実施"
            }
        ]