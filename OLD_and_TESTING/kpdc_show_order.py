from functools import partial
from math import ceil, floor
from multiprocessing import Pool
import pandas as pd
import random


DANCERS_BY_DANCE_FILENAME = 's25_rosters.csv'
ACT_ITERATIONS = 100
DAY_ITERATIONS = 100


def fail(s):
    print(s)
    exit(1)


def get_dancers_by_dance(filename):
    data = pd.read_csv(filename)

    dancers_by_dance = {}
    for _, row in data.iterrows():
        dance = row['Name']
        dancers = row['Members'].replace(' ', '').split('\n')
        dancers_by_dance[dance] = set(dancers)

    return dancers_by_dance


def get_unavailabilities(filename):
    return set(['STAY TONIGHT - CHUNGHA','THE REAL - ATEEZ', 'BAGGY JEANS - NCT U','GINGAMINGAYO - BILLLIE','3D - JUNGKOOK',
    'PRETTY U - SEVENTEEN', 'ON - BTS','SIMON SAYS - NCT 127','GOD OF LIGHT MUSIC - SEVENTEEN']), set(['PLZ DONT BE SAD - HIGHLIGHT', 'MANIAC - VIVIZ'])



def get_openers_and_closers(dances, not_free_on_day_one, not_free_on_day_two):
    dances_by_index = list(sorted([dance for dance in dances]))
    used_dances = set()
    def print_options():
        for i, dance in enumerate(dances_by_index):
            print(f'[{i}] {dance}')

    def read_dance(day, act, opener_or_closer, unallowed_dances):
        opener_or_closer = 'Opener' if opener_or_closer else 'Closer'
        print(f'{opener_or_closer} for day {day} act {act}?')

        while True:
            try:
                index = int(input())
                dance = dances_by_index[index]

                if dance in used_dances:
                    print('You used that option already')
                    raise ValueError()

                if dance in unallowed_dances:
                    print(f'That dance can\'t be scheduled on day {day}')
                    raise ValueError()

                used_dances.add(dance)
                return dance
            except Exception:
                print(f'Put in a valid int between 0 and {len(dances) - 1}, here are the options again:')
                print_options()

    print('Dance options:')
    print_options()

    openers_and_closers = []
    for day in [1, 2]:
        openers_and_closers_for_this_day = []
        unallowed_dances = not_free_on_day_one if day == 1 else not_free_on_day_two

        for act in [1, 2]:
            opener = read_dance(day, act, True, unallowed_dances)
            closer = read_dance(day, act, False, unallowed_dances)
            openers_and_closers_for_this_day.append((opener, closer))

        openers_and_closers.append(openers_and_closers_for_this_day)

    return openers_and_closers


def partition_dances_into_days(
    dances,
    not_free_on_day_one,
    not_free_on_day_two
):
    for dance in not_free_on_day_one:
        if dance in not_free_on_day_two:
            fail(f'{dance} can\'t be scheduled on either day')

    total_dances = len(dances)
    day_one_dances = set(not_free_on_day_two)
    day_two_dances = set(not_free_on_day_one)

    if len(day_one_dances) >= ceil(total_dances/2) and len(day_two_dances) >= ceil(total_dances/2):
        fail(f'Due to availabilities, it\'s impossible to schedule dances such that they\'re balanced among days')

    day_one_desired_count = ceil(total_dances/2)
    day_two_desired_count = floor(total_dances/2)
    if len(day_two_dances) > day_two_desired_count:
        day_one_desired_count -= 1
        day_two_desired_count += 1

    remaining_dances = list(filter(lambda dance: dance not in day_one_dances and dance not in day_two_dances, dances))
    day_one_dances = day_one_dances.union(random.sample(remaining_dances, day_one_desired_count - len(day_one_dances)))
    day_two_dances = day_two_dances.union(filter(lambda dance: dance not in day_one_dances, remaining_dances))

    return day_one_dances, day_two_dances


def solve_act(dancers_by_dance, opener, closer, other_dances):
    dances_by_index = [opener, closer] + list(other_dances)
    index_by_dance = {}
    for i, dance in enumerate(dances_by_index):
        index_by_dance[dance] = i

    n = 2 + len(other_dances)
    transitions = [[[] for _j in range(n + 1)] for _i in range(n + 1)]
    for i in range(n + 1):
        i_dancers = set() if i == n else dancers_by_dance[dances_by_index[i]]
        for j in range(n + 1):
            j_dancers = set() if j == n else dancers_by_dance[dances_by_index[j]]
            for k in range(n):
                k_dancers = dancers_by_dance[dances_by_index[k]]
                if len(j_dancers.intersection(k_dancers)) != 0:
                    continue

                dancers_with_one_dance_break = list(filter(lambda dancer: dancer in i_dancers, k_dancers))
                transitions[i][j].append((k, len(dancers_with_one_dance_break)))

    dp = [[[(float('inf'), None) for _j in range(n + 1)] for _i in range(n + 1)] for _m in range(pow(2, n))]
    dp[1][n][0] = (0, n)
    for m in range(1, 1 << n):
        for i in range(n + 1):
            for j in range(n + 1):
                cur_weight, last = dp[m][i][j]
                if last is None:
                    continue

                for k, w in transitions[i][j]:
                    if m & (1 << k) == 0:
                        nxt = m | (1 << k)
                        dp[nxt][j][k] = min(dp[nxt][j][k], (cur_weight + w, i))

    best_weight = min([dp[(1 << n) - 1][i][1][0] for i in range(n + 1)])
    if best_weight == float('inf'):
        return None, best_weight

    for i in range(n + 1):
        if dp[(1 << n) - 1][i][1][0] == best_weight:
            cur_mask, cur_i, cur_j = (1 << n) - 1, i, 1
            path = [closer]
            while cur_i != n:
                path.append(dances_by_index[cur_i])
                prev_i = dp[cur_mask][cur_i][cur_j][1]
                cur_mask -= (1 << cur_j)
                cur_j = cur_i
                cur_i = prev_i

            return list(reversed(path)), best_weight


def solve_day_once(
    dancers_by_dance,
    remaining_dances,
    act_1_opener,
    act_1_closer,
    act_2_opener,
    act_2_closer,
    _
):
    act_1_remaining_dances = set(random.sample(remaining_dances, floor(len(remaining_dances)/2)))
    act_2_remaining_dances = set(filter(lambda dance: dance not in act_1_remaining_dances, remaining_dances))

    act_1_order, act_1_weight = solve_act(dancers_by_dance, act_1_opener, act_1_closer, act_1_remaining_dances)
    if act_1_order is not None:
        act_2_order, act_2_weight = solve_act(dancers_by_dance, act_2_opener, act_2_closer, act_2_remaining_dances)

    if act_1_order is not None and act_2_order is not None:
        return act_1_order, act_2_order, act_1_weight + act_2_weight

    return None, None, float('inf')


def solve_day(dances, dancers_by_dance, opener_and_closers):
    with Pool() as p:
        act_1_opener, act_1_closer = opener_and_closers[0]
        act_2_opener, act_2_closer = opener_and_closers[1]

        remaining_dances = list(filter(lambda dance: dance not in [act_1_opener, act_1_closer, act_2_opener, act_2_closer], dances))
        f = partial(
            solve_day_once,
            dancers_by_dance,
            remaining_dances,
            act_1_opener,
            act_1_closer,
            act_2_opener,
            act_2_closer
        )

        solutions = p.map(f, range(ACT_ITERATIONS))

    return min(solutions, key=lambda sol: sol[2])


def main():
    dancers_by_dance = get_dancers_by_dance(DANCERS_BY_DANCE_FILENAME)
    not_free_on_day_one, not_free_on_day_two = get_unavailabilities('asdfasdf')

    dances = set(dancers_by_dance.keys())
    day_one_opener_and_closers, day_two_opener_and_closers = get_openers_and_closers(dances, not_free_on_day_one, not_free_on_day_two)

    for o in [day_one_opener_and_closers, day_two_opener_and_closers]:
        for opener, closer in o:
            dances.remove(opener)
            dances.remove(closer)

    best_weight, best_day_one, best_day_two = float('inf'), None, None
    for i in range(DAY_ITERATIONS):
        print(f'Attempt {i}')

        day_one_dances, day_two_dances = partition_dances_into_days(
            dances,
            not_free_on_day_one,
            not_free_on_day_two
        )

        day_one_act_1, day_one_act_2, day_one_weight = solve_day(day_one_dances, dancers_by_dance, day_one_opener_and_closers)
        if day_one_act_1 is not None:
            day_two_act_1, day_two_act_2, day_two_weight = solve_day(day_two_dances, dancers_by_dance, day_two_opener_and_closers)

        if day_one_act_1 is not None and day_two_act_1 is not None and day_one_weight + day_two_weight < best_weight:
            best_weight = day_one_weight + day_two_weight
            best_day_one = (day_one_act_1, day_one_act_2)
            best_day_two = (day_two_act_1, day_two_act_2)

        print(f'Current best: {best_weight}')

    if best_weight == float('inf'):
        print('No solutions found :(')
    else:
        print(f'Total number of times someone has to take a 1-dance break: {best_weight}')

        def print_act(act, title):
            print()
            print(f'-- {title} --')

            for i, dance in enumerate(act):
                suffix = ' (opener)' if i == 0 else (' (closer)' if i == len(act) - 1 else '')
                print(f'[{i}] {dance}{suffix}')

        print_act(best_day_one[0], 'Day 1 Act 1')
        print_act(best_day_one[1], 'Day 1 Act 2')
        print_act(best_day_two[0], 'Day 2 Act 1')
        print_act(best_day_two[1], 'Day 2 Act 2')


if __name__ == '__main__':
    main()