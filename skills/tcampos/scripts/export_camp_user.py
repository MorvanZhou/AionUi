#!/usr/bin/env python3
"""
TCampos Export Camp Users
POST /api/camp/exportCampUser - Export camp user list to Excel
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


def export_camp_user(
    camp_id: int,
    config_file: str = None,
    tipe_token: str = None,
    mode: int = 1
) -> dict:
    """
    Export camp user list to Excel.
    
    Args:
        camp_id: Camp ID
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        mode: Export mode (default: 1)
        
    Returns:
        API response with SheetURL and Total
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "CampID": camp_id,
        "Mode": mode
    }
    
    return api.post("/camp/exportCampUser", request_data)


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
        description='TCampos Export Camp Users - Export camp user list to Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export camp users (default output to ./downloads/)
  python3 export_camp_user.py --camp-id 11103

  # Export to specific directory
  python3 export_camp_user.py --camp-id 11103 --output /custom/path/

  # Only get URL without downloading
  python3 export_camp_user.py --camp-id 11103 --no-download

  # Output raw JSON
  python3 export_camp_user.py --camp-id 11103 --raw
        """
    )
    
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Path to config file')
    parser.add_argument('--tipe-token', default=None, help='tipe_token value (takes priority)')
    parser.add_argument('--camp-id', type=int, required=True, help='Camp ID')
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
        print(f"TCampos Export Camp Users - Camp ID: {args.camp_id}")
        print("=" * 60)
        
        # Call export API
        result = export_camp_user(
            camp_id=args.camp_id,
            config_file=config_file,
            tipe_token=args.tipe_token,
            mode=args.mode
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
        
        print(f"\n📊 营地用户总数: {total} 人")
        
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
