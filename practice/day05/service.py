"""业务层：查找、计算、增删。这里不能出现 input()、print()，也不读写文件"""

def find_workout(workouts, workout_date):
    """只查找，不新建。找不到返回 None"""
    for workout in workouts:
        if workout['date'] == workout_date:
            return workout
    return None


def get_or_create_workout(workouts, workout_date):
    """找到这一天的训练；没有就新建一条，加进列表"""
    workout = find_workout(workouts, workout_date)
    if workout is None:
        workout = {'date': workout_date, 'note': '', 'sets': []}
        workouts.append(workout)
    return workout


def calc_volume(training_set):
    return training_set['weight'] * training_set['reps']


def summarize_workout(workout):
    """统计一次训练的正式组数和总容量"""
    formal_count = 0
    total_volume = 0.0
    for training_set in workout['sets']:
        if training_set['is_warmup']:
            continue
        formal_count += 1
        total_volume += calc_volume(training_set)
    return {'formal_count': formal_count, 'total_volume': total_volume}


def add_set(workouts, workout_date, training_set):
    """给某一天加一组，返回这一天现在共有几组"""
    workout = get_or_create_workout(workouts, workout_date)
    workout['sets'].append(training_set)
    return len(workout['sets'])


def get_last_set(workouts, workout_date):
    """返回某一天的最后一组；这一天没有记录就返回 None"""
    workout = find_workout(workouts, workout_date)
    if workout is None or not workout['sets']:
        return None
    return workout['sets'][-1]


def remove_last_set(workouts, workout_date):
    """删除某一天的最后一组并返回它；没有可删的返回 None"""
    workout = find_workout(workouts, workout_date)
    if workout is None or not workout['sets']:
        return None
    removed = workout['sets'].pop()
    if not workout['sets']:
        workouts.remove(workout)
    return removed
def max_weight_by_exercise(workouts):
    result = {}
    for workout in workouts:
        for training_set in workout['sets']:
            if training_set['is_warmup']:
                continue
            name = training_set['exercise']
            weight = training_set['weight']
            result[name] = max(result.get(name, 0), weight)
    return result