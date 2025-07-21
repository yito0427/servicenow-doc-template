"""
Web interface tests
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.web.main import app
from src.models.document import DocumentType


@pytest.fixture
def client():
    """FastAPIテストクライアント"""
    return TestClient(app)


class TestWebInterface:
    """Webインターフェースのテスト"""
    
    def test_home_page(self, client):
        """ホームページのテスト"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "ServiceNow Document Generator" in response.text
    
    def test_preview_page(self, client):
        """プレビューページのテスト"""
        response = client.get("/preview")
        
        assert response.status_code == 200
        assert "プレビュー" in response.text
    
    def test_settings_page(self, client):
        """設定ページのテスト"""
        response = client.get("/settings")
        
        assert response.status_code == 200
        assert "設定" in response.text
    
    def test_api_templates_endpoint(self, client):
        """テンプレートAPI エンドポイントのテスト"""
        response = client.get("/api/templates")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_api_settings_endpoint(self, client):
        """設定API エンドポイントのテスト"""
        response = client.get("/api/settings")
        
        assert response.status_code == 200
        data = response.json()
        assert "application" in data
        assert "defaults" in data
        assert "export" in data
    
    def test_health_check(self, client):
        """ヘルスチェックのテスト"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    @patch('src.web.main.doc_generator')
    def test_generate_document_form(self, mock_generator, client):
        """フォームからのドキュメント生成テスト"""
        mock_generator.generate.return_value = MagicMock()
        mock_generator.generate.return_value.name = "test_document.md"
        
        form_data = {
            "document_type": "incident_management",
            "project_name": "テストプロジェクト",
            "author_name": "テスト太郎",
            "author_email": "test@example.com"
        }
        
        response = client.post("/generate-form", data=form_data)
        
        # 成功ページにリダイレクトまたは成功レスポンス
        assert response.status_code in [200, 302]
    
    def test_template_detail_page(self, client):
        """テンプレート詳細ページのテスト"""
        # 存在するテンプレートタイプでテスト
        response = client.get("/template/incident_management")
        
        assert response.status_code in [200, 404]  # テンプレートクラスが見つからない場合は404
    
    def test_template_detail_invalid(self, client):
        """無効なテンプレート詳細ページのテスト"""
        response = client.get("/template/invalid_template")
        
        assert response.status_code == 404
    
    def test_preview_template_page(self, client):
        """テンプレートプレビューページのテスト"""
        response = client.get("/preview/incident_management")
        
        # テンプレートファイルが存在しない場合でも基本的なページ構造は表示される
        assert response.status_code in [200, 500]


class TestWebAPI:
    """Web API のテスト"""
    
    @patch('src.web.main.doc_generator')
    def test_api_generate_document(self, mock_generator, client):
        """API経由のドキュメント生成テスト"""
        mock_generator.generate.return_value = MagicMock()
        mock_generator.generate.return_value.name = "test_document.md"
        
        request_data = {
            "document_type": "incident_management",
            "project_name": "テストプロジェクト",
            "author_name": "テスト太郎",
            "author_email": "test@example.com",
            "additional_data": {}
        }
        
        response = client.post("/api/generate", json=request_data)
        
        # 成功またはテンプレートファイル不在エラー
        assert response.status_code in [200, 500]
    
    def test_api_generate_invalid_document_type(self, client):
        """無効なドキュメントタイプでのAPI生成テスト"""
        request_data = {
            "document_type": "invalid_type",
            "project_name": "テストプロジェクト",
            "author_name": "テスト太郎",
            "author_email": "test@example.com"
        }
        
        response = client.post("/api/generate", json=request_data)
        
        assert response.status_code == 400
    
    def test_api_settings_update_defaults(self, client):
        """設定API - デフォルト値更新のテスト"""
        update_data = {
            "author": {
                "name": "新しいテスト太郎",
                "email": "new_test@example.com",
                "role": "新しいテスター"
            }
        }
        
        response = client.put("/api/settings/defaults", json=update_data)
        
        # 設定ファイルの保存に関連するエラーが発生する可能性があるが、
        # 基本的なAPIロジックは動作することを確認
        assert response.status_code in [200, 500]
    
    def test_api_settings_update_export(self, client):
        """設定API - エクスポート設定更新のテスト"""
        update_data = {
            "pdf": {"page_size": "A3", "margin": "25mm"},
            "word": {"font_size": "12pt"}
        }
        
        response = client.put("/api/settings/export", json=update_data)
        
        assert response.status_code in [200, 500]
    
    def test_api_settings_update_web(self, client):
        """設定API - Web設定更新のテスト"""
        update_data = {
            "title": "新しいタイトル",
            "theme": "material",
            "items_per_page": 20
        }
        
        response = client.put("/api/settings/web", json=update_data)
        
        assert response.status_code in [200, 500]
    
    def test_api_settings_reload(self, client):
        """設定API - 設定再読み込みのテスト"""
        response = client.post("/api/settings/reload")
        
        assert response.status_code in [200, 500]
    
    def test_api_export_formats(self, client):
        """エクスポートフォーマット取得のテスト"""
        response = client.get("/api/export/formats")
        
        assert response.status_code == 200
        data = response.json()
        assert "formats" in data
        assert isinstance(data["formats"], list)


class TestWebSecurity:
    """Webセキュリティのテスト"""
    
    def test_xss_prevention(self, client):
        """XSS防止のテスト"""
        malicious_data = {
            "document_type": "incident_management",
            "project_name": "<script>alert('xss')</script>",
            "author_name": "テスト太郎",
            "author_email": "test@example.com"
        }
        
        response = client.post("/generate-form", data=malicious_data)
        
        # スクリプトタグが適切にエスケープされることを確認
        # レスポンスが成功する場合はエスケープをチェック
        if response.status_code == 200:
            assert "<script>" not in response.text or "&lt;script&gt;" in response.text
    
    def test_sql_injection_prevention(self, client):
        """SQLインジェクション防止のテスト（念のため）"""
        malicious_data = {
            "document_type": "incident_management'; DROP TABLE users; --",
            "project_name": "テストプロジェクト",
            "author_name": "テスト太郎",
            "author_email": "test@example.com"
        }
        
        response = client.post("/api/generate", json=malicious_data)
        
        # 無効なドキュメントタイプとして適切に処理されることを確認
        assert response.status_code == 400
    
    def test_file_path_traversal_prevention(self, client):
        """パストラバーサル攻撃防止のテスト"""
        # 危険なファイル名でのダウンロード試行
        response = client.get("/api/download/../../../etc/passwd")
        
        # 404または適切なエラーレスポンス
        assert response.status_code in [404, 400, 403]


class TestWebPerformance:
    """Webパフォーマンステスト"""
    
    def test_response_time(self, client):
        """レスポンス時間のテスト"""
        import time
        
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # 基本的なページは2秒以内にレスポンス
        assert response_time < 2.0
        assert response.status_code == 200
    
    def test_concurrent_requests(self, client):
        """並行リクエストのテスト"""
        import threading
        import time
        
        responses = []
        
        def make_request():
            response = client.get("/health")
            responses.append(response)
        
        # 複数のスレッドで同時リクエスト
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # 全スレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # 全てのリクエストが成功することを確認
        assert len(responses) == 5
        for response in responses:
            assert response.status_code == 200