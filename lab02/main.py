import random
import matplotlib.pyplot as plt


MAX_TIME_LENGTH = 20
MAX_QUEUE_SIZE = 5


class Status:
    def __init__(self):
        self.status_hist = []
        self.queue_length = -1

    def __save_current_status(self, time, action):
        self.status_hist.append({'time': time,
                                 'action': action,
                                 'queue_length': self.queue_length,
                                 'working_status': self.queue_length != -1})
        self.status_hist.sort(key=lambda sh: sh['time'])

    def add_task(self, time):
        if self.queue_length < MAX_QUEUE_SIZE:
            self.queue_length += 1
        self.__save_current_status(time, 'add')

    def remove_task(self, time):
        self.queue_length -= 1
        self.__save_current_status(time, 'remove')


class TaskGenerator:
    def __init__(self, _lambda):
        self._lambda = _lambda

    def get_next_tick(self):
        return random.expovariate(self._lambda)


class TaskResolver:
    def __init__(self, _mu):
        self._mu = _mu

    def get_next_tick(self, queue_length):
        return random.expovariate(self._mu) if queue_length > 0 else MAX_TIME_LENGTH + 1


def main():
    print("Max time: {}, Max queue length: {}".format(MAX_TIME_LENGTH, MAX_QUEUE_SIZE))
    print("Input lambda: ")
    _lambda =  int(input())
    # _lambda = 3
    print("Input mu: ")
    _mu =  int(input())
    # _mu = 7

    tg = TaskGenerator(_lambda)
    tr = TaskResolver(_mu)

    status = Status()

    max_array_time = MAX_TIME_LENGTH
    current_time = 0
    while current_time <= max_array_time:
        t_tick = tg.get_next_tick()
        r_tick = tr.get_next_tick(status.queue_length)

        s_current_time = current_time
        if r_tick < t_tick:
            while status.queue_length != 0 or current_time + r_tick <= s_current_time + t_tick:
                current_time += r_tick
                status.remove_task(current_time)
                r_tick = tr.get_next_tick(status.queue_length)
        else:
            current_time += t_tick
            status.add_task(current_time)
        current_time += t_tick
        status.add_task(current_time)

    for _ in status.status_hist:
        print(_)

    plt.fill = True
    plt.bar([_['time'] if _['action'] == "add" else 0 for _ in status.status_hist],
            [_['queue_length'] if _['action'] == "add" else 0 for _ in status.status_hist],
            width=0.05)
    plt.bar([_['time'] if _['action'] != "add" else 0 for _ in status.status_hist],
            [_['queue_length'] if _['action'] != "add" else 0 for _ in status.status_hist],
            width=0.05)

    plt.show()

if __name__ == '__main__':
    main()