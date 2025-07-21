from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Type

from src.core.base_template import BaseDocumentTemplate
from src.models.document import DocumentType, User
from src.templates.cmdb_design import CMDBDesignTemplate
from src.templates.security_design import SecurityDesignTemplate
from src.templates.environment_release import EnvironmentReleaseTemplate


class DocumentGenerator:
    """設計書生成を管理するクラス"""
    
    # テンプレートクラスのマッピング
    TEMPLATE_MAPPING: Dict[DocumentType, Type[BaseDocumentTemplate]] = {
        DocumentType.CMDB_DESIGN: CMDBDesignTemplate,
        DocumentType.SECURITY_DESIGN: SecurityDesignTemplate,
        DocumentType.ENVIRONMENT_STRATEGY: EnvironmentReleaseTemplate,
    }
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_available_templates(self) -> list:
        """利用可能なテンプレートのリストを返す"""
        return [
            {
                "type": doc_type.value,
                "template_class": template_class.__name__,
                "sections": template_class().get_sections()
            }
            for doc_type, template_class in self.TEMPLATE_MAPPING.items()
        ]
    
    def generate(
        self,
        document_type: DocumentType,
        project_name: str,
        author_name: str,
        author_email: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Path:
        """指定されたタイプの設計書を生成"""
        
        if document_type not in self.TEMPLATE_MAPPING:
            raise ValueError(f"サポートされていないドキュメントタイプ: {document_type}")
        
        # テンプレートクラスのインスタンス化
        template_class = self.TEMPLATE_MAPPING[document_type]
        template = template_class()
        
        # 基本データの準備
        author = User(
            name=author_name,
            email=author_email,
            role="設計者",
            department="IT部門"
        )
        
        data = {
            "project_name": project_name,
            "author": author,
            "version": "1.0",
            "created_date": datetime.now()
        }
        
        # 追加データのマージ
        if additional_data:
            data.update(additional_data)
        
        # ドキュメント生成
        output_path = template.save(data)
        
        return output_path
    
    def generate_sample(self, document_type: DocumentType) -> Path:
        """サンプルデータで設計書を生成"""
        
        sample_data = self._get_sample_data(document_type)
        
        return self.generate(
            document_type=document_type,
            project_name="ServiceNow ITSM導入プロジェクト（サンプル）",
            author_name="山田太郎",
            author_email="yamada.taro@example.com",
            additional_data=sample_data
        )
    
    def _get_sample_data(self, document_type: DocumentType) -> Dict[str, Any]:
        """ドキュメントタイプに応じたサンプルデータを返す"""
        
        if document_type == DocumentType.CMDB_DESIGN:
            return {
                "cmdb_scope": {
                    "description": "全社ITインフラストラクチャの構成管理データベース構築",
                    "objectives": [
                        "ITサービスとビジネスサービスの関係性を可視化",
                        "変更影響分析の精度向上",
                        "インシデント解決時間の短縮"
                    ],
                    "in_scope": [
                        "すべての本番サーバー（物理・仮想）",
                        "ネットワーク機器（ルーター、スイッチ、ファイアウォール）",
                        "ビジネスアプリケーション",
                        "データベースインスタンス"
                    ],
                    "out_of_scope": [
                        "開発環境の一時的リソース",
                        "エンドユーザーデバイス（初期フェーズ）"
                    ]
                },
                "ci_classes": [
                    {
                        "name": "cmdb_ci_linux_server",
                        "label": "Linuxサーバー",
                        "parent": "cmdb_ci_server",
                        "description": "Linux OSで稼働するサーバー",
                        "attributes": [
                            {"name": "kernel_version", "type": "string", "mandatory": True},
                            {"name": "distribution", "type": "string", "mandatory": True}
                        ]
                    }
                ],
                "discovery_strategy": {
                    "mid_servers": [
                        {"location": "東京DC", "count": 2, "target_cis": 500},
                        {"location": "大阪DC", "count": 2, "target_cis": 300}
                    ]
                }
            }
        
        elif document_type == DocumentType.SECURITY_DESIGN:
            return {
                "authentication_method": {
                    "primary": "Azure AD SAML SSO",
                    "primary_details": "Azure Active DirectoryをIdPとして使用し、SAML 2.0でSSO実装"
                },
                "compliance_requirements": [
                    {
                        "name": "個人情報保護法",
                        "requirements": "個人データの適切な管理と保護",
                        "measures": "データ暗号化、アクセス制御、監査ログ"
                    }
                ]
            }
        
        elif document_type == DocumentType.ENVIRONMENT_STRATEGY:
            return {
                "cicd_pipeline": {
                    "stages": [
                        {
                            "name": "ビルド",
                            "tools": "GitHub Actions",
                            "tasks": "コード検証、依存関係チェック",
                            "success_criteria": "すべてのチェックがパス"
                        },
                        {
                            "name": "テスト",
                            "tools": "ServiceNow ATF",
                            "tasks": "自動テスト実行",
                            "success_criteria": "テストカバレッジ80%以上"
                        }
                    ]
                }
            }
        
        return {}