#!/usr/bin/env python3
"""Test Matomo API connection directly."""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

MATOMO_URL = os.getenv("MATOMO_URL")
MATOMO_TOKEN = os.getenv("MATOMO_TOKEN")

def test_api():
    """Test basic API call."""
    params = {
        "module": "API",
        "method": "VisitsSummary.get",
        "idSite": 5,  # galacticaia
        "period": "day",
        "date": "today",
        "format": "JSON",
        "token_auth": MATOMO_TOKEN,
    }
    
    print(f"Testing Matomo API: {MATOMO_URL}")
    # Try POST instead of GET (some Matomo configs require it)
    response = requests.post(f"{MATOMO_URL}/index.php", data=params)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_api()
