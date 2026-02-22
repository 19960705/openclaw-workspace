#!/usr/bin/env python3
"""
EvoMap Memory Bridge Capsule - Cross-session memory continuity
Based on: sha256:def136049c982ed785117dff00bb3238ed71d11cf77c019b3db2a8f65b476f06

Auto-load RECENT_EVENTS.md (24h rolling) + daily memory/YYYY-MM-DD.md + MEMORY.md on session startup
Auto-append significant events before exit
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
RECENT_EVENTS = os.path.join(WORKSPACE, "RECENT_EVENTS.md")
MEMORY_FILE = os.path.join(WORKSPACE, "MEMORY.md")


def load_memory_on_startup():
    """Load all memory files on session startup."""
    memory = {
        "recent_events": [],
        "daily_memories": [],
        "long_term": ""
    }
    
    # 1. Load RECENT_EVENTS.md (24h rolling)
    if os.path.exists(RECENT_EVENTS):
        with open(RECENT_EVENTS, 'r', encoding='utf-8') as f:
            memory["recent_events"] = f.read()
    
    # 2. Load today's and yesterday's daily memory
    today = datetime.now()
    for i in range(2):  # Today and yesterday
        date = today - timedelta(days=i)
        daily_file = os.path.join(MEMORY_DIR, f"{date.strftime('%Y-%m-%d')}.md")
        if os.path.exists(daily_file):
            with open(daily_file, 'r', encoding='utf-8') as f:
                memory["daily_memories"].append({
                    "date": date.strftime('%Y-%m-%d'),
                    "content": f.read()
                })
    
    # 3. Load long-term MEMORY.md
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            memory["long_term"] = f.read()
    
    return memory


def save_event(event: str, metadata: dict = None):
    """Save significant event to memory files."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    event_entry = f"## {timestamp}\n{event}\n"
    
    if metadata:
        event_entry += f"\n**Metadata:** {json.dumps(metadata, ensure_ascii=False)}\n"
    
    # Append to today's daily memory
    today_file = os.path.join(MEMORY_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.md")
    
    # Create directory if not exists
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    with open(today_file, 'a', encoding='utf-8') as f:
        f.write(event_entry + "\n")
    
    # Also append to RECENT_EVENTS.md
    with open(RECENT_EVENTS, 'a', encoding='utf-8') as f:
        f.write(event_entry + "\n")
    
    # Cleanup old events (older than 24h)
    cleanup_recent_events()
    
    return True


def cleanup_recent_events():
    """Remove events older than 24h from RECENT_EVENTS.md"""
    if not os.path.exists(RECENT_EVENTS):
        return
    
    with open(RECENT_EVENTS, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Keep only events from last 24h
    cutoff = datetime.now() - timedelta(hours=24)
    kept_lines = []
    
    for line in lines:
        # Try to extract date from "## YYYY-MM-DD HH:MM" pattern
        if line.startswith('## '):
            try:
                date_str = line[3:].strip()
                event_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                if event_time >= cutoff:
                    kept_lines.append(line)
                else:
                    continue
            except:
                kept_lines.append(line)
        else:
            kept_lines.append(line)
    
    with open(RECENT_EVENTS, 'w', encoding='utf-8') as f:
        f.writelines(kept_lines)


def append_to_long_term(content: str):
    """Append content to long-term memory."""
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{content}\n")


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python memory_bridge.py load     - Load all memory on startup")
        print("  python memory_bridge.py save    - Save event (use stdin)")
        print("  python memory_bridge.py cleanup - Clean old events")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "load":
        memory = load_memory_on_startup()
        print(f"Loaded:")
        print(f"  - Recent events: {len(memory['recent_events'])} chars")
        print(f"  - Daily memories: {len(memory['daily_memories'])} files")
        print(f"  - Long-term: {len(memory['long_term'])} chars")
        
    elif command == "save":
        event = sys.stdin.read().strip()
        if event:
            save_event(event)
            print("Event saved!")
        else:
            print("No event to save")
            
    elif command == "cleanup":
        cleanup_recent_events()
        print("Cleanup done!")
