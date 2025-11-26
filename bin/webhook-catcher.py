#!/usr/bin/env python3
"""
Webhook Catcher - Dumps incoming HTTP requests to a log file or console.
Useful for debugging SignalWire callbacks and webhooks.

Usage: webhook-catcher.py [port] [--log-file /path/to/log]
Default port: 5002

When --log-file is specified:
  - Output goes to the log file instead of stdout
  - SIGHUP causes the log file to be reopened (for log rotation)
  - ANSI colors are disabled
"""

import sys
import json
import os
import signal
import argparse
from datetime import datetime
from flask import Flask, request

try:
    import requests as req_lib
except ImportError:
    req_lib = None

app = Flask(__name__)

# Global state for log file
log_file = None
log_file_path = None
use_colors = True


def open_log_file():
    """Open or reopen the log file."""
    global log_file
    if log_file_path:
        if log_file:
            log_file.close()
        log_file = open(log_file_path, 'a', buffering=1)  # Line buffered


def handle_sighup(signum, frame):
    """Handle SIGHUP by reopening the log file."""
    if log_file_path:
        open_log_file()
        log_output("Log file reopened after SIGHUP")


def log_output(msg):
    """Write to log file or stdout."""
    if log_file:
        log_file.write(msg + '\n')
        log_file.flush()
    else:
        print(msg)
        sys.stdout.flush()


def get_ngrok_url():
    """Get the current ngrok public URL"""
    if req_lib is None:
        return None
    try:
        resp = req_lib.get('http://127.0.0.1:4040/api/tunnels', timeout=2)
        tunnels = resp.json().get('tunnels', [])
        for tunnel in tunnels:
            if tunnel.get('public_url', '').startswith('https://'):
                return tunnel['public_url']
        if tunnels:
            return tunnels[0].get('public_url')
    except:
        pass
    return None


# ANSI colors (disabled when logging to file)
def color(code):
    return code if use_colors else ""

RESET = lambda: color("\033[0m")
BOLD = lambda: color("\033[1m")
DIM = lambda: color("\033[2m")
CYAN = lambda: color("\033[36m")
GREEN = lambda: color("\033[32m")
YELLOW = lambda: color("\033[33m")
MAGENTA = lambda: color("\033[35m")
BLUE = lambda: color("\033[34m")
WHITE = lambda: color("\033[37m")


def print_separator():
    log_output(f"{DIM()}{'─' * 80}{RESET()}")


def print_request(req):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_output("")
    print_separator()
    log_output(f"{BOLD()}{GREEN()}▶ {req.method}{RESET()} {CYAN()}{req.path}{RESET()}")
    log_output(f"{DIM()}{timestamp}{RESET()}")
    print_separator()

    # Query parameters
    if req.args:
        log_output(f"\n{BOLD()}{YELLOW()}Query Parameters:{RESET()}")
        for key, value in req.args.items():
            log_output(f"  {WHITE()}{key}{RESET()}: {value}")

    # Headers (filtered to interesting ones)
    interesting_headers = [
        'content-type', 'content-length', 'user-agent', 'host',
        'x-forwarded-for', 'x-real-ip', 'x-signalwire-signature',
        'authorization', 'accept', 'origin', 'referer'
    ]

    log_output(f"\n{BOLD()}{YELLOW()}Headers:{RESET()}")
    for header, value in req.headers:
        header_lower = header.lower()
        if header_lower in interesting_headers or header_lower.startswith('x-'):
            log_output(f"  {WHITE()}{header}{RESET()}: {value}")

    # Body
    content_type = req.content_type or ''

    if req.data:
        log_output(f"\n{BOLD()}{YELLOW()}Body:{RESET()} {DIM()}({len(req.data)} bytes){RESET()}")

        try:
            if 'json' in content_type:
                # Pretty print JSON
                data = json.loads(req.data)
                formatted = json.dumps(data, indent=2)
                for line in formatted.split('\n'):
                    log_output(f"  {MAGENTA()}{line}{RESET()}")
            elif 'form' in content_type:
                # Form data
                for key, value in req.form.items():
                    log_output(f"  {WHITE()}{key}{RESET()}: {value}")
            else:
                # Raw data
                try:
                    text = req.data.decode('utf-8')
                    for line in text.split('\n')[:50]:  # Limit lines
                        log_output(f"  {line[:200]}")
                except:
                    log_output(f"  {DIM()}(binary data){RESET()}")
        except Exception as e:
            log_output(f"  {DIM()}(could not parse: {e}){RESET()}")

    print_separator()
    log_output(f"{DIM()}Responded with 200 OK{RESET()}")
    log_output("")


@app.route('/webhook', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/webhook/<path:subpath>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def catch_webhook(subpath=''):
    print_request(request)

    # Return a simple response
    return {
        'status': 'received',
        'method': request.method,
        'path': request.path,
        'timestamp': datetime.now().isoformat()
    }, 200


@app.route('/webhook/xml', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/webhook/xml/<path:subpath>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def catch_webhook_xml(subpath=''):
    """Return XML response for LaML/TwiML testing"""
    print_request(request)

    xml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Webhook received successfully</Say>
</Response>'''

    return xml_response, 200, {'Content-Type': 'application/xml'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webhook Catcher')
    parser.add_argument('port', nargs='?', type=int, default=5002, help='Port to listen on')
    parser.add_argument('--log-file', '-l', help='Log file path (enables daemon mode)')
    args = parser.parse_args()

    port = args.port
    log_file_path = args.log_file

    # Set up log file if specified
    if log_file_path:
        use_colors = False
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        open_log_file()
        # Set up SIGHUP handler for log rotation
        signal.signal(signal.SIGHUP, handle_sighup)
        log_output(f"Webhook catcher started on port {port}")
        log_output(f"Logging to {log_file_path}")
    else:
        # Interactive mode - show banner
        ngrok_url = get_ngrok_url()

        print(f"""
{BOLD()}{CYAN()}╔══════════════════════════════════════════════════════════════╗
║                    Webhook Catcher                           ║
╚══════════════════════════════════════════════════════════════╝{RESET()}

Listening on port {BOLD()}{port}{RESET()}
""")

        if ngrok_url:
            print(f"""{BOLD()}{YELLOW()}Public URLs (copy these):{RESET()}
  {GREEN()}{ngrok_url}/webhook{RESET()}
  {GREEN()}{ngrok_url}/webhook/xml{RESET()}
""")
        else:
            print(f"""{DIM()}(ngrok not detected - showing local endpoints){RESET()}
""")

        print(f"""Endpoints:
  {GREEN()}/webhook{RESET()}         - Returns JSON response
  {GREEN()}/webhook/xml{RESET()}     - Returns XML/LaML response
  {GREEN()}/webhook/*{RESET()}       - Catch-all for any subpath

{DIM()}Press Ctrl+C to stop{RESET()}
""")

    # Run with minimal logging in daemon mode
    if log_file_path:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
