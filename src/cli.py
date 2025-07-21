import json
from pathlib import Path
from typing import Optional

import click
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from src.generators.document_generator import DocumentGenerator
from src.models.document import DocumentType


console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="servicenow-doc")
def cli():
    """ServiceNow ITSM導入プロジェクト設計書テンプレート生成ツール"""
    pass


@cli.command()
def list_templates():
    """利用可能なテンプレートの一覧を表示"""
    generator = DocumentGenerator()
    templates = generator.get_available_templates()
    
    table = Table(title="利用可能な設計書テンプレート", show_lines=True)
    table.add_column("ドキュメントタイプ", style="cyan", no_wrap=True)
    table.add_column("テンプレートクラス", style="green")
    table.add_column("セクション数", justify="center", style="yellow")
    
    for template in templates:
        table.add_row(
            template["type"],
            template["template_class"],
            str(len(template["sections"]))
        )
    
    console.print(table)
    
    # 各テンプレートのセクション詳細を表示
    for template in templates:
        console.print(f"\n[bold cyan]{template['type']}[/bold cyan] のセクション:")
        for i, section in enumerate(template["sections"], 1):
            console.print(f"  {section}")


@cli.command()
@click.option(
    "--type", "-t",
    type=click.Choice([dt.value for dt in DocumentType if dt in DocumentGenerator.TEMPLATE_MAPPING]),
    required=True,
    help="生成する設計書のタイプ"
)
@click.option("--project", "-p", required=True, help="プロジェクト名")
@click.option("--author", "-a", required=True, help="作成者名")
@click.option("--email", "-e", required=True, help="作成者のメールアドレス")
@click.option("--data", "-d", type=click.Path(exists=True), help="追加データのJSONまたはYAMLファイル")
@click.option("--output", "-o", type=click.Path(), help="出力ディレクトリ")
def generate(
    type: str,
    project: str,
    author: str,
    email: str,
    data: Optional[str],
    output: Optional[str]
):
    """設計書を生成"""
    try:
        # ドキュメントタイプの変換
        doc_type = next(dt for dt in DocumentType if dt.value == type)
        
        # 追加データの読み込み
        additional_data = {}
        if data:
            data_path = Path(data)
            if data_path.suffix in [".yml", ".yaml"]:
                with open(data_path, "r", encoding="utf-8") as f:
                    additional_data = yaml.safe_load(f)
            else:
                with open(data_path, "r", encoding="utf-8") as f:
                    additional_data = json.load(f)
        
        # ジェネレーターの初期化
        output_dir = Path(output) if output else None
        generator = DocumentGenerator(output_dir)
        
        # ドキュメント生成
        with console.status(f"[bold green]{type}を生成中...", spinner="dots"):
            output_path = generator.generate(
                document_type=doc_type,
                project_name=project,
                author_name=author,
                author_email=email,
                additional_data=additional_data
            )
        
        console.print(Panel.fit(
            f"[bold green]✓[/bold green] 設計書が正常に生成されました！\n"
            f"[bold]ファイル:[/bold] {output_path}",
            title="生成完了",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[bold red]エラー:[/bold red] {e}")
        raise click.Abort()


@cli.command()
@click.option(
    "--type", "-t",
    type=click.Choice([dt.value for dt in DocumentType if dt in DocumentGenerator.TEMPLATE_MAPPING]),
    required=True,
    help="生成するサンプル設計書のタイプ"
)
@click.option("--output", "-o", type=click.Path(), help="出力ディレクトリ")
def generate_sample(type: str, output: Optional[str]):
    """サンプルデータで設計書を生成"""
    try:
        doc_type = next(dt for dt in DocumentType if dt.value == type)
        
        output_dir = Path(output) if output else None
        generator = DocumentGenerator(output_dir)
        
        with console.status(f"[bold green]サンプル{type}を生成中...", spinner="dots"):
            output_path = generator.generate_sample(doc_type)
        
        console.print(Panel.fit(
            f"[bold green]✓[/bold green] サンプル設計書が正常に生成されました！\n"
            f"[bold]ファイル:[/bold] {output_path}",
            title="生成完了",
            border_style="green"
        ))
        
        # ファイルの先頭部分を表示
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            preview = "\n".join(content.split("\n")[:30])
            
        console.print("\n[bold]生成されたファイルのプレビュー:[/bold]")
        syntax = Syntax(preview + "\n...", "markdown", theme="monokai", line_numbers=True)
        console.print(syntax)
        
    except Exception as e:
        console.print(f"[bold red]エラー:[/bold red] {e}")
        raise click.Abort()


@cli.command()
@click.option(
    "--type", "-t",
    type=click.Choice([dt.value for dt in DocumentType if dt in DocumentGenerator.TEMPLATE_MAPPING]),
    required=True,
    help="確認するテンプレートのタイプ"
)
def show_template(type: str):
    """テンプレートの構造を表示"""
    try:
        doc_type = next(dt for dt in DocumentType if dt.value == type)
        template_class = DocumentGenerator.TEMPLATE_MAPPING[doc_type]
        template = template_class()
        
        structure = template.get_template_structure()
        
        console.print(Panel.fit(
            f"[bold]ドキュメントタイプ:[/bold] {structure['document_type']}\n"
            f"[bold]テンプレート名:[/bold] {structure['template_name']}\n"
            f"[bold]必須フィールド:[/bold] {', '.join(structure['required_fields'])}",
            title=f"{type} テンプレート情報",
            border_style="blue"
        ))
        
        console.print("\n[bold]セクション構成:[/bold]")
        for section in structure["sections"]:
            console.print(f"  • {section}")
        
    except Exception as e:
        console.print(f"[bold red]エラー:[/bold red] {e}")
        raise click.Abort()


def main():
    """メインエントリーポイント"""
    cli()


if __name__ == "__main__":
    main()