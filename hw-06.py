import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib

iterations_number = 2000

def chi_based_interval(y, scale, sample_numb):
    sum = np.sum(np.square(np.random.normal(0, scale, sample_numb)))
    right_bound = sum / scipy.stats.chi2.ppf((1 - y) / 2, sample_numb)
    left_bound = sum / scipy.stats.chi2.ppf((1 + y) / 2, sample_numb)
    return right_bound - left_bound

def normal_based_interval(y, scale, sample_numb):
    mean_squared = (np.mean(np.random.normal(0, scale, sample_numb))) ** 2
    right_bound = sample_numb * mean_squared / (scipy.stats.norm.ppf((3 - y) / 4) ** 2)
    left_bound = sample_numb * mean_squared / (scipy.stats.norm.ppf((3 + y) / 4) ** 2)
    return right_bound - left_bound

def estimate(func, y, scale, sample_numb):
    sum = 0
    for i in range(iterations_number):
        sum += func(y, scale, sample_numb)
    return sum / iterations_number

def show_plot(func, y, scale, number_of_samples, type):
    estimations = []
    for sample_number in number_of_samples:
        estimations.append(estimate(func, y, scale, sample_number))
    plt.plot(number_of_samples, estimations, label = 'y = ' + str(y) + ', scale = ' + str(scale))
    plt.xlabel('number_of_samples')
    plt.ylabel('interval length')
    plt.title(type)
    plt.legend()
    plt.show()


show_plot(chi_based_interval, 0.1, 1, np.arange(30, 1500, 40), "(a)")
show_plot(normal_based_interval, 0.1, 1, np.arange(30, 1500, 40), "(b)")