#!/usr/bin/env python3
"""
TCampos Login Module
POST https://tcamp.qq.com/api/account/passwdLogin

This script handles password-based login and saves credentials + token to config file.
"""

import argparse
import json
import os
import sys
import requests
from typing import Optional, Tuple

# Default config file path (in the current working directory for security)
DEFAULT_CONFIG_FILE = os.path.join(os.getcwd(), '.tcampos-config')


def login(account: str, password: str) -> Tuple[bool, dict, str]:
    """
    Login to TCampos using account and password.
    
    Args:
        account: Phone number with country code (e.g., +8613800138000)
        password: Account password
        
    Returns:
        Tuple of (success: bool, response_data: dict, tipe_token: str)
    """
    url = "https://tcamp.qq.com/api/account/passwdLogin"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Origin': 'https://tcamp.qq.com',
        'Referer': 'https://tcamp.qq.com/'
    }
    
    payload = {
        "Account": account,
        "Passwd": password
    }
    
    session = requests.Session()
    
    response = session.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    # Check if login was successful
    success = response_data.get('Code') == 0
    
    # Extract tipe_token from cookies
    tipe_token = None
    for cookie in session.cookies:
        if cookie.name == 'tipe_token':
            tipe_token = cookie.value
            break
    
    # If not in cookies, check response body
    if not tipe_token and success:
        result = response_data.get('Response', {}).get('Result', {})
        tipe_token = result.get('Token') or result.get('tipe_token')
    
    return success, response_data, tipe_token


def save_config(account: str, passwd: str, tipe_token: str, config_file: str = None) -> None:
    """
    Save credentials and token to config file.
    
    Args:
        account: User account
        passwd: User password
        tipe_token: Authentication token
        config_file: Config file path (default: .tcampos-config in current working directory)
    """
    config_file = config_file or DEFAULT_CONFIG_FILE
    
    config_data = {
        'account': account,
        'passwd': passwd,
        'tipe_token': tipe_token
    }
    
    config_dir = os.path.dirname(config_file)
    if config_dir:
        os.makedirs(config_dir, exist_ok=True)
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    # Set file permissions to owner-only for security
    try:
        os.chmod(config_file, 0o600)
    except Exception:
        pass  # Ignore permission errors on some systems
    
    print(f"Config saved to: {config_file}")


def load_config(config_file: str = None) -> dict:
    """
    Load config from file.
    
    Args:
        config_file: Config file path (default: .tcampos-config in current working directory)
        
    Returns:
        Config dictionary
    """
    config_file = config_file or DEFAULT_CONFIG_FILE
    
    if not os.path.exists(config_file):
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def refresh_token(config_file: str = None) -> Tuple[bool, str]:
    """
    Refresh token using cached credentials.
    
    Args:
        config_file: Config file path
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    config = load_config(config_file)
    
    account = config.get('account')
    passwd = config.get('passwd')
    
    if not account or not passwd:
        return False, "No cached credentials found. Please login with --account and --password."
    
    print(f"Refreshing token for account: {account[:7]}****")
    
    success, response_data, tipe_token = login(account, passwd)
    
    if success and tipe_token:
        save_config(account, passwd, tipe_token, config_file)
        return True, "Token refreshed successfully!"
    else:
        error = response_data.get('Response', {}).get('Error', {})
        return False, f"Login failed: {error.get('Message', 'Unknown error')}"


def main():
    parser = argparse.ArgumentParser(description='Login to TCampos and save credentials')
    parser.add_argument('--account', '-a', default=None, help='Phone number with country code (e.g., +8613800138000)')
    parser.add_argument('--password', '-p', default=None, help='Account password')
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE, help='Config file path')
    parser.add_argument('--refresh', '-r', action='store_true', help='Refresh token using cached credentials')
    parser.add_argument('--raw', action='store_true', help='Output raw response JSON')
    
    args = parser.parse_args()
    
    # Refresh mode: use cached credentials
    if args.refresh:
        success, message = refresh_token(args.config)
        print(message)
        sys.exit(0 if success else 1)
    
    # Normal login mode
    if not args.account or not args.password:
        # Try to load from existing config
        config = load_config(args.config)
        if config.get('account') and config.get('passwd'):
            print("Using cached credentials...")
            args.account = config['account']
            args.password = config['passwd']
        else:
            print("Error: Please provide --account and --password, or use --refresh with existing config", file=sys.stderr)
            sys.exit(1)
    
    print(f"Logging in with account: {args.account[:7]}****")
    
    success, response_data, tipe_token = login(args.account, args.password)
    
    if args.raw:
        print("\n=== Response Data ===")
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
        print(f"\n=== tipe_token ===")
        print(tipe_token if tipe_token else "Not found")
        return
    
    if success:
        print("✅ Login successful!")
        
        if tipe_token:
            print(f"Token: {tipe_token[:50]}...")
            save_config(args.account, args.password, tipe_token, args.config)
        else:
            print("\n⚠️ Login succeeded but no tipe_token received")
            print("Response data:")
            print(json.dumps(response_data, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        print("❌ Login failed!")
        error = response_data.get('Response', {}).get('Error', {})
        if error:
            print(f"Error: {error.get('Code')} - {error.get('Message')}")
        else:
            print(f"Response: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
