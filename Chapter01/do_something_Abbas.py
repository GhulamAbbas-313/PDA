import math

def do_something(size, out_list):
    """Heavy computation function (CPU-bound)."""
    for i in range(size):
        # Har number ka square nikal kar uska square root add kar rahe hain
        out_list.append(math.sqrt(i ** 2))
