import multiprocessing
import time

def task(name, delay):
    print(f"Task {name} bắt đầu")
    time.sleep(delay)
    print(f"Task {name} hoàn thành sau {delay} giây")

if __name__ == '__main__':
    start_time = time.time()
    p1 = multiprocessing.Process(target=task, args=("A", 2))
    p2 = multiprocessing.Process(target=task, args=("B", 1))
    p3 = multiprocessing.Process(target=task, args=("C", 3))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    end_time = time.time()
    print(f"Thời gian hoàn thành: {end_time - start_time} giây")
