#!/usr/bin/env python3
"""
ServiceNow Document Template Generator - Web Interface Launcher
"""
import sys
import uvicorn
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    print("🚀 Starting ServiceNow Document Template Generator Web Interface")
    print("📍 Access the application at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("❤️  Stop with Ctrl+C")
    print("-" * 60)
    
    uvicorn.run(
        "src.web.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )