# 第 3 天：把训练记录保存到 JSON 文件，下次运行还能读回来
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / 'workouts.json'


def load_workouts():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_workouts(workouts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(workouts, f, ensure_ascii=False, indent=2)


def add_workout(workouts, workout_date, sets, note=''):
    """添加一次训练。成功返回 True；同一天已经有记录就返回 False，不添加"""
    for workout in workouts:
        if workout['date'] == workout_date:
            return False              # 找到重复：马上返回
    # 循环全部走完都没 return，才说明确实没有重复
    workouts.append({'date': workout_date, 'note': note, 'sets': sets})
    return True


def set_volume(training_set):
    return training_set['weight'] * training_set['reps']


def list_workouts(workouts):
    if not workouts:
        print('暂无训练记录')
        return
    print('=== 历史训练概况 ===')
    for workout in workouts:
        formal_count = 0
        total_vol = 0.0
        for training_set in workout['sets']:
            if training_set['is_warmup']:
                continue
            formal_count += 1
            total_vol += set_volume(training_set)
        note = workout.get('note', '')
        print(f"{workout['date']} {note}：正式组 {formal_count} 组，总容量 {total_vol}kg*次")


# ===== 主程序 =====
workouts = load_workouts()
print(f'读取到 {len(workouts)} 次训练记录')

today_sets = [
    {"exercise": "杠铃卧推", "weight": 20.0, "reps": 12, "is_warmup": True},
    {"exercise": "杠铃卧推", "weight": 60.0, "reps": 8, "is_warmup": False},
    {"exercise": "哑铃飞鸟", "weight": 12.0, "reps": 12, "is_warmup": False},
]
today = date.today().isoformat()

if add_workout(workouts, today, today_sets, note='胸日'):
    save_workouts(workouts)           # 只有真的添加了才写文件
    print(f'保存完成，现在共有 {len(workouts)} 次训练记录')
else:
    print(f'{today} 已经记录过了，本次不保存')

list_workouts(workouts)
print(f'文件位置：{DATA_FILE}')