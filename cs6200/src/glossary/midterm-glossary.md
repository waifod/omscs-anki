# GIOS Midterm Glossary

Scope: the six midterm lectures (P1L2, P2L1, P2L2, P2L3, P2L4, P2L5) as written in this repository's notes, plus the paper corrections already embedded in those notes as "Paper (...)" callouts. Where a callout corrects the lecture, the entry gives the lecture's version first and then the correction, marked "Paper correction (<Author>):". Nothing else from the papers is used.

Conventions: each term is defined once, in the first lecture that explains it (a bare mention in a list does not count), and later lectures cross-reference it. Terms are alphabetical within each lecture. Data structures and OS objects carry a "Stores:" list; items the lecture does not spell out are standard content added to close obvious gaps.

Cross-lecture merging: when several lectures discuss the same concept, the canonical entry (at its first lecture) merges all of them. Material from a later lecture is tagged with that lecture, for example "(P2L4)"; where a later lecture says something different, both versions are kept and the difference is stated. An "Also in:" line lists the other lectures that discuss the concept. Where a later section had a separate entry for the same concept under another name (often the pthreads or generic P2L4 form), that entry is a one-line "See <term> (PxLy)." pointer. Implementation-specific structures (Solaris, Linux) keep their own entries and are linked from the canonical one.

## P1L2 Introduction to Operating Systems

### Abstraction
A simplified interface the OS exposes in place of raw hardware, so applications need not handle device details. The lecture's application abstractions are the process and the thread; its hardware abstractions are the file, the socket, and the memory page.

### Arbitration
The OS function of managing the hardware and distributing it among the applications competing for it: the OS allocates memory for applications, schedules them for execution on the CPU, and controls their access to the various devices. The lecture's quiz classifies distributing memory between multiple processes as arbitration.
- Contrast: abstraction simplifies what the hardware looks like to the software above it; supporting different types of speakers and interchangeable access to a hard disk or SSD are abstractions.

### Block device driver
The OS service directly linked to a hardware component: the block device.

### BSD component
The part of the Mac OS X kernel that provides Unix interoperability (via a BSD command line interface), POSIX API support, and the network I/O interface, layered alongside the Mach microkernel.

### Cache memory
The hardware cache that both the OS and application software use for performance. The lecture's components quiz classifies it as not an OS component: the OS does not directly manage it; the hardware manages the cache itself.
- Beyond the lecture: the OS does control whether a mapping is cacheable and issues explicit flushes where correctness demands them, but no OS component manages the cache.

### Desktop operating system
An OS that targets desktop environments; the lecture's examples are Microsoft Windows and the Unix-based systems OS X and Linux.
- Contrast: embedded operating system.

### Device driver
An OS component directly responsible for making decisions about the usage of the hardware devices. It knows the details of the particular hardware element, which lets the OS control the device without knowing those details itself; this is how the OS supports, for example, different types of speakers.
- See also: Block device driver.

### Embedded operating system
An OS that targets embedded or mobile devices rather than desktops or servers; the lecture's examples are Android, iOS, and Symbian.

### File
The OS abstraction over storage devices: a named sequence of bytes that applications manipulate with operations such as open, read, and write, without knowing disk layout.
- Stores:
  - name or path
  - contents (data blocks on the device)
  - metadata: size, permissions, owner, timestamps
  - when open: a current read/write offset, held in the per-process open-file entry
- (P2L2) Threads of one process share its open files. (P2L5) Files, like sockets, are represented by file descriptors, and the OS uses files as its abstraction over the disk; Flash caches file contents and maps files with `mmap`.
- Also in: P2L2 (shared by threads), P2L4 (hard process state; Linux `files_struct`), P2L5 (file descriptors, Flash).

### File system
A higher-level OS service with no direct corresponding hardware component; it hides hardware complexity by exporting a simpler, more intuitive abstraction, a file, as opposed to a block of disk storage.

### I/O Kit
The Mac OS X framework for writing device drivers.

### IPC (Inter-Process Communication)
Mechanisms that let processes exchange data while the OS preserves isolation between their address spaces. Microkernels depend heavily on IPC because services such as file systems run as separate user-level processes. The two forms the lectures cover are message-passing IPC and shared-memory IPC (see P2L1).
- (P2L1) IPC transfers data between address spaces while maintaining protection and isolation, and must be flexible and performant; a web server and a database in separate processes are the example.
- (P2L2) IPC is costlier than inter-thread communication, which is mostly reads and writes of shared variables; this is one reason to prefer multithreading over multiprocess designs.
- (P2L5) In the MP server model, shared state across processes is hard and costly because of IPC; Flash's helpers notify the main process through IPC (pipes).
- Also in: P2L1, P2L2, P2L5.

### Isolation and protection
The OS function of keeping concurrently running applications from hurting one another while each makes adequate progress: the OS allocates different parts of physical memory to different applications and makes sure that, unless explicitly intended, they do not access each other's memory. The lecture distinguishes the two terms: protection means an application cannot read another application's data; isolation means an application cannot overwrite another application's memory.

### Kernel extension kit
The Mac OS X facility for dynamically loading kernel components.

### Kernel mode
The privileged execution mode in which the OS runs; only code in kernel mode may directly access hardware and execute privileged instructions.
- Contrast: user mode is unprivileged; an attempt to perform a privileged operation from user mode causes a trap.
- (P2L2, P2L4) "Kernel level" also names where threads are managed: kernel-level threads are kernel objects, so operations on them from a user process are system calls that enter kernel mode, while a user-level library manages ULTs entirely in user mode. (P2L4) Solaris KLT structures hold kernel-level registers and LWPs hold user-level registers; the kernel-level signal mask is visible only to the kernel.
- Also in: P2L2 (KLT vs ULT), P2L4 (kernel-level structures and masks).

### LFU (Least Frequently Used)
A page replacement policy that evicts the page accessed the fewest times. An alternative policy to LRU that the same memory mechanisms should support.

### Linux architecture
Layered from the bottom: hardware, the Linux kernel, standard libraries (the system call interface), utility programs (shells, compilers), and user applications. The kernel's logical components are I/O management, memory management, and process management, each with well defined functionality and interfaces; each can be modified or replaced.

### LRU (Least Recently Used)
A page replacement policy that moves to disk the pages accessed longest ago. The lecture's example of a policy layered on generic memory management mechanisms.

### Mac OS X architecture
A Mach microkernel (memory management, thread scheduling, IPC including RPC) combined with a BSD component (Unix interoperability, POSIX, networking), plus the I/O Kit for drivers and the kernel extension kit for dynamic loading. Applications sit above this layer.

### Mach
The microkernel at the core of Mac OS X, providing memory management, thread scheduling, and IPC, including remote procedure calls (RPC).

### Mechanism
An operation the OS provides on an abstraction, such as create and schedule for processes or open, write, and allocate for files and memory.
- Contrast: a policy determines exactly how the mechanisms are used to manage the underlying hardware.

### Memory page
The memory management abstraction: an addressable region of memory of some fixed size, typically 4KB, that the OS can allocate in DRAM, map into a process's address space, and move between DRAM and disk without the user noticing.
- Stores:
  - fixed-size block of data
  - OS-side bookkeeping: current location (physical frame or disk), access information used by replacement policies such as LRU
- (P2L1) The page table maps each virtual page to a physical frame, and swapping moves pages between DRAM and disk. (P2L5) Flash's `mincore` check asks whether the pages of a mapped file are resident in memory.
- Also in: P2L1, P2L5.

### Microkernel
A kernel design that requires only the most basic OS primitives, an address space and a thread, and runs everything else, including file systems and device drivers, at unprivileged user level. Because those components live in separate processes, it needs lots of IPC and supports IPC as one of its core abstractions and mechanisms. Pros: small size, verifiability. Cons: poor portability, harder to find common OS components due to specialized use case, leading to software complexity, and costly frequent user/kernel crossings.
- Contrast: a monolithic OS includes every service in the kernel; a modular OS keeps a core in the kernel and loads modules into it, still in kernel mode.

### Mode bit
The special privilege bit in the CPU that is set in kernel mode, permitting any instruction that directly manipulates hardware, and not set in user mode, where those instructions are forbidden. When a trap occurs, the hardware transfers control from the process to the OS and marks it by setting this bit. It is the hardware basis of the user/kernel protection boundary.
- Stores:
  - current privilege level (kernel or user)

### Modular OS
An OS with a basic set of services and APIs to which additional functionality is added as dynamically installed modules; Linux is the lecture's example. Pros: easier to maintain and upgrade, smaller footprint, less resource needs. Cons: the modularity/indirection can reduce some opportunities for optimization (typically not a significant performance impact); modules from different codebases can be slung together at runtime and can be a source of bugs.

### Monolithic OS
The historical OS design in which every service is included in the kernel from the start. Pros: everything included (the abstractions and all the services are packaged at the same time), compile-time optimizations (inlining, for example). Cons: too much state and too much code, which is hard to maintain, debug and upgrade; large memory requirements (which can impact performance).

### open, send, malloc (example system calls)
The lecture's examples of system calls for the three hardware abstractions: `open` for files, `send` for sockets, and `malloc` for memory. Strictly, `malloc` is a C library function rather than a system call: it gets memory from the kernel through the `brk` or `mmap` system calls. `mmap` reappears in P2L5 in Flash.
- (P2L1) `send` reappears as the write/send call of message-passing IPC. (P2L5) Lecture version: the Flash helper reads the file into memory with `mmap`. Paper correction (Pai et al.): both the main process and the helper `mmap` the file, and the main process checks residency first (see Flash web server, P2L5).
- Also in: P2L1, P2L5.

### Operating system
The layer of systems software between hardware and applications that has privileged access to the hardware, manages it on behalf of applications according to policies, and isolates and protects applications from one another. Its main functions are hiding hardware complexity, managing resources, and providing isolation and protection.

### Optimize for the common case
The design principle of tuning the OS for the expected usage context: where it runs, what users execute, and what the workload requires. P2L4 applies it to interrupts as threads and to signal masks.
- (P2L4) Interrupts as threads: mutex lock/unlock is far more frequent than interrupts, so saving about 12 instructions per mutex outweighs about 40 extra per interrupt. Signal handling with ULTs and KLTs: signal mask updates are frequent and kept cheap at user level, while rare signals absorb the cost of corrective system calls.
- Also in: P2L4.

### OS services
The components an OS exports, often tied to hardware: the scheduler (CPU), the memory manager (physical memory), and the block device driver (block devices), plus higher-level services like the file system. Basic services include process management, file management, device management, and so forth, all made available to applications through system calls.

### Policy
A rule that determines how mechanisms are used to manage hardware, such as the maximum number of sockets a process may open or the choice of which page to evict.

### POSIX (Portable Operating System Interface)
The system call interface that operating systems need to support, with the intent of increasing interoperability among OSes; the Mac OS X BSD component provides POSIX API support, and pthreads (P2L3) is its threading API.
- (P2L3) Pthreads provides Birrell-style mechanisms through the POSIX API. (P2L4) Linux's NPTL (Native POSIX Threads Library) implements it one-to-one.
- Also in: P2L3, P2L4.

### Privileged instruction
An instruction that can execute only in kernel mode, such as direct hardware access. Executing one in user mode causes a trap.

### Protection boundary
The division between user mode and kernel mode that confines applications to unprivileged execution. Crossing it is supported by the hardware; the crossings are system calls, traps, and (from OS to application) signals.
- (P2L1) The OS also uses the boundary to check memory accesses, so one process cannot touch memory mapped by another; IPC is how data crosses between address spaces while keeping that isolation.
- (P2L4) The cost of crossing it drives thread design: the ULT library avoids a crossing on every signal mask change, and NPTL's one-to-one model is acceptable because kernel trapping and user/kernel crossings have become much cheaper.
- Also in: P2L1, P2L4.

### Separation of mechanism and policy
The design principle of building flexible mechanisms that can support many policies, so the policy (for example LRU, LFU, or random replacement) can change with the setting without rewriting the mechanism.

### Signal
A notification the OS sends to an application, delivered across the protection boundary from kernel to process. Signal types, masks, and handlers are covered in P2L4.
- (P2L4) Fuller definition: an event triggered by the CPU and the software running on it (for example SIGSEGV when a process touches unallocated memory). Which signals exist depends on the OS, not the hardware, so two identical machines running different operating systems have different signals. Signals can be synchronous (a direct response to the receiver's action) or asynchronous. Each has a unique identifier, can be masked, and is handled by a handler the process installs (or the OS default action); on delivery the thread's program counter is set to the handler. See Signal handler, Signal mask, Synchronous and asynchronous signals, One-shot signal, and Real-time signal (P2L4).
- (P2L4) The difference from P1L2: P1L2 presents a signal only as the OS-to-application direction of the protection boundary; P2L4 adds that signals also arise from the CPU's own execution (synchronous faults) and contrasts them with hardware interrupts (see Interrupt, P2L4). P2L4 also uses signals as an internal coordination tool: directed signals between KLTs, cross-CPU preemption, and the kernel signalling the library before a KLT blocks. Paper correction (Stein & Shah): Solaris does not notify before blocking but sends SIGWAITING when all LWPs are blocked, and the library preempts a thread by sending its LWP a SIGLWP (see SIGWAITING, P2L4).
- Contrast: Signal (condition variable) (P2L2) is an unrelated thread-synchronization operation that shares the name.
- Also in: P2L4.

### Socket
The OS abstraction over the network: an endpoint of a communication channel that applications use with operations such as `send` and `recv`. In P2L5 sockets, like files, are represented by file descriptors.
- Stores:
  - local and remote addresses and ports
  - protocol and connection state
  - send and receive buffers
- (P2L5) An event for a web server is input on one of its socket (or file) descriptors, and helpers may communicate with the dispatcher over sockets or pipes so `select` and `poll` still work.
- See also: open, send, malloc (example system calls) (P1L2) for `send`/`recv` reappearing as message-passing IPC calls in P2L1.
- Also in: P2L5.

### Synchronous mode (system call)
The mode in which the calling process waits until the system call completes. The lecture notes that asynchronous modes also exist; asynchronous I/O is treated in P2L5.
- (P2L5) A synchronous I/O call blocks the caller, which in an event-driven server blocks the whole process; asynchronous calls return immediately, are made possible by a multithreaded kernel and can also benefit from hardware devices, and helpers emulate them by making the synchronous call in a separate thread or process (see Asynchronous I/O, P2L5).
- Also in: P2L5.

### System call
An operation the OS exposes so an application can request privileged services such as hardware access. The process passes arguments directly or by address, control transfers to the kernel, the kernel performs the operation, and control and results return to the process. Each call incurs user/kernel transitions, so it is not cheap.
- (P2L1) Message-passing IPC is built on system calls (send/write, recv/read) that the OS already provides; shared-memory IPC avoids them on the data path.
- (P2L2) Thread models are judged partly by system call cost: in the one-to-one model every thread operation is a system call, while the many-to-one model needs none for thread decisions.
- (P2L4) Examples: `signal`/`sigaction` install handlers; `clone` creates Linux tasks; the ULT library makes a system call to change a KLT's signal mask. Lecture version: `set_concurrency` is a system call. Paper correction (Stein & Shah): it is `thr_setconcurrency()`, a library call (see set_concurrency, P2L4).
- (P2L5) Examples: `select`, `poll`, `epoll`, `mincore`; asynchronous system calls return immediately and deliver results later.
- Also in: P2L1, P2L2, P2L4, P2L5.

### System call number
The specific number an application uses to make a system call. To make the call, the application writes the arguments and saves the relevant data at a well-defined location, then makes the call using the system call number; the kernel uses the number to work out how many arguments to expect and where to look for them.

### Trap
A hardware-initiated transfer of control from a process to the OS when the process attempts an illegal or privileged operation in user mode. The OS then decides whether to grant the access or terminate the process.
- Contrast: a system call is a deliberate request for kernel service; a trap is an involuntary transfer caused by an illegal action.
- (P2L4) "Kernel trapping" is used in the broader sense of entering the kernel: NPTL's one-to-one model is viable because trapping into the kernel has become much cheaper.
- Also in: P2L4.

### User mode
The unprivileged execution mode in which applications normally run; hardware access and privileged instructions are forbidden.
- (P2L2, P2L4) User-level thread libraries run in user mode, which is why ULT operations avoid system calls and why the kernel cannot see ULTs, their masks, or library mutexes and wait queues.
- Also in: P2L2, P2L4.

### User/kernel transition (mode switch)
A change of the CPU's privilege mode from user to kernel and back, as on every system call or trap. It requires instructions to execute, which take 50 to 100 ns on a 2 GHz Linux box, and indirectly pollutes the hardware cache: the OS brings its own content into the cache, evicting the application's, and the application pays for those evictions on later accesses, since a cache access takes a few cycles while a memory access takes hundreds of cycles.
- The lecture describes this in terms of context switching: the call changes the execution context from the user process to that of the kernel (user mode to kernel mode to user mode), and the return reverses it.
- (P2L2) The one-to-one model pays a crossing on every thread operation; the many-to-one model avoids them.
- (P2L4) The ULT library avoids a crossing on each signal mask update and pays it only when a signal arrives that the masks disagree on; NPTL's one-to-one model is acceptable because crossings have become much cheaper.
- (P2L5) Asynchronous system calls still cross into the kernel but return without waiting for the I/O.
- Also in: P2L2, P2L4, P2L5.

## P2L1 Processes and Process Management

### Address space
The OS abstraction that encapsulates all of a process's state, defined as a range of virtual addresses V_0 to V_max in which every piece of state has a unique address. The OS and memory management hardware map these virtual addresses to physical memory through the page table.
- Stores (regions, typically from low to high addresses):
  - code (text): the program's instructions
  - data: static state available when the process is initialized, such as globals
  - heap: dynamically created state, which may contain holes the process is not permitted to access
  - stack: dynamically created LIFO state that grows and shrinks as the program executes, with stack frames added and removed as functions are called and return
  - plus mapped regions such as shared memory or `mmap`ed files
- (P2L2) A single-threaded process is an address space plus one execution context; threads of a multithreaded process share one address space (code, data, heap, files, and the virtual-to-physical mapping), which is why multithreaded applications need less memory than multiprocess ones and why thread switches skip remapping.
- (P2L4) The virtual address mapping is hard process state, shared by all threads and not swapped between KLTs of the process; Solaris's process structure points to it, and Linux tasks point to it through `struct mm_struct *mm`; `clone` sharing flags decide whether a new task shares it.
- (P2L5) The MT and event-driven server models run in a single address space; MP uses one per process.
- Also in: P2L2, P2L4, P2L5.

### Admission control
The check the OS performs when a process is in the new state, deciding whether to admit it. Provided minimum resources are available, the OS then allocates and initializes the PCB and some initial resources for the process, and the process moves to ready.

### Application (program)
The static entity stored on disk: instructions and initial data. Launching it loads it into memory and creates a process.
- Contrast: an application is passive and on disk; a process is the active, executing instance, and one program can back many processes with the same code but different state.

### Cache hierarchy
The processor cache is not one cache but a hierarchy of them: L1, L2, on down to the last level cache. Each level is larger than the one before it and potentially slower, though all of them are far faster than going out to memory.

### Child process
A process created by another process (its parent), typically with fork. All loaded processes form a tree rooted at the processes the OS creates after boot.
- (P2L4) In Linux a child task is created with `clone`; with all sharing flags cleared it is a new process (this is how `fork` is implemented), with all set it is a thread of the parent.
- Also in: P2L4.

### Code (text) region
The address space region holding the program's executable instructions.
- (P2L2) Threads of one process share the code.
- Also in: P2L2.

### Cold cache
The state in which a process's or thread's data is not in the processor cache, typically after it has been switched out, so accesses go to memory at hundreds of cycles each.
- Contrast: hot cache.
- (P1L2) A user/kernel transition can also cool the cache: the OS brings its content into the cache, evicting the application's, so the application's later accesses go to memory (hundreds of cycles instead of a few).
- Also in: P1L2.

### Context switch
The mechanism by which the OS stops one process (or thread) and starts another: it saves the running context's register state into its PCB in memory and loads the next context's PCB into the CPU registers. Direct costs are the cycles to save and load state; indirect costs come from losing a hot cache: the incoming process's data replaces the old process's cached data, so the next time the old process runs its cache is cold and the CPU spends many more cycles fetching from memory. The aim is to context switch as rarely as practical.
- (P1L2) The lecture also describes a system call in terms of context switching, from user mode to kernel mode and back (see User/kernel transition, P1L2).
- (P2L2) Thread context switches: switching between threads of one process keeps the virtual-to-physical mappings, the costly part of a process switch, so it is cheaper. On a single CPU, switching to another thread pays off when a thread's idle time (for example waiting on disk) exceeds the time of two context switches. Spurious wake-ups waste cycles on context switches to threads that immediately block again.
- (P2L4) Switching between kernel-level threads of the same process saves and restores only light process state (the per-KLT part); hard process state, such as the address mapping, stays in place. Each KLT points to its process, so the kernel can see whether the whole PCB must be swapped. Splitting the PCB into multiple data structures is what lets a context switch save and restore only what changes, while a single control block is saved and restored in its entirety. Paper correction (Eykholt et al.): the paper rejects the two-level interrupt design, in which a bounded first-level handler wakes a second-level thread, partly because it always costs a full context switch.
- (P2L5) MP servers pay the high cost of process context switches; MT servers have a cheap user-level context switch; the event-driven model has no context switching within its single thread, and on one CPU this wins when there is no idle time to hide. Lecture version: on the single-file test the MT and MP implementations trail because of extra synchronization and the cost of context switching. Paper correction (Pai et al.): the paper attributes the slight lag of Flash-MT and Flash-MP to extra kernel overhead such as context switching and does not mention synchronization; synchronization is an MT cost only, since MP processes have private address spaces.
- Also in: P1L2, P2L2, P2L4, P2L5.

### CPU efficiency
Useful CPU time spent executing processes divided by total CPU time, including time spent scheduling. With process run time `T_p` (the timeslice) and scheduler time `T_sched`, an interval containing two of each gives `2 * T_p / (2 * T_p + 2 * T_sched)`. With equal-length execution and scheduling blocks it is 50%; when the process runs for ten times the length of a scheduling block it is roughly 91%.
- (P2L5) CPU utilization appears as an evaluation metric (see CPU utilization, P2L5).
- Also in: P2L5.

### CPU registers
Fast storage in the CPU holding the running context's working state, including the program counter and stack pointer. Their contents are saved to the PCB on a context switch and restored when the process runs again.
- (P2L2) Each thread has its own register values, kept in its thread data structure (execution context), while threads share the address space.
- (P2L4) The PCB split moves registers into the kernel-level thread structure; Solaris distinguishes kernel-level registers (KLT structure) from user-level registers (LWP and ULT structures); one CPU cannot modify another CPU's registers, which forces cross-CPU preemption through signals.
- Also in: P2L2, P2L4.

### CPU scheduler
The OS component that decides which ready process uses the CPU next and for how long. Running it involves preempting the current process, scheduling (selecting) the next one, and dispatching it. Because scheduling time is overhead, the OS wants to spend most CPU time running processes, not choosing them.
- (P1L2) The scheduling component is listed among the OS services as the one that controls access to the CPU; Mach provides thread scheduling in Mac OS X.
- (P2L2) With threads, the kernel-level scheduler maps kernel-level threads onto physical CPUs, while a user-level library decides which ULT runs on each KLT, so scheduling becomes two-level. The order in which threads run after a signal or broadcast is the scheduler's decision. Scope matters: with process scope the kernel splits CPU among processes; with system scope, among threads.
- (P2L4) The kernel sees KLTs, CPUs, and its own scheduler; the library's scheduler (see User-level library scheduler, P2L4) sees ULTs and the KLTs (LWPs, its "virtual CPUs") available to it, and neither sees the other's decisions. The Solaris KLT structure holds scheduling info and is not swappable because the scheduler needs it even when the thread is not running.
- Also in: P1L2, P2L2, P2L4.

### Data region
The address space region holding static state present when the process is first initialized, such as global and static variables.
- (P2L2) Threads of one process share the data region.
- Also in: P2L2.

### Dispatch
The step after scheduling in which the OS switches into the selected process's context and starts it running on the CPU.
- (P2L4) The Solaris CPU structure holds the CPU's dispatching information.
- Contrast: the event dispatcher (P2L5) is an application-level loop that invokes handlers, not the OS step of starting a process.
- Also in: P2L4.

### exec
The process creation mechanism that replaces the calling process's program: the OS loads a new program, rewrites the PCB to describe it, and sets the program counter to its first instruction. Creating a new program normally means fork followed by exec in the child.
- Contrast: fork copies the current program into a new process; exec keeps the process but replaces the program.

### fork
The process creation mechanism in which the OS creates a new PCB for the child and copies the parent's PCB values into it, so both processes continue from the instruction after the fork with the same program counter and state.
- Contrast: Birrell's thread Fork (P2L2) creates a new thread in the same address space, not a new process.
- (P2L4) In Linux, `fork` is implemented by `clone` with all sharing flags cleared, so the child shares nothing with the parent; `clone` with all flags set creates a thread instead.
- Also in: P2L4.

### Heap
The address space region for dynamically created state: memory the process allocates, intermediate results it stores, and data it reads from files. It is drawn as a contiguous region starting after the data, but in reality it may have holes: regions that have no meaning for the process and that it is not permitted to access, with the OS tracking which addresses are valid.
- (P2L2) The heap is part of the address space that threads of one process share.
- Also in: P2L2.

### Hot cache
The state in which the data a process or thread needs is already in the processor cache, so accesses take a few cycles. Specialized threads (P2L2) help keep caches hot.
- (P2L2) A specialized thread working on a small subtask can potentially keep more of its state in the cache; specialized workers and pipelines exploit this locality, plain boss/workers does not.
- (P2L5) A hot cache through specialization is listed again as one reason threads are useful.
- Also in: P2L2, P2L5.

### I/O queue (I/O wait queue)
A queue, one per I/O device, holding processes that have issued a request to that device and are waiting for it to complete. When the device completes the request, the process moves back to the ready state; if nothing is waiting ahead of it in the ready queue, it might be scheduled on the CPU immediately.
- Stores:
  - the device it belongs to
  - an ordered list of PCBs (or links to them) of waiting processes
  - per entry, the pending request

### init
On UNIX-based systems, the first process that starts after the system boots. Every other user-level process can ultimately be traced back to it, so it is called the parent of all processes.
- Contrast: Zygote, the parent of all Android app processes.

### Message-passing IPC
IPC in which the OS establishes a channel, such as a shared buffer, and processes communicate through it with send/write and recv/read system calls. Main benefit: the OS manages the channel and provides the same APIs (same system calls) to both sides for write/send and read/recv, so neither process implements the protocol itself. Main downside: overhead, since every piece of information is copied from the sender's address space into kernel memory and then into the receiver's address space.
- Stores (the channel):
  - kernel buffer of queued messages
  - endpoints (sender and receiver identities)
  - queues of processes blocked waiting to send or receive
- Contrast: shared-memory IPC keeps the OS out of the fast path, so there is no OS overhead on each read and write, but the APIs message passing provides have to be reimplemented and the code tends to be more error-prone.
- (P2L5) Flash's helper processes notify the main process through pipes, a message-passing channel.
- Also in: P2L5.

### Page table
The OS-maintained mapping from a process's virtual addresses to physical memory addresses, which decouples virtual layout from physical layout and lets the OS check that accesses are valid.
- Stores (one entry per virtual page):
  - physical frame number
  - valid/present bit (page in memory or swapped to disk)
  - protection bits (read, write, execute)
  - accessed and dirty bits used by replacement policies
- (P2L2) Threads of one process share the page table (the virtual-to-physical mapping), so a thread switch does not change it. (P2L4) The mapping is hard process state; the Solaris process structure and the Linux `mm_struct` point to it.
- Also in: P2L2, P2L4.

### PCB (Process Control Block)
The data structure the OS maintains for every process, created and initialized when the process is created (for example, the program counter set to the first instruction) and updated as the process's state changes. While the process runs, frequently changing values such as the program counter live in CPU registers; the OS saves them into the PCB when the process stops running.
- Stores:
  - process state (new, ready, running, waiting, terminated)
  - process number
  - program counter
  - CPU registers
  - memory limits, plus the virtual-to-physical memory mappings needed for address translation
  - CPU scheduling info: how long the process has already run, how much time it should get in the future, its priority
  - list of open files
  - and more
  - (P2L2) for a multithreaded process: the per-thread execution contexts, or links to each thread's data structure
  - (P2L4) list of kernel-level threads executing on its behalf
  - (P2L4) user credentials and signal handlers (process-wide, per the Solaris process structure)
- (P2L2) Refinement: a single-threaded process is an address space plus one execution context, both represented in the PCB. A multithreaded process has a more complex PCB because each thread's execution context must be incorporated, and each thread gets its own data structure (see Thread data structure, P2L2).
- (P2L4) Redefinition: on a single CPU the lecture lists the PCB as virtual address mapping, stack, and registers. To support several KLTs per process without replicating the whole PCB, it is split: the per-KLT parts (stack, registers) move into the kernel-level thread structure, and the rest is divided into hard process state (shared by all threads, such as the address mapping) and light process state (per KLT, such as signal mask and system call arguments). The difference from P2L1: P2L1 treats the PCB as one structure saved and restored whole on a context switch; P2L4 argues for multiple smaller structures so only what changes is saved (see Multiple data structures (rationale), P2L4).
- (P2L4) Implementations: Solaris uses a process structure plus LWP, KLT, ULT, and CPU structures (see Kernel process data structure (Solaris)); Linux never had one contiguous PCB, and process state is a collection of structures that each `task_struct` points to (see task_struct).
- Also in: P2L2, P2L4.

### Physical address
A location in actual physical memory (DRAM).
- Contrast: virtual address.

### Preemption
Interrupting the currently running process, typically when its timeslice expires, and saving its context so another process can run. The preempted process goes back to the ready state.
- Contrast: in preemption the OS takes the CPU away from a process that could keep running; in blocking the process gives up the CPU because it must wait for I/O or an event, and it moves to the waiting state rather than ready.
- (P2L4) With threads: if the KLT under a ULT that holds a lock is preempted, the library may waste time scheduling ULTs that need that lock. On a multiprocessor, the library on one CPU may need to preempt a thread on another CPU and does so by signalling it (see Cross-CPU preemption). Paper correction (Stein & Shah): the Solaris library preempts a thread only when a higher-priority thread becomes runnable or the active thread's priority drops, by setting a flag and sending its LWP a SIGLWP; there is no user-level time slicing.
- Also in: P2L4.

### Process
An instance of an executing program: an application that has been loaded into memory and started, represented by its address space and execution context and described to the OS by its PCB. It is an active entity, even when not running at a given moment. The terms task and job are often used interchangeably with process.
- (P1L2) The process is one of the OS's application abstractions, with mechanisms such as create and schedule.
- (P2L2) A single-threaded process has one execution context; a multithreaded process has several sharing one address space.
- (P2L4) In Linux a process is a group of tasks identified by `tgid`, the pid of its first task; a single-threaded process's task id equals the process id.
- (P2L5) The MP server model runs several instances of one single-threaded process.
- Also in: P1L2, P2L2, P2L4, P2L5.

### Process states
The life cycle of a process: new (admission control, PCB allocated), ready (runnable but not on a CPU), running (scheduled and executing), waiting (blocked on I/O or an event), and terminated (exited, with or without error). Running returns to ready on preemption or interrupt; waiting returns to ready when the I/O or event completes.
- (P2L2) A thread that cannot proceed is blocked: it is placed on a mutex or condition variable wait queue rather than an I/O queue, the thread analog of the waiting state (see Blocking, P2L2).
- (P2L4) A blocking ULT blocks its KLT, and when every KLT (LWP) of a process is blocked the whole process is blocked even if other ULTs could run; lecture version: the kernel would ideally signal the library before blocking so it can request another LWP. Paper correction (Stein & Shah): Solaris does not notify before blocking; it sends SIGWAITING once all LWPs are blocked in indefinite waits. Lecture version: an exiting thread is marked as on death row until the reaper garbage-collects it. Paper correction (Stein & Shah): only detached threads go on death row; an undetached thread goes on a zombie list until `thr_join()` reaps it (see Death row, Zombie thread).
- Also in: P2L2, P2L4.

### Process tree
The tree-like hierarchy formed by parent and child processes, rooted at the privileged root processes the OS creates after booting.

### Program counter
The CPU's knowledge of the current executing line within a program, that is, where within the program's code the process currently is. It is maintained in a dedicated CPU register that the CPU updates on every new instruction while the process runs, and the OS saves it to the PCB when the process stops running.
- (P2L2) Each thread has its own program counter in its thread data structure; Fork sets the new thread's to the first instruction of `proc`.
- (P2L4) Interrupt and signal handling set the program counter to the handler's starting address, taken from the interrupt handler table or the signal handler table, while the stack pointer stays the same.
- Also in: P2L2, P2L4.

### Ready queue (run queue)
The queue of processes in the ready state, waiting for the CPU scheduler to select them. Processes end up on it in four ways: a process waiting on an I/O event whose event completed; a running process whose timeslice expired; a new process created via `fork`; and a process waiting for an interrupt when the interrupt occurred.
- Stores:
  - ordered list of PCBs (or thread structures) that are runnable
  - per entry, scheduling info such as priority, used to pick the next one

### Scheduling (schedule)
The step in which the CPU scheduler selects the next process to run from the ready queue, according to criteria such as priority.
- (P2L2, P2L4) With threads, scheduling happens at two levels, the kernel scheduling KLTs and the library scheduling ULTs onto them (see CPU scheduler, P2L1).
- Also in: P2L2, P2L4.

### Shared-memory IPC
IPC in which the OS maps the same physical memory region into the address spaces of multiple processes, which then read and write it directly as ordinary memory. The main benefit: the OS is out of the fast path, not involved in individual exchanges, so the processes incur no OS overhead on each read and write. The OS still has to establish the mapping, which is expensive, so shared memory wins only if that one-time setup cost is amortized across enough messages; for a small number of exchanges, message passing can be the better choice. The disadvantage is that many APIs taken for granted in message passing have to be reimplemented, and without a fixed, well-defined API governing the shared region the code tends to be more error-prone.
- Stores (the channel):
  - a physical memory region mapped into the address space of each participating process
  - whatever data the processes themselves place in it

### Stack
The address space region holding dynamically created state that grows and shrinks as the program runs: a LIFO of stack frames, one added on each function call and removed on return. Each thread (P2L2) has its own stack.
- Stores (per stack frame):
  - return address
  - function arguments
  - local variables
  - saved registers
- (P2L2) Each thread has its own stack, part of its execution context and thread data structure.
- (P2L4) The PCB split moves the stack into the kernel-level thread structure. Interrupt and signal handlers run on the interrupted thread's stack, which is why a handler that locks a held mutex deadlocks. Paper correction (Eykholt et al.): SunOS 5.0 moves interrupt handling onto a preallocated interrupt thread's stack. The ULT library does not control stack growth, which motivates the red zone. Paper correction (Stein & Shah): the red zone is an invalid page after each library-allocated stack, and TLS (holding the thread structure) is carved from the base of each stack. Solaris KLT stacks are swappable.
- Also in: P2L2, P2L4.

### Stack pointer
The CPU register holding the address of the top of the current stack.
- (P2L2) Each thread data structure records its own stack pointer. (P2L4) The Solaris KLT structure holds one; on signal delivery the stack pointer is left unchanged, so the handler runs on top of the interrupted thread's stack.
- Also in: P2L2, P2L4.

### Swapping
The OS moving portions of a process's address space from physical memory to disk, and back when needed, when physical memory cannot hold all processes' state.
- (P2L2) A multithreaded application needs one address space, so it is more likely to fit in memory and needs fewer swaps than a multiprocess one. (P2L4) In Solaris the LWP and the KLT's stack are swappable, while the KLT structure itself is not, since the scheduler needs it even when the thread is not running.
- Also in: P2L2, P2L4.

### Timeslice
The time allocated to a process that has been scheduled to run, the time that process can consume on the CPU; it is `T_p` in the CPU efficiency formula. What timeslice values are appropriate is one of the scheduler's design decisions: the longer `T_p` is relative to the scheduling time, the higher the CPU efficiency (see CPU efficiency). When the timeslice expires the process is preempted and returns to the ready queue.
- (P2L4) Lecture version: the ULT library scheduler can be entered when a timer set by the library expires. Paper correction (Stein & Shah): the Solaris library does no user-level time slicing; threads compete for LWPs by priority.
- Also in: P2L4.

### Virtual address
An address in a process's address space (V_0 to V_max). It need not correspond to any particular physical location; the page table translates it.
- Contrast: a physical address names an actual DRAM location.

### Zygote
The Android daemon process whose purpose is launching app processes. It preloads the Android framework classes, and each new app process is created by forking Zygote, so the app inherits the preloaded framework and Zygote is the parent of all app processes.
- Contrast: init, the parent of all user-level processes on UNIX-based systems.

## P2L2 Threads and Concurrency

### Blocking (blocked thread)
A thread is blocked when it cannot proceed until some event occurs, such as a mutex being released, a condition being signalled, or I/O completing. It is placed on the relevant queue and does not use the CPU until woken.
- Contrast: spinning (P2L4) keeps the thread on the CPU retrying; blocking gives the CPU up.
- (P2L1) Blocking is the thread analog of a process entering the waiting state.
- (P2L3) `pthread_mutex_lock` and `pthread_cond_wait` block; `pthread_mutex_trylock` returns instead of blocking.
- (P2L4) On a multiprocessor, blocking can lose to spinning when the owner is running and will release soon (see Adaptive mutex). A blocking ULT blocks its KLT and every ULT mapped to it. Lecture version: an interrupt handler that might lock a mutex, and so might block, is turned into a real thread. Paper correction (Eykholt et al.): interrupt threads are preallocated, and one is converted into a full thread only when the handler blocks on lock contention.
- (P2L5) A blocking call in an event handler blocks the whole event-driven process, which motivates asynchronous I/O and helpers.
- Also in: P2L1, P2L3, P2L4, P2L5.

### Boss/workers pattern
A multithreading pattern with one boss thread that accepts tasks and assigns them, and worker threads that each complete an entire task. Throughput is limited by the boss and is inversely proportional to the boss's time per task. The boss can signal an idle worker directly (no worker synchronization, but the boss tracks every worker) or place tasks on a shared producer/consumer queue (less boss work per task, more synchronization). Pros: simplicity. Cons: thread pool management overhead and no locality, since the boss ignores what each worker did last.
- Stores (shared work queue):
  - buffer of pending tasks
  - head and tail indices or pointers, and count
  - mutex protecting the queue
  - condition variables for "not empty" (workers wait) and "not full" (boss waits)
- (P2L5) Toy shop comparison: with 6 threads (1 boss, 5 workers) and 11 orders, boss/workers takes 360 ms total versus 320 ms for a pipeline, but averages about 196 ms per order versus 220 ms, so it wins on average completion time and loses on total execution time (see Average completion time, P2L5). An MT web server could have a boss run the first step and workers the rest; Apache runs a boss/workers configuration with a dynamic thread pool in each process.
- (P2L5) Lecture version: the Flash comparison's MT server is described as boss/workers. Paper correction (Pai et al.): each MT thread performs all steps of one request, Flash-MT uses 64 threads, and no boss thread is described.
- Also in: P2L5.

### Bound thread
In the many-to-many model, a user-level thread permanently associated with one specific kernel-level thread, so it is always scheduled on that kernel thread. Lecture version: bound threads are useful when a user-level thread needs better priority or must respond quickly to kernel events, since the kernel can schedule the bound kernel thread immediately (for example a UI thread when user input arrives). P2L4 relates binding to thread pinning: it is analogous to permanently associating a kernel-level thread with a CPU, and in a 1:1 model every user-level thread is bound.
- Paper correction (Stein & Shah): the reason to bind is global (system) scheduling scope for threads needing real-time response, such as mouse tracking. A bound thread that calls `priocntl()` changes its LWP and can run in the real-time class ahead of unbound threads; CPU pinning is not mentioned.
- Contrast: unbound thread.
- Also in: P2L4.

### Broadcast
The condition variable operation that wakes all threads waiting on the condition variable. The lecture notes that broadcast is often of limited use because the woken threads still reacquire the mutex one at a time, and that using broadcast where signal would do costs only performance, while using signal where broadcast is needed can break correctness.
- Paper correction (Birrell): broadcast has two legitimate uses: simplifying a program by waking several threads without separating wait reasons onto different condition variables, and waking several threads when the released resource can be used by more than one. Readers in a readers/writer lock are the standard case: they reacquire the mutex one at a time only to update the counter, then read concurrently. POSIX likewise recommends broadcast when more than one waiter can proceed, and Lampson & Redell treat it as always correct.
- Contrast: signal wakes (at least) one waiter.
- (P2L3) The pthreads form is `pthread_cond_broadcast(cond)`, which wakes all threads waiting on a `pthread_cond_t`. The P2L3 safety tip restates the lecture rule as "when in doubt use broadcast", since misused broadcast costs only performance.
- Also in: P2L3.

### Common pitfalls (mutex and condition variable rules)
The P2L2 rules for using mutexes and condition variables correctly. Mutexes: keep track of which mutex and condition variables go with each shared resource (comments help); always protect shared state, and always with the same mutex, since different mutexes for one resource give no mutual exclusion; do not forget to lock or unlock. Condition variables: signal or broadcast the correct condition; never use signal where broadcast is needed (the reverse is correct but may cost performance); and do not rely on the order of signal or broadcast calls for the order in which threads run.
- (P2L3) Mutex safety tips, the pthreads restatement: always access a given piece of shared data through a single mutex; mutex scope must be global; order locks globally to prevent deadlock (see Lock order); always unlock the correct mutex.
- Paper correction (Birrell): mutexes are ordinary data values, and a module managing many objects can protect each one by associating a mutex with the record that represents it, such as one lock per open file plus a lock for the global table, which allows more parallelism. POSIX and OSTEP agree the requirement is that every thread using the mutex reaches the same instance, not that it is a global variable.
- (P2L3) Condition variable safety tips, the pthreads restatement: when a condition changes, signal or broadcast the correct condition variable; when in doubt use broadcast, since misused broadcast costs performance but misused signal can break correctness; once you figure out the desired behavior, switch to the correct mechanism (signal or broadcast), since broadcast costs performance; and a mutex is not needed to signal or broadcast, so notifying after unlocking can avoid spurious wake-ups.
- Difference between the versions: P2L2 (Spurious wake-up) says the mutex sometimes cannot be released before signalling, when whether to signal depends on shared state, while P2L3 says plainly that no mutex is needed. Birrell's correction under Spurious wake-up reconciles them: test the shared state inside the lock and signal after it.
- Also in: P2L3.

### Condition variable
A synchronization construct, used together with a mutex, on which threads wait until some condition on shared state becomes true and are notified by other threads when it does. It replaces wasteful polling loops, as in the producer/consumer example.
- Stores:
  - reference to its associated mutex
  - queue (list) of waiting threads
- (P2L3) Pthreads version: the type is `pthread_cond_t`, described as a synchronization mechanism that lets blocked threads be notified when a condition occurs. It is created with `pthread_cond_init(cond, attr)` (a `pthread_condattr_t`, or `NULL` for defaults) and freed with `pthread_cond_destroy`; the operations are `pthread_cond_wait`, `pthread_cond_signal`, and `pthread_cond_broadcast` (see Wait, Signal (condition variable), Broadcast). Like Birrell's Wait, `pthread_cond_wait` takes the mutex as an argument on each call. See Common pitfalls (mutex and condition variable rules) (P2L2).
- Also in: P2L3.

### Critical section
The portion of code that must be executed by at most one thread at a time, typically code that reads or writes shared state, protected by a mutex. In the readers/writer example the actual reads and writes are the logical critical sections even though they run outside the mutex; the enter and exit blocks act as higher-level lock and unlock operations around them.
- (P2L3) In pthreads, with no implicit unlock, the critical section is whatever code appears between `pthread_mutex_lock` and `pthread_mutex_unlock`.
- (P2L4) Lecture version: an adaptive mutex spins if the critical section is short and blocks if it is long, so the mutex needs some information about its length. Paper correction (Eykholt et al.): critical-section length is not an input; short hold times are the assumption behind spinning while the owner runs.
- Also in: P2L3, P2L4.

### Data race (race condition)
A situation in which one thread tries to read data while another modifies it, which can lead to inconsistencies; threads are exposed to it because they share the address space. The lecture's examples are two threads inserting into a linked list, where one overwrites the other's insertion, and (in P2L3) passing a loop counter's address to new threads.
- (P2L3) Restated in the same terms: one thread tries to read a value another thread is modifying. Thread argument race example: `main` passes the address of loop counter `i` to each new thread, and may increment `i` before a thread dereferences the pointer, so two threads can print the same number (output such as 0, 2, 2, 3). The fix gives each thread private storage: copy `i` into `tNum[i]` and pass `&tNum[i]`.
- Also in: P2L3.

### Deadlock
A situation in which two or more threads each wait for a resource another holds, so none can proceed. The lecture's example is T1 locking A then B while T2 locks B then A.
- Fixes for the T1/T2 case:
  - fine-grained locking (unlock A before locking B): does not work here, since both A and B are needed
  - get all locks up front and release them all at the end, or use a single mega-lock covering A and B: may be too restrictive, since it limits parallelism
  - lock order (see Lock order): the most ideal solution; foolproof but hard to enforce across a large program with code from different sources, so deadlocks are a reality
- General strategies: deadlock prevention (check each acquire), deadlock detection and recovery (wait-graph cycles plus rollback), and the ostrich algorithm. Prevention and detection/recovery impose enough execution-time overhead that they are typically applied only in really performance-critical systems.
- (P2L3) The mutex safety tips repeat the fix: order locks globally.
- (P2L4) A second kind of deadlock: an interrupt or signal handler that runs on the interrupted thread's stack and tries to lock a mutex the interrupted thread already holds. The thread cannot unlock until the handler returns, and the handler cannot return until it locks. Fixes are masking the interrupt or signal around the mutex, or running handlers as separate threads (see Interrupts as threads), where the handler simply blocks.
- Also in: P2L3, P2L4.

### Deadlock detection and recovery
Analyzing the wait graph for cycles and, when one is found, recovering by rolling back. It is expensive because it requires a rollback strategy, which means maintaining enough state during execution to recover; in some cases rollback is impossible, since inputs and outputs from external sources cannot be rolled back.

### Deadlock prevention
Checking, before each mutex acquisition, whether the operation would cause a deadlock; if it would, the operation is delayed, and the code may have to be restructured so the thread first releases some resource. It is expensive because the check runs on every acquire.

### Execution context
The per-thread part of a running program's state: CPU registers (including the program counter) and the stack. A single-threaded process has one; a multithreaded process has one per thread, all sharing one address space.
- Stores:
  - CPU register values, including the program counter and stack pointer
  - the stack
- (P2L4) Linux's task is "essentially the execution context of a kernel-level thread". Signal masks are kept per execution context (ULT on top of KLT), and interrupts and signals are handled in the context of the interrupted thread.
- (P2L5) MP and MT servers handle one request at a time per execution context and get concurrency from many contexts; the event-driven model interleaves many requests within one execution context.
- Also in: P2L4, P2L5.

### Fork (Birrell thread Fork)
The thread creation operation `Fork(proc, args)`: it creates a new thread with a new thread data structure whose program counter points to the first instruction of `proc`, which will run with `args`. Afterward both threads execute concurrently.
- Contrast: UNIX fork (P2L1) creates a new process with a copied address space.
- (P2L3) The pthreads form is `int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start_routine)(void *), void *arg)`: it creates a thread that runs `start_routine(arg)`, writes its identifier into `*thread`, and returns an `int` indicating success or failure. Differences from Birrell's Fork: it returns a status code, and it takes an attributes structure (`NULL` for defaults) that can make the thread detached from the start.
- (P2L4) Linux `clone` is similar: a function pointer and an argument, plus `sharing_flags` choosing what the child shares.
- Also in: P2L3, P2L4.

### Join (Birrell thread Join)
The operation by which a parent thread waits for a child thread to finish: `Join(thread_id)` blocks until the child completes, returns the child's result, and then the child exits and its resources are deallocated. The lecture also motivates it as keeping a parent from exiting before its children, since child threads exit when parent threads do. One practice for returning a result is to store it in a well-defined location in the shared address space and notify the parent (or another thread) that it is available.
- Paper correction (Birrell): Join is rarely called at SRC and some thread facilities omit it; most forked threads are daemons or report results by other means. The paper does not say what happens to children when the parent exits. See Detached thread (P2L3).
- (P2L3) The pthreads form is `int pthread_join(pthread_t thread, void **status)`: it blocks until the given thread terminates, captures all of the relevant return information in `*status`, including the results returned by the thread, and returns an `int` indicating success or failure. Pthreads threads are joinable by default, and a detached thread cannot be joined; `main` in the producer/consumer example joins both threads for this reason.
- (P2L4) Lecture version: an exited thread's structure is placed on death row. Paper correction (Stein & Shah): only detached threads go on death row; an undetached Solaris thread that exits is kept on a zombie list until another thread calls `thr_join()` on it.
- Also in: P2L3, P2L4.

### Kernel-level thread (KLT)
A thread that is visible to and managed by the kernel, scheduled onto physical CPUs by the kernel scheduler. A multithreaded kernel uses KLTs both to support user-level threads and to run OS services such as daemons and device drivers. A user-level thread can run only when it is associated with a KLT that the kernel has scheduled.
- Contrast: user-level thread.
- (P2L4) Supporting threads at kernel level means the kernel must maintain a data structure for each thread (see Thread data structure, P2L2) plus the scheduling and synchronization mechanisms that make multithreading correct and efficient. The kernel sees KLTs, CPUs, and its scheduler, but not library structures such as mutexes and wait queues. Implementations: Solaris pairs each KLT that runs ULTs with an LWP (see LWP, Kernel-level thread data structure (Solaris)); in Linux a KLT is a task (see Task (Linux)), and NPTL gives every ULT its own task.
- Also in: P2L4.

### Layered pattern
A multithreading pattern in which similar subtasks are grouped into layers, any thread assigned to a layer can perform any subtask in it, and every task passes through all layers. Pros: specialization while being less fine-grained than a pipeline. Cons: not suitable for all applications, and synchronization is more complex because each layer must coordinate with the layers above and below.

### Locality
The property that a thread working repeatedly on similar tasks touches the same subset of state, which is then likely to be in the CPU cache. Specialized workers and pipelines exploit it; plain boss/workers does not.
- (P2L5) Restated as the hot-cache benefit of specializing threads.
- Also in: P2L5.

### Lock (Birrell Lock clause)
Birrell's mutex acquisition construct, `Lock(m) { critical section }`, which acquires the mutex on entry and releases it implicitly at the end of the clause.
- Contrast: pthreads (P2L3) has no implicit unlock; lock and unlock are explicit calls.
- (P2L3) Pthreads version: `pthread_mutex_lock(mutex)` acquires a `pthread_mutex_t`, blocking if necessary, and `pthread_mutex_unlock(mutex)` releases it; the code between the two calls is the critical section. The difference from the Lock clause is that forgetting the unlock, or unlocking the wrong mutex, is now possible, which is why "always unlock the correct mutex" is a safety tip. `pthread_mutex_trylock` is the non-blocking variant.
- (P2L4) Calls to library lock/unlock functions are one of the points where the process enters the ULT library scheduler.
- Also in: P2L3, P2L4.

### Lock order
The deadlock-avoidance rule that every thread acquires multiple mutexes in the same global order (for example, always A before B). The particular order matters less than enforcing it everywhere. The lecture calls it the most ideal solution: foolproof, but it takes effort, since in a large program with many mutexes, especially code from different sources, it is hard to guarantee the same order across every source file.
- (P2L3) Repeated as the mutex safety tip "globally order locks; lock mutexes in order".
- Also in: P2L3.

### Many-to-many model
A multithreading model in which some user-level threads are multiplexed over a set of kernel-level threads and others may be bound one-to-one. The kernel knows the process is multithreaded, so if one KLT blocks another can run the remaining ULTs. Cons: requires coordination between the user-level and kernel-level thread managers.
- Paper correction (Stein & Shah): unbound threads are multiplexed by the library over a pool of nearly identical LWPs, so any unbound thread can run on any LWP in the pool rather than on one fixed kernel thread; a bound thread is permanently attached to its own LWP.
- (P2L4) Solaris 2.0 supports many-to-many and one-to-one mappings. The coordination problem is spelled out: neither the kernel nor the library sees the other's decisions (see Thread management visibility), the library may need to ask for more KLTs (see set_concurrency) and learn when its KLTs block (see SIGWAITING), and signal masks must be reconciled (see Signal handling with ULTs and KLTs). The lecture describes LinuxThreads, which NPTL replaced with one-to-one, as very similar to this model; the note adds that LinuxThreads actually created one kernel process per thread with `clone` (a 1:1 mapping), and the similarity was in the complexity of signal handling and thread management.
- Also in: P2L4.

### Many-to-one model
A multithreading model in which all user-level threads of a process map onto a single kernel-level thread, managed by a user-level library. Pros: portable, independent of kernel limits and policies, no system calls for thread operations. Cons: the OS cannot see the threads, so one ULT making a blocking call blocks the whole process.
- (P2L4) Listed among the mappings ("many:1"); the same blocking problem appears in a many-to-many process whose KLTs all block.
- (P2L5) The event-driven model has the analogous problem: one blocking handler blocks the whole process, which motivates asynchronous I/O and helpers.
- Also in: P2L4, P2L5.

### Multithreading
Running multiple independent execution contexts within one process. Benefits: parallel speedup on multiple CPUs, specialization (priorities and hot caches per task type), a smaller memory footprint than multiple processes (one address space), cheaper communication through shared variables than IPC, and on a single CPU the ability to hide I/O latency whenever a thread's idle time exceeds the cost of two context switches. Thread context switches are cheaper than process switches because the virtual-to-physical mappings stay the same. Multithreading the kernel lets the OS itself run several execution contexts concurrently.
- Contrast: a multiprocess application needs a separate address space per process and communicates through costlier IPC.
- (P2L5) Restated in "Are threads useful?": speedup from parallelism, hot caches from specialization, lower memory and cheaper synchronization than multiprocess designs, and hiding I/O latency on a single CPU. P2L5 adds that whether threads are "useful" depends on the metrics and workload, and compares MT against MP and event-driven servers (see MT (multithreaded) model).
- Also in: P2L4 (multithreaded kernel structures), P2L5.

### Mutex
A lock that provides mutual exclusion on shared state: a thread that locks it gains exclusive access, and other threads trying to lock it block until the owner releases it. Depending on the implementation it is unlocked at the end of a lock clause or by an explicit unlock call.
- Stores:
  - lock status (locked or free)
  - owner thread
  - queue of blocked threads waiting to acquire it
  - (P2L3, pthreads) attributes from initialization, such as process sharing
  - (P2L4, adaptive mutex) the owner is used to check whether it is running on a CPU. Lecture version: the mutex also keeps some information about critical-section length. Paper correction (Eykholt et al.): critical-section length is not used; see Adaptive mutex.
- (P2L3) Pthreads version: the type is `pthread_mutex_t`. Differences from P2L2: there is no implicit unlock (`pthread_mutex_lock`/`pthread_mutex_unlock` are explicit, see Lock), mutexes must be explicitly initialized with `pthread_mutex_init(mutex, attr)` (a `pthread_mutexattr_t`, or `NULL` for defaults), `pthread_mutex_trylock` returns immediately instead of blocking, and `pthread_mutex_destroy` frees the mutex. See Common pitfalls (mutex and condition variable rules) (P2L2) for the rules and the paper correction that mutexes need not be global.
- (P2L4) On a multiprocessor a waiter may spin instead of blocking when the owner is running (see Adaptive mutex, Spinning). A handler that locks a mutex the interrupted thread holds deadlocks, so interrupts or signals are masked around mutex operations, unless interrupts run as threads, which saves about 12 instructions per mutex. The kernel does not see ULT-library mutexes, so a ULT holding a lock whose KLT is preempted can stall other ULTs; an unlock that makes a higher-priority thread runnable can force a cross-CPU preemption.
- (P2L5) MT servers need explicit application-level synchronization for shared state; MP servers do not.
- Also in: P2L3, P2L4, P2L5.

### Mutual exclusion
The guarantee that only one thread at a time accesses some shared data or executes a critical section, with others waiting their turn. It is binary: the resource is either free or held.
- (P2L3) Restated: threads access shared state in a controlled manner, so only one thread at a time can modify or otherwise access a shared variable; pthreads provides it through mutexes.
- Also in: P2L3.

### One-to-one model
A multithreading model in which each user-level thread has its own kernel-level thread. The OS sees all threads and their needs, and the library can rely on kernel threading support. Cons: every thread operation is a system call, the application is limited to the kernel's policies and mechanisms (for example supported scheduling policies, a limit on the number of threads), which hurts portability: an application with particular thread-management needs runs only on kernels that provide exactly that support.
- (P2L4) Solaris 2.0 supports it alongside many-to-many, and the lecture suggests looking at 1:1 models given the visibility problems of many-to-many. Linux NPTL is one-to-one (a kernel task per ULT); it is viable now because kernel traps are cheaper, making the system call con less severe, and memory is larger, though very large thread counts may still justify custom policies.
- Also in: P2L4.

### Ostrich algorithm
Handling deadlock by doing nothing: assuming it will not happen and rebooting if it does.

### Pipeline pattern
A multithreading pattern that divides each task into a sequence of stages, assigns a thread (or several) to each stage, and passes work between stages through shared buffers. Several tasks are in flight at once, one per stage. Throughput is set by the slowest stage, which can be given proportionally more threads. Pros: specialization and locality. Cons: it is difficult to keep the pipeline balanced over time, since a change in input rate or exhausted resources at a stage may require rebalancing; and synchronization overhead is higher, because there are synchronization points at multiple stages along the end-to-end path.
- Stores (inter-stage shared buffer): see Shared buffer.
- (P2L5) Toy shop comparison: the pipeline finishes 11 orders in 320 ms versus 360 ms for boss/workers, but averages 220 ms per order versus about 196 ms (see Average completion time, P2L5). An MT web server can be laid out as a pipeline in which each thread executes one step only. Apache mounts its modules in a pipeline that every request passes through.
- Also in: P2L5.

### Process scope
The scope in which user-level threads are managed by a per-process user-level library that cannot see threads in other processes; the kernel sees only the process, so it divides CPU among processes equally regardless of how many threads each has.
- Contrast: system scope.
- (P2L3) Scope (system or process) is one of the `pthread_attr_t` attributes.
- Also in: P2L3.

### Producer/consumer
A synchronization scenario in which producer threads add items to a shared buffer and consumer threads remove them, with consumers waiting while the buffer is empty (or not yet full, in the lecture's first example) and producers waiting while it is full. It motivates condition variables over polling.
- (P2L3) The pthreads bounded-buffer program: one producer thread loops 20 times, locking `m`, waiting on `c_prod` while the buffer is full (`num == BUF_SIZE`), adding an item, unlocking, and signalling `c_cons`; one consumer loops forever, locking `m`, waiting on `c_cons` while the buffer is empty (`num == 0`), removing an item, unlocking, and signalling `c_prod`. `main` joins both threads because they are joinable. Difference from P2L2's first example: there one consumer waits for the list to be full; here the consumer waits only for it to be non-empty, and both sides wait.
- Stores (P2L3 example, global state):
  - `buffer`: the shared array of `BUF_SIZE` items
  - `add`: index at which the next item is inserted
  - `rem`: index from which the next item is removed
  - `num`: number of items currently in the buffer
  - `m`: the mutex protecting all of the above
  - `c_cons`: condition variable consumers wait on (buffer not empty)
  - `c_prod`: condition variable producers wait on (buffer not full)
- The boss/workers work queue is a producer/consumer queue with the boss as the sole producer.
- Also in: P2L3.

### Proxy variable
A variable that represents the access state of a shared resource, such as `resource_counter`, so that a mutex protects updates to the proxy rather than the resource itself. As long as every access is first reflected in the proxy, the policy can be richer than plain mutual exclusion.

### Readers/writer lock
The construct built in the readers/writer example: a mutex-protected proxy counter plus two condition variables. Readers increment the counter, read outside the mutex, then decrement it and signal a writer when it reaches zero; a writer waits until the counter is zero, sets it to -1, writes, then resets it to 0 and wakes waiters. Waiters recheck their predicate in a `while` loop because the condition can change between removal from the wait queue and reacquiring the mutex.
- Stores:
  - `resource_counter`: 0 means free, greater than 0 is the number of active readers, -1 means a writer is active (equivalent to separate `read_counter` and `write_counter`)
  - `counter_mutex` protecting the counter
  - `read_phase` condition variable on which readers wait
  - `write_phase` condition variable on which writers wait
- Lecture version: on exit the writer broadcasts `read_phase` and signals `write_phase`.
- Paper correction (Birrell): the refined `ReleaseExclusive` wakes only one class: it broadcasts to readers if any are waiting and otherwise signals one writer. Waking both is correct but is the kind of spurious wake-up his revision removes.

### Readers/writer problem
The sharing problem in which zero or more readers may access shared state concurrently, or at most one writer, but never readers and a writer together. A single mutex around the state is too restrictive because it serializes readers.

### Shared buffer
A bounded memory region through which threads pass data, used between boss and workers and between pipeline stages; it decouples the components.
- Stores:
  - array of slots for items
  - add (insert) and remove indices
  - count of items
  - mutex and condition variables guarding it
- (P2L1) Message-passing IPC uses a kernel-managed channel "like a shared buffer" between processes. (P2L3) The producer/consumer example's `buffer`, `add`, `rem`, `num` with `m`, `c_cons`, `c_prod` is a concrete shared buffer.
- Also in: P2L1, P2L3.

### Signal (condition variable)
The condition variable operation that wakes a waiting thread to tell it the condition may now hold. The order in which threads run after signal or broadcast is up to the scheduler, not the order of the calls.
- Lecture version: signal alerts a (single) waiting thread.
- Paper correction (Birrell): Signal awakens at least one blocked thread, possibly more; the SRC implementation could rarely wake several, one reason to recheck the condition in a `while` loop. POSIX `pthread_cond_signal` likewise unblocks at least one thread.
- Contrast: broadcast wakes all waiters. Also distinct from an OS signal (P1L2, P2L4), which is a process notification.
- (P2L3) The pthreads form is `pthread_cond_signal(cond)`, which notifies one thread waiting on a `pthread_cond_t`. P2L3 adds that a mutex is not needed to signal, so signalling after unlocking can avoid spurious wake-ups.
- Also in: P2L3.

### Specialization
Assigning threads to particular tasks or task types so they can be managed differently (for example, higher priority for important work) and keep their working state in a hot cache.
- (P2L5) Listed again as a reason threads are useful (hot cache), and the pipeline's specialization is weighed against boss/workers in the toy shop comparison.
- Also in: P2L5.

### Spurious wake-up
Lecture version: waking a thread that cannot possibly proceed, as when a writer broadcasts or signals while still holding the mutex, so the woken readers move from the condition variable's queue straight onto the mutex's queue. It wastes cycles on context switches but does not affect correctness. Unlocking before signalling avoids it, but the lecture says this is not possible when whether to signal depends on shared state.
- Paper correction (Birrell): Birrell's "spurious wake-ups" are wake-ups of threads that cannot make useful progress, caused by using Broadcast where Signal would do or by waiting on one condition variable for several reasons. The case the lecture describes, a thread woken inside Wait only to block on a mutex the signaller still holds, he calls a "spurious lock conflict". Standard usage (POSIX, OSTEP) is closer to Birrell's: a thread returns from wait without its condition being true.
- Paper correction (Birrell): only the test of shared state needs the mutex. In `ReleaseShared` the reader computes `doSignal := (i = 0)` inside the lock clause and calls `Signal(cW)` after it, avoiding the lock conflict. POSIX also allows signalling without holding the mutex.
- (P2L3) The condition variable safety tips repeat the remedy: a mutex is not needed to signal or broadcast, so notifying after unlocking can prevent spurious wake-ups.
- Also in: P2L3.

### Synchronization mechanism
A construct that coordinates the execution of concurrent threads, such as a mutex (mutual exclusion) or a condition variable (waiting for a condition). Birrell describes further mechanisms; this lecture covers these two.
- (P2L3) Condition variables are again introduced as synchronization mechanisms. (P2L4) Adaptive mutexes and the kernel's lack of visibility into library synchronization. (P2L5) Synchronization is a cost of MT servers that the event-driven model avoids.
- Also in: P2L3, P2L4, P2L5.

### System scope
The scope in which user-level threads are visible to the kernel and managed system-wide, so the kernel allocates CPU in proportion to the number of threads rather than processes. In the lecture's example, if the kernel gives every user-level thread an equal share of the CPU, the process with twice as many threads receives a larger share overall.
- Contrast: process scope.
- (P2L3) Scope is a `pthread_attr_t` attribute. (P2L4) Paper correction (Stein & Shah): global (system) scheduling scope is the reason to bind a thread, for threads needing real-time response (see Bound thread).
- Also in: P2L3, P2L4.

### Thread
An independent execution context within a process. Threads of one process share the address space (code, data, heap, open files, virtual-to-physical mappings) but each has its own registers, program counter, and stack, so they can run different instructions concurrently.
- Contrast: a process has its own address space; switching between threads of one process does not change mappings and is cheaper than switching processes.
- (P1L2) The thread is one of the OS's application abstractions. (P2L3) Pthreads represents a thread with `pthread_t`. (P2L4) Threads can be supported at user level, kernel level, or both; in Linux a thread is a task created by `clone` with all sharing flags set. (P2L5) MT servers achieve concurrency with threads in one address space.
- Also in: P1L2, P2L3, P2L4, P2L5.

### Thread data structure
The structure that represents one thread to its thread manager (library or kernel). A multithreaded process's PCB becomes more complex because it must incorporate these per-thread execution contexts.
- Stores:
  - thread ID
  - program counter
  - stack pointer
  - register values
  - stack
  - state (running, ready, blocked)
  - other attributes, such as priority
  - link to the owning process
  - (P2L4, kernel-level structure) relationship to the CPU it executes on (multi-CPU systems)
- (P2L4) Refinement into two structures. At user level, the threading library keeps a user-level thread data structure (thread IDs, thread registers, thread stacks) so it can track resource use and make scheduling and synchronization decisions; different processes may link entirely different libraries. At kernel level, rather than replicating the whole PCB per KLT, the PCB is split and only the parts that differ per KLT (stack and registers) move into a kernel-level thread data structure, which points to the process on whose behalf it runs, so on a switch between KLTs the kernel can tell whether the whole PCB must be swapped. At scale the system maintains relationships: ULTs to their process's PCB, each PCB to its KLTs, each KLT to its process, and, with multiple CPUs, each KLT to a CPU data structure. Difference from P2L2: P2L2 describes one generic per-thread structure; P2L4 splits it by manager (library vs kernel) and treats the kernel part as a piece carved out of the PCB.
- (P2L3) Pthreads represents a thread with `pthread_t`, which holds the thread's identifier, its execution state, and other thread-relevant information maintained by the library, and configures it at creation through `pthread_attr_t`.
- (P2L4) Implementations: Solaris uses a ULT structure, an LWP, and a KLT structure (see ULT data structure (Solaris), LWP, Kernel-level thread data structure (Solaris)) and returns thread IDs as indexes into a pointer array (see Thread ID (Solaris)); Linux uses `task_struct`. Exited threads' structures may be kept for reuse (see Death row).
- Also in: P2L3, P2L4.

### Thread pool
A set of worker threads created up front rather than on demand, so that thread creation cost is not paid per task. A common refinement, which tends to be the most effective, grows the pool in response to high demand by adding several threads at once, not one thread at a time.
- Stores:
  - the worker threads, initialized up front
  - the shared buffer (work queue) the boss fills and the workers consume
- (P2L4) The same motive, avoiding thread creation cost, drives reuse of exited threads' structures from death row and pre-created interrupt threads. (P2L5) Apache uses a dynamic thread pool in each process, and also adjusts the number of processes dynamically.
- Also in: P2L4, P2L5.

### Unbound thread
In the many-to-many model, a user-level thread that can be scheduled on any of the process's allocated kernel-level threads.
- Contrast: bound thread.
- Paper correction (Stein & Shah): unbound threads are multiplexed over a pool of nearly identical LWPs. (P2L4) Paper correction (Stein & Shah): a bound thread that calls `priocntl()` changes its LWP and can run in the real-time class ahead of unbound threads.
- Also in: P2L4.

### User-level thread (ULT)
A thread created and managed by a user-level library linked into the process. To execute it must be associated with a kernel-level thread that the kernel schedules.
- Contrast: kernel-level thread. The kernel schedules KLTs and sees nothing of ULTs except through their KLT; the library schedules ULTs onto the KLTs available to it. ULT operations avoid system calls but, without kernel visibility, a blocking ULT can block its KLT and everything mapped to it.
- (P2L4) Supporting threads at user level means a library linked with the application provides all management and support for threads: the thread data structure and the scheduling mechanisms (see Thread data structure, User-level library scheduler); different processes may use entirely different libraries. The library sees ULTs and the KLTs available to it, and keeps a per-ULT signal mask the kernel cannot see. In Solaris, ULTs are scheduled onto LWPs; in Linux NPTL each ULT has its own kernel task.
- (P2L5) The many-to-one blocking problem is recalled to motivate helpers in the event-driven model.
- Also in: P2L4, P2L5.

### Wait (condition variable)
The operation `Wait(mutex, cond)`: called with the mutex held, it atomically releases the mutex and places the thread on the condition variable's wait queue; when woken, the thread is removed from the queue and reacquires the mutex before returning. Because those two steps are separate, the caller must recheck its condition in a `while` loop.
- (P2L3) The pthreads form is `pthread_cond_wait(cond, mutex)`, with the arguments in the opposite order: on entry it releases the mutex and places the thread on the condition variable's wait queue, and on wake-up it reacquires the mutex before returning.
- Also in: P2L3.

### Wait graph (wait-for graph)
A graph whose edges go from a thread waiting on a resource to the thread owning it. A cycle is necessary and sufficient for deadlock.
- Stores:
  - nodes: threads (and optionally resources)
  - edges: waiter to owner

### Worker variants (specialized workers)
A boss/workers variant in which groups of workers specialize in different task types. The boss does a little more work per task to route it, which is usually offset by more efficient workers. Pros: locality and quality of service (more threads for urgent or higher-paying work). Cons: load balancing is harder to reason about.

## P2L3 Threads Case Study: PThreads

### Compiling pthreads
Programs that use pthreads include `pthread.h` and must be linked against the pthreads library by passing `-lpthread` at compile time. On certain platforms the better option is `-pthread`, which tells the compiler both to link the pthreads library and to configure the compilation for threads. Without the library, the program may not report certain errors at compile time, but it will still fail.

### Condition variable safety tips
See Common pitfalls (mutex and condition variable rules) (P2L2).

### Detached thread
A thread that cannot be joined back into the parent. Lecture version: pthreads creates joinable threads by default, and for a joinable child the parent should not terminate until the child has completed and been joined with an explicit join; if the parent exits early, the children may become zombies. Detaching lets the parent exit early (with `pthread_exit`) while the children continue their execution, and makes parent and children equivalent, except that the parent still holds some additional information about the children it created. Birrell's interface does not consider detachable threads.
- Paper correction (Birrell): Join "is not called very much at SRC", some thread facilities do not provide it at all, and a thread whose procedure returns with no later Join "quietly evaporates", which is in effect a detached thread. The paper says nothing about what happens to other threads when the forking thread exits. POSIX agrees that detach only lets a thread's storage be reclaimed without a join, and other threads outlive `main` only if it calls `pthread_exit` instead of returning.
- Contrast: joinable thread.
- (P2L4) Lecture version: an exited thread is marked as on death row. Paper correction (Stein & Shah): in Solaris only detached threads go on death row when they exit; undetached threads go on a zombie list until joined.
- Also in: P2L4.

### Joinable thread
The default pthreads thread type: when it terminates, its exit status and resources are retained until another thread calls `pthread_join` on it.
- (P2L4) Lecture version: an exited thread is marked as on death row. Paper correction (Stein & Shah): Solaris keeps an exited undetached thread on a zombie list until `thr_join()` reaps it.
- Also in: P2L4.

### Mutex safety tips
See Common pitfalls (mutex and condition variable rules) (P2L2).

### Producer/consumer example (pthreads)
See Producer/consumer (P2L2).

### pthread_attr_init / pthread_attr_destroy / pthread_attr_{set,get}{attribute}
The calls that allocate and initialize a `pthread_attr_t`, deallocate it, and set or read individual attributes in it.

### pthread_attr_setdetachstate
Sets the detach state in a `pthread_attr_t`; calling it with `PTHREAD_CREATE_DETACHED` before `pthread_create` makes the new thread detached from the start.

### pthread_attr_t
The pthreads attributes data structure passed to `pthread_create` to configure the new thread; passing `NULL` gives default behavior.
- Stores:
  - stack size
  - scheduling policy
  - priority
  - scope (system or process)
  - inheritance
  - joinable or detached state

### pthread_cond_init / pthread_cond_destroy
Allocate and initialize, or destroy, a condition variable. `pthread_cond_init` takes a `pthread_condattr_t` pointer; `NULL` gives the default behavior.

### pthread_cond_signal / pthread_cond_broadcast
See Signal (condition variable) and Broadcast (P2L2).

### pthread_cond_t
See Condition variable (P2L2).

### pthread_cond_wait
See Wait (condition variable) (P2L2).

### pthread_condattr_t
The attributes structure that customizes a condition variable at `pthread_cond_init` time; `NULL` gives the default behavior.
- Stores:
  - process-shared setting: whether the condition variable is used only by the threads of one process (the default) or shared across processes

### pthread_create
See Fork (Birrell thread Fork) (P2L2).

### pthread_detach
`pthread_detach(thread)`: marks an existing thread as detached so it cannot be joined.

### pthread_exit
Terminates the calling thread. Lecture version: a parent whose children are detached does not need to wait for them, so it can simply exit with `pthread_exit`.
- Paper correction (Birrell): per POSIX, detach only lets a thread's storage be reclaimed without a join, and other threads outlive `main` only if it calls `pthread_exit` instead of returning.

### pthread_join
See Join (Birrell thread Join) (P2L2).

### pthread_mutex_destroy
Destroys (frees) a mutex.

### pthread_mutex_init
`pthread_mutex_init(mutex, attr)`: explicitly initializes a mutex before use; `NULL` attributes give the default behavior. The alternative is the static initializer at declaration time, which the producer/consumer example uses for its mutex `m` instead of calling `pthread_mutex_init`.

### pthread_mutex_lock / pthread_mutex_unlock
See Lock (Birrell Lock clause) (P2L2).

### pthread_mutex_t
See Mutex (P2L2).

### pthread_mutex_trylock
Attempts to acquire the mutex and returns immediately with an error if it is already held, instead of blocking like `pthread_mutex_lock`.

### pthread_mutexattr_t
The attributes structure that customizes a mutex at `pthread_mutex_init` time; `NULL` gives the default behavior.
- Stores:
  - process-shared setting: by default a mutex is private to its process, visible only to that process's threads, and it can be changed so the mutex is shared with other processes

### pthread_t
The pthreads data type that represents a thread; `pthread_create` fills it in and later calls such as `pthread_join` take it. Most of its contents are not seen directly by the developer; the pthreads library uses and maintains them.
- Stores:
  - the thread's identifier
  - its execution state
  - any other information relevant to the thread
- (P2L2) It plays the role of the thread ID that Fork returns and Join takes (see Thread data structure). (P2L4) Contrast: the Solaris library returns an index into a thread pointer array (see Thread ID (Solaris)), and Linux identifies a task by `pid`.
- Also in: P2L2, P2L4.

### Pthreads (POSIX Threads)
The POSIX standard threads API, which provides Birrell-style mechanisms: `pthread_create` and `pthread_join` for Fork and Join, `pthread_mutex_*` for mutexes, and `pthread_cond_*` for condition variables, plus detachable threads and attribute structures.
- (P1L2) The Mac OS X BSD component provides POSIX API support (see POSIX (Portable Operating System Interface)). (P2L4) On Linux it is implemented by NPTL, one kernel task per thread, which replaced LinuxThreads; the lecture calls LinuxThreads very similar to the Solaris many-to-many model, but it actually created one kernel process per thread (1:1) and resembled Solaris only in the complexity of its signal handling and thread management.
- Also in: P1L2, P2L4.

### Thread argument race
See Data race (race condition) (P2L2).

### Zombie thread
A terminated joinable thread whose exit status and resources have not yet been reclaimed because no thread has joined it. A thread is not a zombie while it is still running; it becomes one only after it finishes unjoined, and a detached thread never becomes one. Lecture version: if the parent thread exits early, its joinable child threads may turn into zombies: they may have completed or died, but they were never exited or reaped properly.
- (P2L4) Paper correction (Stein & Shah): Solaris puts an exited undetached thread on a zombie list until the thread that calls `thr_join()` on it reaps it; only detached threads go on death row.
- Also in: P2L4.

## P2L4 Thread Design Considerations

### Adaptive mutex
A mutex that, on contention, either spins or blocks depending on circumstances; it makes sense only on multiprocessors, where the owner may be running in parallel. Lecture version: spin if the owner is currently running on a CPU and the critical section is short, block if it is long; this requires recording the owner and some information about critical-section length.
- Paper correction (Eykholt et al.): the adaptive mutex (`MUTEX_DEFAULT`) spins while the recorded owner is running on a processor, checked by polling whether any CPU's current-thread pointer equals the owner, and sleeps once the owner stops running; on a uniprocessor it therefore always sleeps. Critical-section length is not an input; short hold times are the assumption behind the policy, not a measured value.
- Stores:
  - lock status
  - owner thread (used to check whether the owner is on a CPU)
  - queue of blocked waiters
- Difference from Mutex (P2L2): the P2L2 mutex always blocks a contending thread; the adaptive mutex may spin first. The rest of the mutex definition carries over (see Mutex, P2L2).

### Bottom half and top half
Lecture version: when an interrupt is handled by a separate thread, the top half runs in the context of the interrupted thread and must be fast, non-blocking, and minimal; the bottom half runs in the handler thread and may be arbitrarily complex, including blocking. When the interrupt first occurs it may still be necessary to disable certain interrupts, but once handling passes to the separate thread they can be re-enabled, since interrupts arriving then are handled as for any other thread and pose no additional danger of deadlock.
- Paper correction (Eykholt et al.): the paper rejects this two-level design (a bounded first-level handler waking a second-level thread) because it requires restructured drivers and always costs a full context switch. SunOS 5.0 runs the whole handler on the interrupt thread and pays for a full thread only when the handler blocks on contention. Oracle's driver guide uses such a split only for high-level interrupts, through soft interrupts.

### clone
The Linux system call that creates a new task. Like `pthread_create` it takes a function and an argument, plus `sharing_flags` that choose which parts of the parent's state (address space, open files, signal handlers, and so on) the child shares. All flags set creates a thread sharing everything; all flags cleared creates a new process, and Linux implements `fork` this way.

### CPU data structure (Solaris)
The kernel structure representing one physical CPU, from which all the other linked thread structures can be reached. On SPARC a dedicated register holds the currently executing thread.
- Lecture version, stores:
  - current thread
  - list of kernel-level threads
  - dispatching and interrupt handling information
- Paper correction (Eykholt et al.): the cpu structure points to the currently executing thread and to that CPU's idle thread, and holds the current dispatching and interrupt handling information. Thread structures are linked on a per-process list and on a system-wide list of all threads; the paper describes no per-CPU list of kernel threads.

### Cross-CPU preemption
On a multiprocessor, the user-level library running on one CPU may decide that a thread on another CPU should be preempted, for example when T2 unlocks a mutex and higher-priority T3 becomes runnable while T1 runs elsewhere. Since one CPU cannot modify another's registers, the library sends a signal to the other thread's context so the library code runs locally there, blocks T1, and schedules T3.

### Death row
The list where exited threads' data structures are placed instead of being freed immediately, so they can be reused by later thread creations; a reaper thread periodically frees them. Reuse saves thread creation cost.
- Paper correction (Stein & Shah): only detached threads go on death row; an undetached thread goes on a zombie list and is reaped by the thread that calls `thr_join()` on it. The reaper runs when there are idle LWPs or when death row is full, and frees the stacks of threads that used library-allocated stacks. Freed stacks are kept for reuse, so the reaping rate affects thread creation speed.
- Stores:
  - list of exited (detached) thread structures and their stacks awaiting reuse or reaping

### Default signal actions
The OS default responses to a signal when the process installs no handler: terminate, ignore, terminate and core dump, stop, or continue (from stopped).

### Directed signal
A signal sent to a specific thread (kernel-level thread) rather than to the process as a whole. The ULT library uses it to forward a signal to the KLT running the user-level thread that has the signal enabled.

### Hard process state
The part of the process state that is relevant to all user-level threads of a process and is not swapped when switching between its kernel-level threads.
- Stores:
  - virtual address mapping
  - (Solaris per-process list) user credentials
  - (Solaris per-process list) signal handlers
- Contrast: light process state.
- This is the process-wide part of the PCB once it is split for multiple KLTs (see PCB, P2L1).

### Interrupt
A notification of an event generated externally to the CPU that receives it, by I/O devices, timers, or other CPUs. Interrupts are asynchronous, are identified by a number that depends on the hardware, can be masked per CPU, and are handled by handlers the OS specifies for the whole system. Which interrupts exist depends on the hardware; how they are handled depends on the OS. Handling occurs in the context (and on the stack) of the interrupted thread; see Interrupts as threads for the paper correction that SunOS 5.0 instead moves onto a preallocated interrupt thread's stack.
- Contrast: a signal is generated by the CPU and software running on it (the OS), can be synchronous or asynchronous, depends on the OS rather than the hardware, is masked per execution context, and is handled by handlers each process installs. Two identical machines have the same interrupts but different signals if they run different operating systems.
- (P2L1) An interrupt is one way a running process is stopped and returned to the ready state, and one of the events that puts a process on the ready queue.
- Also in: P2L1.

### Interrupt handler table (interrupt vector table)
The system-wide table the CPU consults when an interrupt arrives: the interrupt number indexes it, and the entry gives the starting address of the handler, which is loaded into the program counter.
- Stores:
  - one entry per interrupt number
  - per entry, the starting address of the OS's handler routine

### Interrupt mask
A per-CPU bit vector in which each bit enables or disables one interrupt. If an interrupt is disabled, the hardware routing mechanism does not deliver it to that CPU, and it remains pending.
- Stores:
  - one enable/disable bit per interrupt

### Interrupt routing (multicore)
On a multi-CPU system, interrupt routing logic delivers an interrupt to any CPU that currently has it enabled. Enabling a given interrupt on only one CPU confines its handling overhead to that core and can improve performance.

### Interrupts as threads
Handling interrupts in their own threads so that a handler that needs a mutex blocks like any other thread instead of deadlocking with the interrupted thread. To avoid dynamic thread creation cost, the kernel pre-creates and pre-initializes thread structures for interrupt routines; the lecture says that, since dynamic thread creation is expensive, Solaris looks for locks: a handler that contains no locks cannot block and runs on the interrupted thread's stack, and only a handler that might lock a mutex is turned into a real thread. Lecture version of cost: the checks and possible thread creation add about 40 SPARC instructions per interrupt, but no longer masking around each mutex saves about 12 instructions per lock/unlock, and mutexes are far more frequent than interrupts, so the net is a win (optimize for the common case).
- Paper correction (Eykholt et al.): SunOS 5.0 does this for most interrupts; interrupts above a tunable "thread level" are not handled as threads and can synchronize only through spin mutexes and software interrupts. Thread level is normally the maximum priority; it is lowered, typically to the interrupt level of the scheduling clock, only where firmware cannot tolerate the short dispatcher lockout.
- Paper correction (Eykholt et al.): SunOS 5.0 does the minimum work to move onto the stack of a preallocated interrupt thread and makes it the current thread; the interrupted thread is pinned until the interrupt thread returns or blocks. Running on the interrupted thread's kernel stack, or on a separate interrupt stack, is the traditional UNIX scheme the paper replaces. Only if the interrupt thread blocks does it save its state and become a full thread.
- Paper correction (Eykholt et al.): the roughly 40 extra instructions are not the cost of creating a thread; no thread is created per interrupt, interrupt threads are preallocated, and conversion to a full thread happens only on lock contention.

### Kernel process data structure (Solaris)
The per-process structure the Solaris kernel maintains; it holds user information and points to the address space mapping and to the process's kernel-level threads.
- Stores:
  - list of kernel-level threads
  - pointer to the virtual address space (mapping) structure
  - user credentials
  - signal handlers (the set shared by the whole process)
- This is Solaris's form of the PCB (see PCB, P2L1, for the general structure and its P2L4 split).

### Kernel-level thread data structure
See Thread data structure (P2L2).

### Kernel-level thread data structure (Solaris)
The kernel structure for one kernel-level thread. It holds execution context that is always needed, even when the thread is not running (for example by the scheduler), so it is not swappable; it points to the LWP and to the stack, which are swappable.
- Stores:
  - kernel-level registers
  - stack pointer
  - scheduling info (priority, state, scheduling class)
  - pointers to the associated LWP, process, and CPU structures
  - per the paper correction under CPU data structure: links on the per-process list and the system-wide list of all threads

### kthread_worker
The Linux 3.17 kernel thread structure, declared in `kthread.h`; together with the functions in that header it provides a simple interface for creating and stopping kernel threads. Of its four members, the one that describes the process the kernel thread is running is a `task_struct`; the spinlock and the `list_head` do not.

### Light process state
The part of process state relevant only to a subset of user-level threads, those associated with one kernel-level thread; it is saved and restored when switching between kernel-level threads of the same process.
- Stores:
  - signals (signal mask)
  - system call arguments
  - (Solaris LWP) user-level registers
- Contrast: hard process state, which is shared and stays in place.
- This is the per-KLT part of the PCB once it is split (see PCB, P2L1); Solaris keeps it in the LWP.

### LinuxThreads
The earlier Linux threads implementation that NPTL replaced. The lecture describes it as very similar to the many-to-many model of the Solaris papers, with the same kind of complexity in signal management. Outside the lecture, per the note: LinuxThreads created one kernel process per thread with `clone`, plus a manager thread, so its mapping was 1:1; the similarity to Solaris was in signal handling and thread management complexity, not the mapping.

### LWP (Lightweight Process)
In Solaris, the kernel-visible structure associated with each kernel-level thread that runs user-level threads. To the user-level library, LWPs are the virtual CPUs onto which it schedules ULTs; the kernel can inspect them when making scheduling decisions. Its contents resemble the ULT structure's but are visible to the kernel, and it need not be present when the process is not running, so it is swappable.
- Stores:
  - user-level registers
  - system call arguments
  - resource usage info
  - signal mask
- Also in: P2L2 (Stein & Shah callout: unbound threads share a pool of nearly identical LWPs, a bound thread has its own).

### max_threads
The Linux 3.17 variable that holds the limit on the number of threads. Linux also enforces a minimum: some threads must be available at startup for the OS to boot, so the fork initialization code in `fork.c` ensures that at least 20 threads can be created.

### MSI (Message Signaled Interrupt)
The mechanism most modern devices use to raise interrupts: a special message carried on the same interconnect that connects the device to the CPU complex, rather than a dedicated pin. The interrupt is identified by the message (or by the pin, for pin-based interrupts).

### Multiple data structures (rationale)
The design choice of splitting process state into several smaller structures (ULT, LWP, KLT, process, CPU) rather than one large PCB. A single control block is large, private to each entity even when information could be shared, saved and restored entirely on each context switch, and hard to update. Multiple structures are smaller, easier to share, let a context switch save and restore only what changes, and let the user-level library update only its portion for customized behavior.
- Contrast: the P2L1 PCB is the single-control-block design this argues against (see PCB, P2L1).

### NPTL (Native POSIX Threads Library)
The current Linux threads implementation, using a one-to-one model with a kernel task per user-level thread. It is viable because kernel traps have become cheaper and memory larger, removing the pressure to keep kernel threads few; large thread counts may still justify custom policies.

### One-shot signal
A signal type where n occurrences while pending look like one, and the handler must be explicitly re-enabled after each delivery.
- Contrast: real-time signal.

### Pending (interrupt or signal)
The state of an interrupt or signal that arrived while masked; it is delivered when the mask re-enables it. Multiple pending instances of the same signal are typically handled once, so raising a signal several times does not guarantee several handler runs (except for real-time signals).

### POSIX signal table (signal.h)
The table in the POSIX `signal.h` header listing the full set of signals, with each signal's default action and description. Signals quiz matches from it:
- terminal interrupt: SIGINT
- "high bandwidth data available on a socket": SIGURG, which is actually raised when out-of-band (urgent) data arrives on a socket and has nothing to do with bandwidth
- background process attempting to write: SIGTTOU, which applies only to a background process group writing to its controlling terminal when the terminal's `TOSTOP` flag is set
- file size limit exceeded: SIGXFSZ

### pthread_setconcurrency
The pthreads counterpart of `set_concurrency`. The application passes an exact number of kernel-level threads it would like, or 0 to let the implementation decide. The call is only a hint and is meaningful only on many-to-many implementations; Linux uses a one-to-one model, so there it has no effect.

### Real-time signal
A signal type that is queued, so n occurrences invoke the handler n times.

### Reaper thread
A special thread that periodically garbage-collects thread data structures on death row (see Death row for the paper correction on when it runs).

### Red zone
Lecture version: an unallocated portion of the address space placed between consecutive thread data structures (with their stacks) laid out contiguously, so a thread that overruns its stack faults immediately, attributing the error to the offending thread rather than to the thread whose data it overwrote.
- Paper correction (Stein & Shah): the red zone is the invalid page the library places after each stack it allocates (library stacks are mapped pages of anonymous memory), so the process is signalled if a thread runs off its stack. An application that supplies its own stacks can add a red zone or pack the stacks its own way.

### set_concurrency
Lecture version: a system call by which an application tells the OS how many kernel-level threads it would like, for example two when four ULTs never have more than two runnable at once.
- Paper correction (Stein & Shah): the interface is `thr_setconcurrency()`, a threads library call rather than a system call, which gives the library a hint about the expected concurrency. The library ensures there are at least n LWPs in its pool (or one per thread if there are fewer than n threads) and creates them itself; growth beyond n comes from SIGWAITING.

### setjmp / longjmp
Unix operations useful for saving (`setjmp`) and restoring (`longjmp`) the context of a user-level thread, which a user-level library uses when it schedules ULTs onto the kernel-level threads it sees as virtual CPUs.

### SIGALRM (SIGALARM)
The asynchronous signal delivered when a timer expires (a timeout).

### SIGFPE
The synchronous signal generated by an arithmetic fault such as division by zero.

### SIGKILL
The signal one process sends to another to terminate it. The lecture lists it as synchronous from the sending process's side and asynchronous from the receiver's.

### signal / sigaction
The system calls a process uses to install a custom handler for a signal. Not all signals can be caught.

### Signal handler
The routine run when an enabled signal is delivered. Processes install custom handlers for most signals; when a signal arrives, the thread's program counter is set to the handler's address while its stack pointer stays the same, so the handler runs on the interrupted thread's stack. A handler that tries to lock a mutex the interrupted thread already holds deadlocks.

### Signal handler table
The per-process mapping the OS maintains from signal numbers (for example SIGSEGV is 11) to handling routines.
- Stores:
  - one entry per signal number
  - per entry, the starting address of the process's handler, or the default action (terminate, ignore, core dump, stop, continue)
  - handler flags and the mask to apply during handling

### Signal handling with ULTs and KLTs
The policy for keeping user-level and kernel-level signal masks consistent without a system call on every user-level mask change. Each ULT has a library-visible mask and each KLT a kernel-visible mask; a ULT disabling a signal updates only its own mask. The library, not the application, installs a wrapper around each real handler, so it always sees a signal first and can see every ULT's mask; when a signal arrives it can (1) deliver it if the running ULT has it enabled, (2) schedule a runnable ULT that has it enabled, (3) send a directed signal to the KLT running a ULT that has it enabled, or (4) if no ULT has it enabled, make a system call to disable it in that KLT's mask and reissue it to the entire process, so the kernel delivers it to another KLT whose mask still has it enabled. With several KLTs the masks are fixed one at a time as signals arrive. Re-enabling likewise needs a system call. Mask updates are frequent and cheap; signals are rare, so they absorb the extra cost (optimize for the common case).
- Paper correction (Stein & Shah): the global handler resends the signal to the process if it was undirected, or to the same LWP if it was directed; the kernel's signal delivery information lets it tell the two apart.

### Signal mask
A bit vector with one bit per signal, indicating whether that signal is enabled or disabled for an execution context. A disabled signal is made pending rather than delivered; masking around a mutex acquisition prevents the handler deadlock. Lecture version: signals are masked on a per-process basis, and masks are kept per execution context (ULT on KLT), with separate user-level and kernel-level masks.
- Paper correction (Stein & Shah): each thread has its own signal mask, and each LWP has its own as well; only the set of signal handlers is shared by the whole process. Linux `signal(7)` agrees: masks are per thread, handlers per process.
- Stores:
  - one enable/disable bit per signal (and, alongside it, the set of pending signals)

### SIGSEGV
The synchronous signal (number 11) the OS generates when a process accesses memory that is not allocated to it or is otherwise invalid.

### SIGWAITING (kernel notification before blocking)
Lecture version: it would help if the kernel signalled the user-level library before a KLT blocks, so the library could request more KLTs; the kernel exposes system calls and special signals for this coordination.
- Paper correction (Stein & Shah): Solaris does not notify the library before blocking. The kernel sends SIGWAITING when it detects that all LWPs in the process are blocked in indefinite waits, and if there are runnable threads the library responds by creating a new LWP. Per-block notification is what scheduler activations (Anderson et al.) provide.

### Solaris 2.0 (SunOS 5.0)
The multithreaded Sun kernel studied in the lecture's two papers. It targets multiprocessors, supports single- and multithreaded processes with many-to-many and one-to-one ULT:KLT mappings, and represents threads with ULT, LWP, KLT, process, and CPU structures.

### Spinning
Repeatedly trying to acquire a lock in a loop without blocking. It pays off only when the lock will be released soon, typically when the owner is running on another CPU and the critical section is short.
- Paper correction (Eykholt et al.): critical-section length is not an input; the adaptive mutex spins while the owner is running and sleeps once it stops (see Adaptive mutex).
- Contrast: blocking (P2L2).

### Synchronous and asynchronous signals
Synchronous signals occur in direct response to an action of the receiving thread, such as SIGSEGV or SIGFPE; asynchronous signals arrive independently of what the receiver is doing, such as SIGALRM or a SIGKILL from another process.

### Task (Linux)
The Linux abstraction for an execution context, essentially a kernel-level thread. A single-threaded process has one task; a multithreaded process has one per thread. Linux never had one contiguous PCB; process state is a collection of structures that tasks point to.
- Linux's form of the execution context and kernel-level thread (see Execution context and Kernel-level thread (KLT), P2L2).

### task_struct
The Linux kernel structure describing a task.
- Stores:
  - `pid_t pid`: the task's id
  - `pid_t tgid`: task group id, the pid of the process's first task, which identifies the process
  - `struct list_head tasks`: links into the list of the process's tasks
  - `struct mm_struct *mm`: the memory (address space) descriptor
  - `struct files_struct *files`: the open files table
  - state, priority and scheduling policy, parent and children, signal handlers and pending signals
- Linux's per-task structure in place of a contiguous PCB (see PCB, P2L1, and Thread data structure, P2L2).

### Thread ID (Solaris)
The identifier the Solaris thread library returns on thread creation: an index into an array of thread pointers rather than a direct pointer. If there is a problem with the thread, a raw pointer would just point to corrupt memory; with a table index, the library can encode information in the table entry that gives meaningful feedback or an error message.
- Stores (the thread pointer array):
  - one entry per thread ID
  - per entry, a pointer to the thread data structure, or encoded information giving feedback or an error message

### Thread management visibility
What each side can see. The kernel sees kernel-level threads, CPUs, and the kernel scheduler; the user-level library sees user-level threads and the kernel-level threads available to it. Neither sees the other's decisions: the library can change the ULT:KLT mapping, and the kernel is unaware of library structures such as mutexes and wait queues. For example, if a ULT holding a lock has its KLT preempted, the library may cycle through other ULTs that all need that lock and waste time.
- Also in: P2L2 (the one-to-one model lets the OS see threads and their needs, the many-to-one model hides them, and many-to-many requires coordination between the two thread managers).

### Thread pinning
Permanently associating a kernel-level thread with a CPU on a multi-CPU system. The lecture uses it as the analogy for binding a user-level thread to a kernel-level thread; "bound" is the term Solaris threads introduced for the ULT-to-KLT case (see Bound thread, P2L2, including the Stein & Shah correction that the paper gives global scheduling scope as the reason to bind and does not mention pinning).

### Thread-local storage (TLS)
Per-thread memory that each thread accesses through the same name but with its own copy. The lecture lists it as a field of the Solaris thread data structure.
- Paper correction (Stein & Shah): see ULT data structure (Solaris); TLS holds the thread structure, not the reverse.
- Stores:
  - the thread's private copies of thread-local variables
  - per the paper correction, also the thread structure itself and a private copy of `errno`

### ULT data structure (Solaris)
The user-level library's structure for one user-level thread. Its size is almost entirely known up front, so structures can be packed contiguously, but the library does not control stack growth, which motivates the red zone.
- Lecture version, stores:
  - execution context
  - registers
  - signal mask
  - priority
  - stack pointer
  - thread-local storage
  - stack
- Paper correction (Stein & Shah): the relationship runs the other way: the thread structure itself, along with a private copy of `errno`, is allocated in thread-local storage. The library carves TLS from the base of each new thread's stack, using a size (`_etls`) the run-time linker computes at program start, and on SPARC register `%g7` points to the current thread's TLS.

### User-level library scheduler
The library code that schedules ULTs onto KLTs (LWPs). Lecture version: the process jumps into it when ULTs explicitly yield, when a timer set by the library expires, when ULTs call library functions such as lock and unlock, and when blocked threads become runnable; it can also run in response to signals from timers or the kernel.
- Paper correction (Stein & Shah): the paper describes no user-level time slicing; threads compete for LWPs by priority. An active thread is preempted only when a newly runnable thread has higher priority or the active thread's priority drops below a runnable thread's, and the library does this by setting a flag in the thread structure and sending the thread's LWP a SIGLWP. The Solaris `thr_setprio` man page likewise describes fixed-priority scheduling.
- Also in: P2L2 (in the many-to-one and many-to-many models the user-level library decides which ULT runs on which KLT).

### User-level thread data structure
See Thread data structure (P2L2).

## P2L5 Thread Performance Considerations

### Aggregate metric
A metric combined from others to understand a system more accurately, for example the execution time or the wait time averaged over all tasks, possibly weighted by task priority.

### AMPED (Asymmetric Multi-Process Event-Driven)
An event-driven architecture in which a single event-driven main process handles all requests and delegates potentially blocking I/O to separate helper processes, used when the kernel is not multithreaded and asynchronous I/O is unavailable. It fakes asynchronous I/O for portability and has a smaller footprint than pure MP or MT, since helpers do one isolated task. Cons: it works well for server-type applications but is not necessarily applicable to arbitrary applications, and event routing on multi-CPU systems is complex. Flash follows it.
- Contrast: SPED has no helpers, so it blocks on disk I/O; AMTED uses helper threads instead of processes.

### AMTED (Asymmetric Multi-Threaded Event-Driven)
The multithreaded equivalent of AMPED: the event-driven main thread delegates blocking operations to helper threads in the same address space.

### Apache web server
A web server whose core provides the basic server functionality, accepting connections and managing concurrency, with functionality extended by modules mounted in a pipeline that every request passes through. It combines MP and MT: each instance is a process implementing a multithreaded boss/workers configuration with a dynamic thread pool, and the number of processes is also adjusted dynamically, based on factors such as the number of outstanding connections, the number of pending requests, and CPU usage. In the Flash paper's experiments (then purely multiprocess) it had the lowest performance, having no comparable optimizations.
- Also in: P2L2 (boss/workers, pipeline, and thread pool patterns it combines).

### Application-level caching
Caching performed by the application itself rather than relying only on the OS. Flash caches at multiple levels, on both data and computation: cached files (data caching), and cached pathname-to-file lookups and response headers (computation), the headers staying valid as long as the file does not change.
- Stores (Flash's caches):
  - cached files (data): file contents, mapped into memory with `mmap`
  - cached pathname-to-file lookups (computation)
  - cached response headers (computation, file-dependent)

### Asynchronous I/O
I/O system calls that return immediately: the kernel captures enough information about the caller and about where and how the data should be returned once it becomes available, so the calling thread is not blocked in the kernel while the I/O proceeds. It is made possible by a multithreaded kernel (another kernel thread does the waiting) and can also benefit from hardware devices that report a request's results later; it fits the event-driven model, and is not available on all platforms or devices.
- Contrast: synchronous I/O (P1L2 synchronous mode) blocks the caller; helpers emulate asynchronous I/O by blocking in a separate thread or process.
- Also in: P1L2 (asynchronous system call modes are mentioned).

### Average completion time (toy shop example)
The lecture's comparison metric for 11 toy orders of 120 ms each with 6 threads per model (boss/workers: 1 boss + 5 workers; pipeline: 6 stages of 20 ms): boss/workers takes 360 ms total but averages about 196 ms per order, while the pipeline takes 320 ms total but averages 220 ms per order. Pipeline wins on total execution time, boss/workers on average completion time, which shows that which model is better depends on the metric; changing the number of workers or orders may give the opposite conclusion.
- Boss/workers derivation: waves of 5, 5, 1 orders finish at 120, 240, 360 ms; average (120*5 + 240*5 + 360)/11 = 2160/11, about 196 ms.
- Pipeline derivation: order k finishes at 120 + 20(k-1) ms; total 120 + 10*20 = 320 ms; average 2420/11 = 220 ms.
- Also in: P2L2 (the boss/workers and pipeline patterns being compared).

### Bandwidth
In the Flash experiments, total bytes transferred divided by the total time to transfer them (requests times file size divided by time in the best-case test). Evaluated as a function of file size on the intuition that larger files amortize the connection cost; in the best-case test it rises sharply with file size and then plateaus.

### Baseline
The existing performance of the system being improved, against which an experiment shows its gain over the state of the art or the most common configuration.

### Best case experiment (single-file test)
The Flash paper's synthetic test in which every request asks for the same file, so after the first request it is served from cache, with file size varied from 0 to 200 KB and bandwidth measured. Lecture version of results: all servers rise sharply then plateau; SPED is best, Flash close behind because of its memory-residency check; Zeus drops after about 125 KB; MT and MP are lower because of synchronization and context switching; Apache is lowest.
- Paper correction (Pai et al.): the paper discusses a Zeus anomaly only on FreeBSD, for file sizes between 10 and 100 KB, attributing it to the `writev` byte alignment problem; the Solaris graph the lecture shows is not discussed in terms of a Zeus anomaly, so the ~125 KB figure is a reading of the graph, not a stated result.
- Paper correction (Pai et al.): the paper attributes the slight lag of Flash-MT and Flash-MP to "extra kernel overhead (context switching, etc.)" and does not mention synchronization. MP processes have private address spaces and need no user-level synchronization between requests, while MT needs it for shared data, so synchronization is an MT cost only.

### Client-perceived performance
Performance as the user experiences it, which may call for meeting a threshold rather than maximizing a raw number; for example, smooth video needs at least 30 fps, since humans cannot perceive more than 30 fps, so the goal is to make sure there are at least 30 fps, not to maximize fps.

### Connection rate
In the Flash experiments, the total number of client connections serviced divided by the elapsed time. It falls as file size grows, since each connection involves more work, and it rises with each optimization added to Flash, the fully optimized version being highest.

### CPU utilization
The fraction of time the CPU does useful work; for hardware, the metric of interest may be the increase in utilization.
- Related: CPU efficiency (P2L1), useful execution time over total CPU time including scheduling overhead, is the same kind of ratio applied to the scheduler's cost; P2L5 treats utilization as one evaluation metric among several.
- Also in: P2L1 (as CPU efficiency).

### CS trace
The Rice University computer science department web server trace used in the Flash experiments: many files, too large to fit in memory, so most requests are not served from cache. Results: SPED drops sharply because it blocks on disk I/O; MT beats MP thanks to a smaller memory footprint (more memory to cache files); the lecture also cites cheaper synchronization (see the correction below); Flash is best, with a smaller footprint than MT and MP (more memory to cache files and headers) and no explicit synchronization.
- Paper correction (Pai et al.): MP processes need no user-level synchronization between requests, so synchronization is an MT cost only; it cannot be where MT gains over MP.

### epoll
A newer Linux event-notification system call that avoids `select`'s and `poll`'s scans of large, mostly irrelevant lists of file descriptors.
- Contrast: `select` and `poll` scan through a potentially large list of file descriptors, few of which have input; `epoll` eliminates these scans of large lists of mostly useless descriptors.

### Event
In the event-driven model, a notification that some input or completion occurred, such as receipt of a request, completion of a send, or completion of a disk read. For a web server, an event is input on one of its file descriptors.

### Event dispatcher
The core of an event-driven process: a loop that waits for incoming events and, based on each event's type, invokes the registered handler, which in a single-threaded process is a plain function call.
- Stores:
  - the set of file descriptors (sockets, files, helper pipes) it monitors
  - the registered handlers, keyed by event type or descriptor
  - per-request state for the requests in progress (connection, stage reached, buffers), since many requests are interleaved in one execution context

### Event handler
A function registered with the event dispatcher that processes one kind of event and runs to completion. If it needs to block, it initiates the operation (asynchronously, or via a helper) and returns control to the dispatch loop.

### Event-driven model
A server architecture with a single address space and a single thread of control in which an event dispatcher interleaves the processing of many requests, advancing each until it must wait and then switching to another. On one CPU it avoids context switches when there is no idle time to hide; on multiple CPUs one event-driven process per CPU can serve more requests than CPUs, provided events are steered to the right CPU. Benefits: smaller memory footprint and no context switching or synchronization. Cons: a blocking call in a handler blocks the whole process, which motivates asynchronous I/O and helpers.
- Contrast: MP and MT handle one request per execution context at a time and get concurrency from many contexts.

### Execution time
The total time to complete a job, the natural metric for something like matrix multiplication.

### Experimental methodology
The lecture's guidance for designing and running experiments: decide what systems are compared (vary software with hardware fixed, or vice versa), what workloads are used (real traces or synthetic), and what metrics are measured, chosen with the stakeholders in mind (clients care about response time, operators about throughput). Use standard metrics for the domain, understand the system resources and workload parameters that affect them, choose realistic parameter ranges (hundreds of threads, not three), vary one factor at a time (compare apples to apples), compare against a baseline, run each test N times, compute metrics, present results, and draw a conclusion.

### File descriptor
The handle a process uses to refer to an open file, socket, or pipe; in the event-driven model, events are inputs on file descriptors, which is why sockets, files, and helper pipes can all be watched with `select` or `poll`.
- Stores:
  - an integer index into the process's file descriptor table
  - the table entry: a pointer to the open file object plus per-descriptor flags (such as close-on-exec)
  - the open file object: current offset, access mode and status flags, and a reference to the underlying file (inode), socket, or pipe
- Also in: P1L2 (files and sockets, the abstractions descriptors refer to).

### Flash alignment optimization
Lecture version: Flash makes optimizations that take advantage of the networking hardware and the network interface card: data structures are aligned so that DMA operations can be performed without copying data, and DMA with scatter-gather support lets the response header and the file data be sent from different memory locations, avoiding a copy.
- Paper correction (Pai et al.): the paper frames this as byte position alignment, not a network hardware feature. When `writev()` sends a response header followed by file data, the OS copies the regions into a contiguous kernel buffer, and a header whose length is not a multiple of the word size misaligns every subsequent copy. Flash pads response headers to multiples of 32 bytes to target 32-byte cache lines; DMA is not mentioned.

### Flash web server
An event-driven web server following the AMPED model, with helper processes for the blocking operations, which are essentially disk reads; helpers communicate with the dispatcher through pipes. Lecture version of the flow: the helper reads the file into memory with `mmap`, and the dispatcher uses `mincore` to check whether the pages are resident, calling a local handler if they are (no blocking) and a helper if not. Flash also performs application-level caching and alignment optimizations.
- Paper correction (Pai et al.): the residency check comes first: the main process tests mapped file pages with `mincore()` before use, and only if they are not resident does it dispatch a helper. Both the main process and the helper `mmap` the file, the helper touches every page, then notifies the main process via IPC that the file can be sent without blocking.

### Helper threads and processes
Threads or processes to which an event-driven server's handlers hand off operations that would block, when asynchronous I/O is not available. The handler passes the request to a helper and returns to the dispatcher; the helper performs the synchronous I/O and blocks while the main loop does not. Communication uses sockets or pipes, which present file descriptors so `select` and `poll` still work. Helpers must be processes if the kernel is not multithreaded (AMPED) and can be threads otherwise (AMTED).
- Also in: P2L2 (the many-to-one blocking problem they work around in the event-driven setting).

### Metric
A measurable or quantifiable property of a system that is used to evaluate its behavior, for example the execution time of an implementation compared with alternatives. One may care about averages, extremes, or percentiles (such as completing within 3 ms 95% of the time), and may need to combine or derive metrics.

### mincore
The system call that reports which pages of a mapped region are resident in physical memory; Flash uses it to decide whether serving a file would block.
- Also in: P1L2 (memory pages; `malloc` gets memory through `brk` or `mmap`).

### MP (multiprocess) model
A concurrent server built from multiple instances of the same single-threaded process, each handling one request at a time. Pros: simple to build once the single process is correct. Cons: higher memory footprint, costly process context switches, hard and expensive shared state through IPC, and difficulty having multiple processes listen on one port.
- Also in: P2L2 (multiprocess versus multithreaded applications: a separate address space per process and costlier IPC).

### MT (multithreaded) model
A concurrent server built from multiple threads in one address space. Pros: shared address space and state, cheap user-level context switches, lighter memory requirements. Cons: harder to implement, explicit application-level synchronization, and dependence on OS thread support. Lecture version: in the lecture's diagram each thread performs every step, though boss/workers or pipeline layouts are possible, and the Flash comparison is described as a multithreaded implementation using the boss/workers pattern.
- Paper correction (Pai et al.): in the MT architecture each thread performs all the steps of one HTTP request before accepting a new one, analogous to a process in MP; Flash-MT uses 64 threads and no boss thread is described.
- Contrast: MP isolates requests in separate address spaces, making shared state hard and costly to maintain through IPC; MT shares state, saving memory and switch cost at the price of explicit application-level synchronization.
- Also in: P2L2 (multithreading benefits and the boss/workers and pipeline patterns).

### Owlnet trace
The Rice University trace from a server hosting student websites used in the Flash experiments; it is small enough to fit in a typical server's memory. Results resemble the best case: Flash and SPED best, then MT/MP, then Apache. Flash edges out SPED because the occasional request that needs disk I/O blocks SPED but goes to a Flash helper.

### Percentage of SLA violations
The fraction of requests in which a service fails its service-level agreement; useful when evaluating enterprise software.

### Performance per dollar
Performance delivered per unit of cost, used to judge whether new hardware's cost is justified.

### Performance per watt
Performance delivered per unit of power, relevant when energy costs are high; performance per joule is the variant used when the energy consumed over an execution matters.

### Pipe
A unidirectional kernel byte channel between processes, accessed through file descriptors; Flash's helpers use pipes to notify the event dispatcher.
- Stores:
  - kernel buffer of bytes in transit
  - read and write ends (file descriptors)
  - queues of processes blocked reading an empty pipe or writing a full one

### Platform efficiency
How well a platform's resources are used to deliver a given throughput; higher efficiency means spending less on the platform for the same work, which matters to a datacenter owner.

### poll
A system call, alternative to `select`, that takes a list of file descriptors and reports which have input; it also scans the whole list each time.

### Request rate
The number of requests arriving at or handled by a server per unit time.

### Response time
The time from a client's request to the server's response; the metric clients care about.
- Contrast: throughput, the metric operators care about; a change can improve one while holding or degrading the other.

### select
The system call that takes a range of file descriptors and returns the first descriptor that has some input on it (as the lecture puts it); it must scan a potentially large list of descriptors on every call.

### Service Level Agreement (SLA)
A guarantee that enterprise applications typically give their customers, for example a response within three seconds, or (for a service like Expedia, whose customers are airlines) the most accurate quote for 95% of the flights returned.
- The percentage of SLA violations measures how many requests took longer than promised or returned quotes that were not accurate.

### SPED (Single Process Event-Driven)
The basic event-driven architecture: one process, one thread, an event dispatcher, and no helpers. It performs best when data is in cache but blocks the whole process on any disk I/O, since it lacks asynchronous I/O. Zeus is a SPED server.

### Summary of performance results
Lecture version: with data in cache, SPED "smokes" AMPED Flash because Flash makes an unnecessary memory-residency test on each request; both beat MT/MP, which incur synchronization and context switching overhead. When the workload is disk-bound, Flash far outperforms SPED, which blocks on I/O, and beats MT/MP because its smaller footprint leaves more memory for caching.
- Paper correction (Pai et al.): Flash-SPED only "slightly outperforms" Flash on the single-file test because of the residency check, and on cached trace workloads Flash is "very competitive" with Flash-SPED, with only a slight difference; SPED and AMPED are roughly tied on cached data.
- Paper correction (Pai et al.): the paper attributes the MT/MP lag to kernel overhead such as context switching; synchronization is an MT cost only, since MP needs no user-level synchronization between requests.

### Synthetic workload
Generated, rather than recorded, requests; the Flash paper used a synthetic workload generator which, instead of replaying a real distribution of page accesses, let them run best and worst case analysis and ask "what if" questions about access patterns they had not observed.

### Testbed
The experimental setting: where and how experiments were carried out and which metrics were gathered, often a representative "toy" setup when real software, machines, and workloads are not feasible.

### Throughput
The number of tasks or requests completed per unit time; it measures a platform's utility, from a single server to a datacenter, and is what server operators care about.
- Also in: P2L2 (boss/workers throughput is limited by the boss and inversely proportional to its time per task; pipeline throughput is set by the slowest stage).

### Trace
A recorded sequence of real requests from a production system, replayed to obtain a realistic yet reproducible workload; the Flash paper used the CS and Owlnet traces.

### Wait time
The time until a job starts executing, as opposed to when it finishes; usually something to minimize.

### Workload
The inputs a system is evaluated under. For a web server its parameters include request rate, number of concurrent requests, file size, and access pattern; whether a design is "useful" depends on the workload and the metrics chosen.

### Zeus
A commercial event-driven web server compared in the Flash paper. Lecture version: a SPED implementation with two processes.
- Paper correction (Pai et al.): Zeus v1.30 is a SPED server run as a single process for the synthetic-workload experiments and in a vendor-advised two-process configuration for the real-trace tests. The two-process setup gives it a slight advantage over single-process Flash-SPED in the trace tests, since one process can keep serving while the other blocks on disk I/O.
