import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib
import heapq
import copy
import math
from typing import NoReturn, Tuple, List

iterations_number = 100
slots_number_values = [100, 500, 1000]

def generate_queue(alpha, len):
    return np.random.exponential(alpha, len).tolist()


def generate_client_time(alpha):
    return np.random.exponential(alpha)


def estimate_two_slots(alpha, len):
    estimation = [0] * len
    for _ in range(iterations_number):
        estimation = [sum(x) for x in zip(estimation, sorted(generate_queue(1/alpha, len)))]
    estimation[:] = [x / iterations_number for x in estimation]
    return estimation


def conduct_experiment(number_of_slots, alpha, queue_len):
    queue = generate_queue(1/alpha, number_of_slots)
    heapq.heapify(queue)
    wait_time = [0] * number_of_slots
    for _ in range(number_of_slots, queue_len):
        cur_time = heapq.heappop(queue)
        wait_time.append(cur_time)
        heapq.heappush(queue, generate_client_time(1/alpha) + cur_time)
    return wait_time


def estimate(number_of_slots, alpha, queue_len):
    estimation = [0] * queue_len
    for _ in range(iterations_number):
        estimation = [sum(x) for x in zip(estimation, conduct_experiment(number_of_slots, alpha, queue_len))]
    estimation[:] = [x / iterations_number for x in estimation]
    return estimation


def show_plot_alpha(number_of_customers, alpha):
    for slot_number_value in slots_number_values:
        estimations = estimate(slot_number_value, alpha, number_of_customers)
        plt.plot(range(0, number_of_customers), estimations, label = 'число окон = ' + str(slot_number_value))
    plt.xlabel('номер человека в очереди')
    plt.ylabel('время ожидания')
    plt.title('Каждое окно принимает произвольное число человек: alpha = ' + str(alpha))
    plt.legend()
    plt.show()


def show_plot_two_slots_alpha(alpha):
    for slot_number_value in slots_number_values:
        estimations = estimate_two_slots(alpha, slot_number_value)
        plt.plot(range(0, slot_number_value), estimations,label = 'число окон = ' + str(slot_number_value))
    plt.xlabel('номер человека в очереди')
    plt.ylabel('время ожидания')
    plt.title('Каждое окно принимает не более 2 человек: alpha = ' + str(alpha))
    plt.legend()
    plt.show()


show_plot_two_slots_alpha(1)
show_plot_two_slots_alpha(1/2)
show_plot_two_slots_alpha(2)
show_plot_alpha(3000, 1)
show_plot_alpha(3000, 1/2)
show_plot_alpha(3000, 2)