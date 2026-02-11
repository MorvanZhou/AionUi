#!/usr/bin/env python3
"""
查询用户任务完成情况
POST https://tcampos.qq.com/api/task/listUserTaskRecord
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tcampos_api import get_api_client, DEFAULT_CONFIG_FILE


def list_user_task_record(
    config_file: str = None,
    tipe_token: str = None,
    task_id: int = None,
    keyword: str = None,
    username: str = None,
    status_list: list = None,
    page_size: int = 20,
    page_num: int = 1
) -> dict:
    """
    查询用户任务完成情况
    
    Args:
        config_file: Path to config file
        tipe_token: Direct tipe_token value (takes priority)
        task_id: 任务 ID
        keyword: 关键词搜索
        username: 用户名搜索
        status_list: 完成状态列表，如 [2] 表示只查询已完成的
        page_size: 每页数量
        page_num: 页码
        
    Returns:
        API response data
    """
    if not task_id:
        raise ValueError("task_id 是必需的参数")
    
    api = get_api_client(config_file=config_file, tipe_token=tipe_token)
    
    request_data = {
        "TaskID": task_id,
        "Filter": {
            "Keyword": keyword or "",
            "UserName": username or "",
            "OpStatus": status_list or [],
            "Exercise": {"PassStatusList": []},
            "Creation": {}
        },
        "PageSize": page_size,
        "PageNum": page_num,
        "Sort": []
    }
    
    return api.post("/task/listUserTaskRecord", request_data)


def format_output(data: dict, raw: bool = False) -> None:
    """格式化输出结果"""
    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    
    # 检查是否成功
    if data.get('Code') != 0:
        print(f"❌ 错误: {data.get('Code')} - {data}")
        return
    
    result = data.get('Response', {}).get('Result', {})
    entries = result.get('Entries', [])
    total = result.get('Total', 0)
    progress = result.get('Progress', {})
    
    if not entries:
        print("✓ 没有查询到数据")
        return
    
    print(f"✓ 共查询到 {total} 条用户记录\n")
    print(f"  未开始: {progress.get('NotStart', 0)}, 进行中: {progress.get('Doing', 0)}, 已完成: {progress.get('Done', 0)}")
    print(f"  总体完成率: {progress.get('TotalDoneRatio', 0)*100:.2f}%\n")
    
    # 状态映射
    status_map = {0: '未开始', 1: '进行中', 2: '已完成'}
    
    # 打印表头
    print(f"{'用户ID':<20} {'用户名':<20} {'状态':<10} {'完成率':<8} {'开始时间':<20} {'完成时间':<20}")
    print("-" * 98)
    
    # 打印数据
    for record in entries:
        user_id = record.get('Uid', '-')
        user_name = record.get('UserName', '-')
        status = status_map.get(record.get('OpStatus', 0), str(record.get('OpStatus', '-')))
        # Progress 值可能已是百分比，也可能是 0-1 的比值，根据数值判断
        progress_val = record.get('Progress', 0)
        if progress_val > 100:
            complete_ratio = f"{progress_val/100:.0f}%"
        elif progress_val > 1:
            complete_ratio = f"{progress_val:.0f}%"
        else:
            complete_ratio = f"{progress_val*100:.0f}%"
        
        # 时间戳转换（如果需要）
        start_time = record.get('StartAt', 0)
        complete_time = record.get('FinishAt', 0)
        
        start_time_str = str(start_time) if start_time else '-'
        complete_time_str = str(complete_time) if complete_time else '-'
        
        print(f"{user_id:<20} {user_name:<20} {status:<10} {complete_ratio:<8} {start_time_str:<20} {complete_time_str:<20}")
    
    print(f"\n✓ 显示 {len(entries)} 条记录")


def main():
    parser = argparse.ArgumentParser(description='查询用户任务完成情况')
    parser.add_argument('--config', '-c', default=DEFAULT_CONFIG_FILE)
    parser.add_argument('--task-id', '-t', type=int, required=True, help='任务 ID')
    parser.add_argument('--keyword', '-k', default='', help='关键词搜索')
    parser.add_argument('--username', '-u', default='', help='用户名搜索')
    parser.add_argument('--status', '-s', type=int, help='完成状态(0-未开始, 1-进行中, 2-已完成)')
    parser.add_argument('--page-size', type=int, default=20, help='每页数量')
    parser.add_argument('--page-num', type=int, default=1, help='页码')
    parser.add_argument('--raw', action='store_true', help='输出原始JSON')
    
    args = parser.parse_args()
    
    # 构建状态列表
    status_list = [args.status] if args.status is not None else []
    
    result = list_user_task_record(
        config_file=args.config,
        task_id=args.task_id,
        keyword=args.keyword,
        username=args.username,
        status_list=status_list,
        page_size=args.page_size,
        page_num=args.page_num
    )
    
    format_output(result, args.raw)


if __name__ == '__main__':
    main()
