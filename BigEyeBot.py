import datetime,time
import threading
from adapters import infoVk

######  Main loop ######

def example():
    info = infoVk('put here vk id')
    print(info.getInfo())


if __name__ == '__main__':
    example()
