import time
import os
import tempfile
import sys
import random

def run_cpu_benchmark(iterations=10_000_000):
    """
    Measures CPU performance by performing a series of simple arithmetic operations.
    This simulates a CPU-bound workload, useful for assessing raw processing power.
    """
    start_time = time.perf_counter()
    result = 0
    for i in range(iterations):
        # Perform a simple, CPU-intensive calculation
        result += (i * 2 + 1) % 7 
    end_time = time.perf_counter()
    return end_time - start_time

def run_memory_benchmark(size_mb=512):
    """
    Measures memory allocation and access speed by creating a large list
    and performing operations on it. This simulates a memory-bound workload.
    """
    # Approximate number of elements needed for the desired memory size
    # (assuming an integer takes roughly 8 bytes in a Python list)
    num_elements = (size_mb * 1024 * 1024) // 8 
    if num_elements < 1_000_000: # Ensure a reasonable minimum for the test
        num_elements = 1_000_000

    start_time = time.perf_counter()
    # Allocate and fill a large list with random integers
    data = [random.randint(0, 1000) for _ in range(int(num_elements))]
    # Access and sum all elements to ensure the data is actively used
    total_sum = sum(data)
    end_time = time.perf_counter()
    # Use total_sum to prevent potential compiler/interpreter optimizations
    _ = total_sum 
    return end_time - start_time

def run_disk_benchmark(file_size_mb=200):
    """
    Measures disk I/O performance (write and read) by creating and reading a temporary file.
    This simulates disk-bound operations, crucial for database or file-serving applications.
    """
    # Generate a byte string to write to the file
    data_to_write = b'X' * (file_size_mb * 1024 * 1024) # Convert MB to bytes

    write_time = 0
    read_time = 0
    temp_file_path = None

    try:
        # Create a temporary file for disk operations
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            # Measure write time
            start_time = time.perf_counter()
            temp_file.write(data_to_write)
            temp_file.flush() # Ensure data is written from buffer to OS cache
            os.fsync(temp_file.fileno()) # Force OS to flush buffers to physical disk
            end_time = time.perf_counter()
            write_time = end_time - start_time

        # Measure read time
        start_time = time.perf_counter()
        with open(temp_file_path, 'rb') as temp_file:
            read_data = temp_file.read()
        end_time = time.perf_counter()
        read_time = end_time - start_time

        # Basic verification of data integrity
        if read_data != data_to_write:
            print("Warning: Disk benchmark data mismatch!")

    finally:
        # Clean up the temporary file regardless of test outcome
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return write_time, read_time

def main():
    print("--- VPS Performance Benchmark ---")
    print(f"Python Version: {sys.version.split(' ')[0]}")
    print(f"Platform: {sys.platform}\n")

    print("Running CPU benchmark (simple arithmetic operations)...")
    cpu_time = run_cpu_benchmark()
    print(f"  CPU Benchmark Time: {cpu_time:.4f} seconds\n")

    print("Running Memory benchmark (allocating and summing a large list)...")
    memory_time = run_memory_benchmark()
    print(f"  Memory Benchmark Time: {memory_time:.4f} seconds\n")

    print("Running Disk I/O benchmark (writing and reading a temporary file)...")
    write_time, read_time = run_disk_benchmark()
    print(f"  Disk Write Benchmark Time: {write_time:.4f} seconds")
    print(f"  Disk Read Benchmark Time: {read_time:.4f} seconds\n")

    print("--- Benchmark Complete ---")
    print("These results provide a basic indication of your system's performance.")
    print("For comprehensive and production-grade benchmarking, specialized tools are recommended.")

if __name__ == "__main__":
    main()
