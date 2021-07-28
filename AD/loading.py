import time
import threading


def loading(thread):
    """
    :param thread: thread of the main function
    :return: dispays a loading animation while the main function is in progress
    """
    dt = 0.25
    chars1 = ["\r|", "\r\\", "\r-", "\r/"]
    chars2 = ["\r", "\r|", "\r||", "\r|||", "\r||||", "\r|||||", "\r ||||", "\r  |||", "\r   ||", "\r    |"]
    chars3 = ["\r", "\r...", "\r:::", "\r|||", "\r:::", "\r..."]
    chars = ["\r[      ]", "\r[|     ]", "\r[||    ]", "\r[|||   ]", "\r[ |||  ]", "\r[  ||| ]", "\r[   |||]",
             "\r[    ||]", "\r[     |]"]
    i = 0
    while thread.is_alive():
        print(chars[i % 9], end='', flush=True)
        time.sleep(dt)
        i += 1


def process_func(a, b, c):
    c[0] = a + b
    time.sleep(10)


def main():
    c = [None]
    process = threading.Thread(target=process_func, args=(1, 2, c))
    process.start()
    loading(process)
    print("\r" + str(c[0]), flush=True)


if __name__ == '__main__':
    main()