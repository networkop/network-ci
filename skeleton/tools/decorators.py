import time
import os


def timer(func):
    def timed(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        total_time = stop-start
        print('\rTotal time: %d minutes, %d seconds' % (total_time/60, total_time % 60))
        return result
    return timed


def progress(function):
    import threading

    def inner(*args, **kwargs):
        run = True
        # if running in Jenkins do not decorate
        if os.environ.get('UNL_IP'):
            return function(*args, **kwargs)

        def print_progress(index=0):
            while run:
                print('\r' + 'Progress' + '.' * index),
                index = 0 if index > 2 else index + 1
                time.sleep(0.5)

        process_print = threading.Thread(target=print_progress)
        process_print.start()
        try:
            return function(*args, **kwargs)
        finally:
            run = False
    return inner


@timer
@progress
def main():
    for x in xrange(3):
        time.sleep(1)
    print('Done')
    return 42

if __name__ == '__main__':
    print("Computing, please wait")
    main()

