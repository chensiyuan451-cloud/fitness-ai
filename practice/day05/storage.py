"""数据层：只负责读写 workouts.json。不做计算，不问用户问题"""
import json
from pathlib import Path

# 这个文件在 practice/day05/ 里，.parent.parent 就是 practice
DATA_FILE = Path(__file__).parent.parent / 'workouts.json'


def load_workouts():
    """读取全部记录；文件不存在返回空列表；文件损坏就备份后返回空列表"""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        backup = DATA_FILE.with_name('workouts.broken.json')
        DATA_FILE.replace(backup)
        print(f'数据文件损坏（{e}），已改名为 {backup.name}，从空记录开始')
        return []


def save_workouts(workouts):
    """把全部记录写回文件（覆盖旧内容）"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(workouts, f, ensure_ascii=False, indent=2)