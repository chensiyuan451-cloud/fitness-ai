"""service.py 的测试。运行：python -m pytest practice/day05 -v"""
import service


# ---------- 辅助函数：快速造数据 ----------
# 不以 test_ 开头，所以 pytest 不会把它当成测试
def make_set(exercise, weight, is_warmup=False, reps=8):
    """造一组训练。不传 is_warmup 时默认是正式组"""
    return {'exercise': exercise, 'weight': weight, 'reps': reps, 'is_warmup': is_warmup}


def make_day(date, sets):
    """造一天的训练记录"""
    return {'date': date, 'note': '', 'sets': sets}


# ---------- 原有的 4 个测试 ----------
def test_add_set_merges_same_day():
    workouts = []
    warmup = {'exercise': '卧推', 'weight': 20.0, 'reps': 12, 'is_warmup': True}
    formal = {'exercise': '卧推', 'weight': 60.0, 'reps': 8, 'is_warmup': False}
    assert service.add_set(workouts, '2026-01-01', warmup) == 1
    assert service.add_set(workouts, '2026-01-01', formal) == 2
    assert len(workouts) == 1, '同一天应该只有一条训练记录'


def test_summary_skips_warmup():
    workouts = []
    service.add_set(workouts, '2026-01-01', {'exercise': '卧推', 'weight': 20.0, 'reps': 12, 'is_warmup': True})
    service.add_set(workouts, '2026-01-01', {'exercise': '卧推', 'weight': 60.0, 'reps': 8, 'is_warmup': False})
    summary = service.summarize_workout(workouts[0])
    assert summary == {'formal_count': 1, 'total_volume': 480.0}, summary


def test_missing_date_returns_none():
    workouts = []
    assert service.find_workout(workouts, '2099-01-01') is None
    assert service.get_last_set(workouts, '2099-01-01') is None
    assert service.remove_last_set(workouts, '2099-01-01') is None


def test_remove_last_set_deletes_empty_day():
    workouts = []
    service.add_set(workouts, '2026-01-01', {'exercise': '卧推', 'weight': 20.0, 'reps': 12, 'is_warmup': True})
    service.add_set(workouts, '2026-01-01', {'exercise': '卧推', 'weight': 60.0, 'reps': 8, 'is_warmup': False})
    assert service.remove_last_set(workouts, '2026-01-01')['weight'] == 60.0
    assert service.remove_last_set(workouts, '2026-01-01')['weight'] == 20.0
    assert workouts == [], '最后一组删完，这一天的记录应该整条消失'


# ---------- 改动二：max_weight_by_exercise 的测试 ----------
def test_max_empty_returns_empty_dict():
    assert service.max_weight_by_exercise([]) == {}


def test_max_takes_heavier_when_heavier_comes_later():
    workouts = [
        make_day('2026-01-01', [make_set('卧推', 50.0)]),
        make_day('2026-01-02', [make_set('卧推', 60.0)]),
    ]
    assert service.max_weight_by_exercise(workouts) == {'卧推': 60.0}


def test_max_keeps_heavier_when_lighter_comes_later():
    workouts = [
        make_day('2026-01-01', [make_set('卧推', 60.0)]),
        make_day('2026-01-02', [make_set('卧推', 50.0)]),
    ]
    assert service.max_weight_by_exercise(workouts) == {'卧推': 60.0}


def test_max_ignores_warmup_even_if_heavier():
    workouts = [
        make_day('2026-01-01', [
            make_set('卧推', 80.0, is_warmup=True),
            make_set('卧推', 60.0),
        ]),
    ]
    assert service.max_weight_by_exercise(workouts) == {'卧推': 60.0}


def test_max_warmup_only_exercise_not_in_result():
    workouts = [
        make_day('2026-01-01', [
            make_set('卧推', 60.0),
            make_set('飞鸟', 10.0, is_warmup=True),
        ]),
    ]
    assert service.max_weight_by_exercise(workouts) == {'卧推': 60.0}


def test_max_multiple_exercises_same_day():
    workouts = [
        make_day('2026-01-01', [
            make_set('卧推', 60.0),
            make_set('飞鸟', 13.0),
        ]),
    ]
    assert service.max_weight_by_exercise(workouts) == {'卧推': 60.0, '飞鸟': 13.0}


if __name__ == '__main__':
    # 不用 pytest 时，直接 Run 本文件：自动运行所有 test_ 开头的函数
    for name, func in list(globals().items()):
        if name.startswith('test_') and callable(func):
            func()
            print('通过:', name)
    print('全部通过')