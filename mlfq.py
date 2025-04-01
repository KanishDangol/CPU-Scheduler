from collections import deque

class Process:
    def __init__(self, pid, bursts):
        self.pid = pid
        self.bursts = bursts  # List of CPU and I/O bursts
        self.current_burst = 0  # Index of the current burst
        self.waiting_time = 0  # Accumulated waiting time in the ready queue
        self.turnaround_time = 0  # Total time from arrival to completion
        self.response_time = None  # Time when the process first runs on CPU
        self.io_completion_time = 0  # Time when I/O will complete
        self.last_ready_time = 0  # Time when the process last entered the ready queue

    def is_complete(self):
        return self.current_burst >= len(self.bursts)

def print_queues(queues, io_queue, time):
    print(f"\nTime {time}:")
    for i, q in enumerate(queues, 1):
        print(f"Queue {i}: ", end="")
        if q:
            print(", ".join(f"P{p.pid}(Next CPU: {p.bursts[p.current_burst]})" for p in q))
        else:
            print("Empty")
    print("I/O Queue: ", end="")
    if io_queue:
        print(", ".join(f"P{p.pid}(Remaining I/O: {p.io_completion_time - time})" for p in io_queue))
    else:
        print("Empty")
    print()

def mlfq_scheduler(processes):
    time = 0
    total_cpu_time = 0

    # Initialize the 3 queues and the I/O queue
    q1, q2, q3 = deque(), deque(), deque()
    io_queue = deque()
    completed_processes = []

    # Add all processes to Queue 1 initially
    for process in processes:
        q1.append(process)

    print("MLFQ CPU Scheduling Simulation:\n")

    def execute_process(process, quantum):
        """Execute the process for the given quantum or until its CPU burst ends."""
        cpu_burst = process.bursts[process.current_burst]
        run_time = min(cpu_burst, quantum)
        process.bursts[process.current_burst] -= run_time  # Subtract executed time
        return run_time

    while q1 or q2 or q3 or io_queue:
        # Move processes from I/O queue to the appropriate ready queue
        i = 0
        while i < len(io_queue):
            process = io_queue[i]
            if time >= process.io_completion_time:
                print(f"Time {time}: P{process.pid} completes I/O burst")
                process.current_burst += 1
                process.last_ready_time = time  # Track when it enters ready queue

                # Add the process back to the queue it last came from
                if process in q2:
                    q2.append(process)
                else:
                    q3.append(process)
                io_queue.remove(process)
            else:
                i += 1

        print_queues([q1, q2, q3], io_queue, time)  # Print queue states

        # Determine the next queue to serve
        if q1:
            queue, quantum = q1, 5
        elif q2:
            queue, quantum = q2, 10
        elif q3:
            queue, quantum = q3, float('inf')  # FCFS (no quantum limit)
        else:
            # No process is ready, fast-forward to the next I/O completion
            next_io_completion = min(p.io_completion_time for p in io_queue)
            time = next_io_completion
            continue

        # Select the next process from the current queue
        process = queue.popleft()
        run_time = execute_process(process, quantum)

        # Calculate waiting time and response time if applicable
        process.waiting_time += time - process.last_ready_time
        if process.response_time is None:
            process.response_time = time

        print(f"Time {time}: P{process.pid} runs for {run_time} units")
        time += run_time
        total_cpu_time += run_time

        if process.bursts[process.current_burst] == 0:
            # CPU burst is complete, move to the next burst or finish process
            process.current_burst += 1
            if process.is_complete():
                process.turnaround_time = time
                completed_processes.append(process)
                print(f"Time {time}: P{process.pid} completes all bursts")
            else:
                # Move to I/O queue
                io_burst = process.bursts[process.current_burst]
                print(f"Time {time}: P{process.pid} starts I/O burst of {io_burst} units")
                process.io_completion_time = time + io_burst
                io_queue.append(process)
        else:
            # Process didn't complete its burst, demote to the next queue
            if queue == q1:
                q2.append(process)
                print(f"Time {time}: P{process.pid} is demoted to Queue 2")
            elif queue == q2:
                q3.append(process)
                print(f"Time {time}: P{process.pid} is demoted to Queue 3")
            else:
                q3.append(process)  # Stay in Queue 3

    # Calculate statistics
    total_time = time
    cpu_utilization = (total_cpu_time / total_time) * 100
    avg_waiting_time = sum(p.waiting_time for p in completed_processes) / len(completed_processes)
    avg_turnaround_time = sum(p.turnaround_time for p in completed_processes) / len(completed_processes)
    avg_response_time = sum(p.response_time for p in completed_processes) / len(completed_processes)

    # Print summary
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

# Run the MLFQ scheduler
mlfq_scheduler(processes)

