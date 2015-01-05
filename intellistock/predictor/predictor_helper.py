__author__ = 'polpe'

import numpy as np


def last_n_time_data(ts: np.array, n: int=5, maxtimeint: float=0.5 / 365):
    class s:
        size = ts.shape[1]
        index = size - 1
        clip = np.zeros((2,n), dtype=float)

    def shift_back():
        while s.clip[0,0] == ts[0,s.index]:
            s.index = s.index - 1
            # print('                                            equal = ', clip[0,0] == ts[0,s.index],clip[0,0], ts[0,s.index])

    def append_new_clip():
        # print('                      should be NOT         equal = ', clip[0,0] == ts[0,s.index],clip[0,0], ts[0,s.index])
        shift_back()
        s.clip = np.roll(s.clip, shift=1 ,axis=1)
        s.clip[:,0] = ts[:,s.index]
        # print(clip)
        s.index -= 1

    def min_max_dist():
        mi = 10  # 10 year
        ma = 0
        for i in range(n-1):
            dt = s.clip[0, i+1] - s.clip[0, i]
            if dt > ma:
                ma = dt
            if dt < mi:
                mi = dt
        return mi, ma

    def check_validity():
        for i in range(n-1):
            if not s.clip[0,i] < s.clip[0,i+1]:
                print(s.size, s.index, s.clip, sep='--\n')
                raise AssertionError

    for i in range(n):
        append_new_clip()
    while s.index > 0:
        check_validity()
        mm = min_max_dist()
        if mm[1] < maxtimeint:
            yield (s.clip, 0)
        # else:
        #     print('This instance has too large time intervals between measurements: ', s.clip, 'index = ' + str(s.index), sep='--\n')
        append_new_clip()


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
