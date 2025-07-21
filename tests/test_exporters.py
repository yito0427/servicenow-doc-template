"""
Document exporter tests
"""
import pytest
from pathlib import Path

from src.exporters.document_exporter import DocumentExporter


class TestDocumentExporter:
    """ドキュメントエクスポーターのテスト"""
    
    def test_exporter_creation(self):
        """エクスポーター作成のテスト"""
        exporter = DocumentExporter()
        
        assert exporter is not None
        assert hasattr(exporter, 'supported_formats')
        assert 'md' in exporter.supported_formats
        assert 'txt' in exporter.supported_formats
    
    def test_supported_formats(self):
        """サポートフォーマットのテスト"""
        exporter = DocumentExporter()
        
        # 基本フォーマットがサポートされていることを確認
        assert 'md' in exporter.supported_formats
        assert 'txt' in exporter.supported_formats
        
        # オプショナルフォーマットの確認（依存関係による）
        # これらは環境によって利用可能/不可能が変わる
        optional_formats = ['docx', 'pdf']
        for fmt in optional_formats:
            if fmt in exporter.supported_formats:
                print(f"Optional format {fmt} is available")
    
    def test_export_markdown(self):
        """Markdownエクスポートのテスト"""
        exporter = DocumentExporter()
        test_content = "# テストドキュメント\n\nこれはテストです。"
        
        result = exporter.export(test_content, 'md')
        
        assert isinstance(result, bytes)
        assert result.decode('utf-8') == test_content
    
    def test_export_text(self):
        """テキストエクスポートのテスト"""
        exporter = DocumentExporter()
        test_content = """# テストドキュメント

これは**太字**と*斜体*のテストです。

- リスト項目1
- リスト項目2

[リンク](http://example.com)もあります。
"""
        
        result = exporter.export(test_content, 'txt')
        
        assert isinstance(result, bytes)
        text_result = result.decode('utf-8')
        
        # Markdownの記号が除去されていることを確認
        assert '#' not in text_result
        assert '**' not in text_result
        assert '*' not in text_result
        assert '[' not in text_result or ']' not in text_result
    
    def test_export_word_if_available(self):
        """Word エクスポートのテスト（利用可能な場合）"""
        exporter = DocumentExporter()
        
        if 'docx' in exporter.supported_formats:
            test_content = """# テストドキュメント

## セクション1
これはテストコンテンツです。

### サブセクション
- リスト項目1
- リスト項目2

| 列1 | 列2 |
|-----|-----|
| A   | B   |
"""
            
            result = exporter.export(test_content, 'docx')
            
            assert isinstance(result, bytes)
            assert len(result) > 0
        else:
            pytest.skip("python-docx not available")
    
    def test_export_pdf_if_available(self):
        """PDF エクスポートのテスト（利用可能な場合）"""
        exporter = DocumentExporter()
        
        if 'pdf' in exporter.supported_formats:
            test_content = """# テストドキュメント

これはPDFエクスポートのテストです。

## 特徴
- 日本語対応
- フォーマット保持
- 読みやすいレイアウト
"""
            
            result = exporter.export(test_content, 'pdf')
            
            assert isinstance(result, bytes)
            assert len(result) > 0
            # PDFファイルのマジックナンバーをチェック
            assert result.startswith(b'%PDF')
        else:
            pytest.skip("weasyprint not available")
    
    def test_export_unsupported_format(self):
        """サポートされていないフォーマットのテスト"""
        exporter = DocumentExporter()
        test_content = "# テストドキュメント"
        
        with pytest.raises(ValueError):
            exporter.export(test_content, 'unsupported_format')
    
    def test_export_to_text_formatting(self):
        """テキストエクスポートのフォーマット処理テスト"""
        exporter = DocumentExporter()
        
        # 複雑なMarkdownコンテンツ
        markdown_content = """# メインタイトル

## サブタイトル

これは**太字**と*斜体*のテストです。

### リスト
- 項目1
- 項目2
- 項目3

### コード
`inline code` があります。

```python
def hello():
    print("Hello, World!")
```

### リンク
[Googleへのリンク](https://www.google.com)

### テーブル
| 名前 | 年齢 | 職業 |
|------|------|------|
| 田中 | 30   | エンジニア |
| 佐藤 | 25   | デザイナー |
"""
        
        result = exporter.export(markdown_content, 'txt')
        text_result = result.decode('utf-8')
        
        # Markdownの構文が適切に除去されていることを確認
        assert '**' not in text_result
        assert '***' not in text_result
        assert '```' not in text_result
        assert '|' not in text_result or text_result.count('|') < markdown_content.count('|')
        assert '#' not in text_result
        
        # 基本的なテキストコンテンツは保持されていることを確認
        assert 'メインタイトル' in text_result
        assert 'サブタイトル' in text_result
        assert '太字' in text_result
        assert '斜体' in text_result
    
    def test_markdown_to_html_conversion(self):
        """Markdown to HTML変換のテスト"""
        exporter = DocumentExporter()
        
        markdown_content = """# テストタイトル

## セクション

これは**太字**と*斜体*のテストです。

- リスト項目1
- リスト項目2

1. 番号付きリスト1
2. 番号付きリスト2
"""
        
        html_result = exporter._markdown_to_html(markdown_content)
        
        # HTMLタグが正しく生成されていることを確認
        assert '<h1>テストタイトル</h1>' in html_result
        assert '<h2>セクション</h2>' in html_result
        assert '<strong>太字</strong>' in html_result
        assert '<em>斜体</em>' in html_result
        assert '<ul>' in html_result
        assert '<li>' in html_result
        assert '<ol>' in html_result
    
    def test_table_conversion(self):
        """テーブル変換のテスト"""
        exporter = DocumentExporter()
        
        table_content = """| 名前 | 年齢 | 職業 |
|------|------|------|
| 田中 | 30   | エンジニア |
| 佐藤 | 25   | デザイナー |
"""
        
        html_result = exporter._markdown_to_html(table_content)
        
        # HTMLテーブルが生成されていることを確認
        assert '<table>' in html_result
        assert '<thead>' in html_result
        assert '<tbody>' in html_result
        assert '<th>名前</th>' in html_result
        assert '<td>田中</td>' in html_result
    
    def test_export_with_japanese_content(self):
        """日本語コンテンツのエクスポートテスト"""
        exporter = DocumentExporter()
        
        japanese_content = """# 日本語ドキュメント

これは日本語のテストです。

## 特徴
- ひらがな、カタカナ対応
- 漢字も正しく処理される
- 句読点も適切に扱われます。

### コード例
```javascript
// 日本語コメント
function こんにちは() {
    console.log("こんにちは、世界！");
}
```
"""
        
        # 各フォーマットで日本語が正しく処理されることを確認
        for format in exporter.supported_formats:
            result = exporter.export(japanese_content, format)
            assert isinstance(result, bytes)
            assert len(result) > 0
            
            if format in ['md', 'txt']:
                # テキストベースフォーマットでは日本語が含まれることを確認
                text_result = result.decode('utf-8')
                assert 'こんにちは' in text_result


class TestExporterIntegration:
    """エクスポーター統合テスト"""
    
    def test_multiple_format_export(self):
        """複数フォーマットでのエクスポートテスト"""
        exporter = DocumentExporter()
        
        test_content = """# ServiceNow設計書

## 概要
ServiceNowのインシデント管理設計書です。

### 機能
- インシデント受付
- 分類・優先度設定
- エスカレーション

### SLA
| 優先度 | 対応時間 |
|--------|----------|
| P1     | 15分     |
| P2     | 30分     |
"""
        
        results = {}
        
        # 利用可能な全フォーマットでエクスポート
        for format in exporter.supported_formats:
            results[format] = exporter.export(test_content, format)
        
        # 全てのフォーマットで結果が得られることを確認
        for format, result in results.items():
            assert isinstance(result, bytes)
            assert len(result) > 0
    
    def test_large_content_export(self):
        """大きなコンテンツのエクスポートテスト"""
        exporter = DocumentExporter()
        
        # 大きなコンテンツを生成
        large_content = "# 大きなドキュメント\n\n"
        for i in range(100):
            large_content += f"## セクション {i+1}\n\n"
            large_content += f"これはセクション {i+1} の内容です。" * 10 + "\n\n"
        
        # 各フォーマットで処理できることを確認
        for format in ['md', 'txt']:  # 基本フォーマットのみテスト
            result = exporter.export(large_content, format)
            assert isinstance(result, bytes)
            assert len(result) > 0
    
    def test_special_characters_handling(self):
        """特殊文字の処理テスト"""
        exporter = DocumentExporter()
        
        special_content = """# 特殊文字テスト

## 記号
- & (アンパサンド)
- < > (不等号)
- " ' (引用符)
- © ® ™ (著作権記号)

## 絵文字
- 😀 😊 😎
- 🚀 💻 📊

## その他
- 改行\n文字
- タブ\t文字
"""
        
        # 特殊文字が適切に処理されることを確認
        for format in ['md', 'txt']:
            result = exporter.export(special_content, format)
            assert isinstance(result, bytes)
            assert len(result) > 0
            
            # UTF-8デコードが成功することを確認
            text_result = result.decode('utf-8')
            assert len(text_result) > 0