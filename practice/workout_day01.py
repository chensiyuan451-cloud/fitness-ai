workout_sets =[{'exercise' : '杠铃卧推',
                'weight' : 20.0,
                'reps' : 12,
                'is_warmup' :  True,},
               {'exercise' : '杠铃卧推',
                'weight' : 60.0,
                'reps' : 8,
                'is_warmup' : False,},
               {'exercise' : '杠铃卧推',
                'weight' : 60.0,
                'reps' : 6,
                'is_warmup' : False,},
               {'exercise' : '杠铃卧推',
                'weight' : 50.0,
                'reps' : 10,
                'is_warmup' : False,}
               ]
total_volume = 0.0
i = 0
print('今日训练记录：')
for training_set in workout_sets:
    exercise = training_set['exercise']
    weight = training_set['weight']
    reps = training_set['reps']
    is_warmup = training_set['is_warmup']
    volume = reps*weight
    if is_warmup:
        print(f'{exercise} : {weight}kg*{reps}次，热身组，不计入')
    else:
        total_volume = total_volume +volume
        print(f'{exercise} : {weight}kg*{reps}次，正式组，容量{volume}')
        i = i + 1
print(f'正式组次数:{i}次')
print(f'正式组总容量：{total_volume}kg*次')