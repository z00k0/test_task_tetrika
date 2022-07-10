def sweep_line_algorithm(intervals, max_counter=1):
    timestamp_and_index_list = []

    for index, value in enumerate(intervals):
        timestamp_and_index_list.append((value, 1 if index % 2 == 0 else -1))  # начало интервала помечается 1, окончание -1
    timestamp_and_index_list.sort()
    max_counter = max_counter
    prev_counter = 0
    intersections_timestamps = []
    for _time, index in timestamp_and_index_list:
        counter = prev_counter + index
        if counter == max_counter and prev_counter == max_counter - 1:
            intersections_timestamps.append(_time)
        if counter == max_counter - 1 and prev_counter == max_counter:
            intersections_timestamps.append(_time)
        prev_counter = counter

    return intersections_timestamps


def appearance(intervals):
    timestamps = []  # объединяем lesson, tutor, pupil в плоский список
    lesson = intervals['lesson']
    timestamps.extend(lesson)
    pupil = sweep_line_algorithm(intervals['pupil'], max_counter=1)  # считаем пересечение интервалов учениками, если их несколько
    # если хотя бы один ученик присутствует, считается, что урок состоялся
    timestamps.extend(pupil)
    tutor = intervals['tutor']
    timestamps.extend(tutor)

    timestamp_list = sweep_line_algorithm(timestamps, max_counter=3)  # считаем пересечение трех интервалов: lesson, tutor, pupil
    time_sum = 0
    for index, timestamp in enumerate(timestamp_list):  # считаем время общего присутствия
        if index % 2 == 0:
            time_sum -= timestamp
        else:
            time_sum += timestamp

    print(time_sum)
    return time_sum


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
