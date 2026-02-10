"""
Matomo MCP Server - Conversational Analytics
Talk to your website analytics in natural language.

Author: GalacticaIA / Ronald Mego
License: MIT
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

# Configuration
MATOMO_URL = os.getenv("MATOMO_URL", "https://matomo.kioskoai.com")
MATOMO_TOKEN = os.getenv("MATOMO_TOKEN")

# Site mapping
SITES = {
    "ronaldmego": 4,
    "ronaldmego.com": 4,
    "personal": 4,
    "galacticaia": 5,
    "galacticaia.com": 5,
    "galactica": 5,
    "empresa": 5,
    "becgi": 6,
    "be-cgi": 6,
    "be-cgi.com": 6,
}

mcp = FastMCP("Matomo Analytics 📊")


def matomo_api(method: str, params: dict = None) -> dict:
    """Make a request to Matomo API."""
    base_params = {
        "module": "API",
        "method": method,
        "format": "JSON",
        "token_auth": MATOMO_TOKEN,
    }
    if params:
        base_params.update(params)
    
    # Use POST - some Matomo configs require it for token auth
    response = requests.post(f"{MATOMO_URL}/index.php", data=base_params)
    response.raise_for_status()
    return response.json()


def resolve_site_id(site: str) -> int:
    """Resolve site name to ID."""
    if isinstance(site, int):
        return site
    site_lower = site.lower().strip()
    return SITES.get(site_lower, 4)  # Default to ronaldmego.com


def get_period_params(period: str = "today") -> dict:
    """Get date parameters for Matomo API."""
    period_lower = period.lower()
    
    if period_lower in ["today", "hoy"]:
        return {"period": "day", "date": "today"}
    elif period_lower in ["yesterday", "ayer"]:
        return {"period": "day", "date": "yesterday"}
    elif period_lower in ["week", "semana", "this week", "esta semana"]:
        return {"period": "week", "date": "today"}
    elif period_lower in ["month", "mes", "this month", "este mes"]:
        return {"period": "month", "date": "today"}
    elif period_lower in ["year", "año", "this year", "este año"]:
        return {"period": "year", "date": "today"}
    elif period_lower in ["last 7 days", "últimos 7 días", "7 days", "7 días"]:
        return {"period": "range", "date": f"last7"}
    elif period_lower in ["last 30 days", "últimos 30 días", "30 days", "30 días"]:
        return {"period": "range", "date": "last30"}
    else:
        return {"period": "day", "date": "today"}


@mcp.tool
def get_visits_summary(site: str = "ronaldmego", period: str = "today") -> dict:
    """
    Get visit summary for a site.
    
    Args:
        site: Site name (ronaldmego, galacticaia, becgi) or ID
        period: Time period (today, yesterday, week, month, year, last 7 days, last 30 days)
    
    Returns:
        Visit statistics including unique visitors, visits, actions, bounce rate, etc.
    """
    site_id = resolve_site_id(site)
    params = {"idSite": site_id, **get_period_params(period)}
    
    data = matomo_api("VisitsSummary.get", params)
    
    return {
        "site": site,
        "site_id": site_id,
        "period": period,
        "unique_visitors": data.get("nb_uniq_visitors", 0),
        "visits": data.get("nb_visits", 0),
        "actions": data.get("nb_actions", 0),
        "pageviews": data.get("nb_pageviews", 0),
        "avg_time_on_site": data.get("avg_time_on_site", 0),
        "bounce_rate": data.get("bounce_rate", "0%"),
        "actions_per_visit": data.get("nb_actions_per_visit", 0),
    }


@mcp.tool
def get_top_pages(site: str = "ronaldmego", period: str = "today", limit: int = 10) -> list:
    """
    Get top visited pages for a site.
    
    Args:
        site: Site name or ID
        period: Time period
        limit: Number of pages to return (default 10)
    
    Returns:
        List of top pages with visit counts
    """
    site_id = resolve_site_id(site)
    params = {
        "idSite": site_id,
        "filter_limit": limit,
        **get_period_params(period)
    }
    
    data = matomo_api("Actions.getPageUrls", params)
    
    pages = []
    for page in data[:limit] if isinstance(data, list) else []:
        pages.append({
            "url": page.get("label", ""),
            "pageviews": page.get("nb_hits", 0),
            "unique_pageviews": page.get("nb_visits", 0),
            "avg_time_on_page": page.get("avg_time_on_page", 0),
            "bounce_rate": page.get("bounce_rate", "0%"),
        })
    
    return {"site": site, "period": period, "top_pages": pages}


@mcp.tool
def get_referrers(site: str = "ronaldmego", period: str = "today", limit: int = 10) -> dict:
    """
    Get traffic sources (referrers) for a site.
    
    Args:
        site: Site name or ID
        period: Time period
        limit: Number of referrers to return
    
    Returns:
        Traffic sources breakdown
    """
    site_id = resolve_site_id(site)
    params = {
        "idSite": site_id,
        "filter_limit": limit,
        **get_period_params(period)
    }
    
    # Get referrer types
    types_data = matomo_api("Referrers.getReferrerType", params)
    
    types = []
    for ref in types_data if isinstance(types_data, list) else []:
        types.append({
            "type": ref.get("label", ""),
            "visits": ref.get("nb_visits", 0),
            "actions": ref.get("nb_actions", 0),
        })
    
    return {"site": site, "period": period, "referrer_types": types}


@mcp.tool
def get_countries(site: str = "ronaldmego", period: str = "today", limit: int = 10) -> dict:
    """
    Get visitor countries for a site.
    
    Args:
        site: Site name or ID
        period: Time period
        limit: Number of countries to return
    
    Returns:
        List of countries with visit counts
    """
    site_id = resolve_site_id(site)
    params = {
        "idSite": site_id,
        "filter_limit": limit,
        **get_period_params(period)
    }
    
    data = matomo_api("UserCountry.getCountry", params)
    
    countries = []
    for country in data[:limit] if isinstance(data, list) else []:
        countries.append({
            "country": country.get("label", ""),
            "visits": country.get("nb_visits", 0),
            "actions": country.get("nb_actions", 0),
        })
    
    return {"site": site, "period": period, "countries": countries}


@mcp.tool
def get_devices(site: str = "ronaldmego", period: str = "today") -> dict:
    """
    Get device types used by visitors.
    
    Args:
        site: Site name or ID
        period: Time period
    
    Returns:
        Breakdown by device type (desktop, mobile, tablet)
    """
    site_id = resolve_site_id(site)
    params = {"idSite": site_id, **get_period_params(period)}
    
    data = matomo_api("DevicesDetection.getType", params)
    
    devices = []
    for device in data if isinstance(data, list) else []:
        devices.append({
            "type": device.get("label", ""),
            "visits": device.get("nb_visits", 0),
            "percentage": device.get("nb_visits_percentage", 0),
        })
    
    return {"site": site, "period": period, "devices": devices}


@mcp.tool
def get_live_visitors(site: str = "ronaldmego", minutes: int = 30) -> dict:
    """
    Get live visitor information (last N minutes).
    
    Args:
        site: Site name or ID
        minutes: Minutes to look back (default 30)
    
    Returns:
        Live visitor count and recent visits
    """
    site_id = resolve_site_id(site)
    
    # Get counter
    counter = matomo_api("Live.getCounters", {
        "idSite": site_id,
        "lastMinutes": minutes
    })
    
    return {
        "site": site,
        "last_minutes": minutes,
        "visitors": counter[0].get("visitors", 0) if counter else 0,
        "visits": counter[0].get("visits", 0) if counter else 0,
        "actions": counter[0].get("actions", 0) if counter else 0,
    }


@mcp.tool
def get_search_keywords(site: str = "ronaldmego", period: str = "month", limit: int = 10) -> dict:
    """
    Get search keywords that brought visitors to the site.
    
    Args:
        site: Site name or ID
        period: Time period
        limit: Number of keywords to return
    
    Returns:
        List of search keywords with visit counts
    """
    site_id = resolve_site_id(site)
    params = {
        "idSite": site_id,
        "filter_limit": limit,
        **get_period_params(period)
    }
    
    data = matomo_api("Referrers.getKeywords", params)
    
    keywords = []
    for kw in data[:limit] if isinstance(data, list) else []:
        keywords.append({
            "keyword": kw.get("label", ""),
            "visits": kw.get("nb_visits", 0),
        })
    
    return {"site": site, "period": period, "keywords": keywords}


@mcp.tool
def compare_sites(period: str = "today") -> dict:
    """
    Compare all three sites side by side.
    
    Args:
        period: Time period to compare
    
    Returns:
        Comparison of visits, pageviews, etc. for all sites
    """
    sites_data = []
    
    for name, site_id in [("ronaldmego.com", 4), ("galacticaia.com", 5), ("be-cgi.com", 6)]:
        params = {"idSite": site_id, **get_period_params(period)}
        data = matomo_api("VisitsSummary.get", params)
        
        sites_data.append({
            "site": name,
            "unique_visitors": data.get("nb_uniq_visitors", 0),
            "visits": data.get("nb_visits", 0),
            "pageviews": data.get("nb_pageviews", 0),
            "bounce_rate": data.get("bounce_rate", "0%"),
        })
    
    return {"period": period, "comparison": sites_data}


@mcp.tool
def list_sites() -> list:
    """
    List all available sites being tracked.
    
    Returns:
        List of sites with their IDs and URLs
    """
    return [
        {"id": 4, "name": "ronaldmego.com", "aliases": ["ronaldmego", "personal"]},
        {"id": 5, "name": "galacticaia.com", "aliases": ["galacticaia", "galactica", "empresa"]},
        {"id": 6, "name": "be-cgi.com", "aliases": ["becgi", "be-cgi"]},
    ]


if __name__ == "__main__":
    mcp.run()
