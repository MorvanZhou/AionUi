#!/usr/bin/env python3
"""
List TCampos Camps
POST https://tcampos.qq.com/api/camp/listCamp
"""

import argparse
import json
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def list_camp(
    config_file: str = None,
    tipe_token: str = None,
    name: str = None,
    slug: str = None,
    slugs: list = None,
    topic_name: str = None,
    update_at_from: int = 0,
    update_at_to: int = 0,
    page_size: int = 20,
    page_num: int = 1,
    sort: list = None
) -> dict:
    """
    Query camp list.
    
    Args:
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        name: Camp name filter (fuzzy search)
        slug: Single camp slug for exact search (e.g., "NRp5lExN")
        slugs: List of camp slugs for exact search
        topic_name: Topic name filter (fuzzy search)
        update_at_from: Filter by update time start (Unix timestamp)
        update_at_to: Filter by update time end (Unix timestamp)
        page_size: Results per page
        page_num: Page number
        sort: Sort options
        
    Returns:
        API response data
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    # Build filter
    filter_data = {
        "Name": name or "",
        "UpdateAtFrom": update_at_from,
        "UpdateAtTo": update_at_to
    }
    
    # Add topic name filter if provided
    if topic_name:
        filter_data["TopicName"] = topic_name
    
    # Add slug filter if provided (for exact search)
    slug_list = []
    if slug:
        slug_list.append(slug)
    if slugs:
        slug_list.extend(slugs)
    if slug_list:
        filter_data["CampSlugList"] = slug_list
    
    # Build request body
    request_data = {
        "Filter": filter_data,
        "PageSize": page_size,
        "PageNum": page_num,
        "Sort": sort or []
    }
    
    return api.post("/camp/listCamp", request_data)


def format_camp_info(camp: dict, index: int) -> str:
    """Format single camp information for display."""
    lines = [f"\n{index}. {camp.get('Name', 'N/A')}"]
    lines.append(f"   ID: {camp.get('ID', 'N/A')} | Slug: {camp.get('Slug', 'N/A')}")
    lines.append(f"   Creator: {camp.get('CreatorName', 'N/A')}")
    lines.append(f"   Sign-ups: {camp.get('SignupNum', 0)} (Success: {camp.get('SignupSuccNum', 0)})")
    
    if camp.get('PlanName'):
        lines.append(f"   Plan: {camp.get('PlanName')}")
    
    if camp.get('Topics'):
        topics = ', '.join([t.get('Name', '') for t in camp.get('Topics', [])])
        if topics:
            lines.append(f"   Topics: {topics}")
    
    join_mode = "Direct" if camp.get('JoinMode') == 1 else "Approval Required"
    lines.append(f"   Join Mode: {join_mode}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Query TCampos camp list')
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Path to config file')
    parser.add_argument('--tipe-token', default=None, help='tipe_token value (takes priority)')
    parser.add_argument('--name', default=None, help='Camp name filter (fuzzy search)')
    parser.add_argument('--slug', default=None, help='Camp slug for exact search (e.g., NRp5lExN)')
    parser.add_argument('--slugs', nargs='+', default=None, help='Multiple camp slugs for exact search')
    parser.add_argument('--topic-name', default=None, help='Topic name filter (fuzzy search)')
    parser.add_argument('--update-from', type=int, default=0, help='Filter by update time start (Unix timestamp)')
    parser.add_argument('--update-to', type=int, default=0, help='Filter by update time end (Unix timestamp)')
    parser.add_argument('--page-size', type=int, default=20, help='Results per page')
    parser.add_argument('--page-num', type=int, default=1, help='Page number')
    parser.add_argument('--raw', action='store_true', help='Output raw JSON')
    
    args = parser.parse_args()
    
    try:
        result = list_camp(
            config_file=args.config,
            tipe_token=args.tipe_token,
            name=args.name,
            slug=args.slug,
            slugs=args.slugs,
            topic_name=args.topic_name,
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
            print("TCampos Camp List Query Results")
            print("=" * 60)
            
            response_result = result.get('Response', {}).get('Result', {})
            total = response_result.get('Total', 0)
            camps = response_result.get('Entries', [])
            
            print(f"\nTotal: {total} camps")
            print(f"Page: {args.page_num} | Page Size: {args.page_size}")
            
            if camps:
                print(f"\nShowing {len(camps)} camps:")
                print("-" * 50)
                for i, camp in enumerate(camps, 1):
                    print(format_camp_info(camp, i))
            else:
                print("\nNo camps found matching the criteria.")
            
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
