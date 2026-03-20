#!/usr/bin/env python3
"""
Markdown Presentation Server
Single-file HTTP server for local presentation viewing
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8080
HOST = "127.0.0.1"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with quiet logging"""
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


def main():
    # Change to the directory containing this script
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    
    # Check required files exist
    required_files = ["presentation.html"]
    for i in range(1, 4):
        required_files.extend([f"{i}_prompt.md", f"{i}_result.md"])
    
    missing = [f for f in required_files if not Path(f).exists()]
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        print(f"   Please ensure all files are in: {script_dir}")
        sys.exit(1)
    
    # Create server
    with socketserver.TCPServer((HOST, PORT), QuietHandler) as httpd:
        url = f"http://{HOST}:{PORT}/presentation.html"
        
        print("=" * 50)
        print("  Markdown Presentation Server")
        print("=" * 50)
        print(f"  📁 Serving from: {script_dir}")
        print(f"  🌐 URL: {url}")
        print(f"  ⏹️  Press Ctrl+C to stop")
        print("=" * 50)
        
        # Open browser
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped.")


if __name__ == "__main__":
    main()
