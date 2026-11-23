"""界面层：菜单、input、print 都在这里。计算交给 service，读写文件交给 storage"""
from datetime import date

import service
import storage


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


# ---------- 显示 ----------
def format_set(training_set):
    """把一组训练变成一行文字（只返回，不打印）"""
    exercise = training_set['exercise']
    weight = training_set['weight']
    reps = training_set['reps']
    if training_set['is_warmup']:
        return f'{exercise}: {weight}kg * {reps}次，热身组不计入'
    volume = service.calc_volume(training_set)
    return f'{exercise}: {weight}kg * {reps}次，正式组，容量{volume}'


def show_history(workouts):
    if not workouts:
        print('暂无训练记录')
        return
    print('=== 历史训练概况 ===')
    for workout in workouts:
        summary = service.summarize_workout(workout)
        print(f"{workout['date']}：共 {len(workout['sets'])} 组，"
              f"正式组 {summary['formal_count']} 组，"
              f"总容量 {summary['total_volume']}kg*次")


def show_today(workouts, workout_date):
    workout = service.find_workout(workouts, workout_date)
    if workout is None or not workout['sets']:
        print('今天还没有记录')
        return
    print(f'=== {workout_date} 训练详情 ===')
    for number, training_set in enumerate(workout['sets'], start=1):
        print(f'第{number}组 {format_set(training_set)}')
    summary = service.summarize_workout(workout)
    print(f"正式组 {summary['formal_count']} 组，总容量 {summary['total_volume']}kg*次")


# ---------- 菜单操作 ----------
def handle_add(workouts, workout_date):
    training_set = input_set()
    count = service.add_set(workouts, workout_date, training_set)
    storage.save_workouts(workouts)
    print(f'已保存，今天共 {count} 组')


def handle_remove(workouts, workout_date):
    last_set = service.get_last_set(workouts, workout_date)
    if last_set is None:
        print('今天还没有可删除的组')
        return
    print(f'要删除的是：{format_set(last_set)}')
    if not input_yes_no('确认删除吗？(y/n)：'):
        print('已取消，没有删除')
        return
    service.remove_last_set(workouts, workout_date)
    storage.save_workouts(workouts)
    print('已删除')
def show_max_weight(workouts):
    max_weight = service.max_weight_by_exercise(workouts)
    if not max_weight:
        print('暂无正式组')
        return
    for name, weight in sorted(max_weight.items()):
        print(f'{name}: {weight}kg')



def main():
    workouts = storage.load_workouts()
    today = date.today().isoformat()
    print(f'读取到 {len(workouts)} 次训练记录')

    while True:
        print('\n1. 记录一组  2. 查看历史  3. 删除今天最后一组  4. 查看今天详情  5.查看各动作最大重量  0. 退出')
        choice = input('请选择：').strip()
        if choice == '1':
            handle_add(workouts, today)
        elif choice == '2':
            show_history(workouts)
        elif choice == '3':
            handle_remove(workouts, today)
        elif choice == '4':
            show_today(workouts, today)
        elif choice == '5':
            show_max_weight(workouts)
        elif choice == '0':
            print('再见')
            break
        else:
            print('没有这个选项，请输入 0 到 4')


if __name__ == '__main__':
    main()