# 第 4 天（完整版）：终端录入 + 输入校验 + 删除最后一组 + 今天详情
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / 'workouts.json'


# ---------- 读写文件 ----------
def load_workouts():
    """读取记录；文件损坏时把坏文件改名备份，返回空列表，程序不崩溃"""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        backup = DATA_FILE.with_name('workouts.broken.json')
        DATA_FILE.replace(backup)
        print(f'数据文件损坏（{e}）')
        print(f'已把坏文件改名为 {backup.name}，从空记录开始')
        return []


def save_workouts(workouts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(workouts, f, ensure_ascii=False, indent=2)


# ---------- 读取用户输入 ----------
def input_number(prompt, number_type, low, high):
    """反复询问，直到输入一个在 low~high 之间的数字"""
    while True:
        text = input(prompt).strip()
        try:
            value = number_type(text)
        except ValueError:
            print(f'  "{text}" 不是有效的数字，请重新输入')
            continue
        if low <= value <= high:
            return value
        print(f'  请输入 {low} 到 {high} 之间的数')


def input_yes_no(prompt):
    """只接受 y 或 n，返回 True / False"""
    while True:
        text = input(prompt).strip().lower()
        if text == 'y':
            return True
        if text == 'n':
            return False
        print('  请输入 y 或 n')


def input_set():
    """在终端录入一组训练，返回一个字典"""
    exercise = input('动作名称：').strip()
    while not exercise:
        exercise = input('  动作名称不能为空，请重新输入：').strip()
    weight = input_number('重量(kg)：', float, 0, 500)
    reps = input_number('次数：', int, 1, 100)
    is_warmup = input_yes_no('是热身组吗？(y/n)：')
    return {'exercise': exercise, 'weight': weight, 'reps': reps, 'is_warmup': is_warmup}


# ---------- 查找 ----------
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


# ---------- 计算 ----------
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


# ---------- 显示 ----------
def format_set(training_set):
    """把一组训练变成一行文字（只返回，不打印）"""
    exercise = training_set['exercise']
    weight = training_set['weight']
    reps = training_set['reps']
    if training_set['is_warmup']:
        return f'{exercise}: {weight}kg * {reps}次，热身组不计入'
    return f'{exercise}: {weight}kg * {reps}次，正式组，容量{calc_volume(training_set)}'


def show_history(workouts):
    if not workouts:
        print('暂无训练记录')
        return
    print('=== 历史训练概况 ===')
    for workout in workouts:
        summary = summarize_workout(workout)
        note = workout.get('note', '')
        total_set = len(workout['sets'])
        print(f"{workout['date']} {note}：共 {total_set}组"
              f"正式组 {summary['formal_count']} 组，"
              f"总容量 {summary['total_volume']}kg*次")


def show_today(workouts, workout_date):
    workout = find_workout(workouts, workout_date)
    if workout is None or not workout['sets']:
        print('今天还没有记录')
        return
    print(f'=== {workout_date} 训练详情 ===')
    for number, training_set in enumerate(workout['sets'], start=1):
        print(f'第{number}组 {format_set(training_set)}')
    summary = summarize_workout(workout)
    print(f"正式组 {summary['formal_count']} 组，总容量 {summary['total_volume']}kg*次")


# ---------- 菜单操作 ----------
def add_set(workouts, workout_date):
    training_set = input_set()
    workout = get_or_create_workout(workouts, workout_date)
    workout['sets'].append(training_set)
    save_workouts(workouts)
    print(f"已保存，今天共 {len(workout['sets'])} 组")


def remove_last_set(workouts, workout_date):
    workout = find_workout(workouts, workout_date)
    if workout is None or not workout['sets']:
        print('今天还没有可删除的组')
        return
    last_set = workout['sets'][-1]
    print(f'要删除的是：{format_set(last_set)}')
    if not input_yes_no('确认删除吗？(y/n)：'):
        print('已取消，没有删除')
        return
    workout['sets'].pop()
    if not workout['sets']:
        workouts.remove(workout)
    save_workouts(workouts)
    print('已删除')


def main():
    workouts = load_workouts()
    today = date.today().isoformat()
    print(f'读取到 {len(workouts)} 次训练记录')

    while True:
        print('\n1. 记录一组  2. 查看历史  3. 删除今天最后一组  4. 查看今天详情  0. 退出')
        choice = input('请选择：').strip()
        if choice == '1':
            add_set(workouts, today)
        elif choice == '2':
            show_history(workouts)
        elif choice == '3':
            remove_last_set(workouts, today)
        elif choice == '4':
            show_today(workouts, today)
        elif choice == '0':
            print('再见')
            break
        else:
            print('没有这个选项，请输入 0 到 4')


if __name__ == '__main__':
    main()