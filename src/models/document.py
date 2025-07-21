from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    # 基本設計書類
    CURRENT_STATE_ANALYSIS = "現状分析書"
    BUSINESS_REQUIREMENTS = "業務要件定義書"
    BASIC_DESIGN = "基本設計書"
    DETAILED_DESIGN = "詳細設計書"
    
    # ITSMプロセス設計書類
    INCIDENT_MANAGEMENT = "インシデント管理設計書"
    PROBLEM_MANAGEMENT = "問題管理設計書"
    CHANGE_MANAGEMENT = "変更管理設計書"
    SERVICE_CATALOG = "サービスカタログ設計書"
    
    # CMDB・サービス階層設計書類
    CMDB_DESIGN = "CMDB設計書"
    SERVICE_HIERARCHY = "サービス階層設計書"
    CI_IDENTIFICATION = "CI識別・正規化設計書"
    DISCOVERY_MID = "Discovery・MID設計書"
    
    # セキュリティ・ガバナンス設計書類
    SECURITY_DESIGN = "セキュリティ設計書"
    ACL_ROLE_MAPPING = "ACL・ロールマッピング設計書"
    COMPLIANCE_DESIGN = "コンプライアンス設計書"
    AUDIT_LOG_DESIGN = "監査ログ設計書"
    
    # 環境・リリース管理設計書類
    ENVIRONMENT_STRATEGY = "環境戦略設計書"
    CICD_DEVOPS = "CI/CD・DevOps設計書"
    RELEASE_MANAGEMENT = "リリース管理設計書"
    UPDATE_SET_STRATEGY = "Update Set管理設計書"
    
    # 技術設計書類
    DATABASE_DESIGN = "データベース設計書"
    WORKFLOW_DESIGN = "ワークフロー設計書"
    UI_UX_DESIGN = "UI/UX設計書"
    INTEGRATION_DESIGN = "システム連携設計書"
    LICENSE_ROLE = "ライセンス・ロール設計書"
    
    # 移行・カットオーバー設計書類
    DATA_MIGRATION = "データ移行設計書"
    CUTOVER_PLAN = "カットオーバー計画書"
    MIGRATION_RUNBOOK = "移行ランブック"
    HYPERCARE_PLAN = "HyperCare計画書"
    
    # 組織変更管理・教育設計書類
    OCM_DESIGN = "組織変更管理設計書"
    TRAINING_PLAN = "教育・トレーニング計画書"
    COMMUNICATION_PLAN = "コミュニケーション計画書"
    CHAMPION_NETWORK = "Champion Network設計書"
    
    # 運用・保守設計書類
    OPERATION_DESIGN = "運用設計書"
    MAINTENANCE_PROCEDURE = "保守運用手順書"
    KPI_PA_DESIGN = "KPI・PA設計書"
    PERFORMANCE_CAPACITY = "性能・キャパシティ設計書"
    
    # テスト・品質管理書類
    TEST_DESIGN = "テスト設計書"
    QUALITY_ASSURANCE = "品質保証計画書"
    REVIEW_CHECKLIST = "レビューチェックリスト"


class DocumentStatus(str, Enum):
    DRAFT = "下書き"
    UNDER_REVIEW = "レビュー中"
    APPROVED = "承認済み"
    PUBLISHED = "公開済み"
    ARCHIVED = "アーカイブ"


class User(BaseModel):
    name: str
    email: str
    role: str
    department: Optional[str] = None


class Attachment(BaseModel):
    filename: str
    file_type: str
    size: int
    uploaded_date: datetime


class Document(BaseModel):
    id: str
    title: str
    type: DocumentType
    version: str = "1.0"
    status: DocumentStatus = DocumentStatus.DRAFT
    author: User
    reviewers: List[User] = Field(default_factory=list)
    approvers: List[User] = Field(default_factory=list)
    created_date: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    content: str = ""
    attachments: List[Attachment] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True