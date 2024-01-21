import os
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
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


def process_in_thread(der):
    with ThreadPoolExecutor() as exe:
        for root, dirs, files in os.walk(der):
            element = exe.submit(process_directories, root, dirs, files)
            order.append(element)


if __name__ == "__main__":
    command = input('Enter directory path: ')
    order = []

    with ThreadPoolExecutor() as executor:
        for directory in [os.path.join(command, d) for d in os.listdir(command)]:
            process_in_thread(directory)

    for item in order:
        item.result()

    print(f'{Fore.RED}Complete!!!{Style.RESET_ALL}')
