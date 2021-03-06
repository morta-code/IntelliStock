__author__ = 'polpe'

import numpy as np


def last_n_time_data(ts: np.array, n: int=5, maxtimeint: float=1):
    class S:
        size = ts.shape[1]
        index = size - 1
        clip = np.zeros((2, n), dtype=float)

    def shift_back():
        while S.clip[0,0] == ts[0,S.index]:
            S.index = S.index - 1
            # print('                                            equal = ', clip[0,0] == ts[0,s.index],clip[0,0], ts[0,s.index])

    def append_new_clip():
        # print('                      should be NOT         equal = ', clip[0,0] == ts[0,s.index],clip[0,0], ts[0,s.index])
        shift_back()
        S.clip = np.roll(S.clip, shift=1 ,axis=1)
        S.clip[:,0] = ts[:,S.index]
        # print(clip)
        S.index -= 1

    def min_max_dist():
        mi = 10  # 10 year
        ma = 0
        for i in range(n-1):
            dt = S.clip[0, i+1] - S.clip[0, i]
            if dt > ma:
                ma = dt
            if dt < mi:
                mi = dt
        return mi, ma

    def check_validity():
        for i in range(n-1):
            if not S.clip[0, i] < S.clip[0, i+1]:
                print(S.size, S.index, S.clip, sep='--\n')
                raise AssertionError

    for i in range(n):
        append_new_clip()
    while S.index > 0:
        check_validity()
        mm = min_max_dist()
        if mm[1] < maxtimeint:
            yield (S.clip, 0)
        # else:
        #     print('This instance has too large time intervals between measurements: ', s.clip, 'index = ' + str(s.index), sep='--\n')
        append_new_clip()


def create_training_test_set(ts: np.array, nr_samples: int, nr_features: int, dt_between: float):
    target = set()
    gen = last_n_time_data(ts, nr_features+1)
    xx = np.zeros((nr_samples, nr_features))
    y = np.zeros(nr_samples)
    t = np.zeros_like(y)
    print("Len.ts:", ts.shape)
    clip = next(gen)[0]
    tclip = tuple(clip[1, :nr_features])

    xx_test = np.zeros((nr_samples, nr_features))
    y_test = np.zeros(nr_samples)
    t_test = np.zeros_like(y)
    tclip_test = tuple(clip[1, :nr_features])
    j = 0
    for i in range(nr_samples):
        xx[i, :] = clip[1, :nr_features]
        y[i] = clip[1, nr_features]
        t[i] = clip[0, nr_features]

        test = True
        while t[i] - clip[0, nr_features] < dt_between:
            if test and (t[i] - clip[0, nr_features] > dt_between / 2):
                test = False
                xx_test[j, :] = clip[1, :nr_features]
                y_test[j] = clip[1, nr_features]
                t_test[j] = clip[0, nr_features]
                j += 1

            target.add(tclip)
            while tclip in target:
                try:
                    clip = next(gen)[0]
                    tclip = tuple(clip[1, :nr_features])
                except StopIteration:
                    return xx[i::-1, :], y[i::-1], t[i::-1], xx_test[j::-1], y_test[j::-1], t[j::-1]
    return xx[::-1, :], y[::-1], t[::-1], xx_test[j::-1], y_test[j::-1], t[j::-1]


def create_training_set(ts: np.array, nr_samples: int=100, nr_features: int=4, nr_steps_between: int=1):
    target = set()
    gen = last_n_time_data(ts, nr_features+1)
    xx = np.zeros((nr_samples, nr_features))
    y = np.zeros(nr_samples)
    t = np.zeros_like(y)
    clip = next(gen)[0]
    tclip = tuple(clip[1, :nr_features])
    for i in range(nr_samples):
        xx[i,:] = clip[1, :nr_features]
        y[i] = clip[1, nr_features]
        t[i] = clip[0, nr_features]
        for it in range(nr_steps_between):
            target.add(tclip)
            while tclip in target:
                try:
                    clip = next(gen)[0]
                    tclip = tuple(clip[1, :nr_features])
                except StopIteration:
                    return xx[i::-1, :], y[i::-1], t[i::-1]
    return xx[::-1, :], y[::-1], t[::-1]


def create_training_set_2(ts: np.array, nr_samples: int, nr_features: int, dt_between: float):
    target = set()
    gen = last_n_time_data(ts, nr_features+1)
    xx = np.zeros((nr_samples, nr_features))
    y = np.zeros(nr_samples)
    t = np.zeros_like(y)
    clip = next(gen)[0]
    tclip = tuple(clip[1, :nr_features])
    for i in range(nr_samples):
        xx[i,:] = clip[1, :nr_features]
        y[i] = clip[1, nr_features]
        t[i] = clip[0, nr_features]
        while t[i] - clip[0, nr_features] < dt_between:
            target.add(tclip)
            while tclip in target:
                try:
                    clip = next(gen)[0]
                    tclip = tuple(clip[1, :nr_features])
                except StopIteration:
                    return xx[i::-1, :], y[i::-1], t[i::-1]
    return xx[::-1, :], y[::-1], t[::-1]


# def create_training_set_2(ts: np.array, nr_samples: int, nr_features: int, dt_between: float):
#     gen = last_n_time_data(ts, nr_features+1)
#     xx = np.zeros((nr_samples, nr_features))
#     y = np.zeros(nr_samples)
#     t = np.zeros_like(y)
#     clip = next(gen)[0]
#     for i in range(nr_samples):
#         xx[i, :] = clip[1, :nr_features]
#         y[i] = clip[1, nr_features]
#         t[i] = clip[0, nr_features]
#         while t[i] - clip[0, nr_features] < dt_between:
#             try:
#                 clip = next(gen)[0]
#             except StopIteration:
#                 return xx[i::-1, :], y[i::-1], t[i::-1]
#     return xx[::-1, :], y[::-1], t[::-1]
