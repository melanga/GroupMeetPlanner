import datetime


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


def end_time_adjust(end_time):
    midnight = datetime.datetime.strptime("00:00", "%H:%M")
    six_am = datetime.datetime.strptime("06:00", "%H:%M")
    if six_am >= end_time >= midnight:
        end_time += datetime.timedelta(days=1)
    return end_time
# def calculate_intersection(time_slots):
#     total_intersection = {}
#     for i, time_slot in enumerate(time_slots):
#         if i < time_slots.count() - 1:
#             if i == 0:
#                 time_slot1 = time_slot
#                 time_slot2 = time_slots[i + 1]
#                 total_intersection = intersection(time_slot1.start_time.isoformat(),
#                                                   time_slot1.end_time.isoformat(),
#                                                   time_slot2.start_time.isoformat(),
#                                                   time_slot2.end_time.isoformat())
#             else:
#                 start_time1 = total_intersection['start_time'].isoformat()
#                 end_time1 = total_intersection['end_time'].isoformat()
#                 start_time2 = time_slots[i + 1].start_time.isoformat()
#                 end_time2 = time_slots[i + 1].end_time.isoformat()
#                 total_intersection = intersection(start_time1, end_time1, start_time2, end_time2)
#     print(total_intersection)
#     return []
#
#
# # intersection period of two time intervals
# def intersection(start_time1, end_time1, start_time2, end_time2):
#     start_time1 = datetime.datetime.strptime(start_time1[:5], "%H:%M")
#     end_time1 = datetime.datetime.strptime(end_time1[:5], "%H:%M")
#     start_time2 = datetime.datetime.strptime(start_time2[:5], "%H:%M")
#     end_time2 = datetime.datetime.strptime(end_time2[:5], "%H:%M")
#
#     # check if the time intervals intersect
#     if start_time1 < end_time2 and start_time2 < end_time1:
#         # print("intersect")
#         # calculate intersection time interval
#         print(start_time1.time(), end_time1.time(), start_time2.time(), end_time2.time())
#         start_time = max(start_time1, start_time2)
#         end_time = min(end_time1, end_time2)
#         # print(start_time, end_time)
#         return {'start_time': start_time.time(),
#                 'end_time': end_time.time()}
#     else:
#         # print("no intersect")
#         return None
