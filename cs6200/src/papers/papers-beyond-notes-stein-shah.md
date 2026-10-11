---
id: operating-systems-papers-beyond-notes-stein-shah
title: "Stein & Shah, Implementing Lightweight Threads: Beyond the Notes"
course: operating-systems
lecture: papers-beyond-notes-stein-shah
---

# Stein & Shah: everything not in the notes

Everything in the paper that the original lecture notes do not state, plus places where the paper contradicts them; validated against the paper text. The reference point is the original lecture notes: the notes now carry `> **Paper (...):**` callouts for the lecture-framing discrepancies listed under "Notes vs paper discrepancies", so some gaps below are now annotated in the notes. Paper: <https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-stein-shah-paper.pdf>. The body sections predate the corrections listed under "Covered in the notes", so a few of their bullets are now also in the notes.

Paper has no performance tables or measurements; figures are Figures 1-5 (architecture, LWP interface list, scheduling diagram, thread states, LWP states). Footnotes 1-10 are folded into the section where they appear.

## Abstract
- Stated goals: threads light enough to be created quickly, to exist by the thousands in one UNIX process, and to synchronize rapidly, while still giving fully concurrent access to system resources. (Abstract)
- The LWP pool is managed by the library and grows or shrinks automatically so the process always makes progress without using excessive kernel resources; the programmer can also tune the thread/LWP relationship. (Abstract)
- The paper's stated focus: scheduling and synchronizing user threads, and their interaction with UNIX signals, in a multiplexing threads library. (Abstract)

## Introduction
- The implementation has two parts: the threads library and a kernel modified to support multiple threads of control in one UNIX process (described in [Eykholt 1992]). (Introduction)
- Paper structure: threads model, library architecture (both skippable for readers of the SunOS Multi-thread Architecture paper [Powell 1991]), kernel interfaces for multiple threads of control, scheduling, synchronization, signals, and a thread-aware debugger. (Introduction)

## Threads Model
- The number and identity of threads a process uses are invisible from outside the process; threads are framed as execution resources applied to the problem at hand. (Threads Model)
- Threads share most of the process's OS state, not only memory: e.g., a file opened by one thread can be read by another. There is no system-enforced protection between threads. (Threads Model)
- The library's synchronization facilities are mutexes, condition variables, semaphores, and readers/writer (multiple readers, single writer) locks; synchronization variables are allocated by the application in ordinary memory. (Threads Model)
- Threads in different processes can synchronize via synchronization variables placed in shared memory or mapped files, even though threads in different processes are invisible to each other; such variables must be marked process-shared at initialization. (Threads Model)
- Synchronization variables may have variants with different blocking behavior while keeping the same semantic (e.g., mutual exclusion). (Threads Model)
- Each thread can make arbitrary system calls and interact with other processes normally. Some operations affect all threads: exit() from any thread destroys all threads. (Threads Model)
- Each thread has its own signal mask, so a thread can block asynchronous signals while touching state that a signal handler also modifies. (Threads Model) [Per-thread masks are now stated in the note's Stein & Shah callout; the stated purpose is not.]
- Signal delivery rules: synchronous signals (e.g., SIGSEGV) go to the thread that caused them; externally generated signals go to one thread that has the signal unmasked; if all threads mask it, the signal stays pending on the process until some thread unmasks it; signals can also be sent to a particular thread in the same process. (Threads Model)
- SIG_IGN discards received signals; SIG_DFL default actions (e.g., stop, continue, exit) apply to the whole process, not one thread. (Threads Model)
- Per-thread signal handler vectors were rejected: they add non-trivial storage per thread and permit conflicting requests (e.g., one thread SIG_DFL, another a handler), complicating implementation and use; per-thread handling can be built on top of the shared vector if needed. (Threads Model, footnote 1)
- Two fork variants: one clones the whole process with all its threads; the other reproduces only the calling thread, useful when the child will immediately call exec(). (Threads Model)

## Threads Library Architecture
- Threads are implemented by a dynamically linked library on top of kernel-supported threads of control called LWPs. (Threads Library Architecture)
- These LWPs are unrelated to the LWP library of SunOS 4.0; the authors reused the name out of "lack of imagination" and to match accepted terminology. (Threads Library Architecture, footnote 2)
- Each LWP is separately dispatched by the kernel, can make independent system calls, incur independent page faults, and run in parallel on a multiprocessor. All LWPs in the system are scheduled by the kernel onto CPUs by scheduling class and priority. (Threads Library Architecture)
- The library schedules threads on its LWP pool the way the kernel schedules LWPs on processors. Strictly, the SunOS 5.0 kernel schedules kernel threads on processors, and kernel threads are the execution context underlying LWPs. (Threads Library Architecture, footnote 3)
- Threads are "simply data structures and stacks" maintained by the library and unknown to the kernel. The library can switch an LWP from one thread to another, and create, destroy, block, or activate threads, without OS involvement. (Threads Library Architecture)
- LWPs are much more expensive than threads because each uses dedicated kernel resources. Dedicating one LWP per thread, as in CMU C Threads [Cooper 1990], would stop databases or window systems from using threads freely (e.g., one or more per client) or make them inefficient; a window system may be best written with many threads, but only a few need kernel resources (other than virtual memory) at the same instant. (Threads Library Architecture)
- Binding rationale: a thread needing real-time response (e.g., a mouse-tracking thread) must be scheduled against all other execution entities in the system (global scheduling scope), so the library allows it to be permanently bound to an LWP. A bound thread is still a thread and can synchronize with bound and unbound threads in the process. (Threads Library Architecture) [The global-scope, real-time (mouse-tracking) rationale is now stated in the note's Stein & Shah callout; that a bound thread is still a thread that synchronizes with bound and unbound threads is not.]
- Exposing both levels separates what the programmer sees (threads) from what the kernel provides (LWPs). Most programmers think only in threads; they tune the thread/LWP relationship only when optimizing. The LWP count is framed as the degree of real concurrency the application requires. (Threads Library Architecture)

## Figure 1: Multi-thread Architecture Examples
- Figure 1 shows two processes with threads above LWPs in the user/kernel boundary and LWPs mapped onto CPUs at the hardware level, illustrating different thread-to-LWP multiplexing per process. (Figure 1)

## LWP interfaces
- LWPs share most process resources. LWPs have attributes threads lack: a kernel-supported scheduling class, virtual-time timers, an alternate signal stack, and a profiling buffer. (LWP interfaces)
- The LWP interfaces are compatible with the UNIX International LWP interfaces of the time. (LWP interfaces, footnote 4)
- _lwp_create() creates another LWP in the process. _lwp_makecontext() builds a machine context that emulates the standard calling sequence to a function; it is passed to _lwp_create(), giving some machine independence. (LWP interfaces)
- The kernel-provided LWP synchronization interfaces are mutexes, condition variables (wait, timed wait, signal, broadcast), and counting semaphores. (LWP interfaces, Figure 2)
- LWP sync variants can support priority inversion prevention protocols such as priority inheritance. (LWP interfaces)
- Counting semaphores are provided specifically so that a synchronization mechanism safe with respect to asynchronous signals is available. (LWP interfaces)
- LWP sync routines enter the kernel only when they must; e.g., acquiring an uncontended LWP mutex may need no kernel entry. The kernel knows about LWP sync variables only during actual use. (LWP interfaces)
- LWP sync variables live in application memory; placed in shared memory or a mapped file, they synchronize LWPs across all mapping processes. A mapped file lets the sync variables, with other shared data, persist in the file, so a restarted application can keep using them without initialization. (LWP interfaces)
- A blocked LWP sleeps on a kernel sleep queue associated with the offset in the mapped file or shared memory segment, so processes can synchronize even with the variable mapped at different virtual addresses. Internally this is a hash queue keyed by a two-word value: the vnode (internal file handle) and offset. (LWP interfaces, footnote 6)
- Terminology aside: Multics called this file/segment offset the "virtual address" and called today's virtual address (the effective address computed by instructions) the "logical address". (LWP interfaces, footnote 5)
- _lwp_getprivate()/_lwp_setprivate() give one pointer's worth of LWP-private storage, typically used by a threads package to point to its thread structure. On SPARC this is register %g7. (LWP interfaces)
- %g7 is reserved to the system by the SPARC Application Binary Interface [USO 1990], so ABI-compliant applications cannot use it. (LWP interfaces, footnote 7)
- Alternative considered: a private memory page per LWP. It costs more kernel effort and possibly more memory per LWP, but is probably the best choice on register-constrained machines or where no user register is reserved to the system. (LWP interfaces)
- New signal SIGLWP: reserved for threads packages, used as an inter-LWP signal when directed at a particular LWP via _lwp_kill(). (LWP interfaces)
- New signal SIGWAITING: generated by the kernel when it detects that all LWPs in the process are blocked in indefinite waits; threads packages use it to keep processes from deadlocking for lack of execution resources. (LWP interfaces) [When the kernel generates SIGWAITING is now stated in the note's Stein & Shah callout; the deadlock-avoidance purpose is not.]

## Figure 2: LWP Interfaces
- Full interface list: int _lwp_create(context, flag, lwpidp); void _lwp_makecontext(ucp, func, arg, private, stack, size); void *_lwp_getprivate(); void _lwp_setprivate(ptr); void _lwp_exit(); int _lwp_wait(waitfor, departedp); lwpid_t _lwp_self(); int _lwp_suspend(lwpid); int _lwp_continue(lwpid). (Figure 2)
- Sync and signal entries: void _lwp_mutex_lock(lwp_mutexp); void _lwp_mutex_unlock(lwp_mutex); int _lwp_cond_wait(lwp_condp, lwp_mutexp); int _lwp_cond_timedwait(lwp_condp, lwp_mutexp, timeout); int _lwp_cond_signal(lwp_condp); int _lwp_cond_broadcast(lwp_condp); int _lwp_sema_wait(lwp_semap); int _lwp_sema_post(lwp_semap); int _lwp_kill(lwpid, sig). (Figure 2)

## Threads Library Implementation
- Stack storage is either allocated automatically by the library or passed in by the application at creation. (Threads Library Implementation) [Now stated in the note body (thread-design-considerations.md, section User Level Thread Data Structures), so not beyond the notes.]
- Library-allocated stacks are obtained by mapping pages of anonymous memory, and the library makes the page following the stack invalid: that page is the red zone, so the process is signalled if a thread runs off its stack. (Threads Library Implementation) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- An application supplying its own stacks can provide its own red zone or pack the stacks however it likes. (Threads Library Implementation) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- An earlier implementation used a pointer to the thread structure as the thread ID; it was discarded in favor of an index into a table of pointers so the library can give meaningful errors when passed the ID of an exited and deallocated thread. (Threads Library Implementation; notes cover the index scheme but not that a pointer-ID version existed first)

## Thread-local Storage
- TLS is thread-private storage in addition to the stack: conceptually unshared, statically allocated data, used for thread-private data that must be accessed quickly; each thread has its own copy of thread-local variables while most program variables are shared. (Thread-local Storage)
- The thread structure itself and a thread-private errno are allocated in TLS. (Thread-local Storage) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- TLS is declared with a new #pragma, unshared, supported by the compiler and linker. TLS contents start zeroed; static initialization is not allowed. (Thread-local Storage)
- The run-time linker computes TLS size at program start by summing the TLS segment sizes of all linked libraries and computing each item's offset; the linker defines the symbol _etls for the TLS size. (Thread-local Storage) [That the run-time linker computes the size (_etls) at program start is now stated in the note's Stein & Shah callout; summing the libraries' TLS segment sizes and computing offsets is not.]
- TLS size and offsets are computed at startup rather than link time so a library's TLS requirement is not compiled into the application binary and the library can change it without breaking the binary interface. (Thread-local Storage, footnote 8)
- At thread creation the library uses _etls to allocate TLS from the base of the new thread's stack. (Thread-local Storage) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- After startup TLS size is fixed and cannot grow, which restricts programmatic dynamic linking (dlopen()) to libraries without TLS. (Thread-local Storage)
- Because of these restrictions TLS is not an exported interface; applications get POSIX thread-specific data [POSIX 1992] instead. (Thread-local Storage)
- On SPARC the compiler assumes %g7 points to the TLS base (the same register as the LWP private pointer) and emits %g7-relative TLS references; the library sets %g7 to the running thread's TLS base, with minimal scheduling impact. (Thread-local Storage) [That %g7 points to the current thread's TLS is now stated in the note's Stein & Shah callout; the compiler's %g7-relative references and the shared LWP-private register are not.]

## Thread Scheduling
- LWPs in the pool are set up nearly identical so any thread can run on any of them; while executing, a thread is attached to an LWP and has all the attributes of a kernel-supported thread. (Thread Scheduling) [The pool of nearly identical LWPs on which any unbound thread can run is now stated in the note's Stein & Shah callout (threads-and-concurrency.md); the rest is not.]
- All runnable unbound threads are on a single user-level dispatch queue ordered by priority. (Thread Scheduling)
- Thread priorities range from 0 to "infinity", where infinity is the maximum number representable in 32 bits. (Thread Scheduling, footnote 9)
- Priorities are fixed: the library never changes them dynamically as a time-shared discipline would; only the thread itself or another thread in the same process can change them. An unbound thread's priority is used only by the user-level scheduler and is unknown to the kernel. (Thread Scheduling) [Fixed priorities are now stated in the note's Stein & Shah callout (via the thr_setprio man page); who may change them and the kernel's ignorance of unbound priorities are not.]

## Figure 3: Thread Scheduling
- Figure 3 shows the LWP pool (with a minimum pool size and pool growth driven by SIGWAITING), the run queue, sleep queues on synchronization variables, and LWPs that are idle or switching between threads. (Figure 3)
- An LWP in the pool is either idle or running a thread; an idle LWP waits on a synchronization variable for work (one of two possible, see Idling and parking). (Figure 3 discussion)
- When thread T1 becomes runnable it goes on the dispatch queue, and an idle LWP L1 (if any) is awakened by signalling the idle synchronization variable; L1 switches to the highest-priority thread on the queue. (Figure 3 discussion)
- If T1 blocks on a process-local synchronization object, L1 puts T1 on that object's sleep queue and switches to the highest-priority queued thread, or goes back to idling if the queue is empty. (Figure 3 discussion)
- If all LWPs are busy when T1 becomes runnable, T1 waits on the dispatch queue; an LWP frees up when one is added to the pool or when a running thread blocks on a process-local sync variable, exits, or stops. (Figure 3 discussion)

## Thread States and the Two Level Model
- An unbound thread has five states: RUNNABLE, ACTIVE, SLEEPING, STOPPED, ZOMBIE. (Thread States)
- While ACTIVE, the thread's LWP may be running on a processor, sleeping in the kernel, stopped, or waiting for a CPU on the kernel dispatch queue; the four LWP states refine the single thread ACTIVE state. (Thread States)

## Figure 4: Thread states
- Transitions: RUNNABLE to ACTIVE on dispatch; ACTIVE to RUNNABLE on preempt; ACTIVE to SLEEPING on sleep; SLEEPING to RUNNABLE on wakeup; ACTIVE to ZOMBIE on terminate; stop from RUNNABLE, ACTIVE, or SLEEPING goes to STOPPED; continue from STOPPED goes to RUNNABLE. (Figure 4)

## Figure 5: LWP states
- LWP states within thread ACTIVE: RUNNING, BLOCKED, RUNNABLE, STOPPED. Transitions: RUNNING to BLOCKED on a blocking syscall; BLOCKED to RUNNABLE on wakeup; RUNNABLE to RUNNING on dispatch; RUNNING to RUNNABLE on timeslice or preempt; stop/continue to and from STOPPED. (Figure 5)

## Idling and parking
- Idling: when an unbound thread exits and no threads are RUNNABLE, its LWP switches to a small idle stack associated with each LWP and waits on a global LWP condition variable; when a thread becomes RUNNABLE the condition variable is signalled and an idle LWP wakes and tries to run RUNNABLE threads. (Idling and parking)
- Parking: when a bound thread blocks on a process-local sync variable, its LWP must stop too; it waits on an LWP semaphore associated with the thread. When the thread unblocks the parking semaphore is signalled and the LWP continues the thread. (Idling and parking)
- Optimization: when an unbound thread blocks and nothing else is RUNNABLE, its LWP parks on the thread's semaphore instead of idling, avoiding a context switch to the idle stack and back if the thread becomes runnable quickly. (Idling and parking)

## Preemption
- Threads compete for LWPs by priority, as kernel threads compete for CPUs. The library maintains a queue of ACTIVE threads; if a RUNNABLE thread may outrank some ACTIVE thread, the ACTIVE queue is searched, the victim removed and preempted from its LWP, and that LWP typically runs the higher-priority thread that caused the preemption. (Preemption) [Competing for LWPs by priority is now stated in the note's Stein & Shah callout; the ACTIVE queue search is not.]
- Two triggers: a newly RUNNABLE thread with higher priority than the lowest-priority ACTIVE thread, or an ACTIVE thread's priority lowered below the highest-priority RUNNABLE thread. (Preemption) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- Mechanism: set a flag in the target's thread structure and send its LWP SIGLWP. The library always installs its own SIGLWP handler, which checks for a posted preemption, clears the flag, and switches to another thread. (Preemption) [The flag and SIGLWP are now stated in the note's Stein & Shah callout; the library's SIGLWP handler is not.]
- Side effect: a target blocked in a system call is interrupted by SIGLWP and the call is restarted when the thread resumes; this matters only for calls that should not be restarted. (Preemption)

## The Size of the LWP Pool
- By default the library adjusts the number of LWPs used for unbound threads automatically. (The Size of the LWP Pool)
- Requirement 1: no deadlock for lack of LWPs. Example: more runnable unbound threads than LWPs while all active threads block in the kernel in indefinite waits (e.g., reading a tty); the process cannot progress until a waiter returns. (The Size of the LWP Pool)
- Requirement 2: efficient LWP use. One LWP per thread would leave many LWPs idle and overload the OS with resources for unused LWPs, losing the two-level model's advantages. (The Size of the LWP Pool)
- Let C be the number of ACTIVE plus RUNNABLE threads; C can fluctuate dramatically as events arrive or threads synchronize. If LWP creation/destruction were free, a pool size equal to C at all times would satisfy both requirements; since resizing costs something, the library does not try to match C exactly. (The Size of the LWP Pool)
- SIGWAITING protocol: the library ignores SIGWAITING by default and installs a handler only when the number of threads exceeds the number of LWPs. On SIGWAITING with runnable threads, it creates a new LWP and adds it to the pool. If no threads are runnable and threads are fewer than LWPs, it disables SIGWAITING. (The Size of the LWP Pool) [Creating a new LWP on SIGWAITING when threads are runnable is now stated in the note's Stein & Shah callout; ignoring it by default, installing the handler only when threads exceed LWPs, and disabling it are not.]
- Alternative considered: compute a weighted time average of the application's concurrency and adjust the pool more aggressively; not adopted because it is unknown whether the benefit outweighs the overhead of creating more LWPs. (The Size of the LWP Pool)
- thr_setconcurrency() is a hint from an application that knows its concurrency needs better than the library. With level n: if threads >= n the library ensures at least n LWPs; if threads < n, at least as many LWPs as threads. Growth beyond n comes only from SIGWAITING. (The Size of the LWP Pool) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- thr_setconcurrency() examples: a multi-threaded file copy with one input and one output thread sets 2; a window system server sets expected simultaneously active clients times threads per client. (The Size of the LWP Pool)
- LWP aging: earlier SIGWAITINGs or thr_setconcurrency() calls can leave more LWPs than threads, so LWPs unused for a "long" time, currently 5 minutes, are terminated. Implemented with a per-LWP timer set whenever the LWP starts idling; if it fires, the LWP terminates. (The Size of the LWP Pool)

## Mixed Scope Scheduling
- Bound and unbound threads coexist in one process; window systems benefit: a bound thread in the real-time scheduling class fields mouse events and takes precedence over unbound threads multiplexed on time-sharing LWPs. (Mixed Scope Scheduling) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- When a bound thread calls priocntl(), the system priority control interface, it changes the LWP it is bound to and therefore the thread. Unbound threads keep being multiplexed normally in the presence of bound threads. (Mixed Scope Scheduling) [The priocntl() effect is now stated in the note's Stein & Shah callout; that unbound threads keep being multiplexed normally is not.]

## Reaping bound/unbound threads
- When a detached thread (bound or unbound) exits, it goes on a single queue called deathrow with state ZOMBIE. (Reaping) [Detached-only death row is now stated in the note's Stein & Shah callout; the ZOMBIE state is not.]
- Freeing the stack is deliberately not done at exit, to make thread exit cheap by deferring unnecessary, expensive work. (Reaping)
- The reaper runs when there are idle LWPs or when a reap limit is reached (deathrow full); it traverses deathrow, freeing the stack of each thread that used a library-allocated stack. (Reaping) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- When an undetached thread (bound or unbound) exits, it goes on a separate zombie list and is reaped by the thread that calls thr_join() on it. (Reaping) [Now stated in the note's Stein & Shah callout, so not beyond the notes.]
- Reaper frequency tradeoff: it runs at high priority, so not too often; but not too rarely, because freed stacks go into a cache of available thread stacks that speeds stack allocation for new threads, an otherwise expensive operation, so reaping rate affects thread creation speed. (Reaping) [Stack reuse and its effect on creation speed are now stated in the note's Stein & Shah callout; the high-priority reason not to reap too often is not.]

## Thread Synchronization
- The library implements two basic types of synchronization variables: process-local (the default) and process-shared. (Thread Synchronization)
- In both cases the primitives themselves are safe with respect to asynchronous signals and can be called from signal handlers. (Thread Synchronization)

## Process-local Synchronization Variables
- Default blocking behavior is to put the thread to sleep. Each synchronization variable has its own sleep queue; the primitive puts the blocking thread there and surrenders the executing thread to the scheduler. (Process-local Synchronization Variables)
- Unbound blocker: the scheduler dispatches another thread to its LWP. Bound blocker: it must stay bound, so the LWP is parked on its thread. (Process-local Synchronization Variables)
- On release, the primitive first checks for waiters; a blocked thread is removed from the sleep queue and dispatched by the scheduler. A bound thread is unparked so the kernel dispatches its LWP; an unbound thread is placed on the run queue for its priority and then dispatched to an LWP in priority order. (Process-local Synchronization Variables)

## Process-shared Synchronization variables
- Process-shared objects are placed in memory accessible to more than one process to synchronize threads in different processes. (Process-shared Synchronization variables)
- They must be initialized at creation because their blocking behavior differs from the default; each primitive has an initialization function that marks the variable process-shared, letting the primitives recognize it and block correctly. (Process-shared Synchronization variables)
- Process-shared primitives rely on the LWP synchronization primitives: blocked threads sleep in the kernel still attached to their LWPs, and the LWP primitives handle cross-process synchronization. (Process-shared Synchronization variables)

## Signals
- The core difficulty: providing SunOS MT signal semantics in a two-level model, where the kernel sends signals but cannot see user threads or their masks, so it cannot make correct delivery decisions by itself. (Signals)
- Additional goal: cheap async-safe synchronization primitives. A function is async safe if it is reentrant with respect to signals, i.e., callable from an asynchronously invoked signal handler. (Signals)
- Cheap async-safe primitives matter for multi-threaded libraries with internal critical sections, such as the threads library and its clients like libc. (Signals)
- Example: mutex_lock() interrupted while holding internal threads-library lock L; the handler calls mutex_lock(), tries to take L again, and deadlocks. Masking signals during L's critical section fixes it, so efficient signal masking was a goal because it yields efficient async-safe critical sections. (Signals)

## Signal Model Implementation
- Rejected strategy: each LWP mirrors its current thread's signal mask, letting the kernel choose directly among ACTIVE threads; the set of receivable signals then changes as threads cycle through ACTIVE. (Signal Model Implementation)
- Problems with mirroring: a rarely ACTIVE thread that is the only one with some signal enabled effectively sleeps waiting for a signal it never receives; and a system call is needed whenever an LWP switches between threads with different masks or an active thread changes its mask. (Signal Model Implementation)
- Adopted design: LWP masks and ACTIVE thread masks are treated more independently. The set of signals the process can receive is the intersection of all thread signal masks (in mask terms, a signal is blocked only if every thread blocks it). The library keeps each LWP mask equal to or less restrictive than its thread's mask, so the kernel occasionally delivers signals to ACTIVE threads that have them disabled. (Signal Model Implementation)
- The library interposes its own global signal handlers below the application handlers. On delivery the global handler checks the current thread's mask; if unmasked it calls the application's handler. (Signal Model Implementation) [Now stated in the note body (thread-design-considerations.md, section Threads and Signal Handling: the library wrapper and Case 1), so not beyond the notes.]
- If masked, the global handler sets the current LWP's mask to the current thread's mask, then resends the signal: to the process if undirected, to that LWP if directed. The kernel's signal delivery information lets the handler distinguish directed from undirected signals. (Signal Model Implementation) [The resend rule is now stated in the note's Stein & Shah callout; that the LWP mask is corrected whenever the current thread masks the signal (not only when every thread does) is not.]
- If the signal suits none of the ACTIVE threads, the global handler can cause an inactive thread that has it unmasked to run. (Signal Model Implementation) [Now stated in the note body (thread-design-considerations.md, section Threads and Signal Handling, Case 2), so not beyond the notes.]
- Synchronously generated signals are simply delivered by the kernel to the ACTIVE thread that caused them. (Signal Model Implementation)

## Sending a directed signal
- thr_kill() sends a signal to another thread in the same process; the basic means is to send it to the LWP the thread runs on. (Sending a directed signal)
- If the target is not ACTIVE, thr_kill() just posts the signal in the thread's pending-signals mask; the thread receives the pending signals when it resumes, because the context-switch code sends them to the LWP that resumes the thread. (Sending a directed signal, footnote 10)
- If the target is ACTIVE, thr_kill() sends the signal to its LWP via lwp_kill(). If that LWP blocks the signal (implying the thread does too), the signal stays pending on the LWP until the thread unblocks it, and meanwhile the thread is temporarily bound to that LWP until delivery. (Sending a directed signal)

## Signal Safe Critical Sections
- All asynchronous signals should be masked during critical sections that a signal handler may re-enter, in both applications and the threads library, to prevent deadlock. (Signal Safe Critical Sections) [Now stated in the note body (thread-design-considerations.md, section Why Disable Interrupts or Signals?), so not beyond the notes.]
- thr_sigsetmask() is the interface for this; if no signals occur it makes no system call and costs about as much as writing the user-level thread mask. (Signal Safe Critical Sections; notes cover the no-syscall idea but not the function name)
- Even faster path for the library's own critical sections: it sets/clears a special flag in the thread structure on entry/exit, acting as a mask-all-signals bit; if the flag is set when a signal arrives, the global handler defers the signal as in the mask-mismatch case. (Signal Safe Critical Sections)

## Debugging Threads
- The kernel's standard debugging interface (/proc) is insufficient to control library-supported threads, because the debugger needs information about threads inside the process. (Debugging Threads)
- Rejected: building full knowledge of the threads implementation into the debugger, which would force a debugger re-release whenever internal library data structures change. (Debugging Threads)
- Adopted: a separate dynamically linked thread debugging library, loaded by the debugger via dlopen(), holds all threads-library-specific knowledge and lets the debugger enumerate threads and get/set the state and registers of each thread, ACTIVE or not. (Debugging Threads)
- A version of DBX with thread extensions uses it: it lists all threads and their states (sleeping, running, active, stopped, zombied) and can switch focus to any thread so standard DBX commands inspect its state. (Debugging Threads)

## References
- Cited works: CMU C Threads [Cooper 1990]; multithreading the SVR4 kernel [Eykholt 1992]; the /proc process file system [Faulkner 1991]; UNIX as an application program (Mach) [Golub 1990]; realtime scheduling in SunOS 5.0 [Khanna 1992]; POSIX P1003.4a threads extension [POSIX 1992]; SunOS Multi-thread Architecture [Powell 1991]; priority inheritance protocols [Sha 1990]; SPARC System V ABI supplement [USO 1990]. (References)

## Author Information
- Dan Stein: SunSoft MTS, a developer of the SunOS multi-thread architecture, B.S. CS University of Wisconsin 1981. Devang Shah: SunSoft MTS, M.A. CS UT Austin 1989 (where he extended SunOS 3.2 to provide lightweight processes), B.Tech. Electronics, IT-BHU 1985, previously Tata Consultancy Services. Published at Summer 1992 USENIX, San Antonio. (Author Information)

## Notes vs paper discrepancies
Each item was checked against the paper, the lecture as reconstructed from two independent sets of student notes, Gavrilovska's own CS4210 slides on the paper (no lecture transcript was retrievable), and third-party references; sources are listed under "Discrepancy sources". Verdicts: PAPER CONFIRMED, NOTES WRONG (the notes depart from the paper and the lecture does not support them); LECTURE FRAMING (the notes reproduce the lecture and the paper differs); NOT A REAL DISCREPANCY. The notes now carry a short paper annotation or correction for every item except the -1 sentinel.
- set_concurrency: the lecture calls it a system call that gets the OS to allocate another kernel thread. In the paper, thr_setconcurrency() is a library call giving a hint; the library itself creates LWPs to meet it. Solaris man pages also describe it as a hint (and as obsolete, with no effect, from Solaris 9).
  - Verdict: LECTURE FRAMING, the lecture describes a kernel-supported system call that allocates a kernel thread, and third parties (Solaris man pages, Oracle MT Programming Guide, Gavrilovska's CS4210 slides) side with the paper's library hint.
- Notification before blocking: the lecture wants the kernel to signal the library before blocking. The paper's SIGWAITING arrives after all LWPs are already blocked in indefinite waits; per-block notification is what scheduler activations do.
  - Verdict: LECTURE FRAMING, the lecture says the kernel should notify the library just before blocking, and third parties (Oracle MT Programming Guide, CS4210 slides) side with the paper's SIGWAITING after all LWPs block, the lecture's wish being closer to scheduler activations.
- Red zone motivation: the lecture motivates red zones with thread structures packed contiguously, where one thread overwrites the next. In the paper the red zone is the invalid page after each mmap'd anonymous-memory stack, and TLS (which holds the thread structure) is carved from the base of the thread's stack rather than a separate fixed-size record.
  - Verdict: LECTURE FRAMING, the lecture tells the contiguous-layout, overwritten-neighbour story, and third parties (CS4210 slides, Oracle MT Programming Guide) side with the paper's invalid guard page after each library-allocated stack.
- Death-row reuse: the lecture says death-row thread structures are reused if a creation request arrives before reaping. The paper says the reaper frees stacks into a stack cache, and that cache speeds creation; it also restricts deathrow to detached threads (undetached ones go on a zombie list reaped by thr_join()).
  - Verdict: LECTURE FRAMING, the lecture says structures and stacks are reused before reaping, and the CS4210 slides side with the paper on the detached-only restriction and loosely on reuse through a cache; the timing of reuse rests on the paper alone.
- Thread ID "-1": -1 is an illustrative sentinel; the paper only says the table lets the library return meaningful errors for IDs of exited, deallocated threads. The current note does not use -1; it says only that the table entry can encode information that provides meaningful feedback or an error message.
  - Verdict: NOT A REAL DISCREPANCY, the student notes say only that the table entry can encode information for meaningful errors, no third party covers a sentinel, and -1 is consistent with the paper's rationale.
- Signal masks (corrected in the notes): Signal/Interrupt Similarities said signals are masked per process, matching the lecture's comparison slide, while later sections say per execution context / per user thread. In the paper masks are per thread and per LWP; only handlers are shared per process.
  - Verdict: LECTURE FRAMING, the lecture's interrupts-vs-signals slide says per process, and third parties (Linux signal(7), CS4210 slides) side with the paper's per-thread masks and per-process handlers.
- Many-to-Many description (corrected in the notes): the notes said "some user threads one-to-many with a kernel thread", which reverses the lecture's direction. In the paper unbound threads multiplex over a pool of LWPs and each bound thread has its own dedicated LWP.
  - Verdict: LECTURE FRAMING, the lecture frames M:N as a hybrid of many-to-one and one-to-one (the "one-to-many" wording is the notes' own error), and third parties (Wikipedia, CS4210 slides) side with the paper's pool of LWPs.
- Library timer (valid for generic libraries): the notes list "timer set by the UL library expires" as a way the library scheduler gains control. The paper describes no user-level time slicing: thread priorities are fixed, and preemption happens only on priority changes or a higher-priority thread becoming runnable, delivered via SIGLWP. Time slicing appears only at the LWP level (Figure 5).
  - Verdict: LECTURE FRAMING, the lecture lists the library timer for a generic user-level library, and third parties (Solaris thr_setprio man page, CS4210 slides) side with the paper that Solaris libthread has fixed priorities and SIGLWP preemption, though timer preemption is a legitimate generic design.
- Binding and CPU pinning: the lecture introduces bound threads by analogy to pinning a kernel thread to a CPU, and the notes had turned that into a use case. The paper's rationale is global scheduling scope for real-time response (e.g., mouse tracking, real-time-class LWP via priocntl()); it does not mention CPU pinning.
  - Verdict: LECTURE FRAMING, the lecture mentions pinning as an analogy for binding, and the Solaris thr_setprio man page sides with the paper's system-scope and real-time-class rationale.
- TLS placement: the notes list thread local storage as a field of the thread data structure. In the paper the relationship is inverted: the thread structure itself is allocated in TLS, which is carved from the base of the thread's stack.
  - Verdict: LECTURE FRAMING, the lecture says the thread data structure contains TLS, and the CS4210 slides side with the paper, placing TLS at the base of the stack with %g7 pointing to it.
- All-threads-masked case (corrected in the notes): the notes had the library only make a system call to change the KLT mask. Both the lecture and the paper also resend the signal after correcting the LWP mask (the lecture always to the entire process; the paper to the process if undirected, to the LWP if directed), so another LWP or a later unmasking thread can receive it.
  - Verdict: PAPER CONFIRMED, NOTES WRONG, the lecture also reissues the signal after the system call, and the CS4210 slides agree with the paper, so the notes' omission of the resend is their own.

## Covered in the notes
- Added to the notes from this check: thr_setconcurrency() as a library hint; SIGWAITING after all LWPs block; the red zone as the invalid page after an mmap'd stack; TLS carved from the stack base and holding the thread structure (_etls, %g7); no user-level time slicing, fixed priorities, SIGLWP preemption; binding for system scope and the real-time class via priocntl(); deathrow for detached threads only, the zombie list and thr_join(), the stack cache; resending the signal in the all-masked case; per-thread masks.
- Thread ID as an index into a table of thread pointers rather than a raw pointer, for meaningful errors on stale IDs.
- Thread structure contents (ID, execution context, signal mask, priority, stack pointer) and the existence of thread-local storage.
- Red zones exist and turn a stack overrun into a fault attributed to the offending thread.
- LWPs as virtual CPUs for the user-level scheduler; bound vs unbound threads; process vs system scope; M:N vs 1:1 vs M:1.
- Each thread has a program counter and stack; threads share the address space; mutexes, condition variables, readers/writer locks.
- Deathrow and a reaper thread deferring cleanup to speed creation.
- Cross-CPU preemption via a directed signal to another LWP; the notes now name SIGLWP and the flag.
- Signal masks per user thread and per kernel thread, the kernel cannot see user-thread masks, and handlers are per process.
- Handler-locks-mutex deadlock and the fix of masking signals around the critical section.
- Signal-mask cases: library-installed handler, switching to a thread with the signal enabled, directed re-signal to another LWP, syscall to update the KLT mask when no thread can take the signal, and user-level mask updates without system calls as the common-case optimization.
- join blocks the parent until the child finishes and then deallocates the child.
- Pending signals coalesce: generating a signal several times does not guarantee the handler runs several times (paper: signals received are at most signals sent).
- Each LWP holds user-level registers and a signal mask.


## Discrepancy sources
- <https://www.usenix.org/legacy/publications/library/proceedings/sa92/stein.pdf> (paper)
- <https://github.com/awpala/my-omscs-notes/blob/main/cs-6200/05-P2L4-thread-design-considerations.md> (raw: <https://raw.githubusercontent.com/awpala/my-omscs-notes/main/cs-6200/05-P2L4-thread-design-considerations.md>)
- <https://raw.githubusercontent.com/awpala/my-omscs-notes/main/cs-6200/03-P2L2-threads-and-concurrency.md>
- <https://github.com/Guochiuan/CS6200-notes/blob/main/P2L4%20Thread%20Design%20Considerations.md>
- <https://github.com/Guochiuan/CS6200-notes/blob/main/P2L2%20Threads%20and%20Concurrency.md>
- <https://github.com/hpca01/GIOS/blob/main/thread-design-considerations.md> (checked; a copy of the notes under review, not independent)
- <https://sites.cc.gatech.edu/classes/AY2009/cs4210_fall/lectures/08-UserLevelThreads.pdf> (Gavrilovska, GT CS4210 Fall 2008, "Implementing Lightweight Threads")
- <https://www.coursehero.com/file/38454639/P2L4-ThreadDesignConsiderationsdocx/> (P2L4 transcript; 403, not read)
- <https://docs.oracle.com/cd/E19455-01/817-5435/6mkt2tqfm/index.html> (thr_setconcurrency(3THR), SunOS 5.8)
- <https://docs.oracle.com/cd/E19683-01/817-3944/6mjgl03pl/index.html> (thr_setconcurrency(3THR), SunOS 5.9)
- <https://docs.oracle.com/cd/E19455-01/806-5257/sthreads-56761/index.html> (Oracle MT Programming Guide, Set Thread Concurrency Level)
- <https://docs.oracle.com/cd/E19455-01/806-5257/gen-13/index.html> (Oracle MT Programming Guide, SIGWAITING)
- <https://docs.oracle.com/cd/E19455-01/806-5257/guide-38132/index.html> (Oracle MT Programming Guide, Thread Concurrency)
- <https://docs.oracle.com/cd/E19455-01/817-5435/6mkt2tqfn/index.html> (thr_setprio(3THR), SunOS 5.8)
- <https://docs.oracle.com/cd/E19120-01/open.solaris/816-5137/6mba5vprt/index.html> (Oracle MT Programming Guide, Allocating Stack Space for Threads)
- <https://man7.org/linux/man-pages/man7/signal.7.html>
- <https://en.wikipedia.org/wiki/Thread_(computing)>
- <https://dsf.berkeley.edu/cs262/2005/lecs/24-activations.pdf> (Scheduler Activations, Berkeley CS262)
- <http://www-cs-students.stanford.edu/~dbfaria/quals/summaries/Anderson-1992-2.txt> (Scheduler Activations summary)
