# ==============================================
# 🧩 Mini Project: Distributed Data Sharing using MPI
# Demonstrates: Send, Receive, Gather, Broadcast, and All-to-All communication
# ==============================================

from mpi4py import MPI          # Import MPI library for parallel communication
import numpy as np              # Import NumPy for numerical data handling

# ------------------------------------------------
# 🔹 Step 1: Create Communicator and Basic Setup
# ------------------------------------------------
comm = MPI.COMM_WORLD            # Communicator that includes all processes
rank = comm.Get_rank()           # Unique ID (rank) of each process
size = comm.Get_size()           # Total number of processes running

print(f"Process {rank} started among total {size} processes")

# ------------------------------------------------
# 🔹 Step 2: Each process generates its own local data
# ------------------------------------------------
# Each process creates an array of 2 numbers based on its rank
data_to_send = np.arange(rank * 2, (rank + 1) * 2)
print(f"Process {rank} generated data: {data_to_send}")

# ------------------------------------------------
# 🔹 Step 3: All-to-All Communication
# ------------------------------------------------
# Every process sends data to every other process
# Here, each process sends its array and receives an array of same shape
recv_data = np.empty_like(data_to_send)              # Create empty array for received data
comm.Alltoall([data_to_send, MPI.INT], [recv_data, MPI.INT])
print(f"Process {rank} received (AlltoAll): {recv_data}")

# ------------------------------------------------
# 🔹 Step 4: Gather Data at Root Process (Rank 0)
# ------------------------------------------------
# All processes send their data_to_send to the root process (rank 0)
gathered = comm.gather(data_to_send, root=0)

# Only root process prints the gathered data
if rank == 0:
    print("\n✅ Root process (0) gathered all data:")
    for i, d in enumerate(gathered):
        print(f"  From process {i}: {d}")

# ------------------------------------------------
# 🔹 Step 5: Point-to-Point Send and Receive Example
# ------------------------------------------------
# Process 1 sends a message to process 2
if rank == 1:
    message = "Hello from Rank 1"
    comm.send(message, dest=2)
    print("Rank 1 sent message → Rank 2")

# Process 2 receives message from process 1
elif rank == 2:
    received = comm.recv(source=1)
    print(f"Rank 2 received message: {received}")

# ------------------------------------------------
# 🔹 Step 6: Broadcast Example
# ------------------------------------------------
# Root process (rank 0) broadcasts a message to all others
if rank == 0:
    broadcast_data = "Global Sync Message"       # Message to broadcast
else:
    broadcast_data = None                        # Other processes initially have nothing

# Broadcast same message to all processes
broadcast_data = comm.bcast(broadcast_data, root=0)

# Every process prints the received broadcast message
print(f"Process {rank} received broadcast: {broadcast_data}")
