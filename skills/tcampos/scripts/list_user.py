#!/usr/bin/env python3
"""
TCampos User Profile Module
- List users: POST https://tcampos.qq.com/api/profile/listUser
- Get user detail: GET https://tcampos.qq.com/api/profile/user/:uid
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def list_users(
    config_file: str = None,
    tipe_token: str = None,
    name_or_uid: str = "",
    name: str = "",
    uid: str = "",
    uid_list: list = None,
    phone: str = "",
    email: str = "",
    organization: str = "",
    gender_list: list = None,
    in_camp_list: list = None,
    birthday_from: int = 0,
    birthday_to: int = 0,
    page_size: int = 20,
    page_num: int = 1,
    sort: list = None
) -> dict:
    """
    List users with filters.
    
    Args:
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        name_or_uid: Fuzzy match Name OR Uid
        name: Fuzzy match Name
        uid: Exact match Uid
        uid_list: List of uids to match
        phone: Exact match phone number
        email: Exact match email
        organization: Fuzzy match organization/school
        gender_list: Filter by gender (1=male, 2=female)
        in_camp_list: Filter by camp IDs user participated in
        birthday_from: Birthday start timestamp
        birthday_to: Birthday end timestamp
        page_size: Page size (default 20, max 50)
        page_num: Page number (starts from 1)
        sort: Sort fields, e.g. ["-UpdateAt"]
        
    Returns:
        API response data
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    filter_data = {
        "NameOrUid": name_or_uid,
        "Name": name,
        "Uid": uid,
        "UidList": uid_list or [],
        "ArenaUid": "",
        "Phone": phone,
        "BirthdayFrom": birthday_from,
        "BirthdayTo": birthday_to,
        "GenderList": gender_list or [],
        "InCampList": in_camp_list or [],
        "Email": email,
        "Organization": organization
    }
    
    request_data = {
        "Filter": filter_data,
        "PageSize": min(page_size, 50),  # Max 50
        "PageNum": page_num,
        "Sort": sort or ["-UpdateAt"]
    }
    
    return api.post("/profile/listUser", request_data)


def get_user_detail(
    uid: str,
    config_file: str = None,
    tipe_token: str = None
) -> dict:
    """
    Get user profile detail by uid.
    
    Args:
        uid: User ID
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        
    Returns:
        API response data
    """
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    return api.get(f"/profile/user/{uid}")


def format_gender(gender: int) -> str:
    """Format gender code to string."""
    gender_map = {0: "未知", 1: "男", 2: "女"}
    return gender_map.get(gender, "未知")


def format_user_list(result: dict) -> None:
    """Format and print user list."""
    response = result.get('Response', {})
    data = response.get('Result', {})
    
    total = data.get('Total', 0)
    entries = data.get('Entries', [])
    
    print("=" * 60)
    print("TCampos User List Query Results")
    print("=" * 60)
    print(f"\nTotal: {total} users")
    print(f"\nShowing {len(entries)} users:")
    print("-" * 50)
    
    for i, user in enumerate(entries, 1):
        uid = user.get('Uid', 'N/A')
        name = user.get('Name', '') or '(未填写)'
        gender = format_gender(user.get('Gender', 0))
        phone = user.get('Phone', '') or '(未填写)'
        birthday = user.get('Birthday', '')
        email = user.get('Email', '')
        organization = user.get('Organization', '')
        
        print(f"\n{i}. {name}")
        print(f"   UID: {uid}")
        print(f"   性别: {gender} | 手机: {phone}")
        if birthday:
            # Format YYYYMMDD to YYYY-MM-DD
            if len(birthday) == 8:
                birthday = f"{birthday[:4]}-{birthday[4:6]}-{birthday[6:8]}"
            print(f"   生日: {birthday}")
        if email:
            print(f"   邮箱: {email}")
        if organization:
            print(f"   学校/组织: {organization}")
    
    print("\n" + "=" * 60)


def format_user_detail(result: dict) -> None:
    """Format and print user detail."""
    response = result.get('Response', {})
    data = response.get('Result', {})
    
    account_info = data.get('AccountInfo', {})
    basic_info = data.get('BasicInfo', {})
    camp_records = data.get('CampRecords')
    
    print("=" * 60)
    print("TCampos User Profile Detail")
    print("=" * 60)
    
    # Account Info
    print("\n【账号信息】")
    print(f"  UID: {account_info.get('Uid', 'N/A')}")
    print(f"  创想家 UID: {account_info.get('ArenaUid', '') or '(无)'}")
    print(f"  注册渠道: {account_info.get('Channel', '')} / {account_info.get('Source', '')}")
    print(f"  注册方式: {account_info.get('AddType', '')}")
    
    create_at = account_info.get('CreateAt', 0)
    if create_at:
        from datetime import datetime
        create_time = datetime.fromtimestamp(create_at).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  注册时间: {create_time}")
    
    # Basic Info
    print("\n【基础信息】")
    print(f"  姓名: {basic_info.get('Name', '') or '(未填写)'}")
    print(f"  昵称: {basic_info.get('NickName', '') or '(未填写)'}")
    print(f"  性别: {format_gender(basic_info.get('Gender', 0))}")
    
    phone = basic_info.get('Phone', '')
    contact_phone = basic_info.get('ContactPhone', '')
    if phone:
        print(f"  手机号: {phone}")
    if contact_phone and contact_phone != phone:
        print(f"  联系手机: {contact_phone}")
    
    email = basic_info.get('Email', '')
    contact_email = basic_info.get('ContactEmail', '')
    if email:
        print(f"  邮箱: {email}")
    if contact_email and contact_email != email:
        print(f"  联系邮箱: {contact_email}")
    
    birthday = basic_info.get('Birthday', '')
    if birthday and len(birthday) == 8:
        birthday = f"{birthday[:4]}-{birthday[4:6]}-{birthday[6:8]}"
        print(f"  生日: {birthday}")
    
    province = basic_info.get('Province', '')
    city = basic_info.get('City', '')
    if province or city:
        print(f"  地区: {province} {city}")
    
    organization = basic_info.get('Organization', '')
    category = basic_info.get('Category', '')
    if organization:
        print(f"  学校/组织: {organization}")
    if category:
        print(f"  身份: {category}")
    
    # Social bindings
    bindings = []
    if basic_info.get('BindWx'):
        wx_name = basic_info.get('WxName', '')
        bindings.append(f"微信({wx_name})" if wx_name else "微信")
    if basic_info.get('BindQQ'):
        qq_name = basic_info.get('QQName', '')
        bindings.append(f"QQ({qq_name})" if qq_name else "QQ")
    if bindings:
        print(f"  社交绑定: {', '.join(bindings)}")
    
    # Resume
    resume = basic_info.get('Resume', '')
    if resume:
        try:
            resume_data = json.loads(resume)
            print(f"  简历: {resume_data.get('filename', '已上传')}")
        except:
            print(f"  简历: 已上传")
    
    # Camp Records
    if camp_records:
        print("\n【营地记录】")
        for record in camp_records:
            print(f"  - {record}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Query TCampos users')
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE,
                        help='Config file path')
    
    # Search mode
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List users command
    list_parser = subparsers.add_parser('list', help='List/search users')
    list_parser.add_argument('--search', '-s', default='',
                             help='Search by name or uid (fuzzy match)')
    list_parser.add_argument('--name', default='',
                             help='Filter by name (fuzzy match)')
    list_parser.add_argument('--uid', default='',
                             help='Filter by uid (exact match)')
    list_parser.add_argument('--uids', nargs='+', default=[],
                             help='Filter by multiple uids')
    list_parser.add_argument('--phone', default='',
                             help='Filter by phone (exact match)')
    list_parser.add_argument('--email', default='',
                             help='Filter by email (exact match)')
    list_parser.add_argument('--org', '--organization', default='',
                             help='Filter by organization/school (fuzzy match)')
    list_parser.add_argument('--gender', type=int, nargs='+', default=[],
                             help='Filter by gender (1=male, 2=female)')
    list_parser.add_argument('--camp-id', type=int, nargs='+', default=[],
                             help='Filter by camp IDs user participated in')
    list_parser.add_argument('--page-size', type=int, default=20,
                             help='Page size (default 20, max 50)')
    list_parser.add_argument('--page-num', type=int, default=1,
                             help='Page number (default 1)')
    list_parser.add_argument('--raw', action='store_true',
                             help='Output raw JSON response')
    
    # Get user detail command
    get_parser = subparsers.add_parser('get', help='Get user detail by uid')
    get_parser.add_argument('uid', help='User ID')
    get_parser.add_argument('--raw', action='store_true',
                            help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Default to list if no command specified
    if not args.command:
        parser.print_help()
        print("\nExamples:")
        print("  python list_user.py list --search \"张三\"")
        print("  python list_user.py list --phone \"13800138000\"")
        print("  python list_user.py list --org \"深圳中学\"")
        print("  python list_user.py get 63485076")
        sys.exit(0)
    
    try:
        if args.command == 'list':
            result = list_users(
                config_file=args.config,
                name_or_uid=args.search,
                name=args.name,
                uid=args.uid,
                uid_list=args.uids if args.uids else None,
                phone=args.phone,
                email=args.email,
                organization=args.org,
                gender_list=args.gender if args.gender else None,
                in_camp_list=args.camp_id if args.camp_id else None,
                page_size=args.page_size,
                page_num=args.page_num
            )
            
            if args.raw:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                format_user_list(result)
                
        elif args.command == 'get':
            result = get_user_detail(
                uid=args.uid,
                config_file=args.config
            )
            
            if args.raw:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                format_user_detail(result)
                
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please run login.py first to authenticate.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
