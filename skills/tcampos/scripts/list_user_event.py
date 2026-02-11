#!/usr/bin/env python3
"""
TCampos User Event Module
POST https://tcampos.qq.com/api/profile/listUserEvent

Query user's historical events including camps, matches, and custom events.
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


# Event type constants
EVENT_TYPES = {
    'camp': '营地',
    'match': '比赛',
    'custom': '自定义'
}


def list_user_events(
    uid: str,
    config_file: str = None,
    tipe_token: str = None,
    type_list: list = None,
    page_size: int = 20,
    page_num: int = 1,
    sort: list = None
) -> dict:
    """
    List user events (camps, matches, custom events).
    
    Args:
        uid: User ID (required)
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        type_list: Event types to filter, e.g. ['camp', 'match', 'custom']
        page_size: Page size (default 20, max 50)
        page_num: Page number (starts from 1)
        sort: Sort fields, e.g. ["-UpdateAt"]
        
    Returns:
        API response data
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    filter_data = {
        "TypeList": type_list or []
    }
    
    request_data = {
        "Uid": uid,
        "Filter": filter_data,
        "PageSize": min(page_size, 50),  # Max 50
        "PageNum": page_num,
        "Sort": sort or ["-CreateAt"]
    }
    
    return api.post("/profile/listUserEvent", request_data)


def format_timestamp(ts: int) -> str:
    """Format timestamp to readable date string."""
    if not ts:
        return "(未知)"
    try:
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)


def format_event_list(result: dict, uid: str) -> None:
    """Format and print user event list."""
    response = result.get('Response', {})
    data = response.get('Result', {})
    
    total = data.get('Total', 0)
    entries = data.get('Entries', [])
    
    print("=" * 70)
    print(f"TCampos User Events - UID: {uid}")
    print("=" * 70)
    print(f"\nTotal: {total} events")
    print(f"\nShowing {len(entries)} events:")
    print("-" * 60)
    
    for i, event in enumerate(entries, 1):
        event_type = event.get('Type', 'unknown')
        type_label = EVENT_TYPES.get(event_type, event_type)
        title = event.get('Title', '(无标题)')
        desc = event.get('Desc', '')
        create_at = event.get('CreateAt', 0)
        event_data = event.get('Data', {})
        
        print(f"\n{i}. [{type_label}] {title}")
        print(f"   时间: {format_timestamp(create_at)}")
        
        if desc:
            print(f"   描述: {desc}")
        
        # Display type-specific data
        if event_type == 'camp':
            camp_id = event_data.get('CampID')
            camp_slug = event_data.get('CampSlug')
            if camp_id:
                print(f"   营地 ID: {camp_id}")
            if camp_slug:
                print(f"   营地 Slug: {camp_slug}")
        elif event_type == 'match':
            match_id = event_data.get('MatchID')
            if match_id:
                print(f"   比赛 ID: {match_id}")
        
        # Show other data fields if present
        other_fields = {k: v for k, v in event_data.items() 
                       if k not in ['CampID', 'CampSlug', 'MatchID']}
        if other_fields:
            print(f"   其他数据: {json.dumps(other_fields, ensure_ascii=False)}")
    
    print("\n" + "=" * 70)
    
    # Summary by type
    if entries:
        type_counts = {}
        for event in entries:
            t = event.get('Type', 'unknown')
            type_counts[t] = type_counts.get(t, 0) + 1
        
        print("\n【事件类型统计】")
        for t, count in sorted(type_counts.items()):
            label = EVENT_TYPES.get(t, t)
            print(f"  {label}: {count} 条")


def main():
    parser = argparse.ArgumentParser(
        description='Query TCampos user events (camps, matches, custom)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all events for a user
  python list_user_event.py --uid 23892136

  # List only camp events
  python list_user_event.py --uid 23892136 --type camp

  # List camp and match events
  python list_user_event.py --uid 23892136 --type camp match

  # Pagination
  python list_user_event.py --uid 23892136 --page-size 50 --page-num 1

  # Output raw JSON
  python list_user_event.py --uid 23892136 --raw
"""
    )
    
    parser.add_argument('--uid', '-u', required=True,
                        help='User ID (required)')
    parser.add_argument('--type', '-t', nargs='+', default=[],
                        choices=['camp', 'match', 'custom'],
                        help='Event types to filter (camp/match/custom)')
    parser.add_argument('--page-size', type=int, default=20,
                        help='Page size (default 20, max 50)')
    parser.add_argument('--page-num', type=int, default=1,
                        help='Page number (default 1)')
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE,
                        help='Config file path')
    parser.add_argument('--raw', action='store_true',
                        help='Output raw JSON response')
    
    args = parser.parse_args()
    
    try:
        result = list_user_events(
            uid=args.uid,
            config_file=args.config,
            type_list=args.type if args.type else None,
            page_size=args.page_size,
            page_num=args.page_num
        )
        
        if args.raw:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            format_event_list(result, args.uid)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please run login.py first to authenticate.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
