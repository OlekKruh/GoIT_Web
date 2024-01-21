import os
from colorama import Fore, Style, init
from multiprocessing import Pool, current_process
import time

init()


def process_directories(root, dirs, files):
    time.sleep(1)
    print(f'{Fore.GREEN}Current Directory:{Style.RESET_ALL} {root}')

    if not dirs and not files:
        print(f'{Fore.RED}Directory is empty.{Style.RESET_ALL}')
    else:
        for directory in dirs:
            print(f'{Fore.BLUE}Subdirectory:{Style.RESET_ALL} {directory}')

        for file in files:
            print(f'{Fore.MAGENTA}File:{Style.RESET_ALL} {file}')

    return f'{Fore.RED}Processed:{Style.RESET_ALL} {root}'


def process(der):
    print(f"{Fore.RED}Current process ID:{Style.RESET_ALL} {os.getpid()}")
    print(f"{Fore.RED}Current process Name:{Style.RESET_ALL} {current_process().name}")
    results = []

    for root, dirs, files in os.walk(der):
        res = process_directories(root, dirs, files)
        results.append(res)
    return results


if __name__ == "__main__":
    command = "C:\\Users\\Alex\\Downloads\\Test"  # input('Enter directory path: ')
    subdirectories = [os.path.join(command, d) for d in os.listdir(command)]

    with Pool(2) as pool:
        result_list = pool.map(process, subdirectories)

    pool.close()
    pool.join()

    for result in result_list:
        for item in result:
            print(item)

    print(f'{Fore.RED}Complete!!!{Style.RESET_ALL}')
