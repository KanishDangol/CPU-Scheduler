# CPU Scheduling Algorithms  

This repository contains Python implementations of three CPU scheduling algorithms:  

### 1. First-Come, First-Served (FCFS)  
   - A non-preemptive scheduling algorithm that executes processes in the order they arrive.  
   - Simulates CPU and I/O bursts while tracking waiting time, turnaround time, and response time.  

### 2. Shortest Job First (SJF)  
   - A non-preemptive algorithm that selects the process with the shortest CPU burst next.  
   - Minimizes average waiting time but may cause starvation for longer processes.  

### 3. Multi-Level Feedback Queue (MLFQ)  
   - A preemptive scheduling algorithm using three priority queues with different time quanta.  
   - Dynamically adjusts process priority to balance responsiveness and efficiency.  

Each program simulates process execution, manages I/O and ready queues, and calculates key scheduling metrics such as CPU utilization, average waiting time, and turnaround time.
