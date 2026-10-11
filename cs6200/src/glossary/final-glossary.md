# GIOS Final Glossary

Scope: the ten final lectures (P3L1 to P4L4) as written in this repository's notes, plus the paper corrections already embedded in those notes as "Paper (...)" callouts. Where a callout corrects the lecture, the entry gives the lecture version first and then the correction, marked "Paper correction (<Author>):". Nothing else from the papers is used.

Conventions: each term is defined once, in the first lecture that explains it, and later lectures cross-reference it. Terms are alphabetical within each lecture. Data structures and OS objects carry a "Stores:" list.

## P3L1 Scheduling

### Active array
One of the two task arrays that make up the O(1) scheduler's runqueue. The active array is the one the scheduler draws from to select the next task to run. Each entry corresponds to a priority level and points to the first runnable task at that level; adding a task and selecting a task both take constant time. A task whose time on the CPU is still under its timeslice is placed back on the active array for its priority level. Only when a task exhausts its entire timeslice does it move to the expired array.
- Contrast: the expired array holds tasks that have used up their timeslice and are not scheduled until the active array is empty, at which point the two arrays are swapped.

### Cache affinity
Scheduling a task back onto the CPU it previously ran on so that its execution state is still "hot" in that CPU's cache rather than in main memory. Because performance depends heavily on how much of a task's state is cached, keeping a task on the same CPU maximizes cache reuse. It is achieved with a hierarchical architecture: a load balancing component divides tasks among CPUs, and each CPU has its own scheduler and runqueue that schedules only on that CPU.

### Co-scheduling on hyperthreaded platforms
Choosing which threads share the hardware contexts of one CPU. With two hardware threads and one pipeline, co-scheduling two CPU-bound threads makes them contend for the pipeline, so in the best case each thread's performance degrades by a factor of two while memory sits idle. Co-scheduling two memory-bound threads leaves cycles wasted while both wait on memory. A mix of CPU-bound and memory-bound threads is best: it limits pipeline contention and keeps both the CPU and the memory components utilized.
- Paper correction (Fedorova et al.): the paper develops this with a three-system comparison rather than the lecture's two-hardware-thread picture: a single-threaded core (A, the lower bound), a multithreaded core (B), and a multiprocessor with one core per thread (C, the upper bound). On a purely CPU-bound workload A and B perform comparably while C is four times faster; on a purely memory-bound workload B and C both beat A by a factor of four, because the multithreaded core overlaps the threads' memory latencies. The contention argument rests on instruction delay latency: an ALU instruction has 0 delay, an L1-hit load has 4 cycles, a branch delays the next instruction by 2 cycles. The headline result is that a CMT-aware scheduler can improve performance by as much as a factor of two over a naive one.

### Completely Fair Scheduler (CFS)
The default Linux scheduler for non-realtime tasks, introduced in Linux 2.6.23 to replace the O(1) scheduler. CFS addresses the O(1) scheduler's lack of fairness and the jitter interactive tasks suffered when stuck in the expired queue. It uses a red-black tree as its runqueue, ordered by vruntime, and always schedules the task with the least vruntime. Task selection takes constant time; adding a task takes time logarithmic in the number of tasks, which may limit the scheduler as task counts grow very large.
- Quiz (Linux Schedulers): the main reason O(1) was replaced by CFS is that interactive tasks could wait unpredictable amounts of time, since a task moved to the expired array had to wait until the active array's tasks used up their timeslices. Unpredictable scheduling time under high load is incorrect (O(1) selects in constant time regardless of load), and starvation of low priority tasks is sort of correct but not the main reason.

### CPU bound task
A task that spends most of its time using the CPU rather than waiting on I/O. CPU bound tasks prefer longer timeslices, which limit context switching overhead and keep CPU utilization and throughput high. The user cannot perceive when a CPU bound task starts, only when it completes, so average wait time matters little for these tasks.
- Contrast: an I/O bound task frequently yields the CPU to issue I/O requests and prefers short timeslices.

### CPU scheduler
The component that decides how and when processes and their threads access the shared CPUs, covering both user level and kernel level tasks. It selects a task from the ready queue and dispatches it onto a CPU. The scheduler runs whenever the CPU becomes idle (for example, a task issues an I/O request and goes on a wait queue), when a timeslice expires, or when a new task enters the runqueue. Its objective is to choose the next task to run from the ready queue.

### Cycles per instruction (CPI)
A metric Fedorova considers for deciding whether a thread is CPU bound or memory bound. A memory bound thread blocks on memory and so takes many cycles per instruction, giving a high CPI; a CPU bound thread completes an instruction roughly every cycle, giving a CPI near 1. Because there is no CPI counter on the processor and computing 1 / IPC in software is too costly, Fedorova studies CPI through a simulator. The lecture presents CPI as speculative and, from Fedorova's profiling of benchmark applications, concludes that real applications cluster too closely in CPI for it to be instructive.
- Lecture version: the lecture frames high CPI as implying a memory bound thread and reports that measured CPIs cluster around 2.5 to 4.5, concluding CPI is not that different across applications and so may not be useful for scheduling.
- Paper correction (Fedorova et al.): the paper is less tentative. It states that mean CPI is easily determined with hardware counters and nicely captures average instruction delay, reasons through single-threaded CPI (a high single-threaded CPI means low pipeline resource requirements, a low CPI means high ones), and reports that measured CPI can vary by an order of magnitude across applications, so near-term CPI is predictable and a load-balancing CMT scheduler is a simple matter of engineering. The 2.5 to 4.5 range comes from the lecture graphic, not the paper.
- Paper correction (Fedorova et al.): the paper's own stated limitations are different ones: CPI does not reveal which specific resources (cache hierarchy, floating-point unit) threads contend for, and CPI measured on a busy system is already perturbed by contention. Fedorova's later work (USENIX 2005) identifies L2 cache contention, not pipeline CPI, as the dominant effect.

### Dispatch
The act of placing a selected task onto the CPU. Once the scheduler picks a task, the operating system context switches to it, enters user mode, sets the program counter, and begins execution.

### Expired array
One of the two task arrays in the O(1) scheduler's runqueue, holding tasks that have used up their entire timeslice. The scheduler does not schedule tasks from the expired array while any tasks remain in the active array. When the active array empties, the active and expired arrays are swapped so the expired tasks become eligible again.

### Fairness
The property that over a given time interval each task runs for an amount of time proportional to its priority. The O(1) scheduler makes no such guarantee, which motivated the completely fair scheduler.

### Fedorova's simulated CMT system
The multithreaded system Fedorova simulates to study CPI-based scheduling. She models a system of 4 cores, each a 4-way multithreaded core, for 16 hardware execution contexts, and drives it with a synthetic workload of threads having CPI values of 1, 6, 11, and 16 (four threads of each), measuring aggregate IPC.
- Lecture version: the lecture describes the simulated core as 4-way SMT and labels the platform SMT, treating SMT as a synonym for hyperthreading.
- Paper correction (Fedorova et al.): the simulated core is not SMT. Section 3 models fine-grained multithreading (Laudon et al.): one set of functional units interleaved by switching context every cycle, so at most one instruction issues per cycle and per-core IPC maxes out at 1. The paper names SMT (multiple sets of functional units issuing from several threads in the same cycle) as the design it deliberately did not take, choosing a simple RISC core to fit more cores on the chip.
- Paper correction (Fedorova et al.): for the CPI experiments, Section 5 gives the magnitudes: schedules (a) and (b) perform twice as well as schedule (d) and 1.5 times better than schedule (c). In the poor schedules the CPI-1 threads are packed together (two cores of 1, 1, 6, 6 in (c); one core of 1, 1, 1, 1 in (d)), so those cores are saturated while the cores holding only high-CPI (memory-bound) threads are under-utilized.

### First Come First Serve (FCFS)
The simplest scheduling algorithm, in which tasks are scheduled in the order they arrive. When a task completes, the scheduler picks the next task in arrival order. It can be implemented with a FIFO queue: the scheduler need only track the head of the queue and dequeue tasks from the front.

### Hardware counters
On-chip counters that update as the processor executes and record aspects of execution such as L1, L2, and last-level cache misses, instructions retired (from which IPC can be computed), and power or energy usage. Schedulers use them to estimate a thread's resource needs quickly enough for per-cycle decisions. A high number of LLC misses may mean a memory bound thread or a thread running with a cold cache in a new phase, so schedulers combine several counters and platform-specific trained models. Software interfaces to these counters include oprofile and the Linux perf tool.

### Hyperthreading (hardware multithreading, CMT, SMT)
A hardware technique in which a single CPU has multiple sets of registers, each describing the context of a separate thread, so switching among those threads is very fast. Only one thread executes at a time because there is still one CPU, but the fast switch hides latency such as memory access, which costs hundreds of cycles while a hardware context switch costs only cycles. Each hardware context appears to the scheduler as an entity it can schedule tasks on. Modern platforms commonly support two hardware threads, some up to eight, and the feature can be enabled or disabled at boot time. The same mechanism is called hardware multithreading, chip multithreading (CMT), and simultaneous multithreading (SMT).

### I/O bound task
A task that frequently issues I/O requests and so spends much of its time waiting on devices rather than computing. I/O bound tasks prefer short timeslices, which let them issue I/O requests sooner, keep CPU and device utilization high, and keep user-perceived wait time low.
- Contrast: a CPU bound task prefers longer timeslices to limit context switching overhead.

### Instructions per cycle (IPC)
A performance metric giving the number of instructions issued per CPU cycle. A CPU bound thread that issues an instruction every cycle maximizes IPC. In Fedorova's CPI experiments IPC is the metric of overall performance, and because the simulated system has at most 4 cores the maximum IPC is 4. IPC is the reciprocal of CPI.

### Load balancing
Distributing tasks across CPUs so that no runqueue grows much longer than the others. A load balancing component divides tasks among per-CPU schedulers; it compares runqueue lengths and, when a CPU goes idle, rebalances work from other queues onto the idle CPU's queue. It is the component of the hierarchical scheduler architecture through which cache affinity is achieved: it divides tasks among CPUs, and each per-CPU scheduler then keeps its tasks on that CPU.
- Also in: P4L4 (the internet-service load balancer front-end, which mirrors the boss-worker pattern to route requests across backend nodes, round-robin for a homogenous setup and content-aware for a heterogenous one).

### Multi-level feedback queue (MLFQ)
A runqueue structure of multiple queues, each with a different timeslice value and its own scheduling policy, that uses feedback on task behavior to decide which queue a task belongs in. A new task starts on the topmost queue (smallest timeslice); if it yields before the timeslice expires it stays there, and if it is preempted it is pushed down to a queue with a longer timeslice. A task in a lower queue that begins yielding frequently for I/O can be boosted back up to a smaller-timeslice queue. The MLFQ is more than a set of priority queues because the per-level policies and the movement rules provide feedback about each task. Fernando Corbato received the Turing Award in part for the MLFQ and his work on timesharing. The Solaris scheduler is essentially an MLFQ with 60 levels.
- Stores:
  - multiple distinct queues, each with its own timeslice value and scheduling policy
  - the queue a task currently occupies, used as feedback about whether it is more I/O or CPU intensive

### Multicore system
A system in which each CPU contains multiple internal cores. Each core has its own private L1 and L2 cache, the cores of a CPU share a last-level cache, and DRAM is shared. The operating system sees every core as an entity onto which it can schedule tasks.

### Nice value
A per-process adjustment to the default priority of a timesharing task in the Linux O(1) scheduler. Nice values range from -20 to 19, mapping onto priority levels 120 - 20 through 120 + 19 around the default user priority of 120. A system call adjusts a user process's nice value.

### Non-uniform memory access (NUMA)
A platform with multiple memory nodes connected to the CPUs over a physical interconnect, where a memory node is typically closer to one socket of processors, so those processors access it faster than they access a remote node. NUMA refers to this non-uniform access cost rather than to any scheduling policy.

### NUMA-aware scheduling
Scheduling that keeps a task on the CPU closest to the memory node holding its state, so that memory accesses stay local and fast on a NUMA platform.

### O(1) scheduler
The Linux scheduler, introduced in Linux 2.5, that adds and selects a task in constant time regardless of the number of tasks. It is preemptive and priority-based with 140 priority levels, where 0 is the highest priority and 139 the lowest: 0 to 99 for real-time tasks and 100 to 139 for timesharing tasks, the default user priority being 120. Like the MLFQ it associates a different timeslice with each priority level and uses feedback from past behavior; it gives the smallest timeslices to low-priority CPU bound tasks and the largest to interactive tasks. Feedback is based on how long a task slept during its timeslice: more sleeping marks a task interactive and boosts its priority by 5, less sleeping marks it compute intensive and lowers its priority by 5. It was replaced by the completely fair scheduler in Linux 2.6.23 because its jitter hurt interactive tasks as applications became time sensitive (Skype, movie streaming, gaming).
- Stores:
  - an active array and an expired array of tasks
  - each array entry corresponds to a priority level and points to the first runnable task at that level

### Preemption
Interrupting a running task before it completes so that another task can be scheduled. Removing the run-to-completion assumption allows a newly arrived higher-priority or shorter task to displace the current one. Preemption is required for priority scheduling, so that a high priority task entering the runqueue can displace a lower priority one, and it occurs when a timeslice expires.

### Priority aging
A mechanism against starvation in which a task's effective priority is a function of its numerical priority and the time it has spent in the runqueue. Older tasks are promoted to higher effective priority so they are eventually scheduled.

### Priority inversion
A situation in which a higher priority task waits on a lower priority task, inverting the intended order of execution. If a low priority task holds a mutex that the highest priority task needs, a middle priority task can run ahead of both, so the observed order (for example T2, T3, T1) differs from the priority order (T1, T2, T3). The fix is to temporarily boost the mutex owner's priority to that of the waiting high priority task until it releases the lock, which is why the mutex data structure must track its current owner.

### Priority scheduling
A policy that always runs the highest priority runnable task next, preempting lower priority tasks when a higher priority task becomes runnable. Different tasks commonly have different priorities, for example kernel tasks ranking above user application tasks. A common implementation keeps a separate runqueue per priority level so the scheduler can empty queues in priority order. Its danger is starvation, mitigated by priority aging.
- Quiz (Preemptive Scheduling): with priorities P3 < P2 < P1, T3 arriving at 0 needing 4s, T2 at 3 needing 4s, and T1 at 5 needing 3s, T3 runs 0 to 3, T2 preempts it and runs 3 to 5, T1 preempts T2 and runs 5 to 8, T2 finishes at 10, and T3 finishes at 11: T1 = 8s, T2 = 10s, T3 = 11s.

### Red-black tree
The self-balancing tree the completely fair scheduler uses as its runqueue. Self-balancing keeps all root-to-leaf paths approximately equal in length. Nodes are ordered by vruntime: for any node, all nodes to its left have lower vruntimes and need to run sooner, and all nodes to its right have higher vruntimes and can wait. The leftmost node has the least vruntime and is normally the one scheduled next. Selecting the leftmost task is constant time while inserting a task is logarithmic in the number of tasks.
- Stores:
  - one node per runnable task, keyed by the task's vruntime
  - left subtree with smaller vruntimes, right subtree with larger vruntimes

### Round robin scheduling
A policy for tasks of equal priority that takes tasks from the runqueue in turn: the first task is scheduled, then when it completes or yields the next is scheduled, and so on. It can be generalized to incorporate priorities, and when combined with timeslicing it interrupts a task after a fixed window to cycle in the other tasks rather than waiting for an explicit yield.

### Run to completion scheduling
A model in which, once a task is assigned to a CPU, it runs there until it finishes. The lecture analyzes it under simplifying assumptions: a known set of tasks, known execution times, no preemption, and a single CPU. FCFS and the non-preemptive form of shortest job first are run-to-completion algorithms.

### Runqueue (ready queue)
The data structure holding the tasks that are ready to run, from which the scheduler selects the next task. It is only logically a queue: it can be implemented as a single FIFO queue, as multiple queues, or as a tree, and the choice is tightly coupled to the scheduling algorithm because a structure good for one algorithm may be poor for another. The structure is designed so the scheduler can easily determine which task to run next. One common form is a multi-queue structure whose queues differ by timeslice value, associating I/O intensive tasks with the smallest timeslice and CPU intensive tasks with the largest.

### Scheduling metrics
The quantities used to compare schedulers: throughput (tasks completed per unit time), average job completion time, average job wait time, and CPU utilization. The lecture also notes device utilization as a concern for I/O bound workloads.

### Scheduling policy
The algorithm that decides which task the scheduler selects next, such as FCFS, shortest job first, priority, or round robin. The policy and the runqueue data structure are tightly coupled, since a structure optimized for one policy may be a poor fit for another.

### Shared memory multiprocessor
A system with multiple CPUs that share system memory (DRAM). Each CPU has its own private L1 and L2 cache and a last-level cache that may or may not be shared among the CPUs. The operating system sees all the CPUs as entities onto which it can schedule tasks.
- (P3L4) Also called a symmetric multiprocessor, or SMP. In an interconnect-based configuration multiple memory references can be in flight at once, one per connected memory module; in a bus-based configuration the shared bus supports only one memory reference at a time. Because cache access is faster than main memory, caches hide memory latency, and the effect is more pronounced here because contention among CPUs for shared memory delays accesses. On a write, the system may not write to the cache at all (the write goes directly to main memory and any cached copy is invalidated; the lecture does not name this option), use write-through (applied to both cache and memory), or use write-back (applied to the cache immediately and to main memory later, perhaps on eviction).
- Also in: P3L4 (as "shared memory multiprocessor (SMP)" / symmetric multiprocessor, with bus vs interconnect configurations and the write-through/write-back write policies).

### Shortest Job First (SJF)
A scheduling algorithm that schedules tasks in order of their execution time, running the shortest task next. A plain FIFO queue is a poor runqueue for SJF; an ordered queue (with a more expensive enqueue) or a tree ordered by execution time, where insertion may require rebalancing and the leftmost node is the shortest job, works better. Ties are broken arbitrarily. With preemption added, an arriving task shorter than the running one preempts it. SJF assumes known execution times, which is unrealistic, so running time is estimated from heuristics such as the last run or a windowed average.
- Quiz (SJF Performance): with T1 = 1s, T2 = 10s, T3 = 1s, all in the system at time 0, no preemption, and known execution times, the order is T1, T3, T2 (or T3, T1, T2). Throughput is 3 tasks / 12s = 0.25 tasks/s (same as FCFS), average completion is (1 + 2 + 12) / 3 = 5s (FCFS: 8s), and average wait is (0 + 1 + 2) / 3 = 1s (FCFS: 4s).

### Starvation
A hazard of priority scheduling in which a low priority task is effectively never scheduled because higher priority tasks keep entering the system and taking precedence. It is mitigated by priority aging.

### Timesharing
Interleaving tasks on the CPU by giving each a timeslice so that they share the processor over time. It is achieved through timeslicing and is the only route to sharing the CPU among CPU bound tasks, which otherwise would not yield.

### Timeslice (time quantum)
The maximum amount of uninterrupted time that can be given to a task. A task may run less than this, for example if it blocks on I/O, synchronizes with another task, or is preempted by a higher priority task becoming runnable. Timeslices let tasks be interleaved so they timeshare the CPU, which for CPU bound tasks is the only way to achieve timesharing. Their benefits are that short tasks finish sooner, the scheduler responds faster to changes, and I/O operations start sooner; their cost is the overhead of interrupting the running task, running the scheduler, and context switching. The overhead is minimized when the timeslice is much longer than a context switch.
- Quiz (Timeslice): on one CPU with 10 I/O bound tasks (I/O after every 1ms of CPU, each I/O taking 10ms), 1 CPU bound task, and a 0.1ms context switch, round robin utilization (useful CPU time over useful time plus context switch overhead) is 1 / 1.1 = 91% with a 1ms timeslice and (10 x 1 + 10) / (10 x 1.1 + 10.1) = 20 / 21.1 = 95% with a 10ms timeslice. The large timeslice, which favors the CPU bound task, is better for CPU utilization; a smaller timeslice is better for the I/O device, which cannot do anything while the CPU bound task runs its full 10ms.

### Vruntime (virtual runtime)
The amount of time a task has spent running on the CPU, tracked by the completely fair scheduler to the nanosecond and used to order tasks in its red-black tree. CFS always schedules the task with the least vruntime (normally the leftmost node). It periodically increments the running task's vruntime and compares it with the leftmost node's; if the running task still has the smaller vruntime it keeps running, otherwise it is preempted and reinserted. Vruntime progresses faster for lower priority tasks (so they likely lose the CPU sooner) and more slowly for higher priority tasks, so high priority tasks get to execute on the CPU longer.

### Windowed average
A heuristic for estimating a task's execution time when it is not known in advance, computed as the average of the task's execution times over the past n runs. It lets SJF-style policies work without a priori knowledge of running times.

## P3L2 Memory Management

### Access bit
A page table entry bit that records whether the page has been referenced at all, for reads or writes. The least-recently-used replacement policy uses it to track which pages have been touched so it can predict future use from past use.

### Allocation
The memory management function of tracking how memory is used and what memory is free, through OS mechanisms and data structures. Because physical memory is smaller than virtual memory, some virtual locations may not be present in physical memory and may reference secondary storage such as disk, so the OS must also be able to replace contents in physical memory with contents from disk. Memory allocation decides which physical pages are allocated to a virtual memory region; allocators exist at the kernel level and at the user level.
- Contrast: arbitration interprets, translates, and validates each access.

### Allocation on first touch
The policy of allocating a physical page frame to a virtual memory region only when the process first accesses it, rather than when the memory is reserved. The first access to a never-used region causes the OS to take a free physical page and create a page table entry linking it to the virtual page. The rationale is to avoid committing physical memory for data structures a program reserves but never uses.

### Arbitration
The memory management function of quickly interpreting and verifying a process memory access. It requires the OS to translate a virtual address to a physical address and validate that the access is legal, relying on a combination of hardware support and software.
- Contrast: allocation tracks what memory is used and free; arbitration checks and translates each access.

### Buddy allocator
A Linux kernel allocator that begins with a free memory region whose size is a power of two and, on each request, repeatedly subdivides the area into power-of-two halves until it reaches a chunk small enough to satisfy the request. On a free, a chunk checks its equal-sized "buddy," and if the buddy is also free the two aggregate into a larger chunk; this coalescing can continue up the tree.
- Chunk sizes are powers of two so that the addresses of two buddies differ by exactly one bit, which simplifies the computation of a chunk's buddy.
- Suffers internal fragmentation because its granularity is powers of two, while many kernel data structures are not near a power of two in size (the task struct is about 1.7KB).
- Contrast: the slab allocator avoids this internal fragmentation by sizing entries to the exact object.

### Checkpointing
A failure and recovery technique that periodically saves process state so a failed process can be restarted from a recent known state rather than reinitialized. An optimized version write-protects the state, copies it once, then uses MMU dirty-page tracking to copy only the diffs of pages modified since, producing incremental checkpoints. The same mechanism underlies rewind-replay debugging and process migration.
- Quiz (Checkpointing): the more frequently you checkpoint, the more state you checkpoint, the higher the overheads, and the faster you recover from a fault (all of the above). Spacing checkpoints out lets repeated writes to a page amortize into a single dirtied page; frequent checkpoints buy faster recovery, with less execution to replay, at the cost of higher overhead.

### Copy-on-write (COW)
A mechanism that avoids copying a parent's address space when creating a new process by having the child's page tables point at the parent's physical pages. The shared pages are write-protected, so the same physical page is reachable through two virtual addresses. When either process writes, the MMU detects the write-protected page and raises a page fault; the OS then copies only that page and repoints the faulting process's page table at the new copy. The copy cost is paid only on a write.
- Whether write protection is removed after the copy depends on how many processes still share the page; while other references remain, it stays protected so their writes keep faulting.

### CR2 register
The x86 register that holds the faulting virtual address when a page fault occurs. The page fault handler reads it, together with the error code placed on the kernel stack, to decide what action to take.

### CR3 register
The x86 register that points to the currently active page table. On a context switch the OS loads the incoming process's page table, and hardware uses this register to locate it during translation.

### Demand paging
The process of keeping allocated pages on secondary storage and bringing them into physical memory only when referenced, since virtual memory is much larger than physical memory. A page not present has its present bit set to 0; a reference to it makes the MMU raise a page fault, trapping into the kernel, which locates the page on the swap device, issues the I/O to read it into a free frame, updates the page table entry with the new PFN, and restarts the faulting instruction.
- Also called paging; pages moved out are said to be swapped.

### Descriptor table
A table used in segmented memory translation. Used with the segment selector, it produces the physical (base) address of the segment, which is combined with the offset to produce the linear address of the memory reference (then translated by the paging unit).

### Dirty bit
A page table entry bit set by hardware whenever the page is written to. File systems use it to find cached file pages that have been modified and must be written back to disk, and page replacement uses it to prefer evicting clean pages, which need not be written out.

### External fragmentation
The condition in which multiple interleaved allocate and free operations leave noncontiguous holes of free memory, so requests for large contiguous blocks of memory cannot be satisfied even though enough total free memory is available. An allocator limits it by coalescing free page frames when memory is released so that contiguous regions reform.
- Contrast: internal fragmentation is wasted space inside an allocated page or chunk, not between them.

### Fault (MMU fault)
A condition the MMU generates when a memory access cannot proceed. It can signal an illegal access to unallocated memory, insufficient permissions for the access, or that the requested page is not present in physical memory and must be fetched from disk.

### Hashing page table
A structure that supplements an inverted page table to speed up its linear scan. The address is hashed and looked up in a hash table whose entry points to a small linked list of possible matches, so the search considers only a few possibilities.

### Huge page
A Linux page size of 1GB, requiring a 30-bit offset. Huge pages further shrink the page table (another factor of 512 relative to large pages) and raise TLB hit rates, at the cost of greater internal fragmentation when not densely populated; they suit databases and in-memory data stores.

### Internal fragmentation
Wasted memory within an allocated page or chunk that is not densely populated. Larger pages increase it because an under-used large page leaves bigger unused gaps inside the page, which is a reason smaller 4KB pages remain common.
- Contrast: external fragmentation is free space fragmented across noncontiguous holes between allocations.

### Inverted page table
A system-wide page table, managed per system rather than per process, in which each entry corresponds to a physical frame in main memory. The motivation: high-end platforms have physical memory on the order of tens of terabytes, while the virtual memory of an address space can reach petabytes and beyond, so a page table structure on the order of the available physical memory is much more efficient than one on the order of virtual memory; an inverted table keeps a representation closer to the physical memory layout. A logical address under this scheme carries the process id, the virtual address, and the offset. A linear scan finds the entry matching the PID and virtual address, and that entry's index is the physical frame number, which combined with the offset gives the physical address.
- Stores (per entry):
  - process id (PID) of the owning process
  - the virtual address mapped to this frame
- Linear scans are slow, so the TLB caches lookups and the table is often supplemented with a hashing page table.

### Kernel level allocator
A memory allocator responsible for allocating pages for the kernel and for static process state created at process start, such as code and stack, and for tracking the free memory available in the system.
- Contrast: a user level allocator manages the dynamically allocated heap.

### Large page
A Linux page size of 2MB, requiring a 21-bit offset. Compared with a 4KB page it reduces the page table size by a factor of 512 and yields more TLB hits, at the cost of greater internal fragmentation when the page is sparsely populated.

### Least-Recently Used (LRU)
A page replacement policy that predicts future use from recency of past use, evicting the page not accessed for the longest time on the assumption that recently used pages are more likely to be needed soon. It relies on the hardware access bit to tell which pages have been referenced. The Linux default is an LRU variant that gives pages a second chance, scanning twice before choosing victims.
- Quiz (LRU): LRU is only a heuristic and can behave pathologically. An array of 11 page-sized entries looped over on a system with only 10 physical pages: after pages 1 to 10 load, accessing the 11th evicts page 1 (least recently used), the very next page needed; bringing page 1 back evicts page 2, and so on, so 100% of accesses are demand paged. This is why operating systems can be configured to use different replacement policies.

### Limit register
A register that, with a base address, defines a segment represented as a contiguous section of physical memory, giving the segment's extent.

### Linear address
The address produced by segmentation: the segment's base address, obtained from the segment selector and descriptor table, combined with the offset. In practice it is then passed to the paging unit, which translates it to the physical address.

### Memory management unit (MMU)
Hardware in every CPU package that converts the virtual addresses the CPU issues into physical addresses. It generates faults on illegal or impermissible accesses or when a page is absent, uses designated registers to locate the active page table, and performs the actual translation, which fixes whether a platform offers page-based or segment-based management.

### Migration (process migration)
A service built on the checkpointing mechanisms: the process is checkpointed to another machine and restarted there, which is useful for disaster recovery or for consolidation onto as few machines as possible. It can be implemented by repeating checkpoints in a fast loop until so few pages are dirtied that a pause-and-copy becomes acceptable, or unavoidable.

### Multi-level page table (hierarchical page table)
A page table organized as a tree instead of a single flat array, used to avoid allocating entries for unused regions of the address space. An outer page table directory holds pointers to inner page tables, which hold the page frame numbers and protection bits; inner tables are created only for virtual regions that are actually valid, so holes in the address space cost no inner tables.
- The virtual address is split into one index per level plus the offset: outer indices select the directory entry and then the page table, which yields the PFN.
- Adding levels makes each inner table cover a smaller region, so gaps are more likely to save whole tables; this matters most on sparse 64-bit address spaces.
- The cost of more levels is more memory accesses per translation, increasing translation latency.
- Contrast: a flat page table has an entry for every virtual page number and permits no gaps.
- Quiz (Multi-level page table): a process with 12-bit addresses, a 6-bit offset (64-byte pages), and only the first 2KB and last 1KB allocated needs 2^6 = 64 entries in a single-level table. With a 2-bit outer and 4-bit inner index, each outer entry covers 2^(4+6) = 1KB, one of the four outer regions is unallocated and needs no inner table, and three 16-entry inner tables give 48 entries, a 25% reduction.

### Offset
The low-order portion of a virtual address that is not translated but passed through to index a location within the page frame. Its width determines the page size: an n-bit offset gives a page of 2^n bytes.

### Page
A fixed-size unit into which the virtual address space is subdivided. The OS maps pages onto equal-sized physical page frames, which lets it translate only the start of each page rather than every address and so keeps the page table small.

### Page fault
A trap raised by the MMU when a physical memory access cannot be performed, for example because the page is not present or a protection bit is violated. The CPU places an error code on the kernel stack and traps into the kernel's page fault handler, which acts on the error code and the faulting address; on x86 the error code derives from page table entry flags and the faulting address is in `CR2`.

### Page fault handler
The kernel routine invoked by a page fault trap. It uses the error code and faulting address to determine the action, distinguishing a not-present page that must be brought in from disk from a protection violation that forbids the access.

### Page frame
A fixed-size slot of physical memory, equal in size to a page, into which a virtual page is mapped. Translation produces the page frame number, whose first physical address is combined with the offset to reach a specific DRAM location.

### Page out daemon
An OS daemon that runs periodically to find pages that can be freed when occupied memory crosses a threshold. It is scheduled to run when memory usage is high and CPU usage is low enough that it does not unduly interrupt applications. Linux exposes parameters for the threshold page count and the number of pages replaced per period, and categorizes pages into different types, which helps narrow down the decision of which pages to replace.

### Page replacement
The activity of choosing which pages to swap from physical memory to disk and when. Pages are swapped out when memory usage exceeds a threshold and CPU usage is low; victims are chosen from pages predicted to be unneeded (via policies such as LRU), preferring clean pages via the dirty bit, while non-swappable pages are excluded.

### Page table
A per-process data structure that maps virtual addresses to physical addresses. The virtual page number indexes it to produce the physical frame number, which is summed with the offset to form the physical address; the OS maintains one per process and swaps the active one on each context switch.
- Stores (per entry):
  - page frame number (PFN)
  - valid (present) bit
  - dirty bit
  - access bit
  - protection bits
- Because an entry exists for every virtual page number regardless of use, a flat page table can be very large; a 32-bit architecture with 4KB pages needs 2^20 four-byte entries, about 4MB, and a 64-bit architecture would need about 32PB.
- Quiz (Page table size): on a 12-bit architecture with a single-level page table, a 32-byte page needs a 5-bit offset, leaving a 7-bit VPN and 2^7 = 128 entries; a 512-byte page needs a 9-bit offset, leaving a 3-bit VPN and only 2^3 = 8 entries. Larger pages mean fewer virtual pages and a smaller page table.

### Page table directory
The outer level of a multi-level page table. Its entries are pointers to inner page tables rather than to page frames; a region of virtual memory with no mapping needs no inner table (its directory entry stays empty).

### Page table entry (PTE)
A single mapping in a page table that the MMU uses both to translate and to validate an access. It holds at least a page frame number and a valid bit, plus bits the OS and hardware interpret for management decisions.
- Stores:
  - page frame number (PFN)
  - valid bit, also called the present bit, indicating whether the page is in physical memory
  - dirty bit, set when the page is written
  - access bit, indicating the page was referenced
  - protection bits, specifying read, write, or execute permission

### Page-based memory management
Memory management in which the virtual address space is divided into fixed-size pages mapped onto equal-sized physical page frames, with arbitration performed through page tables. It is the dominant mechanism in modern operating systems.
- Contrast: segment-based memory management uses variably sized segments and segment registers.

### Physical address
The address of the actual location in DRAM where data is stored. The MMU produces it from a virtual address by combining the translated page frame number with the offset.

### Physical frame number (PFN)
The output of a page table lookup: the first physical address of the page frame in DRAM. It is summed with the offset from the virtual address to form the complete physical address.

### Pinning
Disabling swapping for a page so it stays resident and keeps its physical address throughout its lifetime. It is useful when the CPU is interacting with devices that support direct memory access (DMA).
- (P3L5) DMA requires its data buffer to remain in physical memory until the transfer completes, since the DMA controller only has access to physical memory, so the memory regions involved in DMA are pinned, meaning non-swappable.
- Also in: P3L5 (as "pinned memory": the DMA data buffer is pinned, i.e. non-swappable, for the duration of a transfer because the DMA controller reaches only physical memory).

### Present bit
See Valid bit (P3L2).

### Process id in addressing (PID)
The identifier of the accessing process, included in a logical address under inverted page tables alongside the virtual address and offset. The scan matches an entry by the combination of PID and virtual address.

### Protection bits
Page table entry bits that specify whether a page may be read, written, or executed. The MMU consults them to decide whether an access is permitted and raises a page fault on violation.

### Rewind-replay
A debugging technique built on checkpointing. Rewind restarts the execution of a process from an earlier checkpoint; replay re-runs it from there to see whether the error reproduces. Older and older checkpoints can be tried until the error is found.

### Second chance
The variation of LRU that is Linux's default replacement policy. It performs two scans before selecting the pages to swap out, giving pages an extra opportunity to show recent use before eviction.

### Segment
A variably sized component of the address space corresponding to a logically meaningful section such as code, heap, data, or stack. In its pure form a segment is a contiguous region of physical memory defined by a base address and a limit register.

### Segment selector
The part of a virtual address in segmented mode that, with a descriptor table, produces the physical (base) address of the segment, which is combined with the offset to produce the linear address of the memory reference.

### Segmentation (segment-based memory management)
A memory management approach that divides the address space into arbitrarily sized segments mapped to regions of physical memory and swapped in and out, with accesses arbitrated through segment registers. In practice it is combined with paging: the segmentation unit produces a linear address that the paging unit then translates to a physical address.
- Intel x86_32 supports segmentation and paging, and Linux allows up to 8K segments per process plus 8K global segments; x86_64 keeps segmentation for backward compatibility but defaults to paging only.
- Contrast: paging uses fixed-size pages and page tables.

### Slab allocator
A Linux kernel allocator that builds custom object caches on top of slabs, where a slab is contiguously allocated physical memory. At startup it pre-creates caches for different objects, such as the task struct or directory entry objects; an allocation takes a free element from the appropriate cache, and when none is free the kernel adds another slab. Because entries are sized to the exact object, it avoids internal fragmentation, and because each slab stores only one object size it avoids external fragmentation.

### Swapping
Moving pages between DRAM and a secondary storage device, which resides on a dedicated swap partition that may be on disk, a flash device, or the memory of another node. It is the mechanism underlying demand paging and page replacement.

### Translation lookaside buffer (TLB)
A small hardware cache in the MMU that holds recent virtual-to-physical translations so that repeated page table navigation can be bypassed. Each entry also carries the protection and validity bits needed to check the access; a TLB miss falls back to the full page table lookup. High temporal and spatial locality make even a small TLB effective.
- Stores (per entry):
  - the virtual-to-physical address translation
  - the protection and validity bits for the access
- A modern x86 core has a 64-entry data TLB, a 128-entry instruction TLB, and a shared 512-entry second-level TLB.

### User level allocator
A memory allocator used for dynamic process state, namely the heap, through the `malloc` and `free` interface. Its calls request memory from the kernel's free pages and release it when done; once the kernel allocates the memory, management of it belongs to the user level allocator.
- Contrast: a kernel level allocator handles kernel pages and static process state.

### Valid bit
The page table entry bit, also called the present bit, that indicates whether the mapping is valid and the page is in physical memory: 1 if present, 0 otherwise. When the MMU sees 0 during an access it raises a fault and traps to the OS to decide whether to admit the access and where to place the page.

### Virtual address
An address a process uses, decoupled from the physical memory where data actually resides. The OS translates almost all virtual addresses into physical addresses, and the visible virtual range can be far larger than the physical memory behind it.

### Virtual page number (VPN)
The high-order portion of a virtual address used to index the page table. The lookup returns the physical frame number, which is then combined with the offset to complete the translation.

## P3L3 Inter-Process Communication

### Ashmem
A form of shared-memory IPC used by the Android operating system. It differs from the SysV and POSIX shared memory APIs in various details and is mentioned in the lecture only as a reference, not explained.

### Attach (shared memory segment)
Establishing a valid mapping between the virtual addresses of a process and the physical addresses that back a shared memory segment. Multiple processes can attach to the same segment, and reads and writes are then visible across all attached processes. In the SysV API this is done with `shmat`.
- Contrast: detach invalidates the mapping; attaching creates it.

### Copy vs. map
The central tradeoff between message-based and memory-based IPC, both of which aim to move data from one process's address space to another's. Message-based IPC spends CPU cycles copying data to and from ports on every transfer, with user/kernel crossings each time. Memory-based IPC spends CPU cycles once to map physical memory into both address spaces, after which no user/kernel switching is needed; the CPU may still copy data into the shared region.
- The mapping cost is a one-time setup cost; if the channel is set up once and used many times it gives a good payoff. Even for one-time use it can perform well: when moving large amounts of data, the CPU time to copy via message-based IPC can greatly exceed the CPU time of the map operation.
- Quiz (IPC comparison): whether message passing or shared memory IPC performs better depends. Message passing requires multiple copies of the data between the processes and the kernel; shared memory incurs the cost of the kernel establishing valid mappings between the processes' address spaces and the shared pages.

### Detach (shared memory segment)
Invalidating the virtual-to-physical address mappings for the virtual address region that corresponded to a shared memory segment within a process. The page table entries for those virtual addresses become invalid. A segment is not destroyed when detached; it may be attached, detached, and re-attached many times through its lifetime. In the SysV API this is done with `shmdt`.

### ftok
A function that generates a token (key) from a pathname and a project id. Passing the same arguments always yields the same key, so it behaves like a hashing function and lets different processes agree on a unique key for a shared memory segment.

### Inter-Process Communication (IPC)
A set of mechanisms the operating system supports to permit multiple processes to interact, covering synchronization, coordination, and communication. IPC mechanisms are broadly categorized as message-based or memory-based.
- Message-based mechanisms: sockets, pipes, message queues.
- Memory-based mechanisms: shared memory, as unstructured shared physical pages or memory-mapped files.
- Remote procedure calls (RPC) provide higher-level semantics, adding protocol detail about data format and the data exchange procedure.

### IPC_RMID
The command passed to `shmctl` to destroy a SysV shared memory segment.

### ipcrm
A Linux command line utility that removes an IPC construct. Using `-m` with a shared memory identifier removes a shared memory segment.

### ipcs
A Linux command line utility that lists all IPC facilities in the system across all IPC types, including message queues and semaphores. Passing `-m` restricts the output to shared memory.

### Local Procedure Calls (LPC)
A Windows mechanism that exploits the copy-vs-map tradeoff. If the data to transfer is smaller than a threshold, it is copied in and out of a communication channel through a port-like interface; otherwise it is copied once into a page-aligned area that is then mapped into the target process's address space.

### Memory-based IPC
A category of IPC in which processes communicate through shared memory, either as unstructured shared physical memory pages or as memory-mapped files accessible by multiple processes.
- Contrast: message-based IPC exchanges discrete messages through an OS-managed channel.

### Message queue
A form of message passing in which the channel understands the notion of messages. A sending process submits a properly formatted message and the channel delivers it to the receiver. OS-level functionality includes message priority and custom message scheduling. Message queues are supported through different APIs, commonly SysV and POSIX.

### Message-based IPC
A category of IPC in which processes create messages and send and receive them over a channel that the OS creates and maintains. Every send and receive requires a system call and a data copy, so a request-response interaction costs four user/kernel crossings and four data copies; these overheads are one of its negatives. One of its positives is relative simplicity: the kernel handles channel management and synchronization, making sure data is not overwritten or corrupted as processes send or receive it.
- Contrast: memory-based IPC maps shared physical memory and keeps the OS out of the data path after setup.

### mmap
In the POSIX shared memory API, the call used to attach (map) a shared memory region into a process's address space.

### msgget / msgsnd / msgrcv / msgctl
The Linux SysV message queue system calls. `msgget` obtains a message queue identifier, `msgsnd` sends a message, `msgrcv` receives a message, and `msgctl` performs a control operation. Their form parallels the SysV shared memory API.

### munmap
In the POSIX shared memory API, the call used to detach (unmap) a shared memory region from a process's address space.

### Pipe
The simplest form of message passing and part of the POSIX standard. A pipe has exactly two endpoints, so only two processes can communicate through it. There is no notion of a message; a pipe carries a stream of bytes written by one process and read by the other. A common use is connecting one process's output to another's input, as with the shell pipe operator.

### Port
The endpoint of a message-based IPC channel. Processes send or write messages to a port and receive or read messages from a port, and the channel passes the message from one port to the other.

### POSIX shared memory API
A shared memory standard that uses files rather than segments. On Linux it has been supported since the 2.4 kernel and, despite being the standard, is not as widely supported as the SysV API. The files are not real filesystem files; they live in the tmpfs filesystem. Because segments are referenced by a file descriptor, no key generation is needed.
- Calls: `shm_open` creates or opens a region, `mmap` attaches it, `munmap` detaches it, `close` (the regular file-descriptor close; the lecture's "shared memory close"; there is no `shm_close`) removes the file descriptor from the process, and `shm_unlink` deletes the shared memory data structures and frees the segment.

### Process-shared synchronization
Synchronization of accesses to shared memory, required because a shared region can be concurrently accessed by all processes that map it, exactly as in multithreaded environments. Options include synchronization primitives from the threading libraries used within processes and OS-provided mechanisms available for IPC.
- Coordination needs: controlling the number of concurrent accesses to a segment (mutexes) and signaling when data is available or ready for consumption (condition variables and signals).

### PTHREAD_PROCESS_SHARED
A pthreads attribute, set via the mutex or condition variable attribute struct, that makes a synchronization variable visible across processes rather than private to one process. The synchronization data structures themselves must also live in shared memory for this to work.

### Segment (SysV shared memory)
A region of shared memory that need not correspond to contiguous physical pages. The OS treats shared memory as a system-wide resource, imposing a limit on the total number of segments and total shared memory size (currently 4000 segments in Linux; as few as 6 in certain operating systems; 128 in more recent, but not current, Linux versions). Creating a segment allocates physical memory and assigns a unique key that other processes use to refer to it. A segment persists until it is explicitly destroyed or the system reboots, unlike process-local memory reclaimed at exit.

### Semaphore (for IPC)
See Semaphore (P3L4).

### Shared memory data structure
The typical casting of a shared memory region into a struct that holds the data plus coordination state. In the pthreads IPC example the struct holds a data buffer and a mutex that controls access to the data; for arbitrary-size transfers it holds the data buffer, a synchronization construct, and flags that track the progress of data movement.
- Stores:
  - data buffer (the information being shared)
  - a synchronization construct (for example a `PTHREAD_PROCESS_SHARED` mutex)
  - progress or status flags, when transferring data in rounds

### Shared memory IPC
IPC in which processes read and write a shared memory region that the OS maps into both of their virtual address spaces. The mapped virtual addresses need not match across processes, and the shared physical memory need not be contiguous. The big benefit is that after setup the OS is out of the way, and system calls are used only in the setup phase.
- Data copies are reduced but not necessarily avoided: data must be allocated from the shared-region virtual addresses, or it has to be copied in and out of the region. A reader can sometimes operate on another process's arguments in place rather than copying them.
- Processes must explicitly synchronize their accesses, and the developer is responsible for any protocol implementation, adding complexity.

### shm_open
The POSIX shared memory call that creates or opens a shared memory region, returning a file descriptor.

### shm_unlink
The POSIX shared memory call that deletes the shared memory data structures and frees the segment. It contrasts with the regular `close` on the file descriptor (the lecture's "shared memory close"; there is no `shm_close`), which only removes the file descriptor from the calling process.

### shmat
The SysV call `shmat(shmid, addr, flags)` that attaches a shared memory segment into a process's address space. If `addr` is provided the segment maps there; if `NULL` is passed the OS chooses suitable addresses. The returned virtual address must be cast by the programmer to the appropriate type.

### shmctl
The SysV call `shmctl(shmid, cmd, buf)` that sends commands to the OS regarding a shared memory segment. Passing `IPC_RMID` as `cmd` destroys the segment.

### shmdt
The SysV call `shmdt(shmid)` that detaches a shared memory segment, invalidating the virtual-to-physical mappings associated with that segment.

### shmget
The SysV call `shmget(shmid, size, flag)` that creates or opens a shared memory segment of the given `size`, with flags such as permissions. The `shmid` key is supplied by the application, not created by the OS, typically generated with `ftok`.

### Socket
A form of message passing in which processes send and receive messages through the socket interface, using `send` and `recv` to move message buffers in and out of a kernel-level communication buffer. The `socket` call creates the kernel-level socket buffer and associates any required kernel processing with it, such as the full TCP/IP protocol stack for a TCP/IP socket. Sockets can connect processes on different machines; when both processes are on the same machine the OS skips most of the protocol stack, which is hidden from the programmer but detectable through performance measurements.

### SysV shared memory API
The System V API for shared memory, in which the OS supports segments identified by an application-supplied key. Its calls create, attach, detach, and control segments.
- Calls: `shmget` creates or opens a segment, `shmat` attaches it, `shmdt` detaches it, and `shmctl` controls it (with `IPC_RMID` to destroy). `ftok` generates the key.

### tmpfs
The filesystem in which POSIX shared memory files live. It looks and feels like a filesystem, letting the OS reuse filesystem mechanisms and data structures, but it is really state held in physical memory, representing a set of physical pages as a file.

### Transfer in rounds
A technique for sending a message larger than the segment size through a fixed-size shared memory region. The sender writes the message in chunks and the receiver reads and saves each chunk until the whole message arrives. The programmer must include a protocol to track the progress of the data movement, usually via flags in the shared data structure.

## P3L4 Synchronization Constructs

### Atomic instruction
A hardware instruction that performs a multi-step, multi-cycle operation either completely or not at all, giving synchronization constructs the low-level support they need to be correct. The hardware guarantees that the operation happens atomically and that mutual exclusion holds across cores: concurrent attempts to execute the instruction cannot run in parallel but are queued and performed serially. Which atomic instructions exist varies by hardware, and their relative efficiency varies by architecture, so software built on a specific atomic must be ported to use one available on the target platform and must use the most efficient one.
- The lecture names three examples:
  - `test_and_set`
  - `read_and_increment`
  - `compare_and_swap`
- A spinlock lock that reads and sets the lock in separate steps is broken because the check and the set take multiple cycles during which threads can interleave; the fix is a single atomic such as `while(test_and_set(lock) == busy);`.

### Barrier
A synchronization construct that behaves like a reverse semaphore. Where a semaphore admits n threads before it blocks, a barrier blocks all arriving threads until n of them have reached the barrier point, at which time they are released.

### Binary semaphore
A semaphore initialized with the value 1. Because its count admits only one thread at a time, it behaves like a mutex, enforcing mutual exclusion. Posting (incrementing the counter) is equivalent to unlocking the mutex.
- Quiz (Mutex via semaphore): `sem_init(&sem, 0, 1)` makes a semaphore behave like a mutex used by threads within a single process: pshared 0 means not shared across processes, and an initial count of 1 lets `sem_wait` admit exactly one thread at a time, while `sem_post` is identical to freeing the mutex.

### Cache coherence
The property, provided on cache-coherent architectures, that a write to a shared value in one CPU's cache is reflected in or removed from the other CPUs' caches by the hardware, so no CPU reads a stale copy. On non-cache-coherent architectures the problem must be handled in software. The hardware achieves coherence by one of two strategies, write-invalidate or write-update, and the choice is fixed by the platform; the software developer has no say in it.
- Also in: P4L3 (DSM inherits write-invalidate and write-update from SMP as "coherence operations", but controls when they are triggered through the consistency model rather than firing them in hardware on every write).

### Cache coherence and atomics
The reason atomic instructions are expensive. Atomic operations always bypass the caches and go directly to the memory controller, which gives a single central point where all references can be ordered and synchronized, removing the race conditions that updating cached copies would allow. The cost is that an atomic can never leverage the cache: it always accesses main memory and contends on it, and it generates coherence traffic to update or invalidate every cached copy regardless of whether the value changed. On SMP systems atomics are therefore more expensive than on a single-CPU system because of bus or interconnect contention, and more expensive in general because they bypass the cache and always trigger coherence traffic.
- Lecture version: atomics always bypass the cache.
- Paper correction (Anderson): "atomics always bypass the cache" is a teaching simplification. Section II.A describes real implementations that cooperate with the cache. Under write-back invalidation the atomic takes the current value from whichever cache holds it dirty while invalidating that copy, avoiding an extra memory write; under distributed-write coherence the needed block is often already cached, so the initial read is skipped and only the final update needs a bus cycle. What is genuinely unavoidable is the arbitration and the coherence traffic: the invalidation happens before the instruction executes even if the instruction does not change the value of the location.

### Compare-and-swap
An atomic instruction named by the lecture as one of the examples of hardware-supported atomics. It compares a memory location against an expected value and swaps in a new value as a single atomic step.

### Contention (spinlock metric)
The contention a spinlock design places on the shared bus or interconnect, caused both by the atomic memory references themselves and by the subsequent coherence traffic. Contention is undesirable because it delays any other CPU trying to access memory and, most relevant to the lock, delays the acquisition and release of the spinlock. A good spinlock reduces contention. Contention can be estimated by tracking the number of failed `test_and_set` operations: the more that fail, the higher the likely contention.

### Delay (spinlock metric)
The waiting time of a spinlock, defined as the time required for a thread to stop spinning and acquire a lock that has just been freed. A good spinlock has low delay, ideally stopping its spin and acquiring the freed lock immediately.

### Delay-based spinlock
A spinlock that introduces an artificial delay to avoid having every thread execute the atomic at the same moment. One variant delays each time a thread notices the lock is free, which improves contention because fewer threads see a freed lock and rush the atomic together, but worsens delay because a thread that sees the lock free still waits, and that wait is wasted when there is no contention. A second variant delays after every memory reference, which also works on non-cache-coherent architectures by cutting the number of references a spinning thread makes, but hurts delay more because the thread waits on every reference, not only when it detects the lock has freed.
- Paper correction (Anderson): the delay schemes are borrowed from network arbitration, which the lecture does not state. Anderson treats a spin lock as analogous to a carrier-sense multiple-access (CSMA) network and adapts its methods, taking statically assigned slots (delay after noticing the release) from BRAM, static delays between references from Aloha, and dynamic delay from Ethernet's exponential backoff (Section IV.A). The dynamic version doubles a processor's mean delay on each collision, caps the delay at a bound equal to the number of processors so it degenerates to static slots under heavy contention, and starts each visit at half its previous delay rather than from zero. He warns the analogy is imperfect: a network collision aborts all parties equally, whereas a test-and-set collision still lets one processor win, so the cost depends on how many collide.

### Dynamic delay
A delay strategy in which each thread draws a random delay from a range that grows with the perceived contention in the system. It avoids the excessive, unnecessary waiting a static delay can impose under low contention, and under light load it outperforms static delay because it adjusts to the actual contention. Perceived contention can be estimated from the number of failed `test_and_set` operations.
- If the delay is applied after every lock reference, the delay grows not only with contention but also with the length of the critical section, so a thread running a long critical section inflates every spinner's delay even though contention has not increased.

### Latency (spinlock metric)
The time it takes a thread to acquire a free lock. A good spinlock has low latency, ideally acquiring a free lock immediately with a single atomic instruction.

### Monitor
A high-level synchronization construct that removes the need to invoke lock/unlock and wait/signal operations explicitly. A monitor specifies a shared resource, the entry procedures for accessing it, and any condition variables used to wake waiting threads; the locking and checking happen on entry and the unlocking and signaling happen on exit, all behind the scenes, which is why it is called high level. Monitors appeared historically in the Mesa language runtime at Xerox PARC. Java supports monitors: every object has an internal lock and `synchronized` methods are monitor entry points, so the compiled code includes the locking and checking, with `notify` the one operation still performed explicitly. The term also names the programming style that brackets a critical section with explicit enter-critical-section and exit-critical-section code using mutexes and condition variables.

### Non-cache-coherent (NCC) and cache-coherent (CC) architecture
The two classes of architecture distinguished by whether coherence is handled in hardware. On an NCC architecture the hardware does not propagate a cached write to other CPUs' caches, so coherence must be dealt with in software or the caches become incoherent; every memory reference effectively goes to memory. On a CC architecture the hardware performs the steps needed to keep caches coherent when a CPU writes a value that others have cached.

### Overhead (spinlock comparison metric)
The metric in the lecture's spinlock performance comparison: the measured difference between the observed execution time and the theoretical ideal limit, assuming no delay or contention, for executing the given number of critical sections. The measurements ran one process per processor on the 20-processor Sequent Symmetry, a cache-coherent write-invalidate platform, with each process executing a critical section in a loop one million times. Under high load the queueing lock performs best and test-and-test-and-set worst; under light load test-and-test-and-set performs well, dynamic delay beats static delay, and the queueing lock performs worst.
- Paper correction (Anderson): the plotted quantity is spin-waiting overhead, the elapsed time minus the simulated ideal (free spin-waiting) time, which isolates the cost of spinning; spinning directly on test-and-set appears only in Fig. 1, which plots elapsed time rather than overhead.

### P and V operations
The historical names for the semaphore wait and post operations, introduced by Dijkstra. P from *proberen*, meaning to test or try, and V from *verhogen*, meaning to increase. A semaphore manipulated with operations named P and V is using wait and post.

### Path expression
A synchronization construct in which the programmer specifies a regular expression capturing the correct synchronization behavior, for example "Many Reads, Single Write," instead of using locks directly. The runtime guarantees that the interleaving of operations satisfies the expression.

### POSIX semaphore
The POSIX semaphore API, which defines one type `sem_t` and three operations that create the semaphore, wait on it, and unlock it. A `pshared` flag indicates whether the semaphore is to be shared across processes.

### Queueing lock
A spinlock that controls which thread or threads see the lock as free at a given time, so that not every thread rushes to acquire it at once. An arriving thread atomically obtains a ticket giving its position in the queue, placed after the current last element, and then spins on its own private element of a flags array. When a thread releases the lock it signals the next thread: the holder resets its own flag, `flags[myplace mod p]`, to `must_wait`, then sets `flags[(myplace + 1) mod p]` to `has_lock`. This implementation is also called the Anderson lock. The design needs the `read_and_increment` atomic, which is less common than `test_and_set`, and it needs n memory locations rather than the single location other locks use, one per processor. For its contention benefit to materialize the architecture must be cache coherent and every flag element must sit on a separate cache line, otherwise changing one element invalidates the whole line and disturbs threads spinning on the others.
- Stores:
  - a flags array of up to n elements, where n is the number of processors; each element is either `has_lock` or `must_wait`
  - a pointer to the current lock holder, whose element is `has_lock`
  - a pointer (`queuelast`) to the last element on the queue, incremented atomically with `read_and_increment`
- From a latency perspective it is not very efficient, because it performs a more complex atomic, `read_and_increment`, which takes more cycles than `test_and_set`, plus the modular index computation; from a delay perspective it is good, because each holder directly signals the next element; from a contention perspective it is the best discussed, because the atomic runs once up front on `queuelast` while spinning occurs on separate flag variables, so invalidation of the atomic variable does not disturb the spinners.
- Quiz (Queueing lock array): with 32 CPUs and flag values `has_lock` (0) and `must_wait` (1), the array is neither 32 bits nor 32 bytes: each element must be on a different cache line, so with 64-byte lines it is 32 x 64 bytes = 2KB.
- Paper correction (Anderson): the lecture presents the queueing lock as a clear win and stops there. The paper adds that queueing makes preemption worse, because a preempted spinner in line forces every process behind it to wait when it reaches the front, which can impose lock-step behavior for a small, frequently accessed critical section (Section IV.B); and that it makes waiting on multiple locks harder, since a processor can be in only one queue at a time. Anderson notes the design was devised independently by Graunke at Sequent, and that on the Symmetry, which has atomic increment but no read-and-increment returning the old value, his measurements protected the sequence number with a separate backoff lock.

### Read-and-increment
An atomic instruction, named by the lecture as one of the hardware atomics, that reads a memory location and increments it as a single atomic step. The queueing lock relies on it to advance `queuelast`; it is less common than `test_and_set`.

### Reader/writer lock (shared/exclusive lock)
A lock that distinguishes read accesses, which do not modify the shared resource and may proceed concurrently, from write accesses, which modify it and require exclusive access. The developer states only the access type wanted, read or write, and the lock handles access control. Supported in many operating systems and runtimes, where it is sometimes called a shared/exclusive lock, with semantics that differ across environments: implementations vary in how recursively obtained read locks are unlocked (a single `read_unlock` releasing all of a thread's recursive `read_lock` operations, or one `read_unlock` per `read_lock`), in whether a reader that owns the lock may be given priority to upgrade it to a writer lock ahead of a newly arriving write request or must release it and re-acquire it with write access, and in whether an incoming reader is blocked when a writer is already waiting, which depends on the coupling between lock state, thread priorities, and the scheduling policy: if a waiting writer has higher priority than an arriving reader, an implementation that respects priority may block the reader even though the current readers would let it join. In Linux the datatype is `rwlock_t`, with lock and unlock operations for reads and for writes.

### Rendezvous point
A synchronization construct that, like a barrier, waits for multiple threads to arrive at a particular point in execution before any proceeds.

### Semaphore
A synchronization construct that expresses count-related synchronization requirements a mutex cannot. It is initialized with an integer value; a thread arriving at a nonzero semaphore decrements the value and proceeds, while a thread arriving at a zero semaphore must wait, so the number allowed through at once equals the initialization value. On leaving the critical section a thread signals the semaphore, incrementing its counter. Initializing with 5, for example, admits exactly five threads before the rest wait. Semaphores were designed by Edsger Dijkstra, and the wait and post operations are historically written P and V.
- (P3L3) Semaphores are also an OS-supported construct for inter-process synchronization: a binary semaphore (value 0 or 1) acts like a lock, a process blocking while the value is 0 and decrementing it to 0 to proceed when it is 1. The SysV semaphore API parallels the SysV shared memory API in form, and a POSIX equivalent exists.
- Also in: P3L3 (semaphores for IPC, with the SysV and POSIX semaphore APIs; canonical kept here in P3L4 Synchronization Constructs, the teaching home, though P3L3 is the earlier lecture).

### Serializer
A synchronization construct that makes it easier to define priorities and hides the need for explicit signaling and explicit use of condition variables from the programmer.

### Shared memory multiprocessor (SMP)
See Shared memory multiprocessor (P3L1).

### Spinlock
One of the most basic synchronization constructs, used to provide mutual exclusion with lock and unlock operations similar to a mutex. Unlike a mutex, a thread that fails to acquire a locked spinlock is not blocked and does not relinquish the CPU; it spins, running on the CPU and repeatedly checking whether the lock has become free, burning cycles until the lock frees or the thread is preempted. Because of its simplicity the spinlock is used as a building block for more complex synchronization constructs.
- Quiz (Spinlock 1 and 2): software-only versions, `if (lock == free) { lock = busy; } else { goto spin; }` and `while (lock == busy); lock = busy;`, are neither correct nor efficient. They waste CPU spinning while the lock is busy, and several threads can see the lock free at once and all set it busy, so both enter the critical section; no purely software implementation can keep the check and the set from interleaving, so hardware support for an atomic check-and-set is needed.

### Spinlock performance metrics
The three metrics by which spinlock designs are judged: latency, the time to acquire a free lock, which should be low; delay or waiting time, the time to stop spinning and acquire a just-freed lock, which should be low; and contention on the shared bus or interconnect from atomic references and coherence traffic, which should be reduced.
- Quiz (Conflicting metrics): reducing latency conflicts with reducing contention, because executing the atomic as soon as possible creates additional contention; reducing delay conflicts with reducing contention, because continuously spinning to notice the release as soon as possible also creates contention. Latency versus delay is not marked as conflicting, since it depends on the algorithm.

### Static delay
A delay strategy that computes a fixed delay from static information such as the CPU ID on which the process runs. It is simple and, under high load, spreads out atomic references so there is little or no contention. It combines the fixed information with the length of the critical section, so one process waits 1x the critical section, another 2x, and so on. Its drawback is unnecessary delay under low contention: with only CPUs 1 and 32 contending, the process on CPU 32 waits about 32 critical-section lengths. Under light load static delay performs worse than dynamic delay because it can naively impose large delays.

### Symmetric multiprocessor
See Shared memory multiprocessor (P3L1); the lecture uses the two names interchangeably for a system whose multiple CPUs share a common memory.

### Test-and-set
An atomic instruction, a very common one that most hardware platforms support (which makes the test-and-set spinlock very portable), that atomically reads a lock's value and sets it. On the first thread the value is zero, so `test_and_set` sets it to one and returns zero, letting the thread proceed; later threads get 1 (busy) back and spin; each such call sets the lock to 1 again, which is harmless because it was already busy.

### Test-and-set spinlock
A spinlock implemented as `while(test_and_set(lock) == busy);`, spinning directly on the atomic. From a latency standpoint it is as good as possible, using one atomic with nothing faster available. From a delay standpoint it can perform well, since the thread spins on the atomic and the very next call detects a freed lock immediately. From a contention standpoint it performs poorly: while threads spin on `test_and_set` the processor goes to main memory on every instruction, delaying every other CPU that needs memory. The core problem is the continuous spinning on the atomic, which forces repeated trips to memory regardless of cache coherence.

### Test-and-test-and-set spinlock (spin-on-read)
A spinlock that separates the test from the atomic: a thread first checks the cached value of the lock and executes `test_and_set` only when that cached copy shows the lock has become free. Also called spin-on-read or spin-on-cached-value. Latency and delay are okay, slightly worse than the plain test-and-set lock because of the extra check. Contention varies by architecture: on a non-cache-coherent architecture there is no improvement, since every reference goes to memory; with write-update it improves, though all processors then see the lock free and try to lock at once; with write-invalidate it is terrible, because every acquisition attempt generates memory contention and invalidation traffic, and because executing the atomic triggers coherence traffic whether or not the value changed, so write-invalidate forces each spinner back to memory even when the lock's value is unchanged.
- Quiz (Test and test and set): with N processors, the memory contention on lock release is O(N) under write-update, since every processor sees the release immediately and issues one `test_and_set`, and O(N^2) under write-invalidate, since the release invalidates all caches, some processors re-read the lock free and issue `test_and_set`, and although only one succeeds every one of them invalidates everybody's caches.
- Paper correction (Anderson): Anderson credits the spin-on-read idea to Segall and Rudolph, not himself; his contribution is the analysis of why it still performs poorly and the delay and queueing alternatives that follow, and he assumes short-circuit evaluation so the `test_and_set` runs only when the cached read already shows the lock free (Section III.B). The lecture describes what happens on release; Anderson frames it as a transient that ends in quiescence: on release and reacquisition there is a quiesce period during which some processors have a pending read miss and others a pending doomed test-and-set, each failing test-and-set re-invalidating every cached copy, so for a small critical section this transient dominates and spin-on-read has almost as much effect on busy processors as spinning directly on a test-and-set, while a long critical section makes the initial slowdown matter less. The time to quiesce on the Sequent Symmetry grew linearly with the number of spinning processors (Fig. 2), and he lists three causes rather than one: the separation between noticing the release and committing to the test-and-set, invalidation on an unchanged value, and the O(P) cost of refilling P caches after one invalidation (Section III.C).

### Wait-free synchronization (RCU)
An optimistic approach to concurrency that avoids explicit locking and waiting, betting that there will be no concurrent writes so reads can proceed concurrently and safely, in order to improve scalability and efficiency. The lecture's example is the read-copy-update (RCU) lock in the Linux kernel. Like all these methods it still requires hardware support to update a memory location atomically, which is the only way to guarantee a lock is properly acquired and protected state changes are race-free.

### Write-invalidate (WI)
A cache coherence strategy in which, once one CPU updates its copy of a value, the hardware invalidates all other cached entries of that value; future references to an invalidated entry cause a cache miss and go to main memory before being re-cached, and the memory location itself is kept up to date using one of the write methods, write-through or write-back. It poses lower bandwidth requirements on the interconnect because only the address, not the value, is sent for invalidation, and after one invalidation subsequent changes on the same CPU need no further invalidations, so the coherence cost can be amortized over multiple changes while the value is not needed elsewhere.
- Also in: P4L3 (write-invalidate as one of the two DSM coherence operations, triggered by the consistency model rather than on every hardware write).

### Write-update (WU)
A cache coherence strategy in which, once one CPU updates its copy of a value, the hardware updates all other cached entries of that value, so subsequent accesses by any CPU are still served from cache. Its benefit is that the new value is available immediately on other CPUs without a main memory access, which helps programs that need the new value on another CPU right away.
- Also in: P4L3 (write-update as one of the two DSM coherence operations, triggered by the consistency model rather than on every hardware write).

## P3L5 I/O Management

### Asynchronous I/O
An I/O access model in which the calling thread is allowed to continue running as soon as it issues the request, rather than blocking. At some later time the user process can check whether the response is available, or the kernel can notify the process that the operation is complete and the results are ready. The lecture distinguishes this true, OS-supported asynchronous I/O from Flash, which only mimicked asynchronous I/O by delegating I/O calls to special helper threads.
- Contrast: synchronous I/O blocks the calling thread on the device wait queue until the response arrives.

### Base Address Registers (BAR)
The registers that determine how much physical memory, starting at which address, is reserved for a device's memory-mapped interactions. They are configured during the boot process in accordance with the PCI protocol.

### Block device
A device, such as a disk, that operates at the granularity of blocks of data delivered to and from the device via the CPU interconnect. A key property is that individual blocks can be accessed directly: given ten blocks on a disk, the ninth can be requested without reading the others. All block devices expose a standardized interface supporting operations to read and write a block of data.
- Contrast: a character device works with a serial sequence of characters via a get/put interface.

### Block device stack
The layered path from an application's file-based interface down to a block device. The application interacts with files; below it the filesystem resolves a file, checks access, and selects the portion to access; the generic block layer masks device-specific differences; and device drivers interact with the physical block devices. In the same way the filesystem provides a consistent file API to user processes, the OS provides a consistent block API to the filesystem. A later refinement inserts the virtual filesystem (VFS) layer between the application's file API and the filesystems; the stack as first presented has no VFS.

### Bridging controller
A device controller that can handle the difference between different types of interconnects, allowing devices on one interconnect type to attach to another.

### Buffer cache
A cache in main memory used by filesystems to reduce the number of disk accesses. Content is written to and read from the cache, and periodically flushed to disk. Forcing flushes to happen only periodically amortizes the cost of a disk access over the multiple writes that hit the cache in between. The `fsync` system call forces a flush.

### Character device
A device, such as a keyboard, that works with a serial sequence of characters and supports a get/put character interface. All character devices expose a standardized interface supporting operations to get and put a character.
- Contrast: a block device operates on individually addressable fixed-size blocks.

### Command register
A device control register that the CPU uses to control the device, for example to instruct a device to perform a transmission.

### Controller
The component, typically integrated into the device packaging, through which a device interfaces with the rest of the system over a CPU/device interconnect such as a PCI bus. The device controller determines what type of interconnect a device can attach to.

### Data register
A device control register used by the CPU to transfer data into and out of the device.

### Demultiplexing
The protocol functionality of determining which process a chunk of data from a device belongs to. Normally the kernel performs demultiplexing, but under OS bypass that responsibility is left to the device itself, since the kernel is out of the data path.

### Dentry (directory entry)
A Linux data structure that corresponds to a single path component traversed while reaching a file. For a path such as `/users/ada`, the filesystem creates a dentry for `/`, for `/users`, and for `/users/ada`. Dentry objects live only in memory and are not persisted.
- Stores:
  - a single path component of a traversed path

### Dentry cache
An in-memory cache maintained by the filesystem containing dentry objects for directories previously visited. It avoids re-reading the files corresponding to every directory along a path when another file in an already-visited directory is accessed. It is soft state: dentries have no on-disk representation.

### Device access chain
The sequence of layers an I/O request traverses. A user process makes a system call for the operation; the OS runs the in-kernel stack for the device and may preprocess the data, for example running the TCP/IP stack to form the appropriate packet, or the filesystem determining the disk block that stores the file data; the OS invokes the device driver, which configures the request to the device using PIO or DMA; and finally the device performs the actual request. Results and events originating on the device traverse this chain in reverse, from device to driver to kernel to user process.

### Device driver
A device-specific software component through which the OS supports a device. The OS must include a driver for every type of device in the system. Drivers are responsible for all aspects of device access, management, and control, including how requests are passed down and how errors and notifications are handled. Device manufacturers provide drivers for each OS where their device is used, and operating systems standardize driver interfaces through a device driver framework so the OS stays independent of any fixed set of devices. The OS thereby achieves device independence (not specialized per device) and device diversity (any device type, given another driver); swapping hardware only requires swapping its driver.

### Device file (/dev)
The file abstraction through which the OS represents each device, so it can interact with devices through the same interface it maintains for files, with the operations handled in a device-specific manner. On UNIX-like systems all devices appear as files under the `/dev` directory; they are special files, not stored on the real filesystem, treated by the special filesystems tmpfs and devfs. Writing content into `/dev/lp0`, for example, prints it on the first line printer identified by the system.
- Quiz (Looking at /dev): listing `/dev` shows names such as `hda` or `sda` (drives, like hard drives, SSDs, or CD-ROMs), `tty` (terminal stations, usable to pipe output to and from terminals), `null` (the null device), and `lp` (printers).

### Direct block
A block pointer in an inode that points directly to a data block. With 1KB blocks, each direct pointer addresses 1KB of file content.

### Direct Memory Access (DMA)
A device access method in which the CPU still writes commands to the device's command registers, but data movement is handled by a DMA controller configured with the memory address and size of the buffer involved. It requires additional hardware support in the form of the DMA controller. Transmitting a 1500B packet takes 1 CPU access to the command register plus 1 DMA configuration operation. DMA configuration is not trivial and costs many more cycles than a memory access, so for smaller transfers PIO is still more efficient.
- Contrast: programmed I/O moves data through the data registers using repeated CPU accesses and needs no extra hardware.
- Quiz (DMA vs. PIO): with a 1-cycle register store, a 5-cycle DMA configuration, and an 8B bus, PIO wins for a keyboard, since one or two stores are cheaper than configuring DMA; for a NIC it depends on transfer size: packets needing fewer than five stores favor PIO, larger transfers favor DMA.

### Double indirect pointer
An inode pointer that points to a block of single indirect pointers, each of which points to a block of data pointers. With 1KB blocks and 4B pointers, a single double indirect pointer can address 256 * 256 * 1KB = 64MB of file content.

### ext2 (Second Extended Filesystem)
The default filesystem in several versions of Linux until it was replaced by ext3 and ext4; it is not Linux specific. A disk partition formatted as ext2 begins with a first block not used by Linux and often used to boot the system, and the rest is divided into block groups whose sizes bear no relation to the physics of the actual disk. Each block group holds a super block, a group descriptor, bitmaps, inodes, and data blocks. ext2 tries to balance the overall allocation of directories and files across the block groups.
- Stores (per block group):
  - super block: number of inodes, number of disk blocks, start of free blocks
  - group descriptor: location of the bitmaps, number of free inodes, number of directories
  - bitmaps used to quickly find free blocks and inodes
  - inodes, each a 128B structure describing exactly one file
  - the actual data blocks

### File
A logical storage unit that maps to some underlying physical storage location. At the user-process level, applications think about interacting with files rather than blocks of storage. In the VFS, a file is the element on which the VFS operates and is abstracted via a file descriptor.

### File descriptor
An integer created when a file is first opened, through which the OS abstracts a file. Operations such as `read`, `write`, locking the file, `sendfile`, and `close` are supported on a file using its file descriptor.

### Flushing
The periodic writing of buffer cache content to disk. Delaying flushes until periodically amortizes the cost of a disk access over the multiple writes that hit the cache in between; the `fsync` system call forces it.

### Generic block layer
A layer in the block device stack that provides a standard interface from a particular OS to all types of block devices, masking device-specific API differences. The full device features remain available through the device driver but are abstracted away from the filesystem.

### Group descriptor
An ext2 structure describing the overall state of a block group.
- Stores:
  - location of the bitmaps
  - number of free inodes
  - number of directories

### I/O device
A hardware component tied to receiving inputs or directing outputs that applications rely on in addition to the CPU and memory. Examples include keyboards, microphones, displays, speakers, mice, hard disks, and network interface cards.
- Quiz (I/O devices): keyboards and microphones are input devices; speakers and displays are output devices; hard disk drives, network interface cards (NICs), and flash cards are both.

### I/O Port Model
A device access model in which the CPU accesses devices via special instructions. x86 platforms specify in/out instructions; each instruction specifies the target device, the I/O port, and a value stored in registers: the value to be written out to the device or the value read from the device.
- Contrast: memory-mapped I/O routes ordinary memory accesses at a dedicated physical address to the device.

### I/O scheduling
A technique for reducing file access overhead whose main goal is to reduce slow disk head movement by maximizing sequential accesses over random accesses. With the head at position 15 and requests to write block 25 then block 17, the scheduler may reorder them to write block 17 on the way to block 25 rather than backtracking.

### Indirect pointer
An inode pointer used to address larger files while keeping the inode small. An indirect pointer points to a block of pointers, each of which points to data. With 1KB blocks and 4B pointers, a single indirect pointer can address 256KB of file content. Indirect pointers slow file access: without them, a block of content takes at most two disk accesses (inode plus block), while a double indirect pointer doubles the accesses needed (inode plus two pointers plus block).

### inode
A persistent per-file data structure maintained by the VFS that serves as the index node for a file: it maintains a list of all data blocks corresponding to the file, which matters because a file's blocks need not be stored contiguously on disk. In ext2 every inode is a 128B structure describing exactly one file. Adding storage allocates a free block and updates the inode with another entry. The approach makes both sequential and random access easy, but a flat list of block pointers limits file size: a 128B inode with 4B pointers addresses only 32 blocks (assuming only block pointers, no metadata), or 32KB with 1KB blocks.
- Stores:
  - list of pointers to the data blocks of the file
  - file ownership and permissions
  - file size
  - whether the file is locked
  - other file metadata

### Interrupt
A path by which a device signals the CPU, generated by the device as soon as it has information for the CPU. The downside is the interrupt handler: the handler steps cost CPU cycles, interrupt masks may be set and reset, and there are indirect effects such as cache pollution.
- Contrast: polling has the OS read device status registers at times it chooses.

### Journaling
A disk access optimization in which updates are written to a log rather than immediately to their proper disk locations, avoiding the random disk accesses that would otherwise be required. The log entry describes the write, such as the block, the offset, and the content. Logged writes are periodically applied to their proper locations so the log does not grow indefinitely. ext3 and ext4, among many others, use journaling. It also addresses the risk that data held in memory by the I/O scheduler is lost on a crash.

### Memory-mapped I/O
A CPU/device interaction model in which device registers appear to the CPU as memory locations at a specific physical address; when the CPU writes to those locations, the integrated PCI controller routes the accesses to the appropriate device. A portion of physical memory is dedicated to device interactions, controlled by the Base Address Registers.
- Contrast: the I/O Port Model uses special in/out instructions naming an I/O port.

### Microcontroller
The device's own CPU, one of the device-specific internals. A device internally has three separate kinds of component: the microcontroller, on-device memory, and any other logic the device needs, such as analog-to-digital conversion chips or chips to interact with the physical network medium.

### Network device
A device that is between a block device and a character device: it delivers more than a character at a time, but its granularity is not a fixed block size. It behaves more like a stream of data chunks of potentially different sizes.

### OS bypass
A configuration in which a device is made accessible directly from user level without going through the kernel. Memory and registers assigned to the device are directly available to a user process. The OS is involved in configuring this, making sure the device's registers and memory are mapped into the user process, then stays out of the way while retaining coarse-grain control, such as enabling or disabling the device or granting more processes access. A user-level driver linked by the process provides the interface, and the device must have enough registers for the OS to map some into user processes while keeping a few for itself.

### Peripheral Component Interconnect (PCI)
A CPU/device interconnect bus connecting device controllers to the rest of the system. Modern platforms typically support PCI Express, which has more bandwidth, lower latency, and support for more devices than PCI-X and PCI, while most platforms still include PCI-X for compatibility. A system may also include other interconnects, such as a SCSI bus for SCSI disks and an expansion (peripheral) bus for devices like keyboards.

### Pinned memory
See Pinning (P3L2).

### Polling
A path by which the CPU reads a device's status registers to determine whether it has a response or data for the CPU. The OS chooses when to poll and can do so when cache pollution is lowest, but polling can delay observing an event and too much polling adds CPU overhead that may not be affordable.
- Contrast: an interrupt is triggered by the device as soon as it has information for the CPU.

### Prefetching
A technique that increases cache hits by fetching nearby blocks during a request, exploiting locality in file access. A read for block 17 may also read blocks 18 and 19 into the cache. This uses more disk bandwidth but can significantly reduce access latency by raising the cache hit rate.

### Programmed I/O (PIO)
A device access method requiring no extra hardware support beyond a basic interconnect like PCI. The CPU issues instructions by writing into the device's command registers and controls data movement by reading and writing the device's data registers. Transmitting a 1500B packet through 8-byte data registers takes 1 command register access plus 188 data register accesses, 189 CPU accesses in total.
- Contrast: DMA offloads the data movement to a DMA controller after a single configuration step.

### Pseudo device
A Linux device, also called a virtual device, that does not represent actual hardware.
- `/dev/null` accepts and discards all output without producing anything, for example to discard a process's output.
- `/dev/random` produces a variable-length string of pseudo-random numbers; `/dev/urandom` is its more robust counterpart, used for example to create files of pseudo-random bytes.

### Status register
A device control register the CPU reads to understand what is happening on the device, including during polling.

### Superblock
A VFS abstraction providing information about how a particular filesystem is laid out on a storage device. It maintains an overall map of the device used both for allocation and lookup, so the filesystem can tell which blocks hold data, which hold inodes, and which are free. Each filesystem keeps additional, filesystem-specific metadata in the superblock.
- Stores:
  - a map of how persistent elements (inodes and data blocks) are organized on the device
  - filesystem-specific metadata

### Synchronous I/O
An I/O access model in which the calling thread blocks. The OS kernel places the thread on the wait queue associated with the device, and the thread becomes runnable again when the response to its request becomes available.
- Contrast: asynchronous I/O lets the thread continue immediately and learn of completion later.

### Triple indirect pointer
An inode pointer that points to a block of double indirect pointers, extending addressable file size further. For the lecture quiz's inode with 12 direct pointers plus one single, one double, and one triple indirect pointer, 4B pointers, and 1KB blocks (256 pointers per block), the maximum file size is (12 + 256 + 256^2 + 256^3) * 1KB, about 16GB; with 8KB blocks it reaches 64TB, because the gain compounds through the indirect levels.

### User-level driver
A library, linked by a user process, that lets the process interact with a device directly under OS bypass without going through the kernel. Like kernel-level drivers, these libraries are usually provided by device manufacturers.

### Virtual filesystem (VFS)
A layer, included in operating systems like Linux, that hides details of the underlying filesystems from higher-level consumers so applications can see files across multiple devices as a single coherent filesystem, support different filesystem implementations, and access files over the network. Applications interact with the VFS through the same POSIX API, and the VFS specifies a detailed set of filesystem abstractions, including the file, inode, dentry, and superblock, that every underlying filesystem must implement.

## P3L6 Virtualization

### Back-end driver
In the split device driver model, the component that resides in the service VM (bare-metal) or in the host OS (hosted), holding the actual driver for the physical device. It is the same driver the OS would use natively and does not need to be modified; it receives wrapped device operations from the front-end driver and fulfills them.
- Contrast: the front-end driver runs inside the guest VM and must be modified.

### Ballooning
A technique for reclaiming machine memory from a guest when the VMM has overcommitted memory. A balloon process (today usually called a balloon driver) runs inside the guest; when the VMM wants memory back it inflates the balloon, and the guest, using its own page-replacement knowledge, selects which pages to surrender. It compensates for the VMM lacking the guest's knowledge of which pages are good eviction candidates.
- Paper correction (Rosenblum & Garfinkel): the lecture does not cover ballooning; the paper introduces it as VMware ESX Server's answer to the shadow-page-table overcommit problem, alongside content-based page sharing, in which the VMM detects identical physical pages across many similar VMs, points the shadow page tables at a single copy, and copies on write if the contents later diverge (for example, 30 Windows VMs needing only one copy of the kernel in memory).

### Bare-metal virtualization (type 1, hypervisor-based)
A virtualization model in which the VMM runs directly on the hardware and manages all hardware resources and the execution of VMs. Because the hypervisor would otherwise need drivers for every device, this model typically integrates a service VM that runs a standardized OS with full hardware-access privileges to host the device drivers and management tasks. Adopted by Xen and by VMware ESX.
- Contrast: in the hosted (type 2) model a full host OS owns the hardware and integrates the VMM as a module.
- Quiz (Bare metal or hosted): VMware ESX, Citrix XenServer, and Microsoft Hyper-V are bare-metal (hypervisor-based); KVM, Fusion, VirtualBox, and VMware Player are hosted. In KVM, however, the host OS switches into a module that assumes a hypervisor-like role, so the rest of the OS plays a secondary, supporting role, like a privileged partition.

### Behavior-sensitive instruction
A sensitive instruction whose result depends on the configuration of resources: on its location in real memory (location sensitivity) or on the processor mode (mode sensitivity).
- Paper correction (Popek & Goldberg): this classification is from the paper, not the lecture. Together with control-sensitive instructions it defines the sensitive instructions, the set a VMM must mediate.

### Binary translation
A full-virtualization technique that inspects guest instruction sequences at runtime, at the granularity of a basic block, such as a loop or a function, before they execute. Blocks free of the problematic instructions are marked safe and run at hardware speed; a block containing one of the non-virtualizable instructions has that instruction translated into an alternate sequence that emulates the desired behavior. It runs unmodified guests. Overheads are reduced by caching translated code fragments and by analyzing only guest kernel code. Pioneered by Mendel Rosenblum's Stanford group and used by VMware.
- Paper correction (Rosenblum & Garfinkel): the paper adds that VMware translates only privileged (kernel) code, caches results in a trace cache so a block is translated only on first execution, and produces output that looks much like paravirtualized code except that changes are applied at first execution rather than to the OS source. Because the source and target instruction sets are nearly identical it is simpler than cross-ISA translation, and it is not only a correctness fix but a performance optimization, since removing frequently-trapping privileged instructions cuts trap overhead that is especially high on deep modern x86 pipelines; once the trace cache is warm, performance is nearly indistinguishable from direct execution.

### Consolidation
Running multiple VMs on a single physical platform. It leads to fewer machines, less space, fewer admins, and potentially smaller electric bills while still running the same degree and type of workload, decreasing cost and improving manageability. It is the benefit that drove virtualization's return once data centers grew large, servers sat around 10 to 20 percent utilization, and operating expenses reached roughly 70 percent of IT budgets.

### Control-sensitive instruction
A sensitive instruction that changes the resources available (such as memory) or changes the processor mode without going through the memory-trap sequence.
- Paper correction (Popek & Goldberg): this classification is from the paper. With behavior-sensitive instructions it defines the sensitive set.

### Device virtualization
The problem of presenting devices to guest VMs, harder than CPU or memory virtualization because devices lack the ISA-level standardization of x86 and vary widely in interface and semantics. Virtualization solutions use one of three models: passthrough, hypervisor-direct, and split device driver.
- Paper correction (Rosenblum & Garfinkel): the paper frames I/O virtualization historically. IBM mainframes used a channel-based architecture where a separate channel processor let the VMM export device access with very low overhead; x86 lost this, and its large diverse device collection makes the VMM I/O layer a large effort while some devices have severe performance needs. The paper's three concrete approaches only partly line up with the three models: the hosted architecture routes I/O through the host OS's drivers (highest overhead); ESX Server borrows Linux drivers directly (lower overhead, the hypervisor-direct model); and VMware's optimized paravirtualized virtual devices are the split-device-driver idea. It predicts channel-like devices and hardware support that let in-VM drivers reach the device with no trap into the VMM, which is the passthrough model made safe.

### dom0 and domU (Xen domains)
In Xen, VMs are called domains. The privileged service domain is dom0, which runs all the device drivers and the configuration and management tasks; the guest domains are domUs. Xen itself is the hypervisor.

### Efficiency (Popek and Goldberg property)
One of the three VMM properties: a statistically dominant subset of instructions executes directly on the real processor with no VMM intervention. It is the property that formally excludes pure emulators and software interpreters from being VMMs.
- Paper correction (Popek & Goldberg): the lecture names this property "performance" (VMs run at close to native speed). The paper states it formally as the direct-execution requirement.

### Equivalence (Popek and Goldberg property)
One of the three VMM properties: any program runs with an effect identical to running on the bare machine, except for differences caused by timing and by resource availability. It is what distinguishes a VMM from an ordinary time-sharing OS and from plain virtual memory.
- Paper correction (Popek & Goldberg): the lecture names this property "fidelity" (the hardware the VM sees matches the physical platform). The paper gives the formal equivalence statement above.

### Extended page tables and tagged TLBs
Hardware-assisted memory virtualization support in which page-table and TLB structures carry VM identifiers. Tagging lets the hardware distinguish entries belonging to different VMs, so VM context switches (world switches) are more efficient: the TLB entries of the previous VM no longer have to be flushed, because the MMU matches a translation by both virtual address and VM identifier, so entries of different VMs coexist.

### Front-end driver
In the split device driver model, the component inside the guest VM. It takes device operations issued by guest applications and wraps them in special messages passed directly to the back-end component. It looks like a wrapper for the actual device API, so guest applications are unmodified and keep making the same device requests. It must be modified, which is why the split model is usable only in paravirtualized guests.
- Contrast: the back-end driver, the unmodified real driver in the service VM or host.

### Full virtualization
Virtualization that runs an unmodified guest OS, with no additional software or policy changes required to run in the virtualized environment. On pre-2005 x86 it was achieved by binary translation. For memory, it requires the guest OS to keep observing a contiguous linear address space starting at zero.
- Contrast: paravirtualization modifies the guest, which knows it is virtualized.

### Hardware-assisted virtualization
Virtualization support added to x86 circa 2005 by AMD (Pacifica) and Intel (Vanderpool). It closes the holes in the 17 non-virtualizable instructions so they trap to the hypervisor, adds the root/non-root protection mode, adds a hardware-walked per-vCPU control structure, tags memory structures with VM identifiers through extended page tables and tagged TLBs, improves I/O virtualization support, and adds new instructions such as one to switch protection mode.
- Paper correction (Rosenblum & Garfinkel): writing in 2005, the paper noted both vendors had only announced support, and that rather than making existing modes virtualizable they add a new execution mode letting a VMM use direct execution safely, reducing both the number of traps and the cost of each. It forecast that this makes direct-execution-only VMMs possible on x86 and that, if as effective as the old IBM mainframe support, the value of a fully compatible VM abstraction would outweigh any performance benefit from breaking compatibility through paravirtualization.

### Hosted virtualization (type 2)
A virtualization model in which a full host OS manages the hardware and integrates a VMM module that provides VMs with their virtual platform interface, invoking host device drivers and components as needed. It reuses the host's existing services and mechanisms, so less must be built for the VMM, and it can run guest VMs and native host applications side by side. KVM, built into Linux and paired with the QEMU hardware emulator, is one example; it leverages all the advances contributed by the Linux open-source community, so it quickly adapts to new features and fixes.
- Contrast: bare-metal (type 1) virtualization runs the VMM directly on the hardware.
- Paper correction (Rosenblum & Garfinkel): the paper's canonical hosted example is VMware Workstation, whose hosted architecture it illustrates (the term comes from the paper's reference Sugerman et al.). The layer reuses the host's drivers, turning a guest disk access into a system call that reads or writes a host file and rendering the guest display into a host window. Its three advantages are installing like an ordinary application, inheriting the host's rich x86 driver support, and reusing the host's scheduling and resource management; its two disadvantages are high I/O overhead, because every I/O request crosses into the host and traverses its layers, and the host OS's lack of resource-management support for performance isolation and service guarantees, which together are why VMware's ESX Server dropped the host OS.

### Hypercall
In paravirtualization, an explicit call a guest OS makes to the hypervisor to request an operation, behaving like a system call. The hypercall traps to the hypervisor, which performs the operation with the data the guest supplied and passes control back. Paravirtualized guests use hypercalls instead of attempting operations they know will fail, and can batch page-table updates into a single hypercall to amortize the VM-exit cost.

### Hypervisor-direct model
A device virtualization model in which the hypervisor intercepts every device access from the guest, translates it into a generic representation of an I/O operation for that device family (network or disk), and traverses the hypervisor-resident I/O stack down to the real device driver. The requested device need not match the physical device, so the VM stays decoupled from the platform and migration and device sharing remain easy. The downsides are the latency added by emulation and the hypervisor's exposure to the complexity of all device drivers it must support.

### Innocuous instruction
Any instruction that is not sensitive. It can execute directly without VMM mediation.
- Paper correction (Popek & Goldberg): this term is from the paper's instruction classification.

### KVM (kernel-based VM)
The lecture's example of hosted virtualization, built into Linux. The Linux host provides all physical hardware management and runs regular Linux applications directly; guest-VM support comes from the KVM (VMM) module plus the hardware emulator QEMU, used in virtualizer mode: QEMU does not emulate a foreign platform, the guest sees the exact hardware resources of the physical platform, and QEMU intervenes only on certain critical operations, such as any aspect of I/O management (all device drivers are handled by the host Linux), to pass control to the KVM module and the host OS. KVM was originally developed so regular Linux applications could use the virtualization-related hardware appearing in commodity platforms; once users realized it could also run guest operating systems, it became, three months later, a virtualization solution in the mainstream Linux kernel.

### Machine address
In memory virtualization, an address in the underlying physical platform's real memory. The hypervisor maps guest physical addresses to machine addresses; contiguous physical addresses can map to discontiguous machine addresses.
- Contrast: a guest physical address is what the guest kernel believes it owns; a virtual address is what guest applications use.

### Memory virtualization
Providing each guest with memory it can treat as its own. Three address types are distinguished: virtual addresses used by guest applications, physical addresses used by the guest kernel, and machine addresses on the real platform. In full virtualization two page tables exist, one in the guest OS mapping virtual to physical and one in the hypervisor mapping physical to machine; the first translation is done purely in software, while only the second can leverage the MMU and TLB. Because translating through both on every reference is too expensive, the hypervisor instead keeps a shadow page table. In paravirtualization the guest can register its page tables with the hypervisor directly, so only one table is needed.

### Paravirtualization
Virtualization that gives up unmodified guests in favor of performance: the guest OS knows it runs on a hypervisor rather than on native hardware. Instead of attempting operations that would fail, it makes explicit hypercalls to the hypervisor. For memory it need not use contiguous physical memory starting at zero, can register its page tables with the hypervisor, and can batch page-table updates into one hypercall. Adopted by Xen.
- Contrast: full virtualization runs unmodified guests.
- Quiz (BT and PV): access to a swapped-out page traps to the hypervisor in both binary-translated and paravirtualized VMs, because the page is not present and the hardware MMU faults regardless of the approach. An update to a page table entry does not always trap; it depends on whether the guest OS has write permission to the page tables it uses.
- Paper correction (Rosenblum & Garfinkel): the paper's canonical example is Disco, a VMM for the non-virtualizable MIPS architecture, not Xen (Xen is not discussed in the paper). Disco replaced the MIPS equivalents of `POPF` and the code-segment read with accesses to a special memory location, removing their traps and improving performance. The paper frames paravirtualization as replacing the non-virtualizable parts of the instruction set with easily virtualized equivalents so most applications still run unmodified while the OS must be ported; its main drawback is incompatibility (a ported OS, vendor cooperation, no legacy operating systems, no easy migration). In spite of that drawback, academic projects favored it because building a VMM with both full compatibility and high performance is a significant engineering challenge; VMware, aiming at fast, compatible x86 virtualization, built binary translation instead.

### Passthrough model (VMM-bypass)
A device virtualization model in which the VMM-level driver only configures a guest's access permissions to a device (for example, granting access to the device's memory registers), after which the guest VM accesses the device directly without involving the VMM. The guest has exclusive access and operates the device through its own driver, so a device of the exact same type must exist on the physical platform. Sharing a device across VMs is difficult because the hypervisor must continually reassign ownership with no concurrent access, and binding the device to a VM breaks the decoupling that makes migration easy.

### Popek and Goldberg theorem
Theorem 1 of the paper: for a conventional third-generation machine, a VMM can be constructed if the set of sensitive instructions is a subset of the set of privileged instructions. The subset condition guarantees that every instruction the VMM must mediate traps, which is the formal basis of trap-and-emulate. The lecture compresses this into "privileged instructions trap".
- Paper correction (Popek & Goldberg): the paper models the VMM as a control program with a dispatcher at the trap entry point, an allocator deciding which resources each VM gets, and interpreter routines, one per privileged instruction, that simulate the trapped instruction's effect. Pre-2005 x86 violated the subset condition because of 17 sensitive-but-unprivileged instructions, and hardware-assisted virtualization later satisfied it by forcing those instructions to trap.

### Privileged instruction
An instruction that traps when executed in user mode but not in supervisor mode. In a trap-and-emulate VMM, each privileged instruction issued by the guest causes a trap to the hypervisor, which checks whether to allow it and, if so, emulates the expected hardware response invisibly to the guest.
- Paper correction (Popek & Goldberg): the paper defines "privileged" strictly as trapping in user mode, which is why it calls the lecture's "privileged instructions that do not trap" imprecise: those 17 are sensitive but not privileged.

### Protection rings
The hardware privilege levels on x86, which has four, called rings. Ring 0 has the highest privilege and can execute all instructions and access all resources; ring 3 has the least and holds applications, whose privileged operations trap to ring 0. Natively the OS runs at ring 0. In virtualization the hypervisor takes ring 0 and the guest OS is pushed to ring 1, with applications remaining at ring 3. The guest OS and the VMM must not share a protection level, so one faulty guest cannot take down the hypervisor.

### Resource control (Popek and Goldberg property)
One of the three VMM properties: a program cannot access resources not allocated to it, and under certain circumstances the VMM can regain control of resources it has already allocated. The VMM is in complete control of who accesses which resources and when.
- Paper correction (Popek & Goldberg): the lecture names this property "safety and isolation". The paper states it as the resource-control requirement above.

### Root and non-root mode
The two protection modes added to more recent x86, within each of which the four rings exist (also called host and guest). In root mode everything is permitted and the hypervisor resides at ring 0; in non-root mode certain operations are not permitted, and a guest VM runs its OS at ring 0 and applications at ring 3. A guest OS attempt at a privileged operation causes a VMExit that switches to root mode and passes control to the hypervisor; a VMEntry returns control and switches out of root mode.

### Sensitive instruction
An instruction that is either control sensitive or behavior sensitive. Sensitive instructions are the ones a VMM must mediate; the Popek and Goldberg theorem requires them to be a subset of the privileged instructions.
- Paper correction (Popek & Goldberg): this classification, and its split into control-sensitive and behavior-sensitive, is from the paper; any non-sensitive instruction is innocuous.

### Service VM (privileged VM)
In bare-metal virtualization, a special VM running a standardized OS with full hardware-access privileges that holds all the device drivers and runs configuration and management tasks for the hypervisor. It exists so device manufacturers need not write drivers per hypervisor. In Xen it is dom0; VMware ESX once used a Linux-based control core but moved configuration to remote APIs.

### Shadow page table
A single page table the hypervisor maintains that re-maps guest virtual addresses directly to machine addresses, bypassing the guest physical addresses, so hardware MMU and TLB translation can be used on each reference. The hypervisor keeps it consistent with the guest's own table: it invalidates the shadow table on context switch and write-protects the guest page table so that a guest attempt to establish a new mapping traps into the hypervisor, which then updates the shadow table.
- Paper correction (Rosenblum & Garfinkel): the paper calls this the traditional technique and names the structure the shadow page table. It adds that because the VMM controls the shadow page table it can page a VM out to disk and overcommit machine memory beyond physical memory, with the catch that the VMM lacks the guest's knowledge of good eviction candidates, which ESX Server addresses with a balloon driver; it also notes content-based page sharing to reclaim identical pages, and flags hardware-managed shadow page tables as a promising future direction.

### Split device driver model
A device virtualization model in which device access is split between a front-end driver in the guest VM and a back-end driver in the service VM (bare-metal) or host (hosted). The front-end wraps guest device operations in special messages passed directly to the back-end component, which uses the unmodified native driver. The front-end drivers look like wrappers for the device API, so guest applications are unmodified. Because the front-end must be modified, the model is usable only in paravirtualized guests. It eliminates device-emulation overhead, because the virtualization layer does not have to reverse engineer what the guest OS wants, and centralizes the back-end for better management of shared devices.
- Quiz (Hardware virtualization): the split device driver model is still relevant with hardware support for virtualization, because all device requests are consolidated in the service VM, which can make better decisions and enforce stronger policies about how the device is shared without relying on the physical device to support the desired sharing behavior.

### Trap-and-emulate
The core processor-virtualization strategy: the guest runs directly on the hardware, and whenever it issues a privileged instruction the processor traps to the hypervisor, which decides whether to allow the operation. An illegal operation may trigger punitive action such as shutting down the VM; an allowed one is emulated so the guest receives the hardware response it expected. The intervention must be invisible to the guest.
- Paper correction (Popek & Goldberg): this is exactly the VMM construction the paper proves correct, built from a dispatcher, an allocator, and per-instruction interpreter routines. It works only if every instruction that could affect resource control traps, which is the content of Theorem 1.

### Virtual machine (VM)
A guest operating system together with its applications and its virtual resources, running under the illusion that it owns the underlying hardware, all or in part. Also called a guest or a domain. Multiple VMs coexist on one physical machine, with the virtualization layer allocating and managing the real hardware and isolating the VMs. The lecture defines a virtual machine as an efficient, isolated duplicate of a real machine, a definition lifted from Popek and Goldberg, who capture it formally with the equivalence, efficiency, and resource-control properties.
- Quiz (Virtualization tech): by Popek and Goldberg's classical definition, only VirtualBox is a virtualization technology, since with system virtualization the hardware visible to the VM is identical, or at least very similar, to the physical platform. The Java Virtual Machine is a language runtime providing system services and portability, very different from the physical machine, and Virtual GameBoy emulates a different hardware platform.

### Virtual machine monitor (VMM, hypervisor)
The virtualization layer that supports the coexistence of multiple VMs on one physical machine, allocating and managing the real hardware resources and providing isolation across VMs. The lecture gives it three responsibilities: fidelity (the hardware the VM sees matches the physical platform), performance (VMs run at close to native speed), and safety and isolation (the VMM fully controls resource access).
- Paper correction (Popek & Goldberg): the paper names the three properties more formally as equivalence, efficiency, and resource control.

### Virtualization
Deploying multiple operating systems concurrently on one physical hardware platform, each with the illusion of owning the hardware. Originating at IBM in the 1960s for sharing mainframes, it later returned to address server underutilization and operating costs. Its benefits include consolidation, easier migration, improved availability and reliability, containment of bugs and malicious code, OS research, and affordable support for legacy operating systems.
- Paper correction (Rosenblum & Garfinkel): the paper argues the combination that killed VMMs in the 1980s, cheap hardware plus capable multitasking operating systems, is what later caused the problems VMMs solve, since cheap hardware proliferated underused machines and more capable but fragile operating systems pushed admins back to one application per machine. It reframes the VMM as "less a vehicle for multitasking and more a solution for security and reliability", better placed than today's complex and ossified operating systems to implement migration and security, and lists benefits the lecture omits: checkpoint-and-rollback undo, VMM-level security (Livewire intrusion detection, ReVirt break-in analysis), high-assurance isolation (NSA NetTop), trusted computing with remote attestation (Terra), and virtual appliances.

### VM control structure (VMCS / VMCB)
The per-vCPU control structure that captures the state of a virtual processor under hardware-assisted virtualization, called the VM control structure (VMCS) on Intel and the VM control block (VMCB) on AMD. The hardware walks this structure and can specify whether a given system call should trap.
- Stores:
  - per-vCPU virtual processor state
  - trap configuration, specifying which operations (such as particular system calls) cause a trap to the hypervisor

### VMExit and VMEntry
The transitions between non-root and root mode on hardware-assisted x86. A guest OS attempt to perform a privileged operation causes a VMExit, a trap that switches to root mode and passes control to the hypervisor; when the hypervisor finishes it performs a VMEntry, returning control to the VM and switching out of root mode.

### VT-x, VT-d, and IOV / VMDq
Intel's branding for its virtualization support along three axes. VT-x is CPU support: fixing the non-virtualizable instructions and adding features such as extended page tables, with VT-x2 and VT-x3 in later generations. VT-d is chipset support for I/O virtualization, I/O routing, and direct device access (for example SR-IOV at the platform level). IOV (I/O virtualization) and VMDq (virtual machine device queues) are device-resident support, such as DMA remapping so a device DMAs into the correct VM's memory and multiple logical queues so each VM gets its own interface.

### World switch
A context switch between VMs under hardware-assisted virtualization. Tagging page tables and TLBs with VM identifiers (extended page tables and tagged TLBs) makes world switches more efficient, because the TLB entries of the previous VM no longer have to be flushed: the MMU matches a translation by both virtual address and VM identifier.

### x86 non-virtualizable instructions
The 17 x86 instructions that, before 2005, were privileged in the sense of requiring ring 0 yet did not trap when issued from another protection level; they failed silently instead. Because control was not passed to the hypervisor, it could not emulate the intended behavior, and because the failure was silent the guest OS assumed success and continued. Enabling or disabling interrupts via `POPF` / `PUSHF`, which manipulate a bit in a privileged register, is the lecture's example. These instructions are why pre-2005 x86 could not be virtualized by trap-and-emulate alone, and binary translation was the software workaround.
- Quiz (Problematic instructions): with `POPF` / `PUSHF` failing silently outside ring 0, the guest could not request interrupts enabled, could not request them disabled, and could not find out the state of the interrupt-enabled bit (all of the above). The guest assumes each request completed and may interpret other information on the stack as if it came from the privileged register.
- Paper correction (Popek & Goldberg): the precise statement is that these 17 are sensitive but not privileged, since they read or change privileged state yet do not trap outside ring 0; they violate Theorem 1's subset condition. The count of 17 comes from Robin and Irvine's 2000 analysis of the roughly 250 Pentium instructions, not from this paper.
- Paper correction (Rosenblum & Garfinkel): the paper gives two concrete examples. `POPF` is used to set and clear the interrupt-disable flag but in unprivileged mode silently ignores the change rather than trapping; and unprivileged instructions let a guest read the code-segment register to see the processor's real privilege level, and because the read does not trap the VMM cannot patch what the guest sees, so the guest observes the physical rather than its virtual privilege level.

## P4L1 Remote Procedure Calls

### Binding
The mechanism the client uses to find and connect to a server before any call is made. Binding determines which server supports the needed service, chosen by service name and version number, and how to reach it: the server's IP address, port, and transport protocol. For connection-based protocols such as TCP/IP, the connection is established during this step. Binding depends on the server having first registered itself (see Registry).
- Paper correction (Birrell & Nelson): the paper binds through the Grapevine distributed database rather than a per-machine registry. A client binds an importer of an interface to an exporter, naming the interface by type (which abstract interface) and instance (which particular implementor); an importer that supplies only the type is bound to the closest running instance. Importing does not touch the exporter's data structures, which matters for a server with hundreds of users, and a binding is implicitly broken when the exporter crashes and restarts, because a per-export unique identifier is re-checked on every call.

### Call semantics
The guarantee an RPC system gives about how many times the remote procedure actually ran, given that calls and replies can be lost. The lecture presents RPC's synchronous, local-like call behavior and SunRPC's bounded retries without naming a formal spectrum.
- Paper correction (Birrell & Nelson): the packet-level protocol defines the semantics precisely. If the call returns to the user, the server procedure was invoked exactly once; otherwise an exception is reported and the procedure was invoked either once or not at all, with the user told neither which nor whether the fault was a server crash or a communication failure.
- Contrast: at-least-once semantics arise from blindly retransmitting a whole call, as SunRPC's retry on timeout (a bounded, specified number of times) does, which is unsafe for non-idempotent procedures; exactly-once (on return) is the paper's guarantee, achieved by pairing retransmission with call identifiers and a per-activity sequence number so the callee discards duplicates. The ONC RPC standard (RFC 1831) ties these to the transport: over an unreliable transport a reply implies at least once, a remembered transaction ID can give some degree of at-most-once, and only a reliable transport yields exactly once.

### Client stub
The automatically generated code that stands in for the remote procedure inside the client process. When the client calls a procedure such as `add`, execution jumps to the stub instead of to a real implementation, and to the rest of the process the stub looks like the real procedure. The stub creates a buffer, populates it with the function name and arguments (marshaling), and hands it to the RPC runtime to send to the server. On return it receives the reply and places the result into the client address space.
- Paper correction (Birrell & Nelson): the paper calls this piece the user-stub and says the stubs were generated by a program called Lupine from Mesa interface modules, so the lecture's generic "RPC package tools" are Lupine. It also notes that if user and server were linked directly on one machine without the stubs, the program would still work.

### Exporter
In the paper's binding model, the server side of a binding: the party that makes an interface available so that importers can bind to it. Importing has no effect on the exporter's data structures, and the binding is implicitly broken when the exporter crashes and restarts.

### eXternal Data Representation (XDR)
The language-agnostic interface definition language used by SunRPC, defined separately from any programming language. XDR is used both to specify the interface and to specify the encoding of data types. All types named in the `.x` file must be XDR-supported types.

### Grapevine
The distributed, replicated database the paper uses as its binding registry, spread across several servers rather than running per machine. It holds the information that lets an importer locate an exporter of an interface by type and instance.

### Importer
In the paper's binding model, the client side of a binding: the party that binds to an exporter of an interface. An importer naming only the interface type is bound to the closest running instance; naming both type and instance selects a particular implementor.

### Interface definition language (IDL)
The language in which the client-server agreement is expressed: it describes the interface a server exports, including, at a minimum, the procedure name, the argument types, and the result type, plus a version number. The version number lets a client find the most up-to-date server or the server whose version fits the rest of the client program. An IDL can be language-agnostic (SunRPC's XDR) or language-specific (Java RMI uses Java). It is used only to define the interface and to let the RPC system generate stubs, marshaling procedures, and service-discovery information; it is not used to implement the service.

### Java RMI (Java Remote Method Invocations)
An RPC system pioneered by Sun for client/server communication among address spaces in the JVM. Because Java is object-oriented and entities interact through method invocations rather than procedure calls, it is called remote method invocation. Its IDL is language-specific to Java, since all clients and servers are written in Java. Client and server have stubs, but the server-side stub is called a skeleton. Its runtime splits into a Remote Reference Layer and a Transport Layer.

### Lupine
The paper's stub-generating program, which produced the user-stub and server-stub from Mesa interface modules. It also enforces pointer avoidance at stub-generation time, checking that arguments and results are compatible with the lack of a shared address space.

### Marshaling
The process by which the client stub encodes the procedure descriptor and the arguments into a single contiguous data buffer in an agreed-upon format. Arguments may sit in noncontiguous memory in the client address space, but the transport level requires one contiguous buffer, which is why marshaling is needed. The agreed format fixes the serialization layout; for example, an array may be sent as a length followed by elements, or as elements followed by a terminator, and both endpoints must agree in advance. Marshaling routines are generated by the RPC system's compiler, not written by the programmer.

### Partial failure
A failure in which an RPC call does not cleanly complete or cleanly fail, so the client cannot tell what succeeded. When a client hangs on a call, the cause may be a lost client packet (request), a lost server packet (response), a downed network link, a downed server machine, a failed server process, or an overloaded server process, and from a timeout alone the runtime can conclude only that it was any of these, not which. RPC systems return a single catch-all error that captures that something went wrong without claiming the exact cause.
- Paper correction (Birrell & Nelson): the paper is precise about the guarantee behind this error. On an exception the procedure was invoked either once or not at all, and the client is told neither which nor whether the fault was a server crash or a communication failure. This "call failed" exception is the primary way a client tells a remote call apart from a local one.

### Pointer handling
The RPC treatment of pointer arguments. A local pointer references data valid in both the caller's and callee's address space, but in RPC a client pointer points to arbitrary data in the remote address space, so it cannot simply be passed. An RPC system can either disallow pointer arguments entirely, or allow them and marshal the referenced data (not the pointer) into the buffer; on the server the unmarshalling code passes the address of the unpacked data to the local procedure, so a pointer is effectively "passed."
- Paper correction (Birrell & Nelson): the paper does not solve this in the runtime but rules it out at stub-generation time. The programmer must avoid arguments or results incompatible with the lack of a shared address space, and Lupine checks this avoidance; emulating a shared address space is discarded as too expensive for the hardware.

### Portmapper
The SunRPC registry process, which runs on every machine. The server contacts it to register a service and the client contacts it to find a service's contact information. It is started on Linux with `sudo /sbin/portmap`, and `/usr/sbin/rpcinfo -p` lists the program id, version, protocol, socket port number, and service name of every service registered with it. Portmapper itself is registered with both TCP and UDP on socket 111.

### Registration
The step a server performs before any client can bind to it, announcing to the world which procedures it supports, what arguments they require, and where it can be contacted. In SunRPC the registration code is autogenerated by `rpcgen`, and on start the server registers its service name, version, protocol, and port number with the local registry.

### Registry
The systems software that maintains a database of available services so that binding can work. It acts as the yellow pages for services: given a service name and version, it returns the matching server's contact information (IP address, port, transport protocol). A registry can be a distributed online platform open to any service, or a per-machine daemon that knows only local processes, in which case the client must already know the host address and the registry supplies only the port. It needs a naming protocol, from exact name-and-version matching up to schemes that resolve synonyms (requesting `sum` could return `add`).
- Paper correction (Birrell & Nelson): the paper's registry is the Grapevine distributed database, replicated across several servers rather than running per machine, and binding there pairs an importer with an exporter named by interface type and instance.

### Remote Reference Layer (Java RMI)
The component of the Java RMI runtime that contains the common code needed to provide reference semantics. It can support unicast (a client interacting with a single server) or broadcast (a client interacting with multiple servers), and it can specify different return semantics, such as return-first-response and return-if-all-match.
- Contrast: the Transport Layer, the other half of the RMI runtime, implements the transport-protocol functionality.

### RPC (Remote Procedure Call)
A mechanism that simplifies building interactions across address spaces and machines by making a call to a remote server look like an ordinary local procedure call. It offers a high-level interface for data movement and communication, handles low-level communication errors, and hides the complexities of cross-machine interaction. RPC calls are synchronous: the caller blocks until the procedure completes and returns, as with a local call. RPC also performs type checking, hides machine representation differences (endianness, floating point, negative numbers) behind an agreed data representation, supports multiple transport protocols rather than being tied to one, and layers in higher-level mechanisms such as access control, authentication, and fault tolerance.
- Paper correction (Birrell & Nelson): the paper adopts the same rule, that the semantics of remote calls should be as close as possible to those of local calls, and follows it even against distributed-systems practice: it provides no time-out limiting a call's duration in the absence of machine or communication failures, because local calls have none.
- Also in: P3L3 (RPC is listed among the IPC mechanisms as a higher-level form that adds protocol detail about data format and the exchange procedure; it is defined in full here in P4L1).

### RPC encoding
The layout of an RPC message on the wire. Because a server can support multiple programs, versions, and procedures, passing the procedure arguments alone is not enough: the request header must also carry the procedure id, version number, and request id, and the same header is included in the server's response. The arguments or results follow, encoded into a byte stream that depends on the data type; the in-memory and on-wire representations need not map 1-1, as long as both sides use a standard format they can deserialize. The whole packet is preceded by the transport header (TCP/UDP).

### RPC handle
The client handle created when binding happens and passed on every subsequent RPC call, letting the RPC runtime track all RPC-related state per client. In SunRPC it is returned by `clnt_create` and can also track the status of the current request and carry error or authentication information.

### rpcgen
The SunRPC compiler that turns an interface written in an `.x` file into language-specific stubs. Run as `rpcgen -C <interface>.x`, it generates `<interface>.h` (datatype definitions and function prototypes), `<interface>_svc.c` (server stub, including the server `main` with the registration code), `<interface>_clnt.c` (client stub), and `<interface>_xdr.c` (marshaling/unmarshalling routines used by both sides). By default it generates code that is not thread safe; `rpcgen -C -M <interface>.x` makes the generated code thread safe, though `-M` does not by itself produce a multithreaded server. On Solaris `-A` generates a multithreaded server; on Linux a multithreaded server must be implemented manually.
- Quiz (return type of `square_proc_1`): with `rpcgen -C` it is `square_out *`, as in `square_out *square_proc_1(square_in *, CLIENT *)`, with the result in statically allocated storage; with `rpcgen -C -M` it is `enum clnt_stat`, as in `enum clnt_stat square_proc_1(square_in *, square_out *, CLIENT *)`, where the caller supplies a pointer to where the result is written and the return value is the RPC call status.

### RPCRuntime
In the paper's five-piece structure, the component present on both machines that transmits packets between the caller and callee machines. One RPCRuntime runs on the caller machine with the user and user-stub, and another runs on the callee machine with the server and server-stub.

### Server stub
The automatically generated code on the server that receives the incoming packets, parses the bytes to determine which procedure and arguments were requested, unmarshals the data into local data structures, and calls the real local procedure. It then takes the computed result, puts it into a buffer, and returns it to the client over the connection.
- Paper correction (Birrell & Nelson): the paper calls this piece the server-stub and generates it, like the user-stub, with Lupine from Mesa interface modules.

### Skeleton
In Java RMI, the name for the server-side stub. It plays the role the server stub plays in RPC.

### SunRPC
An RPC package originally developed by Sun in the 1980s for its Network File System on UNIX and now widely available elsewhere. It assumes the server machine is known up front and uses a per-machine registry (portmapper) that a client must contact on the target machine before using a service. It makes no assumption about the client's or server's programming language, relying on the language-agnostic XDR for both interface and data-encoding specification. It allows pointers and serializes the pointed-to data, and it supports error handling, including a configurable number of retries when a request times out, while trying to return meaningful errors as often as possible.
- Paper correction (Birrell & Nelson): SunRPC retries on timeout a bounded (specified) number of times; blindly retransmitting the whole call gives only at-least-once semantics, which is unsafe for non-idempotent procedures. That is a different point on the call-semantics spectrum from the paper's Cedar protocol, which pairs retransmission with call identifiers and a per-activity sequence number so the callee discards duplicates and preserves the exactly-once-on-return guarantee.

### Transport Layer (Java RMI)
The component of the Java RMI runtime that implements the transport-protocol functionality, whether TCP, UDP, shared memory, or another protocol.

### Unmarshalling
The process by which the server stub takes the buffer from the network protocol and, using the procedure descriptor and the argument types the described procedure expects, extracts the correct byte chunks and uses them to initialize data structures matching the argument types. The arguments are allocated in the server address space and set to the values the client placed in the buffer. Like marshaling, these routines are generated by the RPC system's compiler rather than written by the programmer.

### Version number
A field in the interface definition identifying a release of a collection of procedures. When several servers offer the same procedure, the version number lets a client pick the most up-to-date one or the one matching the rest of its program. In SunRPC the version applies to an entire collection of procedures and is one of the identifiers the registry tracks.

### .x file
The SunRPC interface file, written in XDR, in which the server specifies the datatypes used for procedure arguments and results and describes the RPC service and its procedures. It names the service (for example `SQUARE_PROG`), the procedures it supports (each with a procedure ID, input and output datatypes, and a version), and a service id. Clients use the service name, procedure name, and version number, while the RPC runtime uses the service id, procedure id, and version id. It is compiled by `rpcgen`.

### XDR data types
The set of types that may appear in an `.x` file. Defaults include `char`, `byte`, `int`, and `float`. XDR also provides `const` (compiled to a `#define`d value in C), `hyper` (64-bit integer), `quadruple`, and `opaque` (uninterpreted binary data, like the C byte type, used for things such as images). The lecture calls `quadruple` a 120-bit float; the note records that it is actually 128 bits (IEEE quadruple precision per XDR RFC 4506 and the Sun/Oracle XDR documentation). Arrays come in fixed-length (`int data[80]`) and variable-length (`int data<80>`) forms; a variable-length array compiles to a struct with an integer `len` and a pointer `val`, and the receiver reads the first four bytes as the length before allocating and copying the data. Strings are the exception: they are stored in memory as normal null-terminated strings but encoded for transmission as a `len` and `data` pair.
- Stores (compiled variable-length array struct):
  - `len`: the actual number of elements in the array
  - `val`: a pointer to where the array data is stored

### XDR encoding
The on-the-wire binary representation XDR defines, separate from its role as an IDL. All data types are encoded in multiples of four bytes, so a single-byte argument takes one byte and three bytes of padding. Big endian is the transmission standard, and all data is converted to it before transmission regardless of either machine's endianness. Integers use two's complement and floating-point numbers use IEEE format.
- Example: a variable-length string (max 10) holding `"hello"` takes 6 bytes in a C process's memory (5 characters plus the null terminator) and 12 bytes on the wire: 4 for the length (5), 5 for `h-e-l-l-o` (the null terminator is not transmitted), and 3 bytes of padding.
- Quiz: a full variable-length `int` array of five elements takes 24 bytes on the wire (4 for the length plus five 4-byte ints, no padding, excluding any RPC/protocol header) but 28 bytes in memory on a 32-bit machine (`len` 4 + `val` pointer 4 + 20), because the wire form carries the length and data but not the pointer.

### XDR routines
The marshaling and unmarshalling routines generated into `<interface>_xdr.c` and used by both client and server. The compiler also generates cleanup operations such as `xdr_free`, typically called within a user-defined `*_freeresult` procedure where the user specifies which state to deallocate after an RPC request; the runtime calls that procedure automatically once it finishes computing the results.


## P4L2 Distributed File Systems

### Cache coherence mechanism
The machinery a DFS needs to keep the portions of a file cached on clients consistent with the server's representation of the file. If two clients cache the same portion and one modifies it and sends the update to the server, a coherence mechanism is what lets the other client become aware of the change.
- Coherence can be triggered on demand (any time a client accesses a file), periodically, or when a client opens a file.
- The mechanism may be client-driven or server-driven.

### Caching (in a DFS)
Allowing clients to locally maintain a portion of filesystem state, such as a file block, and to perform operations (`open`, `read`, `write`) on that cached state. Serving a file from a local cache gives lower latency on file operations because no network cost is incurred, and increases server scalability because local service reduces server load. The cost is that clients must then interact with the server more often: to notify it of modifications and to query it so they can detect that cached files were changed by someone else. Caching requires a stateful server; a stateless server cannot support it because consistency cannot be managed without state.
- Quiz (File Caching): in a DFS with a single file server and many clients, files or blocks can be cached in client memory (the client's buffer cache), on the client's local storage (hard disks, SSDs), or in the file server's buffer cache; the server cache may not be very useful when many clients access it at once with high request interleaving, leaving little locality.

### Concurrent write-sharing
The access pattern in which a new writer wants to write a file concurrently with a current writer that has not closed it. In the lecture's Sprite design, when the new writer's request arrives, the server contacts the current writer to gather the dirty blocks. When the server realizes that this writer has not closed the file, the current writer writes back its dirty blocks and the server marks the file not cacheable, disabling caching for everybody. Both writers continue to have access but all operations go through the server. When a writer closes the file, the server sees it (every operation goes through the server) and makes the file cacheable again; the remaining clients can then start caching the file again.
- Paper correction (Nelson et al.): on detecting concurrent write-sharing at open, the server takes two actions. It tells the one client that has the file open for writing, if any, to write all its dirty blocks back (there can be at most one such client), and it tells all clients that currently have the file open that the file is no longer cacheable, so they drop its blocks and send future accesses to the server. Clients that are not currently open but still hold stale blocks are not notified; they take consistency actions the next time they open the file. Disabling is per file and only while sharing is concurrent, and for simplicity Sprite does not re-enable caching for a file that is still open once it becomes cacheable again, which contradicts the lecture's scenario, where the remaining writer still has the file open.

### Delegation
An NFSv4 mechanism in which the server delegates to a client all rights to manage a file for a given period of time, which avoids the periodic update checks the client would otherwise perform.

### Directory service
See File vs. directory service (P4L2).

### Distributed file system (DFS)
An environment that involves multiple machines in the delivery of the filesystem service. A DFS lets the OS hide the fact that a machine may have no local physical storage: files are maintained on a remote filesystem accessed over the network, behind the same high-level filesystem interface the OS exports to abstract local storage devices.

### File handle
In NFS, an identifier the server creates when an `open` request arrives. It contains information about the server machine and about the file and is returned to the client, which passes it on later accesses via NFS. If the file is deleted or the server machine dies, the handle becomes stale.
- Stores:
  - information identifying the server machine
  - information identifying the file
- Quiz (NFS File Handle): a stale handle means only that the file on the remote server was removed. An outdated file may be a consistency problem but does not make the handle stale, a server that is not responding is an RPC layer (possibly network) error, and NFS does not limit how long a file stays open.

### File sharing semantics
The rules a DFS gives clients for when one client's writes become visible to others. On a single UNIX node, a modification by any process is immediately visible to every other process, even before the change reaches disk, because the processes share the same buffer cache. A DFS cannot cheaply offer this: a write pushed to the server still takes time to arrive, message latencies vary, and there is no safe bound on how long to delay a read to guarantee no staleness. To keep performance acceptable, a DFS typically sacrifices some consistency and accepts more relaxed semantics, such as session semantics, periodic updates, immutable files, or transactions.

### File vs. directory service
The observation that a filesystem holds two kinds of files, regular files and directories, whose access patterns often differ, in terms of locality, lifetime, size distribution, and access frequency, so a DFS may apply one type of semantics to regular files and another to directories, or, with periodic updates for both, use less frequent write-backs for regular files than for directories, since directories are more frequently shared.

### Hotspot
In a partitioned DFS, a machine that becomes overloaded because a file it holds is frequently accessed by most clients. Hotspots make balancing a partitioned system harder, since the distribution of files must account for how they are accessed.

### Immutable files
A file-sharing strategy in which an old file is never modified: you either delete it or create a new file with a new name (e.g. uploading a modified photo to Instagram or Facebook).

### Lease-based locking
The mechanism NFS uses to support locking with server-side state. When a client acquires a lock, the server assigns a time period during which the lock is valid; the client must release the lock within that time or explicitly extend it. This handles client failure: when the lease expires the server can assign the lock to another client, and the returning client knows it no longer holds a valid lock and must redo its changes.

### Network File System (NFS)
A distributed file system in which clients access files across the network. Clients request and access files through the VFS, using the same file descriptors and operations they use for local files; the VFS determines whether a file belongs to the local filesystem or must be pushed to the NFS client for the remote filesystem. The NFS client talks to the NFS server via RPC; the server turns the request into a filesystem operation delivered to the server's local VFS and local filesystem, where it looks identical to a request from any local application.

### NFS versions
NFSv3 is stateless; NFSv4 is stateful, so NFSv4 can support operations like file caching and file locking. Even though NFSv3 is stateless, implementations typically include modules that provide some stateful functionality. For files not accessed concurrently, NFS behaves with session semantics: on `close` all changes are flushed to the server, and on `open` a check updates cached portions if necessary. NFS also supports periodic updates, which break session semantics when multiple clients concurrently update a file; by default the periods are 3 seconds for files and 30 seconds for directories, because directories are modified less frequently and their changes are more easily resolved. NFSv4 adds a delegation mechanism, lease-based locking, and a reader/writer lock called "share reservation" with mechanisms for upgrading between reader and writer.
- Quiz (NFS cache consistency): among UNIX, session, periodic, and immutable, the answer by default is "neither". Not immutable, since files can be modified; not UNIX, since updates are not guaranteed to be immediately visible; not purely session, since it can periodically check for intermediate updates during a session; not purely periodic, since changes still propagate on `close` and are checked on `open`. If the periodic checks are disabled, NFS behaves with session semantics.

### Partitioning
A way to distribute a fileserver in which every machine holds only a subset of all the files; partitioning may be based on filename, on directory (partitioning the hierarchical namespace), or on other criteria. It scales better than replication because adding machines means more files can be supported, and writes are simple because a file lives on a single machine. The downsides are that when a partition goes down its data can no longer be accessed, and balancing is harder because file access patterns can create hotspots.
- Contrast: replication puts all files on every machine; a common hybrid partitions the files and then replicates each partition.
- Quiz: with three machines holding 100 files each, partitioning stores 300 files and loses 33% if one machine fails, while replication stores 100 files and loses 0%.

### Peer
A node in a DFS where files are stored on and served from all machines, blurring the line between servers and clients. Every peer maintains files and provides the filesystem service, each taking some portion of the load by servicing some requests, often those for files local to that peer.
- (P4L3) In DSM the same idea names a node that both requires access to state located elsewhere and provides access to its local state, each peer owning some portion of the overall application state (the union of the pieces on all nodes). This differs from a peer-to-peer system, where configuration and management tasks are performed cooperatively by all peers, whereas a peer distributed application may still have some nodes that provide overall configuration or management.
- Also in: P4L3 (DSM peer: a node that both consumes remote state and provides its local state, contrasted with a peer-to-peer system).

### Periodic updates
A file-sharing strategy that bounds inconsistency in time. The client writes changes back to the server periodically, and the server can periodically send invalidation notifications; once a client receives such a notification it must sync with the most recent version of the file. The filesystem can provide explicit operations for a client to `flush` its updates to the server or `sync` its state with the remote server.

### Remote file access (true remote file service)
The extreme remote file service model in which the file stays on the server and every single operation passes through the server, with the client making no attempt at local caching or buffering. The benefit is that the server has full control and knowledge of how clients access and modify a file, which makes it easier to keep the filesystem consistent. The downsides are that every file operation pays a network cost (even repeated reads of a read-only file, since local caching is bypassed) and that scalability is limited, because the server is overloaded sooner and can serve fewer clients.
- Contrast: the upload/download model moves the whole file to the client for local modification.

### Remote file service: a compromise
The middle ground between upload/download and true remote file access, in which clients are allowed to use their local memory or disk to store at least part of a file, including downloading blocks they are accessing and prefetching blocks they may soon access. The server keeps insight into and some control over client accesses, which eases consistency, while staying out of the way enough to let some operations happen on the client and reduce load. The cost is that the server becomes more complex, maintaining extra state to provide consistency guarantees, and the client must understand file-sharing semantics unlike those of a normal local filesystem.

### Replication
A way to distribute a fileserver in which the filesystem is replicated onto multiple machines so each machine holds all the files. Client requests can be load balanced across all machines for better performance, the system is more available, and it is fault tolerant because when one replica fails the others serve clients with no degradation. The downside is that writes become more complex: clients may be forced to write synchronously to all replicas, or write to one replica and have a background job asynchronously propagate the write. If replicas get out of sync they must be reconciled, for example by voting, where the majority wins.
- Contrast: partitioning gives each machine only a subset of the files; adding machines to a replicated system does not let it support a larger filesystem.
- (P4L3) In DSM the same technique copies state onto multiple nodes so several nodes can access it at once. More general than migration, it is the sensible choice for multiple readers and writers but requires consistency management: writes must be correctly ordered and the most recent copies propagated for up-to-date reads. Replicas can also be created explicitly for load balancing, hot spot avoidance, or reliability, and because overhead is proportional to the number of replicas, limiting replicas controls it.
- Also in: P4L3 (DSM state replication across nodes, more general than migration, requiring consistency management; overhead proportional to the number of replicas).

### Sequential write-sharing
The access pattern in which a new writer opens a file for writing after a previous writer has closed it. In the lecture's Sprite design the server contacts the old writer to gather all dirty blocks (convenient because the client tracks its dirty blocks); if the old writer has closed the file, the server updates its stored writer to point to the new writer, and the new writer may then proceed and cache the file. A fresh `open` by any client still goes through the server, so client and server keep version numbers to stay in sync.
- Paper correction (Nelson et al.): the paper treats sequential write-sharing as two problems with two mechanisms (Section 5.2). Version numbers handle a stale copy in the opener's own cache; the server tracking the last writer and forcing it to flush on a new open by a different client handles current data still sitting in another client's cache. The lecture's single "gather dirty blocks" step is only the second mechanism.

### Session semantics
A relaxed file-sharing scheme in which the client writes back whatever data was modified on `close`, and on `open` skips the cache and checks the server for a more recent version. A client may read a stale version of a file, but at `open` and `close` it is consistent with the rest of the filesystem at that moment. Session semantics are easy to reason about but poor for concurrent sharing: two clients that want to see each other's writes must constantly `close` and re-`open` the file, and files kept open for long periods can become severely inconsistent.
- Quiz (DFS Data Structure): with a server-driven mechanism and session semantics, the server's per-file structures are readers, current writers (plural), and version number, not "current writer". Server-driven means the server pushes invalidations, so it must know who has the file; changes become visible only when a session closes and a subsequent client opens the file, so overlapping sessions can write concurrently. Session semantics does not specify what happens when all of these writers close the file: one version may become the valid one, the versions may be merged, or an error may be raised to the clients.

### Sprite access-pattern analysis
The study the lecture attributes to the Sprite authors measuring how files are accessed in the production filesystem used by their department, used to justify Sprite's design. The reported findings: 33% of all file accesses are writes (so 66% of operations can be improved by caching, and a write-through policy cannot leverage the cache for writes); 75% of files were open less than 0.5 seconds and 90% less than 10 seconds (so session-semantics overheads were still too high); 20-30% of new data was deleted within 30 seconds and 50% within 5 minutes, and file sharing was rare (so write-back on close was judged unnecessary). The authors still needed to support concurrent access even though they did not optimize for it.
- Paper correction (Nelson et al.): the access-pattern numbers come from the "BSD study" (Section 3), a separate trace-driven analysis of three time-shared VAX-11/780s running 4.2 BSD UNIX; Sprite's designers reused that trace rather than tracing Sprite itself, and the paper uses the trace in a simulation (Tables 1 and 2) estimating cache-consistency overhead and again in Section 7 to estimate per-user I/O rates for sizing a Sprite server. A measurement study of Sprite's own production access patterns came later, in Baker et al. (SOSP 1991).
- Paper correction (Nelson et al.): the write figure is "about one-third of all file accesses are writes" (Section 4.3), and the limit is an upper bound, since about a third of accesses are writes a write-through scheme "cannot reduce disk or server traffic by more than two-thirds". The two-thirds improvement is a ceiling on what caching can save, not a count of operations definitely improved.
- Paper correction (Nelson et al.): the paper rejects write-on-close with the same open-duration numbers but frames sharing differently. "Rare" sharing is the paper's expectation about Sprite's own write-sharing, used to justify optimizing the consistency algorithm for the no-sharing case (Section 5); the deletion and open-duration statistics are the BSD study's, and the paper does not list sharing frequency among the BSD study's access statistics in Section 4.3. The paper's own write-sharing evidence is the Section 5.3 simulation: of all write traffic, 4041 blocks were written through for concurrent write-sharing and 6887 flushed for sequential write-sharing, and consistency accounted for about one-fourth of server traffic.

### Sprite cache consistency
Sprite's handling of keeping client caches consistent, which the lecture uses as its case study. Every `open` operation goes to the server, which means directories cannot be cached on the client. When a client wants to open a file being written by another client, the server contacts the writer and collects all outstanding dirty blocks. Caching is completely disabled on concurrent writes, with all writes serialized on the server side; because concurrent writes are infrequent, this cost is not significant.
- Paper correction (Nelson et al.): routing every open through the server is a deliberate design choice with a known cost, not just a consequence of write-back. The consistency algorithm depends on the server being notified whenever one of its files is opened or closed so it can detect concurrent write-sharing, and this "prohibits performance optimizations (such as name caching) that allow clients to open files without contacting the files' servers" (Section 5). Andrew made the opposite choice, using server callbacks. The paper estimates (Table 8, Section 8) that adding Andrew-style name caching and callback to Sprite would improve client-visible speed by only a few percent but cut server and network utilization by as much as one-third, potentially letting one server support 50% more clients.

### Sprite distributed file system
The DFS the lecture studies as a case study in cache consistency. Sprite supports caching and uses a write-back policy to send changes to the server.
- Paper correction (Nelson et al.): cache consistency is only one of the paper's two contributions. The other, which the lecture does not cover, is that Sprite's caches vary in size dynamically: the file system and the virtual memory system each manage a pool of physical pages and negotiate over memory by comparing the ages of their oldest pages, so the file cache can grow to occupy most of a client's memory when virtual memory does not need it (Sections 1 and 6). The paper's headline results are about caching's performance payoff, not consistency: client caches let diskless workstations run within 0-12% of workstations with local disks, cut server load by a factor of two or more, and cut network traffic by about a factor of four.

### Sprite per-file client state
The information a Sprite client keeps on a per-file basis to support caching and the write-back policy. The writer keeps a timestamp on each modified block to enforce the 30-second write-back policy, and the version number lets client and server detect when the client's cached copy is out of date on the next `open`.
- Stores:
  - cache (overall yes/no)
  - cached blocks
  - timer for each dirty block
  - version number

### Sprite per-file server state
The information a Sprite server keeps on a per-file basis to track who is using a file and to drive consistency. The server also maintains a cacheable flag per file so it can enable or disable caching when concurrent sharing begins or ends.
- Stores:
  - readers
  - writer
  - version

### Sprite write-back policy
Sprite's rule for propagating changes to the server. Every 30 seconds a client writes back all blocks that have not been modified within the last 30 seconds; a file may be opened and closed multiple times by the client before any data is sent to the server. The intuition is that recently modified blocks will continue to be modified, so forcing write-backs on them wastes effort, and this avoids sending the same blocks to the server repeatedly. The lecture ties the 30-second threshold directly to the observation that 20-30% of new data was deleted within 30 seconds.
- Paper correction (Nelson et al.): the paper does not derive the 30-second interval from the 30-second deletion figure. It adopts "a delayed-write policy similar to the one used in UNIX: every 30 seconds, all dirty blocks that haven't been modified in the last 30 seconds are written back" (Section 4.3), which is the UNIX convention (the 30-second sync interval) rather than a number tuned to the trace; a block reaches the server's cache in 30-60 seconds and the disk 30-60 seconds after that. The deletion statistics motivate delayed writes in general: because 20-30% of new data dies within 30 seconds and 50% within 5 minutes, "a policy that delays writes several minutes can substantially reduce the traffic", and the paper plans to experiment with longer intervals, so the trace argues for a longer delay than 30 seconds, not for 30 specifically.

### Stateful server
A file server that maintains information about the clients in the system, which files are being accessed, which types of accesses are performed, which clients have a file cached, and which clients have read or written the file. Because of this state the server can allow caching and guarantee consistency, support functionality like locking, and let clients request relative blocks ("next kB of data") instead of absolute offsets. On failure the state must be recovered to keep the filesystem consistent, which requires checkpointing so the state can be rebuilt to represent what the clients were doing before the failure, and there are runtime overheads incurred by the server to maintain state and execute the consistency protocols.
- Contrast: a stateless server keeps no state and so cannot support caching or consistency management.

### Stateless server
A file server that keeps no state: it has no notion of which files or blocks are being accessed, which operations are performed, or how many clients are accessing how many files. Every request must be completely self-contained, which suits the extreme models but rules out any model that relies on caching, since consistency management is impossible without state, and means more bits are transferred per request. The positives are that no CPU or memory is spent managing state and that the design is resilient: because requests rely on no internal state, a failed server simply needs to be restarted: clients reissue any requests that timed out and receive the same answers they would have received anyway, with no special recovery on either side.
- Contrast: a stateful server maintains client and access state and can therefore support caching, consistency, and locking.

### Transactions
A file-sharing strategy in which the filesystem exports an API that lets clients group file updates into a single batch to be applied atomically.

### Upload/download model
The extreme remote file service model in which a client that wants to access a file downloads the entire file, performs its modifications locally, and then uploads the entire file back to the server. The benefit is that all modifications are done locally and therefore quickly, with no network cost per operation. The downsides are that the client must transfer the whole file even for a small modification, and that the server loses file access control once it hands the file over, since it has no idea what the client is doing with the file or when it will return it.
- Contrast: true remote file access keeps the file on the server and sends every operation to it.

### Version number (Sprite)
A counter Sprite uses so a client and the server can stay in sync about whether the client's cached copy of a file is current. The client keeps a version number per cached file and the server keeps one per file; on `open`, which always goes through the server, a mismatch tells the client its cached copy is stale.
- Paper correction (Nelson et al.): the paper splits sequential write-sharing into two separate problems with two separate mechanisms (Section 5.2). Version numbers solve the first, that the opening client may hold out-of-date blocks: the server increments the file's version each time it is opened for writing, and a client flushes its cached copy on open if its version differs from the server's. The second problem, that current data may still sit in another client's cache because the last writer need not have flushed on close, is solved separately by the server tracking the last writer and, on a new open by a different client, telling that last writer to flush its dirty blocks through before the opener reads. The lecture's "contact the old writer and gather dirty blocks" is the second mechanism, so it is not the same check as the version number.

### Write-back policy
A caching policy in which modifications are accumulated in the client cache and sent to the server later, rather than on every write. Sprite adopts a write-back policy because the access-pattern analysis showed a write-through policy cannot leverage the cache for writes (about a third of accesses are writes).
- Contrast: a write-through policy sends each write to the server immediately and so cannot reduce write traffic through caching.

## P4L3 Distributed Shared Memory

### Access algorithm (SRSW, MRSW, MRMW)
The classification of a DSM solution by the memory-access pattern the higher-level application expects, which determines what consistency and sharing support the DSM layer must provide.
- Single reader/single writer (SRSW): the DSM layer only gives the application access to additional remote memory; there are no consistency- or sharing-related challenges to support.
- Multiple readers/single writer (MRSW): a harder case where reads must return a current value and writes must be ordered.
- Multiple readers/multiple writers (MRMW): the most general case; MRSW is a simpler special case of it, and the lesson focuses the rest of the material on MRMW.
- Paper correction (Protic et al.): the paper presents these not as access patterns but as classes of DSM algorithm, each with a characteristic coherence policy. SRSW algorithms prohibit replication (the central-server and "hot potato" migration algorithms fall here). MRSW is also called read-replication and is usually invalidation-based, since a write must prevent use of stale copies; this is the class Li and Hudak's manager algorithms belong to. MRMW is also called full-replication, allows replicated copies with read and write permission, and often serves with write-update protocols, propagating each update to all copies by multicast or broadcast.

### Access latency
The core performance metric for a DSM solution, since the core service DSM provides is memory access. Local memory access is faster than remote access, so a DSM design tries to maximize the proportion of local accesses. Network costs make remote access slower, but through smart placement of data, migration across nodes, and the sharing semantics enforced on updates, the DSM layer can hide these differences from applications.
- Quiz (DSM Performance): if access latency is the primary concern, caching and replication suit the design, not migration. Migration is fine only for single reader/single writer; with multiple readers and writers pages flip back and forth between nodes, which can increase latency. Caching brings data to the node where it is accessed; replication creates copies potentially closer to where data is accessed. With multiple concurrent writes, caching and replication can also lead to high overheads (Sprite disabled caching on detecting concurrent writers).

### Causal consistency
A consistency model that detects possible causal relationships between updates and guarantees that causally related writes are correctly ordered and seen in the same order by all processes. For writes that are not causally related (concurrent writes) there are no ordering guarantees. A write is treated as potentially dependent on a value read earlier by the same process, so a process must see the earlier write before the later, dependent one. Like sequential consistency, writes performed on the same processor are visible in the same order on other processors.
- Paper correction (Protic et al.): causal consistency is not one of the models the paper defines. Its taxonomy runs sequential, processor, weak, release, lazy release, and entry, with no entry for strict or causal consistency; the lesson draws causal consistency from the general distributed-systems literature (Tanenbaum). The lesson's rule, that potentially causally related writes are seen in the same order by all processes while concurrent writes may be seen in different orders, matches the standard definition in that literature.
- Quiz (Consistency Models Quiz 2): P3 and P4 observe the updates to m1 and m2 in reverse orders, and the two updates are not causally related. The execution is not sequentially consistent (all processors must observe the same order) but is causally consistent (the updates are not causally related, so this is fine).
- Quiz (Consistency Models Quiz 3): P1 reads y from m2 (written by P2), then writes z to m3; P4 sees z at m3 while still seeing 0 at m2, and P3 sees the opposite order. The execution is neither sequentially nor causally consistent: the reverse orders are illegal under sequential consistency, and because P1 read y from m2 before writing z to m3, the writes are potentially causally related, so every processor must observe the m3 update after the m2 update.
- Quiz (Consistency Models Quiz 5): ignoring the sync operations from quiz 4 (where P2 and P3 observe the operations in arbitrary orders), the rest of the execution is not causally consistent, because causal consistency does not permit the writes from a single processor to be arbitrarily reordered.

### Coherence operations (write-invalidate, write-update)
The two consistency strategies DSM inherits from SMP systems for keeping multiple copies of data consistent.
- Write-invalidate: when one processor updates a variable, other processors' cached copies of that variable are invalidated.
- Write-update: when one processor updates a variable, other processors' cached copies are updated to the new value.
- In SMP these operations are triggered by hardware on every write; the overhead of doing that on every write in a DSM system is too high once network costs are considered, so DSM controls when they are triggered through the consistency model.

### Consistency management
The DSM function of maintaining meaningful semantics once multiple copies of the same data page are stored in multiple locations: ensuring writes are correctly ordered and that the most recent copies of state are propagated across nodes for up-to-date reads. Replication requires it; one way to control its overhead is to limit the number of replicas, since overhead is proportional to the number of replicas.

### Consistency model
A guarantee that distributed state changes will behave in a defined way as long as the upper software layers follow a certain set of rules. The model holds that memory behaves correctly only if the software follows those rules, which implies the software must use certain memory-access APIs or set its expectations based on the guarantees offered. The exact design of a DSM system depends on the consistency model it enforces, and the model also determines when coherence operations are triggered.

### Distributed shared memory (DSM)
A service that manages memory across multiple nodes so applications have the illusion of running on a single shared-memory machine. Each node owns some portion of the physical memory and provides reads and writes on it, and those reads and writes may originate from any node. Each node participates in consistency protocols so shared accesses have meaningful semantics. A node may contribute only a portion of its physical memory to the global shared memory, using the rest for caching, replication, or metadata needed by the DSM layer, and to achieve low latency the DSM layer caches pages on the nodes where they are accessed. DSM permits scaling memory beyond a single machine's limits by connecting many cheap machines, and is increasingly relevant because commodity interconnects offer low latencies through Remote Direct Memory Access (RDMA) interfaces.

### Eager coherence (proactive, pessimistic)
A coherence approach in which a node pushes invalidation messages out as soon as data is written, similar to the server-based approach from the DFS lecture. Also called proactive or pessimistic.
- Contrast: lazy (reactive, optimistic) coherence, in which a node instead polls for modification information.
- Paper correction (Protic et al.): the paper attaches the eager/lazy distinction to specific named consistency models rather than to coherence triggering in general. In its terminology, release consistency propagates modifications on each release and is sometimes called eager consistency, with Dash and Munin as examples; lazy release consistency postpones propagation until the next relevant acquire and sends only the modifications associated with the chain of synchronization operations on that specific lock, with TreadMarks as the example.

### Entry consistency
A consistency model that associates every ordinary shared variable with a specific synchronization variable, so that an acquire propagates only the subset of data that variable guards. The lesson mentions associating different synchronization operations with different granularities as an option, but does not fully develop entry consistency as a separate model.
- Paper correction (Protic et al.): the paper treats entry consistency as a distinct, more aggressive model beyond release consistency, requiring each ordinary shared variable to be associated with a synchronization variable so an acquire moves only the data that variable guards; Midway first implemented it. The lesson's single acquire/release pair describes release consistency, not entry consistency, so the lesson's "entry/acquire" label does not line up with the paper's naming.

### False sharing
An effect that arises when sharing granularity grows: two unrelated variables, x and y, lie on the same page, and separate processes on different nodes exclusively access x and y respectively. The DSM system interprets the two writes as concurrent access to a shared page and triggers coherence mechanisms that are logically valid but functionally superfluous.
- Paper correction (Protic et al.): the paper frames granularity as a two-sided trade-off. Coarser blocks save directory storage and suit applications with high reference locality, but raise the probability that different processors contend for the same block even when they touch unrelated parts of it. It lists false sharing together with thrashing as the two adverse effects of coarse-grain, virtual-memory-based software DSM.

### Global map
Replicated metadata that maps a page id to its manager (home) node, letting any node determine which node knows everything about a given page. The manager information for every page is replicated on each node, while the per-page metadata itself is partitioned across the system at each manager. A fixed manager can be identified directly from bits of the address; for more flexibility, an object id can index a global mapping table whose entry can be changed to reassign the manager without changing the object identifier.
- Stores:
  - page id to manager (home) node mappings, replicated on every node

### Hardware DSM
DSM supported by a physical interconnect. The OS on each node believes it has access to much larger physical memory and can establish virtual-to-physical mappings pointing to physical addresses on other nodes. Memory accesses that reference remote locations are passed to the network interconnect card (NIC), which translates them into interconnect messages sent to the correct remote node. The NICs are involved in all aspects of memory management, access, and consistency, and support some atomics. This hardware is typically very expensive and reserved for high-end machines.
- Paper correction (Protic et al.): hardware DSM operates at a small, non-structured granularity, typically a cache line, so it is essentially an extension of the cache-coherence schemes of scalable shared-memory multiprocessors. The finer granularity minimizes false sharing and thrashing, and hardware search and directory functions are much faster than software ones, but advanced coherence and latency-reduction techniques complicate design and verification. The paper classifies hardware DSM into three families: cache-coherent non-uniform memory architectures (CC-NUMA, e.g. Memnet, Dash, SCI), cache-only memory architectures (COMA, e.g. KSR1, DDM), and reflective memory systems (RMS, e.g. RMS and Merlin).

### Home node
The node where a page is located, identified by the combination of node identifier and page frame number that forms the page address. The home node drives all coherence operations for its pages and tracks their state, so every node participates in managing the overall distributed memory.
- Stores (per page it owns):
  - pages accessed, and by whom (readers, writers)
  - modifications
  - caching enabled/disabled
  - lock status
- When an owner node is distinguished from the home node, the home node's role narrows to tracking the current owner of each page that maps to its physical memory.

### Lazy coherence (reactive, optimistic)
A coherence approach in which a node polls periodically, or on demand, for modification information about certain memory regions rather than being pushed invalidations. Also called reactive or optimistic.
- Contrast: eager (proactive, pessimistic) coherence, in which a node pushes invalidation messages on every write.

### Migration
A technique for maximizing local memory access in which state is copied over to a node whenever a process there needs to access remote state. It fits the single reader/single writer case, since only one node accesses the state at a time, but moving data incurs overhead that cannot be amortized when a large chunk is copied for a single access. With multiple readers and writers it makes little sense: the single copy would be flipped back and forth between competing nodes, which can increase access latency.
- Contrast: replication, which copies state onto multiple nodes.
- Paper correction (Protic et al.): the paper defines migration by its invariant rather than the access pattern: only a single copy of a data item exists at any one time, so the item must be moved to the requesting site for exclusive use. Designers prefer migration when sequential patterns of write sharing are prevalent, which is broader than strict SRSW. The migration-only variant of SRSW is the "hot potato" algorithm, and because data moves in fixed-size blocks, migration cost is amortized only when a node makes a long uninterrupted run of accesses. The paper names the flip-back-and-forth effect thrashing and counters it with the Mirage system, which defines a time window during which a site is guaranteed to hold a page uninterruptedly after acquiring it, tunable to the application's processor locality.

### MMU support
Hardware support at the memory management unit (MMU) that lets the DSM layer intercept every access to shared state. When the MMU finds no valid mapping for a virtual address, or detects a write to protected memory, it traps into the OS, which passes the access information to the DSM layer. A remote access has no valid local mapping, so the trap lets the DSM layer send the appropriate remote message; cached content is write-protected, so a write attempt traps and lets the DSM layer generate coherence messages. The MMU's dirty and accessed bits can also be used to implement different consistency policies, and DSM can be dynamically engaged and disengaged to avoid overhead on local, non-shared accesses.

### Owner node
The node that currently owns a page and can control all its state modifications and drive its coherence mechanisms. Introduced so that a node repeatedly, and sometimes exclusively, accessing a page that is not its home node need not continually contact the home node for state updates. The owner may differ from the home node and may change as different nodes access the page over an application's execution.

### Peer (DSM node)
See Peer (P4L2).

### Release consistency
A consistency model that splits a synchronization operation into an acquire point (the lecture's "entry/acquire"), invoked when a process requires that all updates by other processors become visible to it, and a release point (the lecture's "exit/release"), invoked when a process wishes to release its updates to all other processors. These finer-grained operations let the system limit the data movement and coherence operations exchanged among nodes, at the cost of maintaining additional state to track the operations it must support.
- Paper correction (Protic et al.): the paper names this model release consistency and defines it as ordinary accesses executing only after prior acquires on the same processor, and a release executing only after prior ordinary reads and writes complete. The acquire/release pair the lesson describes is exactly release consistency; the lesson's "entry/acquire" label does not match the paper, where entry consistency is a separate, more aggressive model.

### Replication (DSM)
See Replication (P4L2).

### Sequential consistency
A consistency model in which updates need not be seen immediately, but the ordering seen must correspond to some possible ordering of the operations that were applied. Updates from different processors may be arbitrarily interleaved, but every process must see the same interleaving, and operations issued by the same process always appear in the order they were issued. The interleaving need not match the real-time order of operations. In the lecture's example, P1 writes x to m1 and P2, independently, writes y to m2; the two writes are unrelated (P2 computed y without any reference to m1), so P3 seeing x at m1 then y at m2, or 0 at m1 then y at m2, are both OK, because each is equivalent to some possible ordering of the operations on a single shared-memory system. What sequential consistency forbids is processes observing different orders of the same updates (P3 versus P4).
- Paper correction (Protic et al.): the paper states it as all processors observing the same interleaving of reads and writes issued in sequences by individual processors. The paper also describes a model the lesson skips, processor consistency, which sits between sequential and weak: all processors must observe the writes of any one processor in the order that processor issued them, but different processors need not agree on the interleaving of writes from different processors, and reads may bypass writes in the service queue. VAX 8800, Plus, Merlin, and RMS are its examples.
- Quiz (Consistency Models Quiz 1): two processes; P1 performs all of the updates (m1 to x, m3 to y), and P2 sees m3 become y only after it has already seen m1 become x. The execution is sequentially consistent, because updates from a single processor must be visible in the same order, and on P2 they are. It would have been a problem if P2's reads of m1 still returned 0 while its read of m3 already returned y.

### Sharing granularity
The unit at which a DSM system tracks sharing and triggers coherence. SMP uses the cache line, but generating coherence traffic at cache-line granularity is too expensive over a network, so DSM uses larger units: variable, page, or object granularity. Variable granularity is still too fine: many variables are only a few bytes long, so coherence traffic overheads stay high. Page granularity fits DSM integrated at the OS level, since the OS does not understand objects, and amortizes remote-access cost over a larger unit. Object granularity suits a DSM supported by the programming language runtime and needs no OS modification, but is not generalizable outside languages with that support. Larger granularities introduce the risk of false sharing.

### Software DSM
DSM realized in software rather than hardware, at the level of the operating system or a programming language runtime. The software must detect local versus remote accesses, create and send messages to the appropriate node, accept messages from other nodes and perform the encoded operations, and participate in memory sharing and consistency support.
- Paper correction (Protic et al.): the paper splits implementation into three groups rather than two, software, hardware, and hybrid, framing the choice as a price/performance trade-off: hardware performs best but is affordable only for high-end machines, low-end systems such as networks of PCs are limited to software, and mid-range clusters suit low-cost hybrid solutions. Even entirely hardware systems expose software-controlled features (prefetch, update, deliver in Dash; prefetch and poststore in KSR1), and purely software systems lean on hardware such as virtual-memory management (IVY) or ECC bits (Blizzard-E). Across the hybrid systems surveyed, prefetching is the task consistently left to software, because whether it helps depends on the application's access pattern, whereas address translation and invalidation are easier to put in hardware.
- Quiz (Implementing DSM): according to the paper, the common task implemented in software in hybrid DSM implementations is prefetching pages (not address translation or triggering invalidations).

### Strict consistency
The theoretically perfect consistency model, in which every node sees all writes in the system in the same order immediately as they are applied, in the exact order they were performed in real time. It requires that changes be instantaneous and immediately visible everywhere. In practice it is impossible: even on a single SMP system there are no ordering guarantees across cores without locking and synchronization, and in distributed systems added latency and the possibility of message loss or reordering make it unachievable.
- Paper correction (Protic et al.): strict consistency is not in the paper's taxonomy; the lesson takes it from the general literature, where it is usually defined as any read to a location returning the value of the most recent write, with "most recent" fixed by absolute global time (Tanenbaum). That definition subsumes the lesson's two phrasings, immediate visibility and a single global order, so the lesson's wording is a stronger, teaching-oriented statement of the same impossible ideal rather than a competing definition.

### Weak consistency
A consistency model that adds synchronization points as operations available to the upper software layers, alongside read and write. A synchronization point makes all updates performed before it visible at other processors, and makes all updates performed on other processors visible subsequently at the synchronizing processor. The point must be called both by the process performing updates and by the process wishing to see them: a process that has not synchronized is not guaranteed to see another's update. A single sync may cover all variables, or different syncs may be associated with different granularities, and the single operation may be separated into entry/acquire and exit/release.
- Paper correction (Protic et al.): the paper's definition carries a guarantee the lesson leaves implicit: the synchronization accesses themselves must be sequentially consistent. Formally, a synchronization access waits for all previous accesses to complete, while ordinary reads and writes wait only for completion of previous synchronization accesses, and memory is required to be consistent only at synchronization points. Sun's SPARC uses a variant of weak consistency.
- Quiz (Consistency Models Quiz 4): in a weak consistency execution with sync operations, P2 and P3 observe the operations in arbitrary orders, but neither of them synchronized. The execution is weakly consistent: the DSM makes no guarantees about the updates they observe, since weak consistency makes no ordering guarantees unless explicit synchronization operations are used.

## P4L4 Datacenter Technologies

### Amazon Web Services (AWS)
Amazon's motivation was an imbalanced workload: the bulk of its retail traffic came during the holiday shopping season, so much of its provisioned hardware sat idle outside that window. In 2006 it opened access to that hardware via web-based APIs, allowing third-party workloads to run on Amazon resources for a fee; this was the birth of AWS and EC2.

### Animoto
The lecture's cloud computing poster child: a company that stitched photos together into movies, a resource-intensive task, and so rented EC2 instances instead of building its own datacenter. It originally used about 50 instances. In April 2008, after it became available to Facebook users, it signed up 750,000 new users in three days, and its instances grew from 50 on Monday to 400 on Tuesday (an order of magnitude in a day) to 3,400 by Friday, roughly two orders of magnitude in a week. It could not have met that demand by owning and managing its own infrastructure.

### Berkeley Data Analytics Stack (BDAS)
One of the two dominant open source big data stacks, alongside Hadoop. It has a data storage layer with an in-memory file system on top, on which either the regular Hadoop MapReduce engine or Spark runs. Spark has front-ends for different execution models: SQL queries, stream processing, graph processing, and machine learning. At the lowest level, Mesos is the scheduling framework and resource manager: it partitions resources among different frameworks (for example a Hadoop, a Spark, and an MPI partition), which coordinate and negotiate through it, providing elasticity across very different frameworks.

### Big data stack
A layered platform that offers big data processing as a service. At a minimum it needs a data storage layer and a data processing layer; such platforms often also add a caching layer for fast repeated access, a language front-end so developers can query their data in a familiar way (like SQL queries or other query mechanisms), popular analytics libraries for analytics and mining (e.g. machine learning algorithms), and streaming support for both inputs (ingesting and staging data that is continuously streamed in) and outputs.
- The lecture's example stacks are Hadoop and the Berkeley Data Analytics Stack (BDAS).

### Business logic tier
The middle tier of a three-tier internet service. It integrates all of the business-specific processing, including the dynamic, user-specific content.

### Cloud computing
A model that provides shared resources, which can be infrastructure resources (compute, storage, networking) or higher-level software resources (email, database services, or processing runtimes), made available over the Internet through APIs for access and configuration. It emerged to address the scale limitations of running one's own datacenter. Infrastructure is rented as virtual machines, potentially interconnected into virtual clusters, plus storage, not as physical machines or disks.
- Goals of cloud computing:
  - on-demand, elastic resources and services
  - fine-grained pricing based on usage
  - professionally managed and hosted
  - API-based access
- APIs can be web-based, library-based, or command line-based.
- Billing is often not by raw usage, because monitoring at that fine grain has high overhead; it follows a discrete step function instead (for example compute billed by size: tiny, medium, extra-large), and some marketplaces use spot pricing or reservation pricing.
- Common management software stacks are the open source OpenStack and VMware's vSphere.
- Quiz (Cloud Computing Definitions): mapping the NIST definition (October 25, 2011) onto the goals, elastic resources are "on-demand", "shared pool", and "rapidly provisioned"; professionally managed is "minimal management effort"; API-based is "ubiquitous"; nothing in the definition maps to fine-grained pricing.

### Cloud computing limitations
Constraints that keep cloud computing from fully realizing the fungible-utility vision. Even with virtualization some hardware dependencies cannot be masked, so software expecting a certain hardware platform cannot simply run elsewhere. Different providers support different APIs, so switching providers requires rewriting code (API lock-in). Placing core business code and data with an external provider raises privacy and security concerns. Latency is an issue given the geographic distance to the resources.

### Cloud deployment models
A classification of clouds by who owns and uses the infrastructure.
- Public cloud: the infrastructure belongs to the cloud provider, and third-party customers/tenants rent the hardware for their tasks.
- Private cloud: the infrastructure and software are owned by the same entity, using cloud technology to keep flexibility and elasticity on in-house machines.
- Hybrid cloud: combines public and private clouds; private clouds hold the main compute resources with failover/spikes handled on public resources, and public clouds may serve auxiliary tasks such as load testing.
- Community cloud: a public cloud used by certain types of users.

### Cloud enabling technologies
The categories of technology needed for cloud computing to work correctly and efficiently.
- Virtualization: provides fungible resources that can be dynamically repurposed for different customer needs.
- Resource provisioning and scheduling: enables the dynamic provisioning and scheduling of the infrastructure resources; `mesos` and `yarn` (Hadoop's YARN) address this.
- Big data processing: processes large amounts of data to meet customers' needs for scale; `Hadoop MapReduce` and `Spark` are popular.
- Data storage: distributed filesystems that typically operate in append-only mode, plus NoSQL databases and storing data across distributed memories instead of repeatedly accessing disk.
- Isolation (resource slices): software that can enable and configure software-defined slices of resources (each customer gets its own software-defined data center) so cloud users are isolated from one another.
- Monitoring: processes logs in real time and detects anomalies or failures, for the provider to preside over the datacenter and as a service giving customers real-time, possibly interactive (not just batch) access to the information their applications produce; `Flume`, `CloudWatch`, and `Log Insight` are examples.

### Cloud service models
A classification of clouds by what layer of the stack they provide, in contrast to running an application fully on premises.
- Infrastructure as a Service (IaaS): provides virtualized infrastructure instances such as compute instances (CPUs with memory, storage, network), and possibly GPUs; Amazon EC2 is the example.
- Platform as a Service (PaaS): provides APIs and an execution environment, including the OS and tools needed to develop and run certain applications; Google App Engine and the original Windows Azure are examples.
- Software as a Service (SaaS): provides a complete application; Gmail is the example.
- Responsibility split (the lecture's diagram): in IaaS the customer manages applications, data, runtime, middleware, and O/S, and the provider manages virtualization, servers, storage, and networking; in PaaS the customer manages only applications and data; in SaaS the provider manages everything; on premises the customer manages everything.

### Community cloud
A public cloud that is used by certain types of users.

### Database tier
The third tier of a three-tier internet service. It deals with all data storage and management.

### Economies of scale
One of the two principles behind why cloud computing works. A provider leverages a large number of customers on a single piece of hardware, which amortizes the cost of that hardware across those customers, assuming the number of customers is large enough.

### Elastic Compute Cloud (EC2)
Amazon's Infrastructure as a Service offering, launched alongside AWS in 2006, that rents out virtual machine instances rather than physical servers. The customer has no control over whether instances run on the same physical server or on many different ones. EC2 is the lecture's example of IaaS.

### Elasticity
The ideal property that the capacity of available resources scales with demand. The scaling should be instantaneous, so capacity rises as soon as demand rises and falls when it falls, making the cost to support a service directly proportional to demand. Scaling should happen automatically, and resources should be accessible anywhere, anytime.

### Failure probability formula
The expression for the chance that at least one component fails in a system of independent components. If a single component fails with probability `p`, then the probability that at least one of `n` components fails is `1 - (1 - p)^n`. With `p = 0.03` and `n = 10` it is about 26%, and with `n = 100` it rises to about 95%. Because real cloud systems have thousands or hundreds of thousands of components, something will always be failing.
- Mechanisms to deal with failure:
  - timeouts for detection
  - restart and retry for recovery
  - backup, replication, and checkpointing

### Fungible resources
Resources that can easily be repurposed to support different customers with different types of requirements. The lecture states that without fungibility the economic opportunity for cloud providers disappears, and that virtualization is the technology that provides fungibility. The broader cloud vision is to turn the IT resource into a fungible utility, like electricity from a switch, where the user need not care which hardware is used or where it is.

### Hadoop stack
One of the two dominant open source big data stacks, alongside BDAS. At the bottom, the Hadoop file system (HDFS) splits large amounts of data and replicates it, so data does not get lost and there are no hot spots. On top, the MapReduce processing framework lets computation operate on that data and schedules data manipulation operations on specific nodes, ideally so data does not constantly move between nodes. HBase provides a table-like view of the stored data, similar to databases but not the same as a relational representation, and the Hive language front-end translates an SQL query into a number of MapReduce operations on data stored in HBase tables. Higher-level services include the R environment, for describing how data should be processed and analyzed, and Mahout, a collection of machine learning algorithms; supporting services provide locking and coordination, and streaming of data into the distributed environment.

### Heterogenous architecture
An internet service setup in which different nodes are designated to perform certain functions or handle certain types of requests, for example dividing requests by content such as the alphabetical order of a file name, or specializing eBay servers for browsing versus bidding/buying.
- Benefit: the system can exploit caching and locality, since each node repeatedly performs one or a few actions.
- Downsides: the front-end must be more complex because it must parse requests to route them; overall management is harder because scaling and reconfiguration must track which server types are affected; workload changes force reconfiguration rather than simple scaling; nodes can become hotspots with long backlogs even while other nodes idle.
- Quiz (toy shop, each worker builds a specific toy): to stay balanced as orders increase you first profile what kinds of toys (requests) users order and what resources each request type requires; only then can you determine exactly which workers, work benches, and parts (processes, server nodes, storage) to add. Management is much more complex than for a homogenous design.
- Contrast: a homogenous architecture lets any node handle any request.

### Homogenous architecture
An internet service setup in which any node can process any type of request and perform any processing action required end to end. Data may be replicated or distributed across nodes, but every node can reach any information needed for the service.
- Benefit: the front-end load balancer can be kept very simple, assigning requests round-robin to the next available node, optionally using CPU load or utilization information.
- Downside: little opportunity to benefit from caching, because a simple front-end does not track the locality of tasks per node.
- Quiz (toy shop, every worker builds any toy): to stay balanced as orders increase, add more of everything (workers, work benches, tools and parts); no decisions are needed about what the new resources do, so management is fairly simple.
- Contrast: a heterogenous architecture specializes nodes for certain functions or request types.

### Internet service
Any type of service that is accessible via a web interface, where users communicate through web requests issued by their web browsers. Internet services are most commonly divided into three tiers (presentation, business logic, database), connected and coordinated by middleware components, with multiprocess configurations communicating through IPC.

### Law of large numbers
One of the two principles behind why cloud computing works. The average resource needs across a large number of clients remain fairly constant, so a provider can support many clients with variable peak loads on a fixed amount of resources, because those peaks tend to be shifted in time.

### Load balancer (front-end)
A front-end component that routes an incoming request to an appropriate or available machine implementing the internet service. It mirrors the boss-worker pattern: the front-end is the boss and the nodes are the workers, which may be general purpose or specialized. Its complexity depends on the backend: simple and round-robin for a homogenous setup, more complex and content-aware for a heterogenous setup.

### Middleware
Components that exist to connect and coordinate the tiers of an internet service.

### Multitenancy
The property that cloud customers share the same physical resources. Virtualized rather than physical resources are exposed, so a tenant is often sharing physical hardware with other tenants. Some high-performance or GPU-enabled instances are instead single tenant, with the VM running independently on physical hardware, because of the technical challenge of reaching sufficient performance in a virtualized environment.

### Performance and isolation (multi-tenant)
A requirement that cloud management guarantee performance and isolation across multi-tenant environments, so that a misbehaving tenant cannot wreak havoc on other tenants or the entire system. Clouds must also guarantee the privacy of client data and the security of the execution environment: the provider must not access tenant state, and the platform must be protected from a single tenant's vulnerabilities.

### Presentation tier
The first tier of a three-tier internet service. It is typically responsible for static content related to the webpage layout.

### Requirements for the cloud
The properties a cloud must satisfy to deliver on the premise of cloud computing. It must provide fungible resources, integrate resource management that dynamically adjusts allocations to need, operate at very large scale (thousands and tens of thousands of nodes), tolerate the inevitable failures that come with scale, and guarantee performance and isolation plus the privacy of client data and the security of the execution environment across multi-tenant environments.

### Scale out
Expanding a service deployment by running the service on more nodes. Multiprocess configurations, potentially spread across multiple nodes, are the easiest way to handle increases in incoming request rates for services with high or variable request rates.

### Scale out limitations
The reason that continually adding nodes does not work forever, illustrated by a toy shop manager who eventually cannot control more workers, benches, and parts because a single person has limited attention and the shop has a physical limit. For internet services, datacenter size limits the resources that can be placed there, management complexity limits how many things can be managed, and running one's own software stacks and operating systems tightens these constraints further. Cloud computing emerged to address these limits.
- Quiz (Data Center Quiz, for fun): the lecture answers with 2011 numbers, about 510,000 datacenters worldwide occupying about 285.5 million square feet (aggregated by datacenterknowledge.com); current estimates are much higher.

### Three-tier architecture
The common division of an internet service into a presentation tier (static webpage layout), a business logic tier (dynamic, user-specific processing), and a database tier (data storage and management). These tiers need not run as separate processes on separate machines; for example the Apache HTTP web server can fulfill both the presentation and business logic tiers.

