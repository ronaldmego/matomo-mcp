# CLAUDE.md - Matomo MCP Project

## Overview

Conversational interface for Matomo Analytics using MCP (Model Context Protocol).
Users can ask about their website performance in natural language.

## Architecture

```
User Query → Streamlit UI → LangChain Agent → Gemini 2.5 Pro
                                    ↓
                            FastMCP Tools → Matomo API
```

## Files

| File | Purpose |
|------|---------|
| `server.py` | FastMCP server with Matomo tools |
| `app.py` | Streamlit chat interface |
| `test_api.py` | Direct API testing |
| `.env` | Configuration (not in git) |

## Running

```bash
# Development
streamlit run app.py --server.port 4005 --server.address 100.64.216.28

# Production (via PM2)
pm2 start "streamlit run app.py --server.port 4005 --server.address 100.64.216.28" --name matomo-mcp
```

## Tools Implemented

1. `get_visits_summary` - Basic stats (visitors, pageviews, bounce)
2. `get_top_pages` - Most visited URLs
3. `get_referrers` - Traffic sources
4. `get_countries` - Visitor geography
5. `get_devices` - Desktop/mobile/tablet
6. `get_live_visitors` - Real-time count
7. `get_search_keywords` - SEO keywords
8. `compare_sites` - Multi-site comparison
9. `list_sites` - Available sites

## Sites Tracked

| ID | Site | Aliases |
|----|------|---------|
| 4 | ronaldmego.com | personal, ronaldmego |
| 5 | galacticaia.com | empresa, galacticaia, galactica |
| 6 | be-cgi.com | becgi, be-cgi |

## API Notes

- Matomo requires POST for token auth (not GET)
- All tools return Spanish-friendly field names
- Period accepts: today, yesterday, week, month, year, last 7 days, last 30 days

## Port

- **4005** (Tailscale only: 100.64.216.28)
- Registered in `~/maintenance/docs/infrastructure/port-registry.md`

## Next Steps

- [ ] Add caching for repeated queries
- [ ] Implement date range comparisons
- [ ] Add goal/conversion tracking
- [ ] Export reports as PDF
- [ ] Deploy to production with PM2
