import time
import os
from multiprocessing import Pool
from colorama import Fore, Style, init

init()


def factorize(number, dividers):
    time.sleep(0.5)
    print(f"{Fore.MAGENTA}Current process ID:{Style.RESET_ALL} {os.getpid()}")
    res_list = []
    for divider in dividers:
        if number % divider == 0:
            res_list.append(divider)
    return res_list


if __name__ == "__main__":
    start_time = time.time()
    x = (126, 256, 99990, 10651160)

    y = [
        [1, 2, 4, 8, 16, 32, 64, 128],
        [1, 3, 5, 15, 17, 51, 85, 255],
        [1, 3, 9, 41, 123, 271, 369, 813,
         2439, 11111, 33333, 99999],
        [1, 2, 4, 5, 7, 10, 14, 20, 28, 35,
         70, 140, 76079, 152158, 304316,
         380395, 532553, 760790, 1065106,
         1521580, 2130212, 2662765, 5325530,
         10651060]
    ]

    pairs = [(x[i], y[i]) for i in range(len(x))]

    for pair in pairs:
        result = factorize(*pair)
        print(f'{Fore.BLUE}{result}{Style.RESET_ALL}')

    stop_time1 = time.time()
    delta1 = stop_time1 - start_time
    print(f'{Fore.YELLOW}First test END. Time: {delta1:.10f}{Style.RESET_ALL}\n')

    start_time2 = time.time()
    with Pool() as pool:
        results = pool.starmap(factorize, pairs)
        pool.close()
        pool.join()

    for result in results:
        print(f'{Fore.BLUE}{result}{Style.RESET_ALL}')

    stop_time2 = time.time()
    delta2 = stop_time2 - start_time2
    print(f'{Fore.YELLOW}Second test END. Time: {delta2:.10f}{Style.RESET_ALL}\n')