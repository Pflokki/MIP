import random


def get_next_point(p_list: list):
    ver = random.randint(1, 100)
    r_ver = 0
    for point in p_list:
        if point == 0:
            continue
        l_ver = r_ver
        r_ver += point * 100
        if l_ver < ver <= r_ver:
            return p_list.index(point)
    raise ValueError


def main():
    f_count = 100
    mpv_size = 5
    mpv = [0.21, 0.17, 0.02, 0.28, 0.32,
           0, 0.46, 0, 0.54, 0,
           0.42, 0.3, 0.03, 0.16, 0.09,
           0, 0.39, 0, 0.33, 0.28,
           0.36, 0, 0, 0.18, 0.46]

    p_list = [0] * mpv_size

    print("Enter step count: ")
    m_step_count = int(input())

    print("First point: ")
    m_point = int(input()) - 1

    for _ in [*range(f_count)]:
        point = m_point
        step_count = m_step_count
        print_str = "start(p{}) -> ".format(point + 1)
        while step_count > 0:
            mpv_current_point_index = mpv_size * point
            point = get_next_point(mpv[mpv_current_point_index: mpv_current_point_index + mpv_size])
            p_list[point] += 1
            print_str += "p{} -> ".format(point + 1)
            step_count -= 1

        print("{}end".format(print_str))

    print(p_list)
    print(list(map(lambda p: p / (f_count * m_step_count), p_list)))


if __name__ == '__main__':
    main()
