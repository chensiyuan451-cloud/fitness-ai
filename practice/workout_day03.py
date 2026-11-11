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
    for time in workouts:
        if time['date'] == workout_date:
            return print(f'已有相同日期保存失败')
        else:
         print(f'保存完成，现在有 {len(workouts)}次训练记录')
    workout = {'date': workout_date, 'sets': sets, 'note': note}
    workouts.append(workout)
    return workouts


workouts = load_workouts()
print(f'读取到{len(workouts)}次训练记录')
def set_volume(training_set):
        return training_set['weight'] * training_set['reps']
def list_workouts(workouts):
    if not workouts:
        print('暂无训练记录')
        return
    print('===历史训练概况===')
    for workout in workouts:
        w_date = workout['date']
        note = f'{workout["note"]}' if workout.get('note') else ''
        formal_count = 0
        total_vol = 0.0
        for training_set in workout['sets']:
            if training_set['is_warmup']:
                continue
            formal_count += 1
            total_vol += set_volume(training_set)
        print(f'{w_date}{note},正式组{formal_count},总容量{total_vol}kg*次')
today_sets = [
    {"exercise": "杠铃卧推", "weight": 20.0, "reps": 12, "is_warmup": True},
    {"exercise": "杠铃卧推", "weight": 60.0, "reps": 8, "is_warmup": False},
    {"exercise": "哑铃飞鸟", "weight": 12.0, "reps": 12, "is_warmup": False},
]
today = date.today().isoformat()
add_workout(workouts, today, today_sets, note='胸日')
save_workouts(workouts)
list_workouts(workouts)
print(f'文件位置，{DATA_FILE}')
