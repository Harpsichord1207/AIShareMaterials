#!/usr/bin/env python3
"""
Markdown Presentation Server
Single-file HTTP server for local presentation viewing and MD file browsing
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
import urllib.parse
from pathlib import Path

PORT = 8080
HOST = "127.0.0.1"


class MarkdownHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with API endpoints for file browsing"""

    def log_message(self, format, *args):
        # Suppress default logging
        pass

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # API: Browse directory
        if parsed.path == '/api/browse':
            self.handle_browse(parsed)
            return

        # API: Get file content
        if parsed.path == '/api/file':
            self.handle_file(parsed)
            return

        # API: List drives (Windows) or root directories
        if parsed.path == '/api/drives':
            self.handle_drives()
            return

        # Default: serve files
        super().do_GET()

    def handle_browse(self, parsed):
        """List MD files in a directory"""
        params = urllib.parse.parse_qs(parsed.query)
        dir_path = params.get('path', ['.'])[0]

        try:
            # Resolve path
            target = Path(dir_path).resolve()

            if not target.exists():
                self.send_error(404, "Directory not found")
                return

            if not target.is_dir():
                self.send_error(400, "Not a directory")
                return

            # Get subdirectories and MD files
            items = []
            for item in sorted(target.iterdir()):
                try:
                    if item.is_dir():
                        # Just show all directories, no recursive check
                        items.append({
                            'name': item.name,
                            'path': str(item),
                            'type': 'directory'
                        })
                    elif item.is_file() and item.suffix.lower() == '.md':
                        items.append({
                            'name': item.name,
                            'path': str(item),
                            'type': 'file',
                            'size': item.stat().st_size
                        })
                except PermissionError:
                    continue

            # Parent directory
            parent = str(target.parent) if target.parent != target else None

            response = {
                'current': str(target),
                'parent': parent,
                'items': items
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except PermissionError:
            self.send_error(403, "Permission denied")
        except Exception as e:
            self.send_error(500, str(e))

    def handle_file(self, parsed):
        """Read MD file content"""
        params = urllib.parse.parse_qs(parsed.query)
        file_path = params.get('path', [None])[0]

        if not file_path:
            self.send_error(400, "Missing file path")
            return

        try:
            target = Path(file_path).resolve()

            if not target.exists():
                self.send_error(404, "File not found")
                return

            if not target.is_file():
                self.send_error(400, "Not a file")
                return

            if target.suffix.lower() != '.md':
                self.send_error(400, "Not a markdown file")
                return

            content = target.read_text(encoding='utf-8')

            response = {
                'path': str(target),
                'name': target.name,
                'content': content
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except PermissionError:
            self.send_error(403, "Permission denied")
        except Exception as e:
            self.send_error(500, str(e))

    def handle_drives(self):
        """List available drives (Windows) or common directories"""
        drives = []

        if sys.platform == 'win32':
            # Windows: list drives
            import string
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if Path(drive).exists():
                    drives.append({'name': drive, 'path': drive})
        else:
            # Unix: common directories
            common = ['/home', '/Users', '/tmp', '/']
            for d in common:
                if Path(d).exists():
                    drives.append({'name': d, 'path': d})

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(drives, ensure_ascii=False).encode('utf-8'))


def main():
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    # Check required files
    if not Path("presentation.html").exists():
        print("❌ Missing presentation.html")
        sys.exit(1)

    with socketserver.TCPServer((HOST, PORT), MarkdownHandler) as httpd:
        print("=" * 50)
        print("  Markdown Presentation Server")
        print("=" * 50)
        print(f"  📁 Serving from: {script_dir}")
        print(f"  🌐 Presentation: http://{HOST}:{PORT}/presentation.html")
        print(f"  📂 File Browser: http://{HOST}:{PORT}/browser.html")
        print(f"  ⏹️  Press Ctrl+C to stop")
        print("=" * 50)

        webbrowser.open(f"http://{HOST}:{PORT}/presentation.html")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped.")


if __name__ == "__main__":
    main()
