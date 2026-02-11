#!/usr/bin/env python3
"""
TCampos API Base Module
Provides common API request functionality with automatic authentication and token refresh.
"""

import json
import os
import warnings
from typing import Optional

# Suppress urllib3 SSL warnings (LibreSSL compatibility)
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

import requests

# Default config file path (in the current working directory for security)
DEFAULT_CONFIG_FILE = os.path.join(os.getcwd(), '.tcampos-config')


def _do_login(account: str, password: str) -> tuple:
    """
    Internal login function to avoid circular import.
    
    Args:
        account: Phone number with country code
        password: Account password
        
    Returns:
        Tuple of (success: bool, tipe_token: str or None)
    """
    url = "https://tcamp.qq.com/api/account/passwdLogin"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
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
    
    return success, tipe_token


class TCamposAPI:
    """TCampos API Client with automatic token refresh"""
    
    BASE_URL = "https://tcampos.qq.com/api"
    
    def __init__(self, config_file: str = None, tipe_token: str = None, auto_refresh: bool = True):
        """
        Initialize API client.
        
        Args:
            config_file: Path to config JSON file (default: .tcampos-config in current working directory)
            tipe_token: Direct tipe_token value (takes priority)
            auto_refresh: Whether to automatically refresh token on expiration
        """
        self.config_file = config_file or DEFAULT_CONFIG_FILE
        self.tipe_token = tipe_token
        self.auto_refresh = auto_refresh
        self.config = {}
        self.session = requests.Session()
        self._load_config()
    
    def _load_config(self) -> None:
        """Load config from file or use provided token."""
        # Priority 1: Direct tipe_token parameter
        if self.tipe_token:
            self.session.cookies.set('tipe_token', self.tipe_token, domain='tcampos.qq.com')
            return
        
        # Priority 2: Environment variable
        env_token = os.environ.get('TIPE_TOKEN')
        if env_token:
            self.session.cookies.set('tipe_token', env_token, domain='tcampos.qq.com')
            return
        
        # Priority 3: Config file
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(
                f"Config file not found: {self.config_file}\n"
                "Please run login.py first to authenticate."
            )
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        token = self.config.get('tipe_token')
        
        # If no token but have credentials, try to login automatically
        if not token:
            account = self.config.get('account')
            passwd = self.config.get('passwd')
            
            if account and passwd:
                print(f"🔑 No token found. Auto-logging in with account: {account[:7]}****")
                if self._refresh_token():
                    return
            
            raise ValueError(
                "No tipe_token found in config file and auto-login failed.\n"
                "Please run login.py to authenticate."
            )
        
        self.session.cookies.set('tipe_token', token, domain='tcampos.qq.com')
    
    def _get_headers(self) -> dict:
        """Get request headers."""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Origin': 'https://tcampos.qq.com',
            'Referer': 'https://tcampos.qq.com/'
        }
    
    def _refresh_token(self) -> bool:
        """
        Refresh token using cached credentials.
        
        Returns:
            True if token refresh was successful
        """
        # Always reload config to get the latest credentials
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        
        account = self.config.get('account')
        passwd = self.config.get('passwd')
        
        if not account or not passwd:
            print("⚠️ No cached credentials found. Cannot auto-refresh token.")
            return False
        
        print(f"🔄 Token expired. Refreshing with account: {account[:7]}****")
        
        success, new_token = _do_login(account, passwd)
        
        if success and new_token:
            # Update config with new token
            self.config['tipe_token'] = new_token
            
            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            # Update session cookie
            self.session.cookies.set('tipe_token', new_token, domain='tcampos.qq.com')
            
            print("✅ Token refreshed successfully!")
            return True
        else:
            print("❌ Token refresh failed. Please re-login manually.")
            return False
    
    def _is_token_expired(self, response_data: dict) -> bool:
        """Check if API response indicates token expiration."""
        if response_data.get('Code') == 1:
            error = response_data.get('Response', {}).get('Error', {})
            error_code = error.get('Code', '')
            if error_code in ['InvalidJWTClaims', 'TokenExpired', 'Unauthorized']:
                return True
        return False
    
    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None, retry_on_auth_fail: bool = True) -> dict:
        """
        Internal request method with automatic token refresh.
        
        Args:
            method: HTTP method ('GET' or 'POST')
            endpoint: API endpoint path
            data: Request body data (for POST)
            params: Query parameters (for GET)
            retry_on_auth_fail: Whether to retry after refreshing token
            
        Returns:
            API response data
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        if method == 'POST':
            response = self.session.post(url, json=data, headers=self._get_headers())
        else:
            response = self.session.get(url, params=params, headers=self._get_headers())
        
        # Check for HTTP-level authentication errors
        if response.status_code in [401, 403]:
            if self.auto_refresh and retry_on_auth_fail:
                if self._refresh_token():
                    return self._request(method, endpoint, data, params, retry_on_auth_fail=False)
            raise PermissionError(
                f"API authentication failed (HTTP {response.status_code}). Please re-login."
            )
        
        response.raise_for_status()
        result = response.json()
        
        # Check for token expiration in response body
        if self._is_token_expired(result):
            if self.auto_refresh and retry_on_auth_fail:
                if self._refresh_token():
                    return self._request(method, endpoint, data, params, retry_on_auth_fail=False)
            raise PermissionError(
                "Token expired. Please re-login."
            )
        
        return result
    
    def post(self, endpoint: str, data: dict) -> dict:
        """
        Send POST request with automatic token refresh.
        
        Args:
            endpoint: API endpoint path (e.g., /camp/listCamp)
            data: Request body data
            
        Returns:
            API response data
        """
        return self._request('POST', endpoint, data=data)
    
    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Send GET request with automatic token refresh.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            API response data
        """
        return self._request('GET', endpoint, params=params)


def get_api_client(config_file: str = None, tipe_token: str = None, auto_refresh: bool = True) -> TCamposAPI:
    """
    Get API client instance.
    
    Args:
        config_file: Path to config file (default: .tcampos-config in current working directory)
        tipe_token: Direct tipe_token value (takes priority)
        auto_refresh: Whether to automatically refresh token on expiration
        
    Returns:
        TCamposAPI client instance
        
    Raises:
        FileNotFoundError: If config file is missing (AI should ask user for credentials)
        ValueError: If config file exists but has no token (AI should ask user for credentials)
    """
    config_file = config_file or DEFAULT_CONFIG_FILE
    return TCamposAPI(config_file=config_file, tipe_token=tipe_token, auto_refresh=auto_refresh)
