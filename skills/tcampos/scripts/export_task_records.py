#!/usr/bin/env python3
"""
TCampos Export Task Records
POST /api/task/exportUserTaskRecords - Export user task records to Excel
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def export_task_records(
    task_id: int,
    op_status: list = None,
    mode: int = 1,
    config_file: str = None,
    tipe_token: str = None
) -> dict:
    """
    Export user task records to Excel.
    
    Args:
        task_id: Task ID
        op_status: Filter by operation status (e.g., [1, 2, 3])
        mode: Export mode (default: 1)
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        
    Returns:
        API response with SheetURL and Total
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "TaskID": task_id,
        "OpStatus": op_status or [],
        "Mode": mode
    }
    
    return api.post("/task/exportUserTaskRecords", request_data)


def download_file(url: str, output_path: str, tipe_token: str = None) -> str:
    """
    Download file from URL with authentication.
    
    Args:
        url: File URL to download
        output_path: Local path to save file
        tipe_token: Authentication token
        
    Returns:
        Path to downloaded file
    """
    # Parse and properly encode the URL
    parsed = urllib.parse.urlparse(url)
    # Encode the path component (preserve slashes)
    encoded_path = urllib.parse.quote(parsed.path, safe='/')
    encoded_url = urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, encoded_path,
        parsed.params, parsed.query, parsed.fragment
    ))
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    if tipe_token:
        headers['Cookie'] = f'tipe_token={tipe_token}'
    
    request = urllib.request.Request(encoded_url, headers=headers)
    
    with urllib.request.urlopen(request) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='TCampos Export Task Records - Export user task records to Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export task records (default output to ./downloads/)
  python3 export_task_records.py --task-id 3406

  # Export to specific directory
  python3 export_task_records.py --task-id 3406 --output /custom/path/

  # Filter by operation status
  python3 export_task_records.py --task-id 3406 --status 2  # Only passed
  python3 export_task_records.py --task-id 3406 --status 1 --status 2  # Pending and passed

  # Only get URL without downloading
  python3 export_task_records.py --task-id 3406 --no-download

  # Output raw JSON
  python3 export_task_records.py --task-id 3406 --raw

Operation Status:
  1 - 待审核/进行中
  2 - 已通过/已完成
  3 - 已拒绝/未通过
        """
    )
    
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Path to config file')
    parser.add_argument('--tipe-token', default=None, help='tipe_token value (takes priority)')
    parser.add_argument('--task-id', type=int, required=True, help='Task ID')
    parser.add_argument('--status', type=int, action='append', dest='op_status',
                        help='Filter by operation status (can specify multiple)')
    parser.add_argument('--mode', type=int, default=1, help='Export mode (default: 1)')
    parser.add_argument('--output', '-o', default='./downloads', help='Output directory for downloaded file (default: ./downloads)')
    parser.add_argument('--no-download', action='store_true', help='Only get URL, do not download')
    parser.add_argument('--raw', action='store_true', help='Output raw JSON')
    
    args = parser.parse_args()
    
    try:
        # Load config for token
        config_file = args.config
        tipe_token = args.tipe_token
        
        if not tipe_token and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                tipe_token = config.get('tipe_token')
        
        print("=" * 60)
        print(f"TCampos Export Task Records - Task ID: {args.task_id}")
        print("=" * 60)
        
        # Call export API
        result = export_task_records(
            task_id=args.task_id,
            op_status=args.op_status,
            mode=args.mode,
            config_file=config_file,
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
        sheet_url = response_result.get('SheetURL')
        total = response_result.get('Total', 0)
        
        print(f"\n📊 任务记录总数: {total} 条")
        
        if args.op_status:
            status_names = {1: '待审核', 2: '已通过', 3: '已拒绝'}
            status_str = ', '.join(status_names.get(s, str(s)) for s in args.op_status)
            print(f"🔍 筛选条件: 状态={status_str}")
        
        if sheet_url:
            print(f"\n📄 文件URL: {sheet_url}")
            
            if not args.no_download:
                # Extract filename from URL
                filename = sheet_url.split('/')[-1]
                # URL decode filename
                filename = urllib.parse.unquote(filename)
                output_path = os.path.join(args.output, filename)
                
                # Create output directory if needed
                os.makedirs(args.output, exist_ok=True)
                
                print(f"⬇️ 下载中...")
                download_file(sheet_url, output_path, tipe_token)
                print(f"✅ 已保存: {output_path}")
        else:
            print("\n⚠️ 无数据或暂无导出文件")
        
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
