# Mini Project: Square Calculator using Multiprocessing (Chapter 3)

import multiprocessing
import time
import os

# ====== Function for Child Process ======
def calculate_square(numbers, conn):
    """Function executed in each process to calculate squares"""
    process_id = os.getpid()
    print(f"[Process {process_id}] Started...")
    result = []

    for n in numbers:
        square = n * n
        print(f"[Process {process_id}] {n}² = {square}")
        result.append(square)
        time.sleep(0.3)

    conn.send(result)  # send result to parent
    conn.close()
    print(f"[Process {process_id}] Finished.")


# ====== MAIN PROGRAM ======
if __name__ == '__main__':
    print("=== Square Calculator (Process Based Parallelism) ===\n")

    # Input data
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    mid = len(data)//2

    # Create two pipes (for communication)
    parent_conn1, child_conn1 = multiprocessing.Pipe()
    parent_conn2, child_conn2 = multiprocessing.Pipe()

    # Divide work between two processes
    process1 = multiprocessing.Process(target=calculate_square, args=(data[:mid], child_conn1))
    process2 = multiprocessing.Process(target=calculate_square, args=(data[mid:], child_conn2))

    start_time = time.time()

    # Start processes
    process1.start()
    process2.start()

    # Get data from both child processes
    result1 = parent_conn1.recv()
    result2 = parent_conn2.recv()

    # Wait for processes to complete
    process1.join()
    process2.join()

    # Combine results
    all_results = result1 + result2
    print("\nFinal Combined Squares:", all_results)

    print(f"\n✅ Total Execution Time: {round(time.time() - start_time, 2)} seconds")
    print("=== Program Finished ===")
# 🔹 1. Concept:

# Miss, ye project Process-Based Parallelism dikhata hai.
# Normally jab hum program chalate hain to sab code ek ke baad ek linearly run hota hai (isko kehte hain sequential execution).

# Lekin parallel execution me hum ek se zyada kaam ek sath multiple CPU cores par chala sakte hain.
# Ye kaam multiprocessing module karta hai.

# 🔹 2. Process kya hota hai?

# Process ek independent program hota hai jo apna memory space aur CPU time use karta hai.
# Agar hum 2 processes banayein to dono independent chalenge aur ek dusre ko disturb nahi karenge.

# Yahan har process apni list of numbers ka square calculate karta hai.

# 🔹 3. Pipe kya hoti hai?

# Pipe ek communication channel hoti hai jahan ek process data send karta hai aur doosra process usko receive karta hai.

# Is project me har child process apna result Pipe ke zariye parent process ko bhejta hai.