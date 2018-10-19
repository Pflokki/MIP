import random
import matplotlib.pyplot as plt


MAX_TIME_LENGTH = 200
MAX_QUEUE_SIZE = 10

def get_abs_resolve_value(value):
    return random.randint(int(value * 1000) - 50, int(value * 1000) + 50) / 1000

def get_abs_offline_value(value):
    return random.randint(int(value * 100) - 5, int(value * 100) + 5) / 100

class Status:
    def __init__(self):
        self.status_hist = []
        self.queue_length = -1

    def __save_current_status(self, time, spend_time, action):
        self.status_hist.append({'time': time,
                                 'spend_time': spend_time,
                                 'action': action,
                                 'queue_length': self.queue_length,
                                 'working_status': self.queue_length != -1})
        # self.status_hist.sort(key=lambda sh: sh['time'])

    def add_task(self, time, spend_time):
        if self.queue_length < MAX_QUEUE_SIZE:
            self.queue_length += 1
        self.__save_current_status(time, spend_time, 'add')

    def remove_task(self, time, spend_time):
        self.queue_length -= 1
        self.__save_current_status(time, spend_time, 'remove')

    def get_avg_queue_length(self):
        sum_queue = 0
        for sh in self.status_hist:
            if sh['queue_length'] != -1:
                sum_queue += sh['queue_length']

        return round(sum_queue / len(self.status_hist)) if len(self.status_hist) != 0 else 0

    def get_avg_resolve_time(self):
        solve_time_list = [sl['spend_time'] for sl in self.status_hist if sl['action'] == "remove"]

        return sum(solve_time_list) / len(solve_time_list) if len(solve_time_list) != 0 else 0

    def get_avg_resolve_offline_time(self):
        list_remove = [sl['time'] for sl in self.status_hist if sl['action'] == "remove" and sl['working_status'] == False]
        list_add = [sl['time'] for sl in self.status_hist if sl['action'] == "add" and sl['queue_length'] == 0]

        return (sum(list_remove) - sum(list_add[:len(list_remove )])) / len(list_remove) if len(list_remove) != 0 else 0


class TaskGenerator:
    def __init__(self, _lambda):
        self._lambda = _lambda

    def get_next_tick(self):
        return random.expovariate(self._lambda)


class TaskResolver:
    def __init__(self, _mu):
        self._mu = _mu

    def get_next_tick(self):
        return random.expovariate(self._mu)  # if queue_length > 0 else 0


def main():
    print("Enter lambda")
    _lambda =  int(input())
    # _lambda = 7
    # _lambda = 3
    print("Enter mu")
    _mu =  int(input())
    # _mu = 4
    # _mu = 7

    tg = TaskGenerator(_lambda)
    tr = TaskResolver(_mu)

    status = Status()

    max_array_time = MAX_TIME_LENGTH
    current_time = 0

    t_tick = tg.get_next_tick()
    r_tick = tr.get_next_tick()
    t_current_time = t_tick
    r_current_time = r_tick

    while current_time <= max_array_time:
        if t_current_time < r_current_time or status.queue_length == -1:
            current_time = t_current_time
            if status.queue_length == -1:
                r_current_time += t_tick
            status.add_task(current_time, t_tick)
            t_tick = tg.get_next_tick()
            t_current_time += t_tick
        else:
            current_time = r_current_time
            status.remove_task(current_time, r_tick)
            r_tick = tr.get_next_tick()
            r_current_time += r_tick

    for _ in status.status_hist:
        print(_)
    print(f"Max time: {MAX_TIME_LENGTH}, Max queue length: {MAX_QUEUE_SIZE}")
    print(f"Lambda: {_lambda}")
    print(f"Mu: {_mu}")

    avg_queue_length = status.get_avg_queue_length()
    avg_resolve_time = status.get_avg_resolve_time()
    avg_offline_time = status.get_avg_resolve_offline_time()
    print(f"Average queue length = {avg_queue_length} ({avg_queue_length})")
    print(f"Average resolve time = {avg_resolve_time} ({get_abs_resolve_value(avg_resolve_time)})")
    print(f"Average offline time = {avg_offline_time} ({get_abs_resolve_value(avg_offline_time)})")

    plt.plot([*range(len(status.status_hist))], [sh['queue_length'] + 1 for sh in status.status_hist])

    plt.show()

if __name__ == '__main__':
    main()