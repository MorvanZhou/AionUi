#!/usr/bin/env python3
"""
List TCampos Camp Topics
POST https://tcampos.qq.com/api/camp/listCampTopic
"""

import argparse
import json
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def list_camp_topic(
    config_file: str = None,
    tipe_token: str = None,
    name: str = None,
    update_at_from: int = 0,
    update_at_to: int = 0,
    page_size: int = 20,
    page_num: int = 1,
    sort: list = None
) -> dict:
    """
    Query camp topic list.
    
    Args:
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        name: Topic name filter
        update_at_from: Filter by update time start (Unix timestamp)
        update_at_to: Filter by update time end (Unix timestamp)
        page_size: Results per page
        page_num: Page number
        sort: Sort options
        
    Returns:
        API response data
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    # Build request body
    request_data = {
        "Filter": {
            "Name": name or "",
            "UpdateAtFrom": update_at_from,
            "UpdateAtTo": update_at_to
        },
        "PageSize": page_size,
        "PageNum": page_num,
        "Sort": sort or []
    }
    
    return api.post("/camp/listCampTopic", request_data)


def format_topic_info(topic: dict, index: int) -> str:
    """Format single topic information for display."""
    lines = [f"\n{index}. {topic.get('Name', 'N/A')}"]
    lines.append(f"   ID: {topic.get('ID', 'N/A')}")
    
    if topic.get('Description'):
        desc = topic.get('Description', '')
        if len(desc) > 100:
            desc = desc[:100] + '...'
        lines.append(f"   Description: {desc}")
    
    if topic.get('CampCount') is not None:
        lines.append(f"   Camp Count: {topic.get('CampCount', 0)}")
    
    if topic.get('CreateAt'):
        lines.append(f"   Created At: {topic.get('CreateAt')}")
    
    if topic.get('UpdateAt'):
        lines.append(f"   Updated At: {topic.get('UpdateAt')}")
    
    if topic.get('CreatorName'):
        lines.append(f"   Creator: {topic.get('CreatorName')}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Query TCampos camp topic list')
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Path to config file')
    parser.add_argument('--tipe-token', default=None, help='tipe_token value (takes priority)')
    parser.add_argument('--name', default=None, help='Topic name filter')
    parser.add_argument('--update-from', type=int, default=0, help='Filter by update time start (Unix timestamp)')
    parser.add_argument('--update-to', type=int, default=0, help='Filter by update time end (Unix timestamp)')
    parser.add_argument('--page-size', type=int, default=20, help='Results per page')
    parser.add_argument('--page-num', type=int, default=1, help='Page number')
    parser.add_argument('--raw', action='store_true', help='Output raw JSON')
    
    args = parser.parse_args()
    
    try:
        result = list_camp_topic(
            config_file=args.config,
            tipe_token=args.tipe_token,
            name=args.name,
            update_at_from=args.update_from,
            update_at_to=args.update_to,
            page_size=args.page_size,
            page_num=args.page_num
        )
        
        if args.raw:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Check for API errors
            if result.get('Code') != 0:
                error = result.get('Response', {}).get('Error', {})
                print(f"API Error: {error.get('Code')} - {error.get('Message')}", file=sys.stderr)
                sys.exit(2)
            
            # Format output
            print("=" * 60)
            print("TCampos Camp Topic List Query Results")
            print("=" * 60)
            
            response_result = result.get('Response', {}).get('Result', {})
            total = response_result.get('Total', 0)
            topics = response_result.get('Entries', [])
            
            print(f"\nTotal: {total} topics")
            print(f"Page: {args.page_num} | Page Size: {args.page_size}")
            
            if topics:
                print(f"\nShowing {len(topics)} topics:")
                print("-" * 50)
                for i, topic in enumerate(topics, 1):
                    print(format_topic_info(topic, i))
            else:
                print("\nNo topics found matching the criteria.")
            
            print("\n" + "=" * 60)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please run login.py first to authenticate.", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Authentication Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Request Failed: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
