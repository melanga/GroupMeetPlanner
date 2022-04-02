import datetime


# end time can be inputted from midnight to six a.m.
def end_time_adjust(end_time):
    midnight = datetime.datetime.strptime("00:00", "%H:%M")
    six_am = datetime.datetime.strptime("06:00", "%H:%M")
    if six_am >= end_time >= midnight:
        end_time += datetime.timedelta(days=1)
    return end_time


def check_time_validity(start_time, end_time):
    start_time = datetime.datetime.strptime(start_time[:5], "%H:%M")
    end_time = datetime.datetime.strptime(end_time[:5], "%H:%M")
    end_time = end_time_adjust(end_time)
    return start_time < end_time


def intersection_of_intervals(time_slots):
    intersection_period = {
        'start_time': time_slots[0].start_time.isoformat(),
        'end_time': time_slots[0].end_time.isoformat(),
    }
    for time_slot in time_slots:
        start_time1 = datetime.datetime.strptime(intersection_period['start_time'][:5], "%H:%M")
        end_time1 = end_time_adjust(datetime.datetime.strptime(intersection_period['end_time'][:5], "%H:%M"))
        start_time2 = datetime.datetime.strptime(time_slot.start_time.isoformat()[:5], "%H:%M")
        end_time2 = end_time_adjust(datetime.datetime.strptime(time_slot.end_time.isoformat()[:5], "%H:%M"))
        if start_time1 < end_time2 and start_time2 < end_time1:
            start_time = max(start_time1, start_time2)
            end_time = min(end_time1, end_time2)
            intersection_period['start_time'] = start_time.time().isoformat(timespec='minutes')
            intersection_period['end_time'] = end_time.time().isoformat(timespec='minutes')
        else:
            intersection_period['start_time'] = ""
            intersection_period['end_time'] = ""
    return intersection_period


# output the combinations of time slots with one time slot by each user
def time_slot_combinations(time_slots_per_user):
    # number of arrays
    n = len(time_slots_per_user)
    indices = [0 for i in range(n)]
    combinations = []
    while 1:
        combination = []
        # get the current combination and append
        for i in range(n):
            combination.append(time_slots_per_user[i][indices[i]])
        combinations.append(combination)

        # find the rightmost array that has more elements left after the current element in that array
        next_index = n - 1

        while next_index >= 0 and (indices[next_index] + 1 >= time_slots_per_user[next_index].count()):
            next_index -= 1

        # no such array is found so no more combinations left
        if next_index < 0:
            break

        # if found move to next element in that array
        indices[next_index] += 1

        # for all arrays to the right of this array current index again points to first element
        for i in range(next_index + 1, n):
            indices[i] = 0
    return combinations


# calculates the intersection combinations available for time slot combinations
def calculate_intersections_of_combinations(combinations):
    intersections_of_combinations = []
    for combination in combinations:
        intersection_of_combination = intersection_of_intervals(combination)
        if intersection_of_combination['start_time'] != "":
            intersections_of_combinations.append(intersection_of_combination)
    return intersections_of_combinations


def get_available_times(time_slots):
    available_time_slot_combinations = time_slot_combinations(time_slots)
    intersections_of_combinations = calculate_intersections_of_combinations(available_time_slot_combinations)
    available_times = []
    if len(intersections_of_combinations) <= 1:
        available_times = intersections_of_combinations
    # if times intersect combine those times
    for i, intersection in enumerate(intersections_of_combinations):
        intersection_period = {
            'start_time': intersection['start_time'],
            'end_time': intersection['end_time'],
        }
        if i < len(intersections_of_combinations)-1:
            start_time1 = datetime.datetime.strptime(intersection['start_time'][:5], "%H:%M")
            end_time1 = end_time_adjust(datetime.datetime.strptime(intersection['end_time'][:5], "%H:%M"))
            start_time2 = datetime.datetime.strptime(intersections_of_combinations[i+1]['start_time'][:5], "%H:%M")
            end_time2 = end_time_adjust(datetime.datetime.strptime(intersections_of_combinations[i+1]['end_time'][:5], "%H:%M"))
            if start_time1 < end_time2 and start_time2 < end_time1:
                start_time = min(start_time1, start_time2)
                end_time = max(end_time1, end_time2)
                intersection_period['start_time'] = start_time.time().isoformat(timespec='minutes')
                intersection_period['end_time'] = end_time.time().isoformat(timespec='minutes')
                available_times.append(intersection_period)
            else:
                available_times.append(intersection)
                available_times.append(intersections_of_combinations[i+1])
    return available_times
