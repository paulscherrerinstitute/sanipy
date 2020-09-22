from colorama import Fore


RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW


def colored(color, msg):
    return color + str(msg) + Fore.RESET



