# Getting Started with WireStarter

This guide will take you from zero to a working SignalWire AI voice agent in about 15 minutes.

## What You'll Build

By the end of this guide, you'll have:
- A Docker-based development environment
- A voice AI agent running on your machine
- A public URL for SignalWire to reach your agent
- A web interface to test calls from your browser

## Prerequisites

Before starting, you'll need:

1. **Docker Desktop** - [Download here](https://docs.docker.com/desktop/)
2. **A SignalWire Account** - [Sign up free](https://signalwire.com/signup)
3. **An ngrok Account** - [Sign up free](https://ngrok.com)

## Step 1: Get Your SignalWire Credentials

1. Log in to your [SignalWire Dashboard](https://signalwire.com/signin)

2. **Get your Space Name**
   - Look at the URL in your browser: `https://YOURSPACE.signalwire.com`
   - Your space name is the part before `.signalwire.com`

3. **Get your Project ID and API Token**
   - Click on **API** in the left sidebar
   - You'll see your **Project ID** (a UUID like `a1b2c3d4-e5f6-...`)
   - Click **Show** next to API Tokens, or create a new one
   - Copy your **API Token**

## Step 2: Get Your ngrok Token

1. Log in to [ngrok Dashboard](https://dashboard.ngrok.com)
2. Go to **Your Authtoken** in the left sidebar
3. Copy your authtoken

**Optional: Reserve a Static Domain**
- Go to **Domains** → **New Domain**
- This gives you a permanent URL like `yourname.ngrok.io` instead of random URLs

## Step 3: Run WireStarter

### Create a Workspace Directory

```bash
mkdir ~/workdir
export WORKDIR=~/workdir
```

### Start the Container

```bash
docker run -it --name wirestarter \
  -p 9080:9080 \
  -e HOST_WORKDIR=$WORKDIR \
  -v $WORKDIR:/workdir \
  briankwest/wirestarter
```

### First Run: Interactive Setup

On first login, WireStarter automatically launches an interactive setup wizard that walks you through configuring everything:

1. **SignalWire Credentials** - Enter your space name, project ID, and API token
2. **ngrok Configuration** - Enter your authtoken and optional static domain
3. **Credential Validation** - Automatically tests your SignalWire credentials

The setup wizard saves everything to `/workdir/.env` so you only need to do this once.

After setup completes, you'll be in the SignalWire Shell (`swsh`). Type `exit` to access the full bash environment.

**Tip:** You can re-run the setup wizard anytime by typing `setup`.

## Step 4: Create Your First Agent

Inside the container:

```bash
# Create a new agent project
newagent myagent

# Change to the project directory
cd /workdir/myagent

# Start the agent
up
```

You'll see output like:

```
════════════════════════════════════════════════════════════════════════════════
SignalWire Agents SDK Server
────────────────────────────────────────────────────────────────────────────────
SWML endpoint:  http://0.0.0.0:5000/swml
SWAIG endpoint: http://0.0.0.0:5000/swml/swaig/
Web root:       http://0.0.0.0:5000/
Get token:      http://0.0.0.0:5000/get_token
Debug webhook:  http://0.0.0.0:5000/debug
Post-prompt:    http://0.0.0.0:5000/post_prompt

Public URLs:
  SWML:        https://yourname.ngrok.io/swml
  SWAIG:       https://yourname.ngrok.io/swml/swaig/
  Get token:   https://yourname.ngrok.io/get_token
  Debug:       https://yourname.ngrok.io/debug
  Post-prompt: https://yourname.ngrok.io/post_prompt

WebRTC Call Address:
  /public/myagent?channel=audio

Debug level: 1 (0=off, 1=basic, 2=verbose)
════════════════════════════════════════════════════════════════════════════════
```

## Step 5: Test Your Agent

1. Open your public URL in a browser: `https://yourname.ngrok.io/`
2. You'll see the SignalWire Agents SDK web interface
3. Click **Call Agent**
4. Allow microphone access when prompted
5. Talk to your agent!

**Want to call from a phone number?** You can optionally buy a SignalWire phone number and point it at your SWML webhook URL. The agent automatically creates an External SWML Handler resource you can also assign to a number.

## Step 6: Customize Your Agent

Your agent's code is in `/workdir/myagent/agents/main_agent.py`. Here's what you can customize:

### Change the Voice

```python
# Default voice
self.add_language("English", "en-US", "rime.spore")

# Try other voices:
# self.add_language("English", "en-US", "rime.marsh")
# self.add_language("English", "en-US", "rime.cove")
# self.add_language("Spanish", "es-MX", "rime.spore")
```

### Change the Personality

Edit the prompts in `_configure_prompts()`:

```python
def _configure_prompts(self):
    self.prompt_add_section(
        "Role",
        "You are a friendly pizza ordering assistant. "
        "Help customers order pizza and answer menu questions."
    )

    self.prompt_add_section(
        "Guidelines",
        body="Follow these guidelines:",
        bullets=[
            "Be enthusiastic about pizza",
            "Suggest popular toppings",
            "Confirm orders before finalizing",
            "Keep responses brief for voice"
        ]
    )
```

### Add Custom Functions (SWAIG)

Your agent can call custom code during conversations:

```python
@AgentBase.tool(
    name="check_order_status",
    description="Check the status of a pizza order",
    parameters={
        "type": "object",
        "properties": {
            "order_number": {
                "type": "string",
                "description": "The order number to look up"
            }
        },
        "required": ["order_number"]
    }
)
def check_order_status(self, args, raw_data):
    order_number = args.get("order_number", "")
    # Your business logic here - database lookup, API call, etc.
    return SwaigFunctionResult(f"Order {order_number} is being prepared and will be ready in 15 minutes.")
```

After making changes, restart the agent with `up`.

## Step 7: Run the Tests

```bash
cd /workdir/myagent
pytest tests/ -v
```

This runs the test suite which verifies:
- Agent loads correctly
- SWML structure is valid
- SWAIG functions work

## Project Structure

```
myagent/
├── agents/
│   ├── __init__.py
│   └── main_agent.py      # Your agent code
├── skills/
│   └── __init__.py        # Reusable skills
├── tests/
│   └── test_agent.py      # Test suite
├── web/
│   └── index.html         # Web interface
├── app.py                  # Server entry point
├── .env                    # Your credentials
└── README.md              # Project documentation
```

## Useful Commands

| Command | Description |
|---------|-------------|
| `up` | Run your agent (auto-restarts on crash) |
| `urls` | Show your public ngrok URLs |
| `testapp` | Test your endpoints are reachable |
| `pytest tests/ -v` | Run the test suite |
| `webhook` | Start a standalone webhook catcher |

## Debugging

### See What's Happening During Calls

Debug webhooks show real-time call events in your terminal. Set `DEBUG_WEBHOOK_LEVEL=2` in `.env` for verbose output.

### Test SWAIG Functions

Use the web interface at your ngrok URL - there's a "Try it" button for testing your SWAIG functions.

### Check the SWML Output

```bash
curl -s -u signalwire:yourpassword https://yourname.ngrok.io/swml | python -m json.tool
```

## Next Steps

- **Add more functions** - Connect to databases, APIs, or other services
- **Use Skills** - Pre-built capabilities from the SignalWire Agents SDK
- **Deploy to production** - Run on a cloud server without ngrok
- **Read the docs** - [SignalWire Agents SDK Documentation](https://github.com/signalwire/signalwire-agents)

## Troubleshooting

### "Connection refused" when calling

- Make sure `up` is running in your agent directory
- Check `urls` to verify ngrok is working
- Verify basic auth credentials match in SignalWire dashboard

### "Invalid credentials" on startup

- Double-check your `.env` file
- Space name should NOT include `.signalwire.com`
- Run `sw_test` to validate credentials

### Can't hear the agent / agent can't hear me

- Check browser microphone permissions
- Try a different browser (Chrome works best)
- Ensure Echo Cancellation is enabled in the web UI

### Agent creates new SWML handlers every restart

- Make sure `AGENT_NAME` is set in your project's `.env`
- The agent uses this to find and reuse existing handlers

## Getting Help

- **GitHub Issues**: [WireStarter](https://github.com/signalwire/WireStarter/issues)
- **SignalWire Community**: [community.signalwire.com](https://community.signalwire.com)
- **Documentation**: [developer.signalwire.com](https://developer.signalwire.com)
