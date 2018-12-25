#! /usr/bin/env python3
import random
import math

OUTP_F = "delta_"

N = 100
SERIES_COUNT = 10000
EDGE_COUNT = 30 
FAST_SAMPLE = [0, 1, 3, 5, 7, 10, 12, 15, 17, 20, 22, 25]
SD_SHIFT_MUL = 10
left_b = -1
right_b = 1
default_sigma = 0.1

p_opt_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_jkf_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_sig_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_jsg_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]
p_del_ar = [[0 for j in range(SERIES_COUNT)] for i in range(EDGE_COUNT + 1)]

def generate_dataset():
    x = [-1 + float(right_b - left_b) / N * i for i in range(N)]
    y = [x[i] + random.gauss(0, default_sigma) for i in range(N)]

    return list(zip(x, y))

def print_dataset(dataset):
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
    sigma = math.sqrt(tmp * (size - 1.) / size)

    return (mean_par, sigma)

def par_corr(par_opt, par_j, n):
    par_c = n * par_opt - (n - 1) * par_j
    return (par_c, par_opt - par_c) 

def sigma_lse(dataset, par_opt):
    size = len(dataset)
    sigma = 0
    for i in range(size):
        sigma += (dataset[i][0] * par_opt - dataset[i][1]) ** 2
    return math.sqrt(sigma / (size - 1.))



def shifted_y(dataset_pair, i, j, mul):
    if i != j:
        return dataset_pair[1]
    return dataset_pair[0] + mul * default_sigma

def shifted_dataset(dataset, n, mul):
    return [(dataset[i][0], shifted_y(dataset[i], i, n, mul)) for i in range(len(dataset))]

def iterate(dataset):
    p_opt = lse(dataset)
    ls_sig = sigma_lse(dataset, p_opt)
    jk_res = jackknife(dataset)
    jk_sig = sigma_lse(dataset, jk_res[0])
    delta_par = par_corr(p_opt, jk_res[0], N)[1]
    return (p_opt, jk_res[0], ls_sig, delta_par, jk_sig)

def set_params(i, j, iterate_tuple):
    p_opt_ar[j][i] = iterate_tuple[0]
    p_jkf_ar[j][i] = iterate_tuple[1]
    p_sig_ar[j][i] = iterate_tuple[2]
    p_del_ar[j][i] = iterate_tuple[3]
    p_jsg_ar[j][i] = iterate_tuple[4]

def stage(i, mul):
    dataset = generate_dataset()
    set_params(i, 0, iterate(dataset))

#    for j in range(EDGE_COUNT):
    for j in FAST_SAMPLE:
        new_dataset = shifted_dataset(dataset, j, mul)
        set_params(i, j + 1, iterate(new_dataset))

    if i % (SERIES_COUNT / 100) == 0:
        print("\r{0:.3f}% complete...\t\t".format(float(i) / SERIES_COUNT * 100), end = '')


def get_result():
    with open(OUTP_F + str(SD_SHIFT_MUL) + ".txt", 'w') as f:
        print("#---|-----  LSE -----|-----  JK ------|----- DELTA ----|---- SD_LSE ----|---- SD_J -----")
        lse_value = sum([p_opt_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        jkf_value = sum([p_jkf_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        del_value = sum([p_del_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        sig_value = sum([p_sig_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        jsg_value = sum([p_jsg_ar[0][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
        print("{0:3} | {1:.12f} | {2:.12f} | {3:.12f} | {4:.12f} | {5:.12f}".format(0, lse_value, jkf_value, math.fabs(del_value), jsg_value, sig_value))
        print("----|----------------|----------------|----------------|----------------|---------------")
        #f.write("{0} {1}\n".format(0, math.fabs(del_value)))
        for j in FAST_SAMPLE:
            lse_value = sum([p_opt_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
            jkf_value = sum([p_jkf_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
            del_value = sum([p_del_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
            sig_value = sum([p_sig_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
            jsg_value = sum([p_jsg_ar[j + 1][i] for i in range(SERIES_COUNT)]) / SERIES_COUNT
            print("{0:3} | {1:.12f} | {2:.12f} | {3:.12f} | {4:.12f} | {5:.12f}".format(j + 1, lse_value, jkf_value, math.fabs(del_value), jsg_value, sig_value))
            f.write("{0} {1}\n".format(j + 1, math.fabs(del_value)))


    

if __name__ == '__main__':
    random.seed(25121991)
    for i in range(SERIES_COUNT):
        stage(i, SD_SHIFT_MUL)
    print("Success for #{0}".format(SD_SHIFT_MUL))
    get_result()
#    print("------------------------------------")
#    print("Shifted (25): LSE = ", )
#    new_dataset = shifted_dataset(dataset, 25, 10)
#    iterate(new_dataset)
