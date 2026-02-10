# Matomo MCP - Conversational Analytics 📊

Talk to your website analytics in natural language.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## What is this?

An MCP (Model Context Protocol) server + chat interface that lets you ask questions about your Matomo analytics data naturally:

- "¿Cómo va mi sitio hoy?"
- "¿Cuántas visitas tuve esta semana?"
- "¿De qué países vienen las visitas?"
- "¿Hay alguien en el sitio ahora?"

## Features

- 🗣️ **Natural language queries** - Ask about your analytics in Spanish or English
- 📊 **Real-time data** - Live visitor counts, today's stats
- 🔍 **Multi-site support** - Track multiple sites from one interface
- 🤖 **AI-powered insights** - Gemini 2.5 Pro understands context
- 🔒 **Self-hosted** - Runs on your own infrastructure

## Tools Available

| Tool | Description |
|------|-------------|
| `get_visits_summary` | Unique visitors, pageviews, bounce rate |
| `get_top_pages` | Most visited pages |
| `get_referrers` | Traffic sources breakdown |
| `get_countries` | Visitor geography |
| `get_devices` | Desktop/mobile/tablet split |
| `get_live_visitors` | Who's on the site right now |
| `get_search_keywords` | SEO keywords |
| `compare_sites` | Side-by-side site comparison |

## Quick Start

```bash
# Clone
git clone https://github.com/GalacticaIA/matomo-mcp.git
cd matomo-mcp

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Matomo URL, token, and Gemini API key

# Run
streamlit run app.py --server.port 4005
```

## Configuration

Create a `.env` file:

```env
MATOMO_URL=https://your-matomo-instance.com
MATOMO_TOKEN=your_api_token
GOOGLE_API_KEY=your_gemini_api_key
```

### Getting your Matomo Token

1. Log into Matomo
2. Go to Settings → Personal → Security
3. Create a new token with "view" permissions

## Tech Stack

- **FastMCP** - MCP server framework
- **Streamlit** - Chat UI
- **LangChain** - Agent orchestration
- **Gemini 2.5 Pro** - Language model

## Why MCP?

Model Context Protocol (MCP) is a standard for connecting AI models to external tools. This project wraps Matomo's API into MCP tools that any compatible AI can use.

## License

MIT - Use freely, just keep the attribution.

## Author

[Ronald Mego](https://ronaldmego.com) - Data & AI

---

Built with FastMCP + LangChain + Gemini
