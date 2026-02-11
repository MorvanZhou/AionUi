#!/usr/bin/env python3
"""
TCampos List Camp Tasks
POST /api/task/listCampTask - Query tasks in a camp
"""

import argparse
import json
import os
import sys

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def list_camp_task(
    camp_id: int,
    name: str = "",
    type_list: list = None,
    page_size: int = 100,
    page_num: int = 1,
    config_file: str = None,
    tipe_token: str = None
) -> dict:
    """
    List tasks in a camp.
    
    Args:
        camp_id: Camp ID
        name: Filter by task name (fuzzy match)
        type_list: Filter by task types (e.g., ['homework', 'article'])
        page_size: Number of results per page (default: 100)
        page_num: Page number (default: 1)
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        
    Returns:
        API response with task list
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "CampID": camp_id,
        "Filter": {
            "Name": name or "",
            "TypeList": type_list or []
        },
        "PageSize": page_size,
        "PageNum": page_num,
        "Sort": []
    }
    
    return api.post("/task/listCampTask", request_data)


def main():
    parser = argparse.ArgumentParser(
        description='TCampos List Camp Tasks - Query tasks in a camp',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all tasks in a camp
  python3 list_camp_task.py --camp-id 11103

  # Filter by task name
  python3 list_camp_task.py --camp-id 11103 --name "入营"

  # Filter by task type
  python3 list_camp_task.py --camp-id 11103 --type homework
  python3 list_camp_task.py --camp-id 11103 --type article

  # Output raw JSON
  python3 list_camp_task.py --camp-id 11103 --raw

Task Types:
  - homework: 作业任务
  - article: 文章/阅读任务
  - video: 视频任务
  - exam: 考试任务
        """
    )
    
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Path to config file')
    parser.add_argument('--tipe-token', default=None, help='tipe_token value (takes priority)')
    parser.add_argument('--camp-id', type=int, required=True, help='Camp ID')
    parser.add_argument('--name', '-n', default='', help='Filter by task name (fuzzy match)')
    parser.add_argument('--type', '-t', dest='task_type', action='append', 
                        help='Filter by task type (can specify multiple: --type homework --type article)')
    parser.add_argument('--page-size', type=int, default=100, help='Page size (default: 100)')
    parser.add_argument('--page-num', type=int, default=1, help='Page number (default: 1)')
    parser.add_argument('--raw', action='store_true', help='Output raw JSON')
    
    args = parser.parse_args()
    
    try:
        result = list_camp_task(
            camp_id=args.camp_id,
            name=args.name,
            type_list=args.task_type,
            page_size=args.page_size,
            page_num=args.page_num,
            config_file=args.config,
            tipe_token=args.tipe_token
        )
        
        if args.raw:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        
        if result.get('Code') != 0:
            error = result.get('Response', {}).get('Error', {})
            print(f"API Error: {error.get('Code')} - {error.get('Message')}", file=sys.stderr)
            sys.exit(2)
        
        response_result = result.get('Response', {}).get('Result', {})
        entries = response_result.get('Entries', []) or []
        total = response_result.get('Total', 0)
        
        print("=" * 80)
        print(f"TCampos Camp Tasks - Camp ID: {args.camp_id}")
        print("=" * 80)
        print(f"\n📋 任务总数: {total}")
        
        if not entries:
            print("\n⚠️ 暂无任务数据")
        else:
            print("\n" + "-" * 80)
            # Header
            print(f"{'ID':<8} {'类型':<10} {'必修':<6} {'任务名称':<35} {'完成率':>8}")
            print("-" * 80)
            
            for task in entries:
                task_id = task.get('ID', '')
                name = task.get('Name', '')[:35]
                task_type = task.get('Type', '')
                required = '✓ 必修' if task.get('Required') else '○ 选修'
                
                progress = task.get('Progress', {})
                total_done_ratio = progress.get('TotalDoneRatio', 0)
                done = progress.get('Done', 0)
                task_total = progress.get('Total', 0)
                
                # Format progress
                progress_str = f"{total_done_ratio*100:.1f}% ({done}/{task_total})"
                
                print(f"{task_id:<8} {task_type:<10} {required:<6} {name:<35} {progress_str:>15}")
            
            print("-" * 80)
            
            # Summary
            print("\n📊 任务进度统计:")
            required_tasks = [t for t in entries if t.get('Required')]
            optional_tasks = [t for t in entries if not t.get('Required')]
            
            if required_tasks:
                avg_required = sum(t.get('Progress', {}).get('TotalDoneRatio', 0) for t in required_tasks) / len(required_tasks)
                print(f"  必修任务: {len(required_tasks)} 个, 平均完成率: {avg_required*100:.1f}%")
            
            if optional_tasks:
                avg_optional = sum(t.get('Progress', {}).get('TotalDoneRatio', 0) for t in optional_tasks) / len(optional_tasks)
                print(f"  选修任务: {len(optional_tasks)} 个, 平均完成率: {avg_optional*100:.1f}%")
        
        print("\n" + "=" * 80)
        
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
