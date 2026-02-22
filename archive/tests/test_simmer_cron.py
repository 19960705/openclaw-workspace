#!/usr/bin/env python3
"""Test script for simmer cron - just the API part"""

import sys
import os

# Load API key the same way as simmer-check.py
env_file = os.path.expanduser("~/.openclaw/workspace/.env.simmer")
api_key = None
venue = "polymarket"

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith("SIMMER_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
            elif line.startswith("SIMMER_VENUE="):
                venue = line.strip().split("=", 1)[1]

print(f"API key loaded: {api_key[:20]}...")
print(f"Venue: {venue}")

if not api_key:
    print("ERROR: No SIMMER_API_KEY found")
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.simmer-venv/lib/python3.14/site-packages"))
from simmer_sdk.client import SimmerClient

print("Creating client...")
client = SimmerClient(api_key=api_key, venue=venue)

print("Fetching markets...")
markets = client.get_markets(limit=10)

print(f"Success! Got {len(markets)} markets")
for m in markets[:3]:
    q = getattr(m, 'question', '')
    print(f"  - {q[:60]}")
