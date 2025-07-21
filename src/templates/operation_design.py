from datetime import datetime
from typing import Any, Dict

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType


class OperationDesignTemplate(BaseDocumentTemplate):
    """運用設計書テンプレート"""
    
    def get_template_name(self) -> str:
        return "operation_design.j2"
    
    def get_document_type(self) -> DocumentType:
        return DocumentType.OPERATION_DESIGN
    
    def get_required_fields(self) -> list:
        base_fields = super().get_required_fields()
        # 基本フィールドのみを必須とし、その他はprepare_contextでデフォルト値を設定
        return base_fields
    
    def get_sections(self) -> list:
        return [
            "1. 概要",
            "2. 運用体制",
            "3. 監視・保守",
            "4. バックアップ・復旧",
            "5. 変更管理",
            "6. セキュリティ運用",
            "7. 性能管理",
            "8. 障害対応",
            "9. 定期メンテナンス",
            "10. 運用改善"
        ]
    
    def prepare_context(self, data: Dict[str, Any]) -> Dict[str, Any]:
        context = {
            "project_name": data.get("project_name"),
            "author": data.get("author"),
            "version": data.get("version", "1.0"),
            "created_date": data.get("created_date", datetime.now()),
            "operation_overview": data.get("operation_overview", {}),
            "organization": data.get("organization", {}),
            "monitoring_maintenance": data.get("monitoring_maintenance", {}),
            "backup_recovery": data.get("backup_recovery", {}),
            "change_management": data.get("change_management", {}),
            "security_operations": data.get("security_operations", {}),
            "performance_management": data.get("performance_management", {}),
            "incident_response": data.get("incident_response", {}),
            "maintenance_schedule": data.get("maintenance_schedule", {}),
            "operation_improvement": data.get("operation_improvement", {})
        }
        
        # デフォルト値の設定
        if not context["operation_overview"]:
            context["operation_overview"] = self._get_default_operation_overview()
        
        if not context["organization"]:
            context["organization"] = self._get_default_organization()
        
        if not context["monitoring_maintenance"]:
            context["monitoring_maintenance"] = self._get_default_monitoring_maintenance()
        
        if not context["backup_recovery"]:
            context["backup_recovery"] = self._get_default_backup_recovery()
        
        if not context["change_management"]:
            context["change_management"] = self._get_default_change_management()
        
        if not context["security_operations"]:
            context["security_operations"] = self._get_default_security_operations()
        
        if not context["performance_management"]:
            context["performance_management"] = self._get_default_performance_management()
        
        if not context["incident_response"]:
            context["incident_response"] = self._get_default_incident_response()
        
        if not context["maintenance_schedule"]:
            context["maintenance_schedule"] = self._get_default_maintenance_schedule()
        
        if not context["operation_improvement"]:
            context["operation_improvement"] = self._get_default_operation_improvement()
        
        return context
    
    def _get_default_operation_overview(self) -> Dict[str, Any]:
        return {
            "purpose": "ServiceNowプラットフォームの安定稼働と継続的なサービス改善を実現する",
            "scope": "ServiceNow本番環境および関連システムの全運用業務",
            "objectives": [
                "システム可用性99.9%以上の維持",
                "ユーザー満足度の継続的向上",
                "セキュリティインシデント0件の維持",
                "運用コストの最適化",
                "業務継続性の確保"
            ],
            "service_hours": {
                "business_hours": "平日 8:00-18:00",
                "extended_hours": "平日 7:00-20:00",
                "emergency_support": "24時間365日"
            }
        }
    
    def _get_default_organization(self) -> Dict[str, Any]:
        return {
            "operation_model": "ハイブリッド運用（内製＋外部委託）",
            "teams": [
                {
                    "team": "ServiceNow管理チーム",
                    "size": "5名",
                    "responsibility": "プラットフォーム管理、設定変更、ユーザーサポート",
                    "skill_level": "エキスパート",
                    "location": "社内"
                },
                {
                    "team": "インフラ運用チーム",
                    "size": "3名",
                    "responsibility": "サーバー・ネットワーク監視、基盤保守",
                    "skill_level": "上級",
                    "location": "社内・委託"
                },
                {
                    "team": "24時間監視センター",
                    "size": "12名（3交代）",
                    "responsibility": "システム監視、初期対応、エスカレーション",
                    "skill_level": "中級",
                    "location": "委託"
                },
                {
                    "team": "ヘルプデスク",
                    "size": "8名",
                    "responsibility": "ユーザーサポート、問い合わせ対応",
                    "skill_level": "初級-中級",
                    "location": "社内・委託"
                }
            ],
            "roles_responsibilities": [
                {
                    "role": "運用マネージャー",
                    "count": 1,
                    "responsibilities": [
                        "運用全体の統括管理",
                        "SLA管理・報告",
                        "予算管理",
                        "ベンダー管理"
                    ]
                },
                {
                    "role": "ServiceNowアドミニストレーター",
                    "count": 2,
                    "responsibilities": [
                        "システム設定・カスタマイズ",
                        "アップデート・パッチ適用",
                        "ユーザー・権限管理",
                        "レポート・ダッシュボード管理"
                    ]
                }
            ]
        }
    
    def _get_default_monitoring_maintenance(self) -> Dict[str, Any]:
        return {
            "monitoring_scope": [
                "システム可用性・応答時間",
                "リソース使用率（CPU、メモリ、ディスク）",
                "データベース性能",
                "ユーザー接続数・セッション",
                "統合システム接続状況",
                "セキュリティイベント"
            ],
            "monitoring_tools": [
                {
                    "tool": "ServiceNow Performance Analytics",
                    "purpose": "アプリケーション性能監視",
                    "metrics": "レスポンス時間、ユーザー数、処理量"
                },
                {
                    "tool": "Zabbix",
                    "purpose": "インフラ監視",
                    "metrics": "サーバーリソース、ネットワーク"
                },
                {
                    "tool": "Splunk",
                    "purpose": "ログ分析・セキュリティ監視",
                    "metrics": "ログ解析、異常検知"
                }
            ],
            "alerting_rules": [
                {
                    "metric": "システム応答時間",
                    "warning": "3秒超過",
                    "critical": "5秒超過",
                    "action": "パフォーマンス調査開始"
                },
                {
                    "metric": "CPU使用率",
                    "warning": "80%超過",
                    "critical": "90%超過",
                    "action": "リソース増強検討"
                },
                {
                    "metric": "同時接続ユーザー数",
                    "warning": "800名超過",
                    "critical": "1000名超過",
                    "action": "負荷分散検討"
                }
            ]
        }
    
    def _get_default_backup_recovery(self) -> Dict[str, Any]:
        return {
            "backup_strategy": {
                "backup_types": [
                    {
                        "type": "フルバックアップ",
                        "frequency": "週次（日曜日 2:00）",
                        "retention": "3ヶ月",
                        "storage": "オフサイト"
                    },
                    {
                        "type": "差分バックアップ",
                        "frequency": "日次（毎日 2:00）",
                        "retention": "2週間",
                        "storage": "オンサイト・オフサイト"
                    },
                    {
                        "type": "設定バックアップ",
                        "frequency": "設定変更時",
                        "retention": "1年",
                        "storage": "バージョン管理システム"
                    }
                ],
                "backup_verification": "月次復旧テスト実施"
            },
            "disaster_recovery": {
                "rto": "4時間（Recovery Time Objective）",
                "rpo": "1時間（Recovery Point Objective）",
                "dr_site": "セカンダリデータセンター",
                "failover_procedure": "自動フェイルオーバー + 手動確認"
            },
            "business_continuity": {
                "critical_functions": [
                    "インシデント管理",
                    "重要業務システムの監視",
                    "緊急連絡機能"
                ],
                "workaround_procedures": "緊急時手動運用手順を整備",
                "communication_plan": "関係者への緊急連絡体制"
            }
        }
    
    def _get_default_change_management(self) -> Dict[str, Any]:
        return {
            "change_categories": [
                {
                    "category": "緊急変更",
                    "approval": "運用マネージャー承認",
                    "implementation": "即時実行可能",
                    "documentation": "事後文書化"
                },
                {
                    "category": "標準変更",
                    "approval": "事前承認済み",
                    "implementation": "手順書に従い実行",
                    "documentation": "実行記録のみ"
                },
                {
                    "category": "通常変更",
                    "approval": "変更管理委員会",
                    "implementation": "承認後計画実行",
                    "documentation": "完全文書化"
                }
            ],
            "change_windows": [
                {
                    "window": "定期メンテナンス",
                    "schedule": "毎月第3土曜日 22:00-06:00",
                    "scope": "計画停止を伴う変更"
                },
                {
                    "window": "週次メンテナンス",
                    "schedule": "毎週土曜日 02:00-04:00",
                    "scope": "システム影響の小さい変更"
                }
            ],
            "approval_matrix": [
                {
                    "change_type": "設定変更",
                    "approver": "ServiceNowアドミニストレーター",
                    "condition": "影響度：小"
                },
                {
                    "change_type": "システム変更",
                    "approver": "運用マネージャー + IT部門長",
                    "condition": "影響度：中以上"
                }
            ]
        }
    
    def _get_default_security_operations(self) -> Dict[str, Any]:
        return {
            "security_monitoring": [
                "不正ログイン試行の検知",
                "権限昇格の監視",
                "データアクセスパターンの異常検知",
                "システム設定変更の追跡",
                "外部システム連携の監視"
            ],
            "access_control": {
                "password_policy": "最小12文字、大小英数字+記号、90日更新",
                "mfa_requirement": "管理者権限必須、一般ユーザー推奨",
                "session_management": "アイドル30分でタイムアウト",
                "privilege_review": "四半期ごとの権限レビュー"
            },
            "vulnerability_management": {
                "patch_management": "月次パッチ適用（重要度：高は即座）",
                "vulnerability_scan": "週次自動スキャン",
                "penetration_test": "年次実施",
                "security_assessment": "四半期評価"
            },
            "incident_response": {
                "detection": "SIEM・EDRによる自動検知",
                "response_time": "Critical: 1時間、High: 4時間、Medium: 24時間",
                "escalation": "CSIRT → IT部門長 → 経営層",
                "forensics": "外部専門機関との連携"
            }
        }
    
    def _get_default_performance_management(self) -> Dict[str, Any]:
        return {
            "performance_targets": [
                {
                    "metric": "システム可用性",
                    "target": "99.9%",
                    "measurement": "月次",
                    "sla_penalty": "99.5%未満で課金調整"
                },
                {
                    "metric": "応答時間",
                    "target": "平均3秒以内",
                    "measurement": "リアルタイム",
                    "sla_penalty": "5秒超過が10%以上"
                },
                {
                    "metric": "同時接続数",
                    "target": "1000ユーザー",
                    "measurement": "ピーク時",
                    "sla_penalty": "性能劣化発生時"
                }
            ],
            "capacity_planning": {
                "growth_projection": "年間20%増",
                "resource_monitoring": "月次キャパシティレポート",
                "scaling_triggers": "リソース使用率80%で拡張検討",
                "budget_planning": "年次予算計画に反映"
            },
            "optimization": [
                "データベースクエリ最適化",
                "インデックス見直し",
                "キャッシュ戦略調整",
                "ガベージコレクション調整",
                "ネットワーク帯域最適化"
            ]
        }
    
    def _get_default_incident_response(self) -> Dict[str, Any]:
        return {
            "severity_levels": [
                {
                    "level": "Critical（P1）",
                    "criteria": "システム全停止、重要業務影響",
                    "response_time": "15分以内",
                    "escalation": "30分後に次レベル",
                    "communication": "1時間ごと状況報告"
                },
                {
                    "level": "High（P2）",
                    "criteria": "部分機能停止、業務影響あり",
                    "response_time": "1時間以内",
                    "escalation": "4時間後に次レベル",
                    "communication": "2時間ごと状況報告"
                },
                {
                    "level": "Medium（P3）",
                    "criteria": "軽微な機能障害",
                    "response_time": "4時間以内",
                    "escalation": "翌営業日",
                    "communication": "日次報告"
                }
            ],
            "response_procedures": [
                {
                    "step": "1. 初期対応",
                    "activities": "影響範囲確認、ステークホルダー通知、暫定対処",
                    "responsible": "監視センター",
                    "sla": "15分以内"
                },
                {
                    "step": "2. 詳細調査",
                    "activities": "根本原因調査、解決策検討、影響評価",
                    "responsible": "専門チーム",
                    "sla": "1-4時間"
                },
                {
                    "step": "3. 復旧作業",
                    "activities": "解決策実装、動作確認、影響範囲検証",
                    "responsible": "専門チーム",
                    "sla": "SLA基準内"
                },
                {
                    "step": "4. 事後処理",
                    "activities": "原因分析、再発防止策、文書化",
                    "responsible": "運用チーム",
                    "sla": "3営業日以内"
                }
            ],
            "escalation_matrix": [
                {
                    "level": "L1",
                    "responsible": "監視センター・ヘルプデスク",
                    "scope": "初期対応、基本的なトラブルシューティング"
                },
                {
                    "level": "L2",
                    "responsible": "ServiceNowアドミニストレーター",
                    "scope": "アプリケーション層の問題対応"
                },
                {
                    "level": "L3",
                    "responsible": "インフラエンジニア",
                    "scope": "システム・インフラ層の問題対応"
                },
                {
                    "level": "L4",
                    "responsible": "ベンダーサポート",
                    "scope": "製品固有の高度な技術問題"
                }
            ]
        }
    
    def _get_default_maintenance_schedule(self) -> Dict[str, Any]:
        return {
            "regular_maintenance": [
                {
                    "task": "システム健全性チェック",
                    "frequency": "日次",
                    "time": "毎日 6:00",
                    "duration": "30分",
                    "responsible": "監視センター"
                },
                {
                    "task": "ログファイルローテーション",
                    "frequency": "日次",
                    "time": "毎日 2:00",
                    "duration": "15分",
                    "responsible": "自動実行"
                },
                {
                    "task": "データベースメンテナンス",
                    "frequency": "週次",
                    "time": "毎週日曜 3:00",
                    "duration": "2時間",
                    "responsible": "DBA"
                },
                {
                    "task": "セキュリティパッチ適用",
                    "frequency": "月次",
                    "time": "第3土曜 22:00",
                    "duration": "4時間",
                    "responsible": "インフラチーム"
                }
            ],
            "planned_outages": [
                {
                    "purpose": "ServiceNowアップデート",
                    "frequency": "四半期",
                    "notification": "2週間前通知",
                    "duration": "4-6時間",
                    "rollback_plan": "前バージョンへの復旧"
                },
                {
                    "purpose": "ハードウェアメンテナンス",
                    "frequency": "年次",
                    "notification": "1ヶ月前通知",
                    "duration": "8時間",
                    "rollback_plan": "冗長系への切替"
                }
            ],
            "maintenance_checklist": [
                "事前通知の実施確認",
                "バックアップ完了確認",
                "ロールバック手順準備",
                "メンテナンス作業実施",
                "動作確認・検証",
                "作業完了報告"
            ]
        }
    
    def _get_default_operation_improvement(self) -> Dict[str, Any]:
        return {
            "improvement_cycle": {
                "pdca_approach": "Plan-Do-Check-Actサイクルで継続改善",
                "review_frequency": "月次運用レビュー、四半期改善計画",
                "kpi_monitoring": "運用KPIの定期監視と分析",
                "feedback_collection": "ユーザーフィードバックの収集と分析"
            },
            "automation_initiatives": [
                "定型作業の自動化（バックアップ、ログ収集）",
                "アラート対応の自動化",
                "レポート生成の自動化",
                "プロビジョニング自動化",
                "セルフヒーリング機能の実装"
            ],
            "process_optimization": [
                "インシデント対応プロセスの効率化",
                "変更管理プロセスの簡素化",
                "ユーザーサポートプロセスの改善",
                "監視・アラートの精度向上",
                "ドキュメント管理プロセスの整備"
            ],
            "skill_development": [
                "ServiceNow認定資格取得推進",
                "新技術・新機能の学習",
                "ベストプラクティスの共有",
                "外部研修・カンファレンス参加",
                "知識管理システムの活用"
            ]
        }