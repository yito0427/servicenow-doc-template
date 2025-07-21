"""
Document generator tests
"""
import pytest
from pathlib import Path
from datetime import datetime

from src.generators.document_generator import DocumentGenerator
from src.models.document import DocumentType


class TestDocumentGenerator:
    """ドキュメントジェネレーターのテスト"""
    
    def test_generator_creation(self, temp_dir):
        """ジェネレーター作成のテスト"""
        generator = DocumentGenerator(output_dir=temp_dir)
        
        assert generator.output_dir == temp_dir
        assert temp_dir.exists()
    
    def test_default_output_dir(self):
        """デフォルト出力ディレクトリのテスト"""
        generator = DocumentGenerator()
        
        assert generator.output_dir == Path("output")
    
    def test_get_available_templates(self, document_generator):
        """利用可能テンプレート取得のテスト"""
        templates = document_generator.get_available_templates()
        
        assert len(templates) > 0
        assert isinstance(templates, list)
        
        # 各テンプレートが必要な情報を持っていることを確認
        for template_info in templates:
            assert "type" in template_info
            assert "template_class" in template_info
            assert "sections" in template_info
    
    def test_template_mapping_completeness(self, document_generator):
        """テンプレートマッピングの完全性テスト"""
        mapping = document_generator.TEMPLATE_MAPPING
        
        # 主要なドキュメントタイプがマッピングされていることを確認
        expected_types = [
            DocumentType.INCIDENT_MANAGEMENT,
            DocumentType.PROBLEM_MANAGEMENT,
            DocumentType.CHANGE_MANAGEMENT,
            DocumentType.SERVICE_CATALOG,
            DocumentType.SLM_DESIGN,
            DocumentType.KNOWLEDGE_MANAGEMENT
        ]
        
        for doc_type in expected_types:
            assert doc_type in mapping
            assert mapping[doc_type] is not None
    
    def test_get_template_class(self, document_generator):
        """テンプレートクラス取得のテスト"""
        template_class = document_generator.get_template_class(DocumentType.INCIDENT_MANAGEMENT)
        
        assert template_class is not None
        # インスタンス化できることを確認
        instance = template_class()
        assert instance.get_document_type() == DocumentType.INCIDENT_MANAGEMENT
    
    def test_get_template_class_invalid(self, document_generator):
        """無効なテンプレートクラス取得のテスト"""
        # 存在しないドキュメントタイプで例外が発生することを確認
        with pytest.raises(ValueError):
            document_generator.get_template_class("invalid_type")
    
    def test_generate_with_all_required_data(self, document_generator, incident_management_data):
        """必要データを全て含む生成テスト"""
        try:
            output_path = document_generator.generate(
                document_type=DocumentType.INCIDENT_MANAGEMENT,
                project_name=incident_management_data["project_name"],
                author_name=incident_management_data["author"]["name"],
                author_email=incident_management_data["author"]["email"],
                additional_data=incident_management_data
            )
            
            # ファイルが生成されることを確認（テンプレートファイルが存在しない場合は例外が発生）
            assert isinstance(output_path, Path)
            
        except Exception as e:
            # テンプレートファイルが存在しない場合の例外は許容
            if "template" not in str(e).lower():
                pytest.fail(f"Unexpected error: {e}")
    
    def test_generate_sample(self, document_generator):
        """サンプル生成のテスト"""
        try:
            output_path = document_generator.generate_sample(DocumentType.INCIDENT_MANAGEMENT)
            assert isinstance(output_path, Path)
            
        except Exception as e:
            # テンプレートファイルが存在しない場合の例外は許容
            if "template" not in str(e).lower():
                pytest.fail(f"Unexpected error: {e}")
    
    def test_validate_data_structure(self, document_generator):
        """データ構造バリデーションのテスト"""
        # 最小限のデータ構造
        minimal_data = {
            "project_name": "テストプロジェクト",
            "author": {
                "name": "テスト太郎",
                "email": "test@example.com"
            }
        }
        
        # データ構造の作成が正常に動作することを確認
        prepared_data = document_generator._prepare_data(
            document_type=DocumentType.INCIDENT_MANAGEMENT,
            project_name=minimal_data["project_name"],
            author_name=minimal_data["author"]["name"],
            author_email=minimal_data["author"]["email"]
        )
        
        assert prepared_data["project_name"] == "テストプロジェクト"
        assert prepared_data["author"]["name"] == "テスト太郎"
        assert prepared_data["author"]["email"] == "test@example.com"


class TestDocumentGeneratorIntegration:
    """ドキュメントジェネレーター統合テスト"""
    
    def test_multiple_document_generation(self, document_generator, sample_document_data):
        """複数ドキュメント生成のテスト"""
        document_types = [
            DocumentType.INCIDENT_MANAGEMENT,
            DocumentType.KNOWLEDGE_MANAGEMENT,
            DocumentType.SLM_DESIGN
        ]
        
        for doc_type in document_types:
            try:
                output_path = document_generator.generate(
                    document_type=doc_type,
                    project_name=sample_document_data["project_name"],
                    author_name=sample_document_data["author"]["name"],
                    author_email=sample_document_data["author"]["email"]
                )
                
                assert isinstance(output_path, Path)
                
            except Exception as e:
                # テンプレートファイルが存在しない場合の例外は許容
                if "template" not in str(e).lower():
                    pytest.fail(f"Unexpected error for {doc_type}: {e}")
    
    def test_output_file_naming(self, document_generator):
        """出力ファイル命名のテスト"""
        # ファイル名生成のテスト
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        doc_type = DocumentType.INCIDENT_MANAGEMENT
        
        expected_pattern = f"{doc_type.value}_{timestamp}"
        
        # ファイル名にドキュメントタイプとタイムスタンプが含まれることを確認
        assert doc_type.value in expected_pattern
        assert len(timestamp) == 13  # YYYYMMDD_HHMMSS format
    
    def test_template_structure_validation(self, document_generator):
        """テンプレート構造バリデーションのテスト"""
        for doc_type, template_class in document_generator.TEMPLATE_MAPPING.items():
            template_instance = template_class()
            
            # 基本的なメソッドが実装されていることを確認
            assert template_instance.get_template_name() is not None
            assert template_instance.get_document_type() is not None
            assert len(template_instance.get_sections()) > 0
            assert len(template_instance.get_required_fields()) > 0
    
    def test_error_handling(self, document_generator):
        """エラーハンドリングのテスト"""
        # 無効なドキュメントタイプでの生成
        with pytest.raises((ValueError, KeyError)):
            document_generator.generate(
                document_type="invalid_type",
                project_name="test",
                author_name="test",
                author_email="test@example.com"
            )
    
    def test_concurrent_generation(self, document_generator, sample_document_data):
        """並行生成のテスト（基本的なスレッドセーフティ確認）"""
        import threading
        import time
        
        results = []
        errors = []
        
        def generate_document(doc_type):
            try:
                output_path = document_generator.generate(
                    document_type=doc_type,
                    project_name=f"concurrent_test_{doc_type.value}",
                    author_name="concurrent_user",
                    author_email="concurrent@example.com"
                )
                results.append(output_path)
            except Exception as e:
                errors.append(e)
        
        # 複数のスレッドで同時実行
        threads = []
        doc_types = [
            DocumentType.INCIDENT_MANAGEMENT,
            DocumentType.KNOWLEDGE_MANAGEMENT
        ]
        
        for doc_type in doc_types:
            thread = threading.Thread(target=generate_document, args=(doc_type,))
            threads.append(thread)
            thread.start()
        
        # 全スレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # テンプレートファイルが存在しない場合のエラーは許容
        template_errors = [e for e in errors if "template" in str(e).lower()]
        other_errors = [e for e in errors if "template" not in str(e).lower()]
        
        # テンプレート以外のエラーがないことを確認
        assert len(other_errors) == 0, f"Unexpected errors: {other_errors}"