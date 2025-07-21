"""
Document-specific validators for ServiceNow templates
"""
from typing import Any, Dict, List
from datetime import datetime

from src.validators.base_validator import BaseValidator, ValidationLevel, ValidationReport
from src.models.document import DocumentType


class DocumentValidator(BaseValidator):
    """汎用ドキュメントバリデーター"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationReport:
        """基本的なドキュメントデータの検証"""
        self.reset()
        
        # 必須フィールドの検証
        self.validate_required_field(data, "project_name", str)
        self.validate_required_field(data, "author", dict)
        
        # プロジェクト名の検証
        if "project_name" in data:
            self.validate_project_name(data["project_name"])
        
        # 作成者情報の検証
        if "author" in data and isinstance(data["author"], dict):
            self._validate_author(data["author"])
        
        # バージョン情報の検証
        if "version" in data:
            self.validate_version_format(data["version"])
        
        # クライアント情報の検証
        if "client" in data and isinstance(data["client"], dict):
            self._validate_client(data["client"])
        
        # 作成日の検証
        if "created_date" in data:
            self._validate_created_date(data["created_date"])
        
        return self.generate_report("Document")
    
    def _validate_author(self, author: Dict[str, Any]) -> None:
        """作成者情報の検証"""
        # 必須フィールド
        self.validate_required_field(author, "name", str)
        self.validate_required_field(author, "email", str)
        
        # 名前の検証
        if "name" in author and isinstance(author["name"], str):
            if len(author["name"].strip()) < 2:
                self.add_result(
                    ValidationLevel.WARNING,
                    "author.name",
                    "作成者名が短すぎます",
                    "フルネームまたは適切な識別名を使用してください"
                )
        
        # メールアドレスの検証
        if "email" in author and isinstance(author["email"], str):
            self.validate_email(author["email"], "author.email")
        
        # 役職の検証
        if "role" in author and isinstance(author["role"], str):
            self.validate_text_length(author["role"], "author.role", 2, 50)
    
    def _validate_client(self, client: Dict[str, Any]) -> None:
        """クライアント情報の検証"""
        # 推奨フィールド
        if "name" not in client:
            self.add_result(
                ValidationLevel.INFO,
                "client.name",
                "クライアント名の設定を推奨します",
                "プロジェクトの明確化のためクライアント名を設定してください"
            )
        elif isinstance(client["name"], str):
            self.validate_text_length(client["name"], "client.name", 2, 100)
        
        if "department" in client and isinstance(client["department"], str):
            self.validate_text_length(client["department"], "client.department", 2, 50)
    
    def _validate_created_date(self, created_date: Any) -> None:
        """作成日の検証"""
        if isinstance(created_date, str):
            self.validate_date_format(created_date, "created_date")
        elif isinstance(created_date, datetime):
            # 未来の日付チェック
            if created_date > datetime.now():
                self.add_result(
                    ValidationLevel.WARNING,
                    "created_date",
                    "作成日が未来の日付に設定されています",
                    "現在の日付または過去の日付を設定してください"
                )


class IncidentManagementValidator(BaseValidator):
    """インシデント管理設計書バリデーター"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationReport:
        """インシデント管理設計書の検証"""
        self.reset()
        
        # 基本検証
        doc_validator = DocumentValidator()
        base_report = doc_validator.validate(data)
        self.results.extend(base_report.results)
        
        # インシデント管理固有の検証
        self._validate_incident_types(data)
        self._validate_priority_levels(data)
        self._validate_sla_targets(data)
        self._validate_escalation_rules(data)
        
        return self.generate_report("Incident Management")
    
    def _validate_incident_types(self, data: Dict[str, Any]) -> None:
        """インシデントタイプの検証"""
        if "incident_types" in data:
            if not self.validate_list_field(data, "incident_types", min_items=3, max_items=20):
                return
            
            incident_types = data["incident_types"]
            # 重複チェック
            if len(incident_types) != len(set(incident_types)):
                self.add_result(
                    ValidationLevel.WARNING,
                    "incident_types",
                    "インシデントタイプに重複があります",
                    "重複する項目を削除してください"
                )
            
            # 推奨項目チェック
            recommended_types = ["システム障害", "パフォーマンス問題", "ユーザーサポート"]
            missing_types = [t for t in recommended_types if t not in incident_types]
            if missing_types:
                self.add_result(
                    ValidationLevel.INFO,
                    "incident_types",
                    f"推奨インシデントタイプが不足しています: {', '.join(missing_types)}",
                    "一般的なインシデントタイプの追加を検討してください"
                )
    
    def _validate_priority_levels(self, data: Dict[str, Any]) -> None:
        """優先度レベルの検証"""
        if "priority_levels" in data:
            if not self.validate_list_field(data, "priority_levels", min_items=3, max_items=7):
                return
            
            priority_levels = data["priority_levels"]
            # 推奨レベル数チェック
            if len(priority_levels) < 4:
                self.add_result(
                    ValidationLevel.INFO,
                    "priority_levels",
                    "優先度レベルが少ないです",
                    "一般的には4-5段階の優先度設定を推奨します"
                )
    
    def _validate_sla_targets(self, data: Dict[str, Any]) -> None:
        """SLA目標の検証"""
        if "sla_targets" in data and isinstance(data["sla_targets"], dict):
            sla_targets = data["sla_targets"]
            
            # 推奨SLAレベル
            recommended_levels = ["critical", "high", "medium", "low"]
            missing_levels = [level for level in recommended_levels if level not in sla_targets]
            
            if missing_levels:
                self.add_result(
                    ValidationLevel.INFO,
                    "sla_targets",
                    f"推奨SLAレベルが不足しています: {', '.join(missing_levels)}",
                    "包括的なSLA設定のため全優先度レベルの設定を推奨します"
                )
            
            # SLA時間の形式チェック
            for level, time_target in sla_targets.items():
                if isinstance(time_target, str):
                    if not self._validate_time_format(time_target):
                        self.add_result(
                            ValidationLevel.WARNING,
                            f"sla_targets.{level}",
                            f"SLA時間の形式が不明確です: {time_target}",
                            "「4時間」「30分」「2営業日」などの明確な形式を使用してください"
                        )
    
    def _validate_escalation_rules(self, data: Dict[str, Any]) -> None:
        """エスカレーションルールの検証"""
        if "escalation_rules" in data and isinstance(data["escalation_rules"], str):
            escalation_rules = data["escalation_rules"]
            
            if len(escalation_rules.strip()) < 10:
                self.add_result(
                    ValidationLevel.WARNING,
                    "escalation_rules",
                    "エスカレーションルールの説明が簡潔すぎます",
                    "具体的な条件と手順を詳細に記述してください"
                )
            
            # 時間指定の確認
            if not any(word in escalation_rules for word in ["分", "時間", "日", "営業日"]):
                self.add_result(
                    ValidationLevel.INFO,
                    "escalation_rules",
                    "エスカレーション時間の指定が見つかりません",
                    "具体的な時間制限を含めることを推奨します"
                )
    
    def _validate_time_format(self, time_str: str) -> bool:
        """時間形式の検証"""
        import re
        time_patterns = [
            r'\d+分',
            r'\d+時間',
            r'\d+日',
            r'\d+営業日',
            r'\d+\s*(分|時間|日|営業日)'
        ]
        return any(re.search(pattern, time_str) for pattern in time_patterns)


class KnowledgeManagementValidator(BaseValidator):
    """ナレッジ管理設計書バリデーター"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationReport:
        """ナレッジ管理設計書の検証"""
        self.reset()
        
        # 基本検証
        doc_validator = DocumentValidator()
        base_report = doc_validator.validate(data)
        self.results.extend(base_report.results)
        
        # ナレッジ管理固有の検証
        self._validate_knowledge_types(data)
        self._validate_content_categories(data)
        self._validate_search_features(data)
        self._validate_quality_metrics(data)
        
        return self.generate_report("Knowledge Management")
    
    def _validate_knowledge_types(self, data: Dict[str, Any]) -> None:
        """ナレッジタイプの検証"""
        if "knowledge_types" in data:
            if not self.validate_list_field(data, "knowledge_types", min_items=2, max_items=15):
                return
            
            knowledge_types = data["knowledge_types"]
            # 推奨タイプチェック
            recommended_types = ["How-to記事", "FAQ", "トラブルシューティングガイド", "ベストプラクティス"]
            
            if isinstance(knowledge_types[0], dict):
                # 詳細形式の場合
                type_names = [kt.get("name", "") for kt in knowledge_types if isinstance(kt, dict)]
            else:
                # 簡単形式の場合
                type_names = knowledge_types
            
            missing_types = [t for t in recommended_types if t not in type_names]
            if missing_types:
                self.add_result(
                    ValidationLevel.INFO,
                    "knowledge_types",
                    f"推奨ナレッジタイプが不足しています: {', '.join(missing_types)}",
                    "包括的なナレッジ管理のため基本的なタイプの追加を検討してください"
                )
    
    def _validate_content_categories(self, data: Dict[str, Any]) -> None:
        """コンテンツカテゴリの検証"""
        if "content_categories" in data:
            if not self.validate_list_field(data, "content_categories", min_items=3, max_items=20):
                return
            
            content_categories = data["content_categories"]
            
            # カテゴリ詳細の検証
            if content_categories and isinstance(content_categories[0], dict):
                for i, category in enumerate(content_categories):
                    if isinstance(category, dict):
                        self._validate_category_details(category, f"content_categories[{i}]")
    
    def _validate_category_details(self, category: Dict[str, Any], field_prefix: str) -> None:
        """カテゴリ詳細の検証"""
        required_fields = ["name", "description", "audience"]
        for field in required_fields:
            if field not in category:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"{field_prefix}.{field}",
                    f"カテゴリの{field}が設定されていません",
                    f"カテゴリの明確化のため{field}を設定してください"
                )
    
    def _validate_search_features(self, data: Dict[str, Any]) -> None:
        """検索機能の検証"""
        if "search_features" in data and isinstance(data["search_features"], list):
            search_features = data["search_features"]
            
            # 基本的な検索機能チェック
            recommended_features = ["全文検索", "ファセット検索", "タグ検索"]
            
            if isinstance(search_features[0], dict):
                feature_names = [sf.get("name", "") for sf in search_features]
            else:
                feature_names = search_features
            
            missing_features = [f for f in recommended_features if f not in feature_names]
            if missing_features:
                self.add_result(
                    ValidationLevel.INFO,
                    "search_features",
                    f"推奨検索機能が不足しています: {', '.join(missing_features)}",
                    "ユーザビリティ向上のため基本的な検索機能の追加を検討してください"
                )
    
    def _validate_quality_metrics(self, data: Dict[str, Any]) -> None:
        """品質メトリクスの検証"""
        if "quality_metrics" in data and isinstance(data["quality_metrics"], list):
            quality_metrics = data["quality_metrics"]
            
            # 推奨メトリクス
            recommended_metrics = ["ナレッジ活用率", "検索成功率", "ナレッジ品質スコア", "更新適時性"]
            
            if isinstance(quality_metrics[0], dict):
                metric_names = [qm.get("name", "") for qm in quality_metrics]
            else:
                metric_names = quality_metrics
            
            missing_metrics = [m for m in recommended_metrics if m not in metric_names]
            if missing_metrics:
                self.add_result(
                    ValidationLevel.INFO,
                    "quality_metrics",
                    f"推奨品質メトリクスが不足しています: {', '.join(missing_metrics)}",
                    "ナレッジ品質管理の向上のため基本的なメトリクスの追加を検討してください"
                )


class SLMDesignValidator(BaseValidator):
    """SLM設計書バリデーター"""
    
    def validate(self, data: Dict[str, Any]) -> ValidationReport:
        """SLM設計書の検証"""
        self.reset()
        
        # 基本検証
        doc_validator = DocumentValidator()
        base_report = doc_validator.validate(data)
        self.results.extend(base_report.results)
        
        # SLM固有の検証
        self._validate_service_categories(data)
        self._validate_measurement_metrics(data)
        self._validate_reporting_frequency(data)
        self._validate_review_cycles(data)
        
        return self.generate_report("SLM Design")
    
    def _validate_service_categories(self, data: Dict[str, Any]) -> None:
        """サービスカテゴリの検証"""
        if "service_categories" in data:
            if not self.validate_list_field(data, "service_categories", min_items=2, max_items=15):
                return
            
            service_categories = data["service_categories"]
            
            # 推奨カテゴリ
            recommended_categories = ["基幹業務システム", "インフラサービス", "オフィス系システム"]
            missing_categories = [c for c in recommended_categories if c not in service_categories]
            
            if missing_categories:
                self.add_result(
                    ValidationLevel.INFO,
                    "service_categories",
                    f"推奨サービスカテゴリが不足しています: {', '.join(missing_categories)}",
                    "包括的なSLM管理のため基本的なカテゴリの追加を検討してください"
                )
    
    def _validate_measurement_metrics(self, data: Dict[str, Any]) -> None:
        """測定メトリクスの検証"""
        if "measurement_metrics" in data and isinstance(data["measurement_metrics"], list):
            measurement_metrics = data["measurement_metrics"]
            
            # 必須メトリクス
            required_metrics = ["可用性", "応答時間", "顧客満足度"]
            
            if isinstance(measurement_metrics[0], dict):
                metric_names = [mm.get("name", "") for mm in measurement_metrics]
            else:
                metric_names = measurement_metrics
            
            missing_metrics = [m for m in required_metrics if m not in metric_names]
            if missing_metrics:
                self.add_result(
                    ValidationLevel.WARNING,
                    "measurement_metrics",
                    f"重要な測定メトリクスが不足しています: {', '.join(missing_metrics)}",
                    "SLM管理の基本となるメトリクスを追加してください"
                )
            
            # メトリクス詳細の検証
            if measurement_metrics and isinstance(measurement_metrics[0], dict):
                for i, metric in enumerate(measurement_metrics):
                    if isinstance(metric, dict):
                        self._validate_metric_details(metric, f"measurement_metrics[{i}]")
    
    def _validate_metric_details(self, metric: Dict[str, Any], field_prefix: str) -> None:
        """メトリクス詳細の検証"""
        required_fields = ["name", "definition", "formula"]
        for field in required_fields:
            if field not in metric:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"{field_prefix}.{field}",
                    f"メトリクスの{field}が設定されていません",
                    f"メトリクスの明確化のため{field}を設定してください"
                )
    
    def _validate_reporting_frequency(self, data: Dict[str, Any]) -> None:
        """レポート頻度の検証"""
        if "reporting_frequency" in data and isinstance(data["reporting_frequency"], dict):
            reporting_frequency = data["reporting_frequency"]
            
            # 推奨頻度
            recommended_frequencies = ["daily", "weekly", "monthly", "quarterly"]
            missing_frequencies = [f for f in recommended_frequencies if f not in reporting_frequency]
            
            if missing_frequencies:
                self.add_result(
                    ValidationLevel.INFO,
                    "reporting_frequency",
                    f"推奨レポート頻度が不足しています: {', '.join(missing_frequencies)}",
                    "継続的な監視のため定期的なレポート設定を検討してください"
                )
    
    def _validate_review_cycles(self, data: Dict[str, Any]) -> None:
        """レビューサイクルの検証"""
        if "review_cycles" in data and isinstance(data["review_cycles"], list):
            review_cycles = data["review_cycles"]
            
            if len(review_cycles) < 2:
                self.add_result(
                    ValidationLevel.INFO,
                    "review_cycles",
                    "レビューサイクルが少ないです",
                    "定期的・継続的な改善のため複数のレビューサイクルを設定することを推奨します"
                )
            
            # レビューサイクル詳細の検証
            if review_cycles and isinstance(review_cycles[0], dict):
                for i, cycle in enumerate(review_cycles):
                    if isinstance(cycle, dict):
                        self._validate_review_cycle_details(cycle, f"review_cycles[{i}]")
    
    def _validate_review_cycle_details(self, cycle: Dict[str, Any], field_prefix: str) -> None:
        """レビューサイクル詳細の検証"""
        required_fields = ["name", "frequency", "participants"]
        for field in required_fields:
            if field not in cycle:
                self.add_result(
                    ValidationLevel.WARNING,
                    f"{field_prefix}.{field}",
                    f"レビューサイクルの{field}が設定されていません",
                    f"レビューサイクルの明確化のため{field}を設定してください"
                )