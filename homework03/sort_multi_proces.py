import os
from colorama import Fore, Style, init
from multiprocessing import Pool
import random
import time

init()


def sort_by_extension(path_list):
    print(f"{Fore.MAGENTA}Current process ID:{Style.RESET_ALL} {os.getpid()}")

    start_time1 = time.time()
    delay_time = random.uniform(0.1, 2.0)
    time.sleep(delay_time)

    sorted_files = sorted(os.listdir(path_list), key=lambda x: os.path.splitext(x)[1])
    if len(sorted_files) == 0:
        print(f'{Fore.RED}Directory is Empty.{Style.RESET_ALL}')
    else:
        for file in sorted_files:
            print(f'{file}')

    end_time1 = time.time()
    processing_time1 = end_time1 - start_time1
    print(f'{Fore.GREEN}Sorted finished in {processing_time1:.2f} seconds.{Style.RESET_ALL}')
    return


if __name__ == "__main__":
    start_time = time.time()
    command = "C:\\Users\\Alex\\Downloads\\Test"  # input('Enter directory path: ')
    list_of_dirs = []

    for root, dirs, files in os.walk(command):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            list_of_dirs.append(full_path)

    print(f'{Fore.GREEN}List of subdirectories with full paths:{Style.RESET_ALL}')
    for dir_path in list_of_dirs:
        print(f'{Fore.BLUE}{dir_path}{Style.RESET_ALL}')

    with Pool(3) as pool:
        pool.map(sort_by_extension, list_of_dirs)
        pool.close()
        pool.join()

    end_time = time.time()
    processing_time = end_time - start_time
    print(f'{Fore.YELLOW}Program ENDs. All processes completed.\n'
          f'Total time is: {processing_time:.2f} seconds.{Style.RESET_ALL}')
