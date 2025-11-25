#!/usr/bin/env python3
"""
Webhook Catcher - Dumps incoming HTTP requests to the console.
Useful for debugging SignalWire callbacks and webhooks.

Usage: webhook-catcher.py [port]
Default port: 5002
"""

import sys
import json
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
WHITE = "\033[37m"


def print_separator():
    print(f"{DIM}{'─' * 80}{RESET}")


def print_request(req):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print()
    print_separator()
    print(f"{BOLD}{GREEN}▶ {req.method}{RESET} {CYAN}{req.path}{RESET}")
    print(f"{DIM}{timestamp}{RESET}")
    print_separator()

    # Query parameters
    if req.args:
        print(f"\n{BOLD}{YELLOW}Query Parameters:{RESET}")
        for key, value in req.args.items():
            print(f"  {WHITE}{key}{RESET}: {value}")

    # Headers (filtered to interesting ones)
    interesting_headers = [
        'content-type', 'content-length', 'user-agent', 'host',
        'x-forwarded-for', 'x-real-ip', 'x-signalwire-signature',
        'authorization', 'accept', 'origin', 'referer'
    ]

    print(f"\n{BOLD}{YELLOW}Headers:{RESET}")
    for header, value in req.headers:
        header_lower = header.lower()
        if header_lower in interesting_headers or header_lower.startswith('x-'):
            print(f"  {WHITE}{header}{RESET}: {value}")

    # Body
    content_type = req.content_type or ''

    if req.data:
        print(f"\n{BOLD}{YELLOW}Body:{RESET} {DIM}({len(req.data)} bytes){RESET}")

        try:
            if 'json' in content_type:
                # Pretty print JSON
                data = json.loads(req.data)
                formatted = json.dumps(data, indent=2)
                for line in formatted.split('\n'):
                    print(f"  {MAGENTA}{line}{RESET}")
            elif 'form' in content_type:
                # Form data
                for key, value in req.form.items():
                    print(f"  {WHITE}{key}{RESET}: {value}")
            else:
                # Raw data
                try:
                    text = req.data.decode('utf-8')
                    for line in text.split('\n')[:50]:  # Limit lines
                        print(f"  {text[:200]}")
                except:
                    print(f"  {DIM}(binary data){RESET}")
        except Exception as e:
            print(f"  {DIM}(could not parse: {e}){RESET}")

    print_separator()
    print(f"{DIM}Responded with 200 OK{RESET}")
    print()

    sys.stdout.flush()


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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5002

    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗
║                    Webhook Catcher                            ║
╚══════════════════════════════════════════════════════════════╝{RESET}

Listening on port {BOLD}{port}{RESET}

Endpoints:
  {GREEN}/webhook{RESET}         - Returns JSON response
  {GREEN}/webhook/xml{RESET}     - Returns XML/LaML response
  {GREEN}/webhook/*{RESET}       - Catch-all for any subpath

{DIM}Press Ctrl+C to stop{RESET}
""")

    app.run(host='0.0.0.0', port=port, debug=False)
