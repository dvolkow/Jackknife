#! /usr/bin/env python3
import random
import math

OUTP_F = "dataset.txt"
N = 300
SERIES_COUNT = 1000
EDGE_COUNT = 30 
FAST_SAMPLE = [0, 1, 5, 10, 15, 20, 25]
left_b = -1
right_b = 1
default_sigma = 0.1

p_opt_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_jkf_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_sig_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_del_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]

def generate_dataset():
    random.seed()
    x = [-1 + float(right_b - left_b) / N * i for i in range(N)]
    y = [x[i] + random.gauss(0, default_sigma) for i in range(N)]

    return list(zip(x, y))

def print_dataset(dataset):
    with open(OUTP_F, 'w') as f:
        for pair in dataset:
            f.write('{0:.2f} {1}\n'.format(pair[0], pair[1]))

def lse(dataset):
    x_x = 0.
    x_y = 0.
    for pair in dataset:
        x_x += pair[0] * pair[0]
        x_y += pair[0] * pair[1]
    return x_y / x_x


def jackknife(dataset):
    par = 0.
    size = len(dataset)
    for i in range(size):
        par += lse([dataset[j] for j in range(size) if j != i])
    mean_par = par / size
    tmp = 0
    for i in range(size):
        par = lse([dataset[j] for j in range(size) if j != i])
        tmp += (par - mean_par) ** 2
    sigma = math.sqrt((size - 1.) / size * tmp)

    return (mean_par, sigma)

def par_corr(par_opt, par_j, n):
    par_c = n * par_opt - (n - 1) * par_j
    return (par_c, par_opt - par_c) 

def shifted_y(dataset_pair, i, j, mul):
    if i != j:
        return dataset_pair[1]
    return dataset_pair[0] + mul * default_sigma

def shifted_dataset(dataset, n, mul):
    return [(dataset[i][0], shifted_y(dataset[i], i, n, mul)) for i in range(len(dataset))]

def iterate(dataset):
    print_dataset(dataset)
    p_opt = lse(dataset)
    jk_res = jackknife(dataset)
    delta_par = par_corr(p_opt, jk_res[0], N)[1]
    return (p_opt, jk_res[0], jk_res[1], delta_par)

def set_params(i, j, iterate_tuple):
    p_opt_ar[j][i] = iterate_tuple[0]
    p_jkf_ar[j][i] = iterate_tuple[1]
#    p_sig_ar[j][i] = iterate_tuple[2]
    p_del_ar[j][i] = iterate_tuple[3]

def stage(i, mul):
    dataset = generate_dataset()
    set_params(i, 0, iterate(dataset))

#    for j in range(EDGE_COUNT):
    for j in FAST_SAMPLE:
        new_dataset = shifted_dataset(dataset, j, mul)
        set_params(i, j + 1, iterate(new_dataset))

    if i % (SERIES_COUNT / 100) == 0:
        print("\r{0:.3f}% complete...".format(float(i) / SERIES_COUNT * 100), end = '')


def get_result():
    print("#---|---  LSE ---|---- JK ----|-- DELTA --")
    lse_value = sum([p_opt_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
    jkf_value = sum([p_jkf_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
    del_value = sum([p_del_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
    print("{0:3} | {1:.8f} | {2:.8f} | {3:.8f}".format(0, lse_value, jkf_value, del_value))
    for j in FAST_SAMPLE:
        lse_value = sum([p_opt_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        jkf_value = sum([p_jkf_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        del_value = sum([p_del_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        print("{0:3} | {1:.8f} | {2:.8f} | {3:.8f}".format(j + 1, lse_value, jkf_value, del_value))


    

if __name__ == '__main__':
    for i in range(SERIES_COUNT):
        stage(i, 10)
    print("Success")
    get_result()
#    print("------------------------------------")
#    print("Shifted (25): LSE = ", )
#    new_dataset = shifted_dataset(dataset, 25, 10)
#    iterate(new_dataset)
