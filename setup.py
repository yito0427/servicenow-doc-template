#!/usr/bin/env python3
"""
ServiceNow Documentation Template Generator
Simple setup script for direct Python execution
"""

import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    # CLIを直接実行
    from src.cli import main
    main()