"""
FastAPI Web Interface for ServiceNow Document Template Generator
"""
import io
from pathlib import Path
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.generators.document_generator import DocumentGenerator
from src.models.document import DocumentType, User
from src.exporters.document_exporter import DocumentExporter
from src.config.settings import get_settings, reload_settings
from src.validators.validation_manager import ValidationManager, ValidationMode

app = FastAPI(
    title="ServiceNow Document Template Generator",
    description="Generate ServiceNow delivery documents from templates",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="src/web/templates")
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

# Initialize document generator and exporter
doc_generator = DocumentGenerator()
doc_exporter = DocumentExporter()


class DocumentRequest(BaseModel):
    document_type: str
    project_name: str
    author_name: str
    author_email: str
    additional_data: Optional[Dict[str, Any]] = {}


class PreviewRequest(BaseModel):
    document_type: str
    sample_data: Optional[Dict[str, Any]] = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, template: str = None):
    """ホームページの表示"""
    available_templates = doc_generator.get_available_templates()
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "templates": available_templates,
            "document_types": [{"value": dt.value, "name": dt.value} for dt in DocumentType],
            "selected_template": template
        }
    )


@app.get("/api/templates", response_class=JSONResponse)
async def get_templates():
    """利用可能なテンプレート一覧の取得"""
    return doc_generator.get_available_templates()


@app.get("/api/templates/{document_type}/preview", response_class=JSONResponse)
async def preview_template(document_type: str):
    """テンプレートのプレビュー"""
    try:
        doc_type = DocumentType(document_type)
        sample_output = doc_generator.generate_sample(doc_type)
        
        # ファイル内容を読み取り
        with open(sample_output, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {"content": content, "filename": sample_output.name}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid document type: {document_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preview", response_class=HTMLResponse)
async def preview_page(request: Request):
    """プレビューページ（テンプレート選択なし）"""
    return templates.TemplateResponse(
        "preview.html",
        {
            "request": request,
            "templates": [dt for dt in DocumentType],
            "current_template": None,
            "template_info": None,
            "preview_content": None,
            "source_content": None
        }
    )


@app.get("/preview/{document_type}", response_class=HTMLResponse)
async def preview_template_page(request: Request, document_type: str):
    """特定テンプレートのプレビューページ"""
    try:
        doc_type = DocumentType(document_type)
        template_class = doc_generator.TEMPLATE_MAPPING[doc_type]
        template_instance = template_class()
        
        # サンプルデータでテンプレート生成
        sample_data = _get_sample_data(doc_type)
        rendered_content = template_instance.render(sample_data)
        
        # HTMLレンダリング用にMarkdownを変換
        html_content = _markdown_to_html_simple(rendered_content)
        
        template_info = {
            "name": doc_type.value,
            "sections": template_instance.get_sections(),
            "required_fields": template_instance.get_required_fields(),
            "description": template_instance.__class__.__doc__ or ""
        }
        
        return templates.TemplateResponse(
            "preview.html",
            {
                "request": request,
                "templates": [dt for dt in DocumentType],
                "current_template": document_type,
                "template_info": template_info,
                "preview_content": html_content,
                "source_content": rendered_content
            }
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Template not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate", response_class=JSONResponse)
async def generate_document(request: DocumentRequest):
    """ドキュメント生成"""
    try:
        doc_type = DocumentType(request.document_type)
        
        output_path = doc_generator.generate(
            document_type=doc_type,
            project_name=request.project_name,
            author_name=request.author_name,
            author_email=request.author_email,
            additional_data=request.additional_data
        )
        
        return {
            "message": "Document generated successfully",
            "filename": output_path.name,
            "path": str(output_path)
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid document type: {request.document_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """ファイルダウンロード"""
    file_path = Path("output") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    def iterfile():
        with open(file_path, mode="rb") as file_like:
            yield from file_like
    
    return StreamingResponse(
        iterfile(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/template/{document_type}", response_class=HTMLResponse)
async def template_detail(request: Request, document_type: str):
    """テンプレート詳細ページ"""
    try:
        doc_type = DocumentType(document_type)
        template_class = doc_generator.TEMPLATE_MAPPING[doc_type]
        template_instance = template_class()
        
        template_info = {
            "name": doc_type.value,
            "sections": template_instance.get_sections(),
            "required_fields": template_instance.get_required_fields(),
            "description": template_instance.__class__.__doc__ or ""
        }
        
        return templates.TemplateResponse(
            "template_detail.html",
            {
                "request": request,
                "template": template_info,
                "document_type": document_type
            }
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Template not found")


@app.post("/generate-form")
async def generate_from_form(
    request: Request,
    document_type: str = Form(...),
    project_name: str = Form(...),
    author_name: str = Form(...),
    author_email: str = Form(...)
):
    """フォームからのドキュメント生成"""
    try:
        doc_type = DocumentType(document_type)
        
        output_path = doc_generator.generate(
            document_type=doc_type,
            project_name=project_name,
            author_name=author_name,
            author_email=author_email
        )
        
        return templates.TemplateResponse(
            "success.html",
            {
                "request": request,
                "filename": output_path.name,
                "document_type": doc_type.value,
                "project_name": project_name
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": str(e),
                "document_type": document_type
            }
        )


@app.post("/api/export/{filename}")
async def export_document(filename: str, format: str = "pdf"):
    """ドキュメントを指定フォーマットでエクスポート"""
    file_path = Path("output") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Read original content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        exported_data = doc_exporter.export(content, format)
        
        # Determine media type
        media_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
            'md': 'text/markdown'
        }
        
        media_type = media_types.get(format, 'application/octet-stream')
        
        # Generate filename
        base_name = file_path.stem
        export_filename = f"{base_name}.{format}"
        
        return StreamingResponse(
            io.BytesIO(exported_data),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={export_filename}"}
        )
    except ImportError as e:
        raise HTTPException(status_code=501, detail=f"Export format not available: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@app.get("/api/export/formats")
async def get_export_formats():
    """利用可能なエクスポートフォーマットの取得"""
    return {
        "formats": doc_exporter.supported_formats,
        "descriptions": {
            "md": "Markdown (元のフォーマット)",
            "txt": "プレーンテキスト",
            "docx": "Microsoft Word文書",
            "pdf": "PDF文書"
        }
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy", 
        "version": "1.0.0",
        "export_formats": doc_exporter.supported_formats
    }


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """設定ページ"""
    settings = get_settings()
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "settings": settings
        }
    )


@app.get("/api/settings")
async def get_settings_api():
    """設定情報を取得"""
    settings = get_settings()
    return settings.model_dump()


@app.put("/api/settings/defaults")
async def update_defaults(request: Request):
    """デフォルト値設定を更新"""
    try:
        data = await request.json()
        settings = get_settings()
        
        # デフォルト値を更新
        if "author" in data:
            settings.defaults.author.name = data["author"].get("name", settings.defaults.author.name)
            settings.defaults.author.email = data["author"].get("email", settings.defaults.author.email)
            settings.defaults.author.role = data["author"].get("role", settings.defaults.author.role)
        
        if "client" in data:
            settings.defaults.client.name = data["client"].get("name", settings.defaults.client.name)
            settings.defaults.client.department = data["client"].get("department", settings.defaults.client.department)
        
        if "document" in data:
            settings.defaults.document.version = data["document"].get("version", settings.defaults.document.version)
            settings.defaults.document.language = data["document"].get("language", settings.defaults.document.language)
            settings.defaults.document.format = data["document"].get("format", settings.defaults.document.format)
        
        # 設定をファイルに保存
        from pathlib import Path
        config_path = Path("config/templates.yaml")
        settings.to_yaml(config_path)
        
        return {"message": "デフォルト設定が正常に更新されました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/settings/export")
async def update_export_settings(request: Request):
    """エクスポート設定を更新"""
    try:
        data = await request.json()
        settings = get_settings()
        
        if "pdf" in data:
            settings.export.pdf.page_size = data["pdf"].get("page_size", settings.export.pdf.page_size)
            settings.export.pdf.margin = data["pdf"].get("margin", settings.export.pdf.margin)
        
        if "word" in data:
            settings.export.word.font_size = data["word"].get("font_size", settings.export.word.font_size)
        
        # 設定をファイルに保存
        from pathlib import Path
        config_path = Path("config/templates.yaml")
        settings.to_yaml(config_path)
        
        return {"message": "エクスポート設定が正常に更新されました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/settings/web")
async def update_web_settings(request: Request):
    """Web設定を更新"""
    try:
        data = await request.json()
        settings = get_settings()
        
        settings.web.title = data.get("title", settings.web.title)
        settings.web.theme = data.get("theme", settings.web.theme)
        settings.web.items_per_page = data.get("items_per_page", settings.web.items_per_page)
        
        # 設定をファイルに保存
        from pathlib import Path
        config_path = Path("config/templates.yaml")
        settings.to_yaml(config_path)
        
        return {"message": "Web設定が正常に更新されました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/settings/export-config")
async def export_config_file():
    """設定ファイルをエクスポート"""
    try:
        from pathlib import Path
        config_path = Path("config/templates.yaml")
        
        if not config_path.exists():
            raise HTTPException(status_code=404, detail="設定ファイルが見つかりません")
        
        def iterfile():
            with open(config_path, mode="rb") as file_like:
                yield from file_like
        
        return StreamingResponse(
            iterfile(),
            media_type="application/x-yaml",
            headers={"Content-Disposition": "attachment; filename=templates_config.yaml"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/settings/reload")
async def reload_config():
    """設定を再読み込み"""
    try:
        reload_settings()
        return {"message": "設定が正常に再読み込みされました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/validate")
async def validate_document_data(request: DocumentRequest):
    """ドキュメントデータのバリデーション"""
    try:
        doc_type = DocumentType(request.document_type)
        
        # データを準備
        data = {
            "project_name": request.project_name,
            "author": {
                "name": request.author_name,
                "email": request.author_email
            },
            **request.additional_data
        }
        
        # バリデーション実行
        validator_manager = ValidationManager(ValidationMode.PERMISSIVE)
        validation_report = validator_manager.validate_document(doc_type, data)
        
        return {
            "is_valid": validation_report.is_valid,
            "document_type": validation_report.document_type,
            "total_checks": validation_report.total_checks,
            "errors": validation_report.errors,
            "warnings": validation_report.warnings,
            "results": [
                {
                    "level": result.level.value,
                    "field": result.field,
                    "message": result.message,
                    "suggestion": result.suggestion,
                    "is_valid": result.is_valid
                }
                for result in validation_report.results
            ]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/validate/{document_type}/report")
async def get_validation_report(document_type: str, format: str = "json"):
    """バリデーションレポートを取得"""
    try:
        doc_type = DocumentType(document_type)
        
        # サンプルデータでバリデーション
        sample_data = _get_sample_data(doc_type)
        
        validator_manager = ValidationManager(ValidationMode.PERMISSIVE)
        validation_report = validator_manager.validate_document(doc_type, sample_data)
        
        if format == "text":
            report_content = validator_manager.export_validation_report(validation_report, "text")
            return Response(content=report_content, media_type="text/plain")
        elif format == "markdown":
            report_content = validator_manager.export_validation_report(validation_report, "markdown")
            return Response(content=report_content, media_type="text/markdown")
        elif format == "html":
            report_content = validator_manager.export_validation_report(validation_report, "html")
            return Response(content=report_content, media_type="text/html")
        else:
            # JSON形式（デフォルト）
            return {
                "document_type": validation_report.document_type,
                "is_valid": validation_report.is_valid,
                "summary": {
                    "total_checks": validation_report.total_checks,
                    "passed_checks": validation_report.passed_checks,
                    "failed_checks": validation_report.failed_checks,
                    "errors": validation_report.errors,
                    "warnings": validation_report.warnings
                },
                "results": [
                    {
                        "level": result.level.value,
                        "field": result.field,
                        "message": result.message,
                        "suggestion": result.suggestion,
                        "is_valid": result.is_valid
                    }
                    for result in validation_report.results
                ]
            }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid document type: {document_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_sample_data(doc_type: DocumentType) -> Dict[str, Any]:
    """サンプルデータの生成"""
    from datetime import datetime
    
    settings = get_settings()
    
    # 設定ファイルからデフォルト値を取得
    defaults = settings.defaults
    template_defaults = settings.get_default_values(doc_type.value)
    
    base_data = {
        "project_name": "サンプルプロジェクト",
        "author": {
            "name": defaults.author.name,
            "email": defaults.author.email,
            "role": defaults.author.role
        },
        "client": {
            "name": defaults.client.name,
            "department": defaults.client.department
        },
        "delivery_date": datetime.now().strftime("%Y年%m月%d日"),
        "version": defaults.document.version,
        "document_id": f"DOC-{doc_type.value.upper()}-001"
    }
    
    # テンプレート固有のデフォルト値を追加
    base_data.update(template_defaults)
    
    return base_data


def _markdown_to_html_simple(content: str) -> str:
    """簡単なMarkdown to HTML変換"""
    import re
    
    html = content
    
    # Headers
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*$)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Lists
    lines = html.split('\n')
    result_lines = []
    in_ul = False
    
    for line in lines:
        if re.match(r'^\s*[-*+]\s', line):
            if not in_ul:
                result_lines.append('<ul>')
                in_ul = True
            item_text = re.sub(r'^\s*[-*+]\s', '', line)
            result_lines.append(f'<li>{item_text}</li>')
        else:
            if in_ul:
                result_lines.append('</ul>')
                in_ul = False
            if line.strip():
                result_lines.append(f'<p>{line}</p>')
            else:
                result_lines.append('<br>')
    
    if in_ul:
        result_lines.append('</ul>')
    
    html = '\n'.join(result_lines)
    
    # Tables
    html = _convert_tables_to_html_simple(html)
    
    return html


def _convert_tables_to_html_simple(content: str) -> str:
    """簡単なMarkdownテーブルをHTML変換"""
    lines = content.split('\n')
    result = []
    in_table = False
    table_rows = []
    
    for line in lines:
        if line.strip().startswith('|') and line.strip().endswith('|'):
            if '---' in line or '===' in line:
                continue  # Skip separator lines
            
            if not in_table:
                in_table = True
                table_rows = []
            
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            table_rows.append(cells)
        else:
            if in_table:
                # End of table, convert to HTML
                result.append(_table_rows_to_html_simple(table_rows))
                table_rows = []
                in_table = False
            
            result.append(line)
    
    if in_table and table_rows:
        result.append(_table_rows_to_html_simple(table_rows))
    
    return '\n'.join(result)


def _table_rows_to_html_simple(rows: list) -> str:
    """テーブル行をHTMLテーブルに変換"""
    if not rows:
        return ''
    
    html = ['<table class="table table-bordered">']
    
    # Header row
    if rows:
        html.append('<thead><tr>')
        for cell in rows[0]:
            html.append(f'<th>{cell}</th>')
        html.append('</tr></thead>')
    
    # Body rows
    if len(rows) > 1:
        html.append('<tbody>')
        for row in rows[1:]:
            html.append('<tr>')
            for cell in row:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
    
    html.append('</table>')
    return '\n'.join(html)


if __name__ == "__main__":
    uvicorn.run(
        "src.web.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"]
    )