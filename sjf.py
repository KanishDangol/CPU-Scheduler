from collections import deque

class Process:
    def __init__(self, pid, bursts):
        self.pid = pid  # Process ID
        self.bursts = bursts  # List of CPU and I/O bursts
        self.current_burst = 0  # Index of the current burst
        self.waiting_time = 0  # Accumulated waiting time in the ready queue
        self.turnaround_time = 0  # Total time from arrival to completion
        self.response_time = None  # Time when the process first runs on CPU
        self.io_completion_time = 0  # Time when I/O will complete
        self.last_ready_time = 0  # Time when the process last entered the ready queue

    def is_complete(self):
        """Check if the process has finished all bursts."""
        return self.current_burst >= len(self.bursts)

def print_queues(ready_queue, io_queue, time):
    """Print the current state of the ready and I/O queues."""
    print(f"\nTime {time}:")
    print("Ready Queue: ", end="")
    if ready_queue:
        print(", ".join(f"P{p.pid}(Next CPU: {p.bursts[p.current_burst]})" for p in ready_queue))
    else:
        print("Empty")

    print("I/O Queue: ", end="")
    if io_queue:
        print(", ".join(f"P{p.pid}(Remaining I/O: {p.io_completion_time - time})" for p in io_queue))
    else:
        print("Empty")
    print()

def sjf_scheduler(processes):
    time = 0  # System clock
    total_cpu_time = 0  # Total CPU time used
    ready_queue = deque(sorted(processes, key=lambda p: p.bursts[0]))  # Start with all processes in the ready queue, sorted by first CPU burst
    io_queue = deque()  # I/O queue for processes waiting on I/O
    completed_processes = []  # Store completed processes

    print("SJF CPU Scheduling Simulation:\n")

    while ready_queue or io_queue:
        # Move processes from I/O queue to ready queue if their I/O burst is done
        i = 0
        while i < len(io_queue):
            process = io_queue[i]
            if time >= process.io_completion_time:  # I/O completed
                print(f"Time {time}: P{process.pid} completes I/O burst")
                process.current_burst += 1  # Move to the next CPU burst
                process.last_ready_time = time  # Track when it enters ready queue
                ready_queue.append(process)  # Move back to the ready queue
                io_queue.remove(process)  # Remove from I/O queue
            else:
                i += 1  # Check the next process in I/O queue

        # Sort the ready queue by the next CPU burst time (Shortest Job First)
        ready_queue = deque(sorted(ready_queue, key=lambda p: p.bursts[p.current_burst]))

        print_queues(ready_queue, io_queue, time)  # Print queue states

        if ready_queue:
            # Select the next process from the ready queue
            process = ready_queue.popleft()
            cpu_burst = process.bursts[process.current_burst]

            # Calculate and accumulate waiting time
            process.waiting_time += time - process.last_ready_time

            print(f"Time {time}: P{process.pid} starts CPU burst of {cpu_burst} units")

            # If this is the first time on CPU, set the response time
            if process.response_time is None:
                process.response_time = time

            # Execute the CPU burst
            time += cpu_burst  # Advance the clock
            total_cpu_time += cpu_burst  # Track CPU utilization
            process.current_burst += 1  # Move to the next burst

            # If there are more bursts, move to I/O queue
            if not process.is_complete():
                io_burst = process.bursts[process.current_burst]
                print(f"Time {time}: P{process.pid} starts I/O burst of {io_burst} units")
                process.io_completion_time = time + io_burst  # Set when I/O will finish
                io_queue.append(process)  # Add to I/O queue
            else:
                # Process is complete
                process.turnaround_time = time  # Completion time equals turnaround time
                completed_processes.append(process)  # Add to completed list
                print(f"Time {time}: P{process.pid} has completed all bursts\n")

        else:
            # If no process is ready, fast-forward time to the next I/O completion
            next_io_completion = min(p.io_completion_time for p in io_queue)
            time = next_io_completion

    # Calculate statistics
    total_time = time  # Total elapsed time
    cpu_utilization = (total_cpu_time / total_time) * 100
    avg_waiting_time = sum(p.waiting_time for p in completed_processes) / len(completed_processes)
    avg_turnaround_time = sum(p.turnaround_time for p in completed_processes) / len(completed_processes)
    avg_response_time = sum(p.response_time for p in completed_processes) / len(completed_processes)

    # Print summary of results
    print("\nSummary:\n")
    print("PID\tWaiting Time\tTurnaround Time\tResponse Time")
    for p in completed_processes:
        print(f"P{p.pid}\t{p.waiting_time}\t\t{p.turnaround_time}\t\t{p.response_time}")

    print(f"\nCPU Utilization: {cpu_utilization:.2f}%")
    print(f"Avg Waiting Time (Tw): {avg_waiting_time:.2f}")
    print(f"Avg Turnaround Time (Ttr): {avg_turnaround_time:.2f}")
    print(f"Avg Response Time (Tr): {avg_response_time:.2f}")

# Input process data
process_data = [
    [1, [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4]],
    [2, [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8]],
    [3, [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6]],
    [4, [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3]],
    [5, [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4]],
    [6, [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8]],
    [7, [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10]],
    [8, [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]],
]

# Create Process objects
processes = [Process(pid, bursts) for pid, bursts in process_data]

# Run the SJF scheduler
sjf_scheduler(processes)
