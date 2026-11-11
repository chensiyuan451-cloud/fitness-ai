# 第 2 天：用函数整理代码，并按动作统计容量
def set_volume(training_set):
    return training_set['weight'] * training_set['reps']

def format_set(training_set):
    exercise = training_set['exercise']
    weight = training_set['weight']
    reps = training_set['reps']
    if training_set['is_warmup']:
        return f'{exercise}: {weight}kg * {reps}次，热身组不计入'
    return f'{exercise}: {weight}kg * {reps}次，正式组，容量{set_volume(training_set)}'

def summarize(workout_sets):
    total_volume = 0.0
    formal_count = 0
    volume_by_exercise = {}
    sets_by_exercise = {}

    for training_set in workout_sets:
        if training_set['is_warmup']:
            continue
        volume = set_volume(training_set)
        total_volume += volume
        formal_count += 1
        name = training_set['exercise']
        volume_by_exercise[name] = volume_by_exercise.get(name, 0) + volume
        sets_by_exercise[name] = sets_by_exercise.get(name, 0) + 1
    return {
        'total_volume': total_volume,
        'formal_count': formal_count,
        'volume_by_exercise': volume_by_exercise,
        'sets_by_exercise': sets_by_exercise
    }
def max_weight(workout_sets):
    heaviest = 0
    for training_set in workout_sets:
        if training_set['is_warmup']:
            continue
        heaviest = max(heaviest, training_set['weight'])
    return heaviest

workout_sets = [
    {"exercise": "杠铃卧推", "weight": 20.0, "reps": 12, "is_warmup": True},
    {"exercise": "杠铃卧推", "weight": 60.0, "reps": 8, "is_warmup": False},
    {"exercise": "杠铃卧推", "weight": 60.0, "reps": 6, "is_warmup": False},
    {"exercise": "杠铃卧推", "weight": 50.0, "reps": 10, "is_warmup": False},
    {"exercise": "哑铃飞鸟", "weight": 12.0, "reps": 12, "is_warmup": False},
    {"exercise": "哑铃飞鸟", "weight": 12.0, "reps": 10, "is_warmup": False},
]
print('今天的训练记录')
for training_set in workout_sets:
    print(format_set(training_set))
summary = summarize(workout_sets)
print(f'正式组数量: {summary["formal_count"]}')
print(f'正式组容量: {summary["total_volume"]}kg*次')
print('各动作容量:')
for name, volume in summary['volume_by_exercise'].items():
    print(f'{name}: {volume}')
print('正式组分别组数:')
for name, i in summary['sets_by_exercise'].items():
    print(f'{name}: {i}')
print(f'最大重量:{max_weight(workout_sets)}')
