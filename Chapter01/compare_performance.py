import time
import threading
import multiprocessing
from do_something import do_something

size = 1000000   # kitne numbers process karne hain
tasks = 10       # kitni baar function run karna hai


# ---------------- SERIAL EXECUTION ----------------
def serial_execution():
    start = time.time()
    for _ in range(tasks):
        out = []
        do_something(size, out)
    print("Serial Time:", round(time.time() - start, 3), "seconds")


# ---------------- MULTITHREADING EXECUTION ----------------
def threading_execution():
    start = time.time()
    threads = []

    for _ in range(tasks):
        out = []
        # Important: 'target' me sirf function ka naam dete hain, call nahi karte
        t = threading.Thread(target=do_something, args=(size, out))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Multithreading Time:", round(time.time() - start, 3), "seconds")


# ---------------- MULTIPROCESSING EXECUTION ----------------
def multiprocessing_execution():
    start = time.time()
    processes = []

    for _ in range(tasks):
        out_list = []  # normal list use karo (Manager ki zarurat nahi)
        # har process alag run hoga, to shared memory ki problem nahi
        p = multiprocessing.Process(target=do_something, args=(size, out_list))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("Multiprocessing Time:", round(time.time() - start, 3), "seconds")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("\n--- Performance Comparison Project ---")
    print("Testing with size =", size, "and tasks =", tasks, "\n")

    serial_execution()
    threading_execution()
    multiprocessing_execution()

    print("\nAll tasks complete ✅")
