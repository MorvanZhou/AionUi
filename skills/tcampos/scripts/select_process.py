#!/usr/bin/env python3
"""
TCampos Camp Selection Process & Data Export
- GET /api/camp/:camp_id/selectProcess - Get selection process
- POST /api/camp/exportSignupRecords - Export signup records
- POST /api/exam/exportUserExamRecords - Export exam records  
- POST /api/interview/exportUserInterviewRecords - Export interview records
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def get_select_process(
    camp_id: int,
    config_file: str = None,
    tipe_token: str = None
) -> dict:
    """
    Get camp selection process.
    
    Args:
        camp_id: Camp ID
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        
    Returns:
        API response data with selection process info
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    return api.get(f"/camp/{camp_id}/selectProcess")


def export_signup_records(
    camp_id: int,
    config_file: str = None,
    tipe_token: str = None,
    mode: int = 1,
    op_status_list: list = None,
    channel_list: list = None,
    batch_list: list = None
) -> dict:
    """
    Export signup records to Excel.
    
    Args:
        camp_id: Camp ID
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        mode: Export mode (default: 1)
        op_status_list: Filter by operation status
        channel_list: Filter by channel
        batch_list: Filter by batch
        
    Returns:
        API response with SheetURL
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "Mode": mode,
        "CampID": camp_id,
        "OpStatusList": op_status_list or [],
        "ChannelList": channel_list or [],
        "BatchList": batch_list or []
    }
    
    return api.post("/camp/exportSignupRecords", request_data)


def export_exam_records(
    camp_id: int,
    config_file: str = None,
    tipe_token: str = None,
    op_status: list = None,
    to_sheet: bool = True
) -> dict:
    """
    Export exam/test records to Excel.
    
    Args:
        camp_id: Camp ID
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        op_status: Filter by operation status
        to_sheet: Whether to export as Excel (default: True)
        
    Returns:
        API response with SheetURL
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "CampID": camp_id,
        "OpStatus": op_status or [],
        "ToSheet": to_sheet
    }
    
    return api.post("/exam/exportUserExamRecords", request_data)


def export_interview_records(
    camp_id: int,
    config_file: str = None,
    tipe_token: str = None,
    mode: int = 1,
    op_status: list = None
) -> dict:
    """
    Export interview records to Excel.
    
    Args:
        camp_id: Camp ID
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        mode: Export mode (default: 1)
        op_status: Filter by operation status
        
    Returns:
        API response with SheetURL
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "Mode": mode,
        "CampID": camp_id,
        "OpStatus": op_status or []
    }
    
    return api.post("/interview/exportUserInterviewRecords", request_data)


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
    from urllib.parse import urlparse, quote, urlunparse
    parsed = urlparse(url)
    # Encode the path component (preserve slashes)
    encoded_path = quote(parsed.path, safe='/')
    encoded_url = urlunparse((
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


def format_process_info(process_data: dict) -> str:
    """Format selection process information for display."""
    lines = []
    
    join_mode = process_data.get('CampJoinMode', 0)
    join_mode_text = {1: "直接加入", 2: "需要审核", 3: "筛选流程"}.get(join_mode, f"未知({join_mode})")
    lines.append(f"参与方式: {join_mode_text}")
    
    # Summary
    summary = process_data.get('Summary', {})
    lines.append(f"\n📊 数据汇总:")
    lines.append(f"   总报名数: {summary.get('SignupNumTotal', 0)}")
    lines.append(f"   最终通过: {summary.get('UserNumPassed', 0)}")
    
    # Items (selection stages)
    items = process_data.get('Items', [])
    if items:
        lines.append(f"\n📋 筛选环节 ({len(items)} 个):")
        lines.append("-" * 40)
        
        state_map = {0: "未开始", 1: "进行中", 2: "已结束"}
        type_map = {1: "报名", 2: "笔试", 3: "面试", 4: "录取"}
        
        for i, item in enumerate(items, 1):
            state = state_map.get(item.get('State', 0), "未知")
            item_type_val = item.get('Type')
            item_type = type_map.get(item_type_val, f"类型{item_type_val}") if item_type_val is not None else ""
            
            type_suffix = f" [{item_type}]" if item_type else ""
            lines.append(f"\n  {i}. {item.get('Name', 'N/A')}{type_suffix}")
            lines.append(f"     状态: {state}")
            
            if item.get('StartAt'):
                from datetime import datetime
                start = datetime.fromtimestamp(item['StartAt']).strftime('%Y-%m-%d %H:%M')
                end = datetime.fromtimestamp(item.get('EndAt', 0)).strftime('%Y-%m-%d %H:%M')
                lines.append(f"     时间: {start} ~ {end}")
            
            if item.get('UserNumPassed', 0) > 0 or item.get('UserNumTotal', 0) > 0:
                lines.append(f"     通过人数: {item.get('UserNumPassed', 0)}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='TCampos Camp Selection Process & Data Export',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get selection process info
  python3 select_process.py --camp-id 11264

  # Export signup records (default output to ./downloads/)
  python3 select_process.py --camp-id 11264 --export signup

  # Export exam records
  python3 select_process.py --camp-id 11264 --export exam

  # Export interview records
  python3 select_process.py --camp-id 11264 --export interview

  # Export all records
  python3 select_process.py --camp-id 11264 --export all

  # Export and download to specific directory
  python3 select_process.py --camp-id 11264 --export signup --output /custom/path/
        """
    )
    
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Path to config file')
    parser.add_argument('--tipe-token', default=None, help='tipe_token value (takes priority)')
    parser.add_argument('--camp-id', type=int, required=True, help='Camp ID')
    parser.add_argument('--export', choices=['signup', 'exam', 'interview', 'all'], 
                        help='Export type: signup, exam, interview, or all')
    parser.add_argument('--output', '-o', default='./downloads', help='Output directory for downloaded files (default: ./downloads)')
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
        
        # Get selection process first
        print("=" * 60)
        print(f"TCampos Camp Selection Process - Camp ID: {args.camp_id}")
        print("=" * 60)
        
        process_result = get_select_process(
            camp_id=args.camp_id,
            config_file=config_file,
            tipe_token=args.tipe_token
        )
        
        if args.raw and not args.export:
            print(json.dumps(process_result, ensure_ascii=False, indent=2))
            return
        
        if process_result.get('Code') != 0:
            error = process_result.get('Response', {}).get('Error', {})
            print(f"API Error: {error.get('Code')} - {error.get('Message')}", file=sys.stderr)
            sys.exit(2)
        
        process_data = process_result.get('Response', {}).get('Result', {})
        print(format_process_info(process_data))
        
        # Export data if requested
        if args.export:
            print("\n" + "=" * 60)
            print("📥 数据导出")
            print("=" * 60)
            
            export_types = [args.export] if args.export != 'all' else ['signup', 'exam', 'interview']
            
            for export_type in export_types:
                print(f"\n▶ 导出 {export_type} 数据...")
                
                try:
                    if export_type == 'signup':
                        result = export_signup_records(
                            camp_id=args.camp_id,
                            config_file=config_file,
                            tipe_token=args.tipe_token
                        )
                    elif export_type == 'exam':
                        result = export_exam_records(
                            camp_id=args.camp_id,
                            config_file=config_file,
                            tipe_token=args.tipe_token
                        )
                    elif export_type == 'interview':
                        result = export_interview_records(
                            camp_id=args.camp_id,
                            config_file=config_file,
                            tipe_token=args.tipe_token
                        )
                    
                    if args.raw:
                        print(json.dumps(result, ensure_ascii=False, indent=2))
                        continue
                    
                    if result.get('Code') != 0:
                        error = result.get('Response', {}).get('Error', {})
                        print(f"  ⚠️ 导出失败: {error.get('Message', 'Unknown error')}")
                        continue
                    
                    sheet_url = result.get('Response', {}).get('Result', {}).get('SheetURL')
                    
                    if sheet_url:
                        print(f"  📄 文件URL: {sheet_url}")
                        
                        if not args.no_download:
                            # Extract filename from URL
                            filename = sheet_url.split('/')[-1]
                            # URL decode filename
                            filename = urllib.parse.unquote(filename)
                            output_path = os.path.join(args.output, filename)
                            
                            # Create output directory if needed
                            os.makedirs(args.output, exist_ok=True)
                            
                            print(f"  ⬇️ 下载中...")
                            download_file(sheet_url, output_path, tipe_token)
                            print(f"  ✅ 已保存: {output_path}")
                    else:
                        print(f"  ⚠️ 无数据或暂无导出文件")
                        
                except Exception as e:
                    print(f"  ❌ 导出失败: {e}")
        
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
