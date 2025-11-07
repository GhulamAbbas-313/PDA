import logging
import threading
import time
import random
import os
from threading import Thread, Barrier

# ========== GLOBAL CONFIG ==========
LOG_FORMAT = '%(asctime)s | %(threadName)-15s | %(levelname)-8s | %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


# ===================================================
# 1️⃣ Semaphore Example: Producer & Consumer
# ===================================================
semaphore = threading.Semaphore(0)
item = 0

def consumer():
    """Consumer waits for producer to produce an item."""
    logging.info("Consumer is waiting for an item...")
    semaphore.acquire()  # waits until producer releases
    logging.info(f"Consumer consumed item: {item}")

def producer():
    """Producer produces an item and notifies consumer."""
    global item
    time.sleep(1)
    item = random.randint(1, 100)
    logging.info(f"Producer produced item: {item}")
    semaphore.release()  # notify consumer


# ===================================================
# 2️⃣ Lock Example: Using a Lock to Avoid Conflict
# ===================================================
threadLock = threading.Lock()

class MyThreadClass (Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration

    def run(self):
        """Thread safely prints using Lock."""
        threadLock.acquire()
        logging.info(f"{self.name} running (PID {os.getpid()})")
        threadLock.release()
        time.sleep(self.duration)
        logging.info(f"{self.name} finished")


# ===================================================
# 3️⃣ RLock Example: Add/Remove Items Safely
# ===================================================
class Box:
    def __init__(self):
        self.lock = threading.RLock()
        self.total_items = 0

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.execute(1)

    def remove(self):
        with self.lock:
            self.execute(-1)

def adder(box, items):
    """Add items safely using RLock"""
    while items:
        box.add()
        logging.info(f"Added one item, remaining to add: {items-1}")
        items -= 1
        time.sleep(0.5)

def remover(box, items):
    """Remove items safely using RLock"""
    while items:
        box.remove()
        logging.info(f"Removed one item, remaining to remove: {items-1}")
        items -= 1
        time.sleep(0.5)


# ===================================================
# 4️⃣ Event Example: Producer & Consumer with Event
# ===================================================
items = []
event = threading.Event()

class ProducerEvent(threading.Thread):
    def run(self):
        for i in range(3):
            time.sleep(1)
            item = random.randint(1, 50)
            items.append(item)
            logging.info(f"Event Producer added: {item}")
            event.set()
            event.clear()

class ConsumerEvent(threading.Thread):
    def run(self):
        while True:
            time.sleep(2)
            event.wait()
            if items:
                consumed = items.pop()
                logging.info(f"Event Consumer used: {consumed}")


# ===================================================
# 5️⃣ Barrier Example: Race Simulation
# ===================================================
runners = ['Huey', 'Dewey', 'Louie']
finish_line = Barrier(3)

def runner():
    name = runners.pop()
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time)
    logging.info(f"{name} reached finish line after {sleep_time}s")
    finish_line.wait()

# ===================================================
# 🧠 MAIN FUNCTION
# ===================================================
def main():
    logging.info("=== DEMO START: Thread Synchronization ===")

    # Semaphore demo
    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start(); c.start()
    p.join(); c.join()

    # Lock demo
    threads = [MyThreadClass(f"Thread-{i}", random.randint(1,3)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()

    # RLock demo
    box = Box()
    t1 = threading.Thread(target=adder, args=(box, 3))
    t2 = threading.Thread(target=remover, args=(box, 3))
    t1.start(); t2.start()
    t1.join(); t2.join()

    # Event demo
    prod = ProducerEvent()
    cons = ConsumerEvent()
    prod.start(); cons.start()
    prod.join()

    # Barrier demo
    race_threads = [Thread(target=runner) for _ in range(3)]
    for r in race_threads: r.start()
    for r in race_threads: r.join()

    logging.info("=== DEMO END ===")

# ===================================================
if __name__ == "__main__":
    main()
# 1️⃣ Semaphore Example

# Code part: producer() aur consumer()

# 🔹 Explanation:

# Producer ek item banata hai.

# Consumer tab tak wait karta hai jab tak producer usko signal na de (semaphore.release()).

# semaphore.acquire() ka matlab — “ruk ja jab tak permission na mile”.

# 🧾 Output me kya hota hai:
# Consumer is waiting for an item...
# Producer produced item: 42
# Consumer consumed item: 42

# 🔸 Miss ko bol:

# “Miss, yahan producer ek item banata hai aur semaphore ke zariye consumer ko notify karta hai. Ye synchronization ensure karta hai ke consumer tab tak wait kare jab tak producer item ready na kare.”

# 2️⃣ Lock Example

# Code part: MyThreadClass

# 🔹 Explanation:

# Teen threads (Thread-0, Thread-1, Thread-2) ek sath run karte hain.

# threadLock.acquire() ensure karta hai ke ek time me sirf ek thread log kare.

# Agar lock na hota to teenon threads ek sath print karte aur output overlap hota.

# 🧾 Output example:
# Thread-0 running (PID 15360)
# Thread-0 finished
# Thread-1 running (PID 15360)
# Thread-1 finished
# Thread-2 running (PID 15360)
# Thread-2 finished

# 🔸 Miss ko bol:

# “Lock ka use is liye kiya gaya hai ke ek waqt me sirf ek thread console par likhe. Isse data aur output mix nahi hota.”

# 3️⃣ RLock Example

# Code part: Box class, adder() aur remover()

# 🔹 Explanation:

# RLock Recursive Lock hai — ek thread lock ko dobara le sakta hai bina deadlock ke.

# adder() items add karta hai, remover() remove karta hai safely.

# 🧾 Output example:
# Added one item, remaining to add: 2
# Removed one item, remaining to remove: 2
# Added one item, remaining to add: 1
# Removed one item, remaining to remove: 1

# 🔸 Miss ko bol:

# “RLock tab use hota hai jab ek hi thread ko multiple baar lock acquire karna padta hai — yahan ek box me item safely add aur remove karne ke liye.”

# 4️⃣ Event Example

# Code part: ProducerEvent aur ConsumerEvent

# 🔹 Explanation:

# ProducerEvent items list me item add karta hai.

# event.set() consumer ko signal karta hai ke naya item available hai.

# ConsumerEvent event ka wait karta hai aur fir item consume karta hai.

# 🧾 Output example:
# Event Producer added: 23
# Event Consumer used: 23
# Event Producer added: 45
# Event Consumer used: 45

# 🔸 Miss ko bol:

# “Event synchronization ek notification system jaisa hai — producer jab naya data deta hai to event trigger karta hai aur consumer tab process karta hai.”

# 5️⃣ Barrier Example

# Code part: runner() function

# 🔹 Explanation:

# 3 runners ek race me hain (Huey, Dewey, Louie).

# Har runner finish line par wait karta hai jab tak sab 3 wahan na pohonch jaayein.

# Barrier(3) ka matlab — sab 3 threads synchronize hone tak wait karo.

# 🧾 Output example:
# Louie reached finish line after 1s
# Dewey reached finish line after 2s
# Huey reached finish line after 3s

# 🔸 Miss ko bol:

# “Barrier ek coordination point hoti hai — ye ensure karta hai ke sab threads ek certain stage par aake ek sath proceed karein.”