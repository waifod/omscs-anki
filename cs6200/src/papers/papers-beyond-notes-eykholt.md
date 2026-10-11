---
id: operating-systems-papers-beyond-notes-eykholt
title: "Eykholt et al., Multithreading the SunOS Kernel: Beyond the Notes"
course: operating-systems
lecture: papers-beyond-notes-eykholt
---

# Eykholt et al. (SunOS): everything not in the notes

Everything in the paper that the original lecture notes do not state, plus places where the paper contradicts them; validated against the paper text. The reference point is the original lecture notes: the notes now carry `> **Paper (...):**` callouts for the lecture-framing discrepancies listed under "Notes vs paper discrepancies", so some gaps below are now annotated in the notes. Paper: <https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-eykholt-paper.pdf>.

## Abstract
- The redesign was driven by four challenges: symmetric multiprocessing, multithreaded applications, real-time, and multimedia, applied to the SunOS/SVR4 kernel. (Abstract)
- The kernel was restructured around threads, which are used for most asynchronous processing, including interrupts; the result is fully preemptible and capable of real-time response. The notes never say the kernel is preemptible. (Abstract)

## Introduction
- The team explicitly wanted to go further than "merely adding locks to the kernel and keeping the user process model unchanged". (Introduction)
- Design goal: multiple threads of control per user process, each able to execute system calls and handle page faults independently, and able to run concurrently on different processors on an MP. The user-visible thread architecture is described in [Powell 1991]. (Introduction)
- Second design goal: bounded dispatch latency for real-time threads [Khanna 1992]. Real-time response requires absolute control over scheduling, hence preemption at almost any point in the kernel and elimination of unbounded priority inversions wherever possible. (Introduction)
- Rationale for kernel threads: the kernel is itself a complex multithreaded program, so it benefits from a thread facility essentially the same as the one offered to user applications for managing multiple asynchronous activities. (Introduction)
- The result is the SunOS 5.0 kernel, the core OS component of Solaris 2.0: fully preemptible, real-time scheduling, symmetric MP support, user-level multithreading. Several of its locking strategies were described earlier in [Kleiman 1992]. (Introduction)


## Overview of the Kernel Architecture
- The kernel thread is the fundamental entity scheduled and dispatched onto a CPU. It is "very lightweight": only a small data structure and a stack. (Overview)
- Switching between kernel threads never requires changing virtual memory address space information, so it is relatively inexpensive. The notes make this point only for threads of the same user process, not for kernel threads in general. (Overview)
- Kernel threads are fully preemptible and can be scheduled by any scheduling class, including the real-time (fixed-priority) class. Because all other execution entities are built on kernel threads, they form a fully preemptible, real-time "nucleus" inside the kernel. (Overview)
- Kernel synchronization primitives support protocols that prevent priority inversion, so a thread's priority is determined both by the service it performs and by which activities it is impeding by holding locks [Khanna 1992]. The P2 notes never mention priority inversion or priority inheritance; the P3L1 scheduling note later covers priority inversion and boosting the mutex owner's priority. (Overview)
- Asynchronous kernel work (asynchronous disk writes, servicing STREAMS queues, callouts) is done by kernel threads. This removes "diversions" in the idle loop and trap code, increases concurrency (other CPUs can do the work), and gives each asynchronous activity its own priority for scheduling. (Overview)
- "All LWPs have a kernel thread, but not all kernel threads have an LWP" (e.g., system threads, interrupt threads). The notes only describe kernel threads that back LWPs. (Overview, Figure 1)
- The user library [Stein 1992] can switch a user thread onto any of the process's LWPs. Two stated motivations for separating user threads from LWPs: the library can switch user threads quickly without entering the kernel, and a process can have thousands of user threads without overwhelming kernel resources. (Overview)

### Figure 1: Multi-thread architecture examples
- Figure 1 shows three example processes (proc 1, proc 2, proc 3) with differing combinations of user threads, LWPs, and CPUs across User/Kernel/Hardware layers, using separate symbols for thread, LWP, and CPU; each LWP sits on its own kernel thread. (Figure 1)

## Data Structures
- Traditional UNIX: all kernel per-process data lived in the user and proc structures, and processor data in global variables. Per-process data was split into non-swappable data in proc and swappable data in user; the process's swappable kernel stack was allocated with the user structure in the user area, usually one or two pages long. (Data Structures)
- The restructured kernel splits data three ways: per-LWP-and-kernel-thread, per-process, and per-processor. (Data Structures)
- The proc structure keeps a "vestigial" user structure, now much smaller than a page and no longer practical to swap. (Data Structures)
- The LWP structure holds the process control block (pcb) for user-level processor registers, plus system call arguments, signal masks, resource usage, and profiling pointers, and pointers to its kernel thread and its proc. The notes omit profiling pointers, the pcb term, and the back-pointers. (Data Structures)
- The LWP's kernel stack is allocated together with the LWP structure inside a swappable area. (Data Structures, Figure 2)
- Kernel thread structure fields: kernel registers, scheduling class, dispatch queue links, and pointers to the stack and the associated LWP, process, and CPU structures. The notes say only "scheduling info" for the scheduling class and dispatch queue links. (Data Structures)
- Because the thread structure is not swapped, it also holds some LWP data needed even while the LWP structure is swapped out. (Data Structures)
- Thread structures are linked on a per-process list of threads and also on a system-wide list of all existing threads. (Data Structures, Figure 3) [Now stated in the note's Eykholt callout, so not beyond the notes.]
- The cpu structure holds pointers to the currently executing thread and to that CPU's idle thread, plus current dispatching and interrupt-handling information. It has an architecture-dependent substructure; the main body is meant to fit most MP architectures. (Data Structures) [The current thread, idle thread, and dispatching/interrupt-handling contents are now stated in the note's Eykholt callout; the architecture-dependent substructure is not.]
- On SPARC the dedicated register is global register %g7, pointing to the current thread structure; the C macro `curthread` gives single-instruction access to its fields. Current LWP, proc, and CPU are reached through pointers in the thread structure. Additional global registers may later be dedicated to other hot structures. (Data Structures)

### Figure 2: MT Data Structures for a Process
- Figure 2 shows one proc (with its VM address space) owning several kernel threads; each thread has user-side LWP data and points to a swappable region containing that LWP's lwp structure and kernel stack. (Figure 2)

## Kernel Thread Scheduling
- SunOS 5.0 has several scheduling classes. A class determines relative priority within the class and converts it to a global priority. Supported classes: system, timesharing, and real-time (fixed-priority). (Kernel Thread Scheduling)
- With multithreading, scheduling classes and the dispatcher operate on threads instead of processes. (Kernel Thread Scheduling)
- The dispatcher runs the thread with the greatest global priority; threads of equal priority are dispatched round-robin. (Kernel Thread Scheduling)
- The kernel was made preemptible to better support the real-time class and interrupt threads. Preemption is disabled only in a small number of bounded code sections, so a runnable thread runs as soon as practical after its priority becomes high enough. (Kernel Thread Scheduling)
- Example: when running thread A releases a lock on which higher-priority thread B sleeps, A immediately puts itself back on the run queue and lets the CPU run B. (Kernel Thread Scheduling)
- On an MP, if A outranks B but B outranks the current thread on another CPU, that CPU is directed to preempt its current thread and choose the best thread. The notes describe only the user-library analogue (signalling another KLT). (Kernel Thread Scheduling)
- User code running on a kernel thread of sufficient priority (e.g., real-time) executes even while lower-priority kernel threads wait for CPU. Details in [Khanna 1992]. (Kernel Thread Scheduling)

## System Threads
- System threads can be created for short- or long-term kernel activities, are scheduled like any other thread, and usually belong to the system scheduling class. (System Threads)
- System threads need no LWP, so their thread structure and stack are allocated together in a non-swappable area. (System Threads, Figure 3)
- A new segment driver, `seg_kp`, handles stack allocation: kernel virtual memory that can be paged or swapped out, with "red zones" against stack overflow. System threads use it for stack and thread structure in a non-swappable region; LWPs use it for the LWP structure and kernel stack in a swappable region. The notes mention red zones only for user-level thread stacks. (System Threads)

### Figure 3: System Threads
- Figure 3 shows system thread structures chained on the `allthreads` list, each with its stack allocated adjacent to it. (Figure 3)


## Synchronization Architecture
- Internally the kernel implements the same synchronization objects the user-level libraries offer to applications [Powell 1991]: mutexes, condition variables, counting semaphores, and multiple-readers/single-writer (readers/writer) locks. The P2 notes cover mutexes, CVs, and the readers/writer problem built from them; semaphores and reader/writer locks as primitives come only in P3L4. (Synchronization Architecture)
- An object's behavior is specified when it is initialized (type plus optional type-specific argument). Operations take a pointer to the object and may behave differently depending on that type. (Synchronization Architecture)
- Most object types can collect statistics such as blocking counts or times. A patchable kernel variable can make the default types statistics-gathering, so stats can be enabled per object or kernel-wide. (Synchronization Architecture)
- How progress is impeded (sleep, spin, or other) is a function of initialization; by default, primitives that can logically block may sleep. (Synchronization Architecture)
- Priority inheritance [Khanna 1992] is supported only for primitives that are strictly bracketing (the locker must be the unlocker) with a single determinable owner: mutexes and rw locks held for writing. Semaphores, CVs, and read-held rw locks do not get it. (Synchronization Architecture)
- For long or indeterminate waits there are signal-interruptible variants (`cv_wait_sig()`, `sema_p_sig()`). On a pending signal the primitive returns a value saying it was interrupted, and the caller must release resources and return. There is no non-local jump to the head of the system call as with the traditional `sleep` routine. (Synchronization Architecture)

### Figure 4: Kernel Thread Synchronization Interfaces
- Mutex API: `mutex_init(kmutex_t *lp, char *name, kmutex_type_t type, void *arg)`, `mutex_destroy`, `mutex_enter`, `mutex_exit`, `int mutex_tryenter`. (Figure 4)
- CV API: `cv_wait(cp, lp)`, `int cv_wait_sig(cp, lp)`, `int cv_timedwait(cvp, lp, long tim)` (timed wait), `cv_signal`, `cv_broadcast`. (Figure 4)
- Readers/writer API: `rw_init(krwlock_t *lp, char *name, krw_type_t type, void *arg)`, `rw_destroy`, `rw_enter(lp, krw_t rw)` (mode argument selects reader or writer), `int rw_tryenter`, `rw_exit`, `rw_downgrade` (writer to reader), `int rw_tryupgrade` (reader to writer, may fail). (Figure 4)
- Counting semaphore API: `sema_init(ksema_t *sp, unsigned int val, char *name, ksema_type_t type, void *arg)`, `sema_destroy`, `sema_p`, `int sema_p_sig`, `int sema_tryp`, `sema_v`. (Figure 4)
- All init calls take a name string plus a type and type-specific argument; try variants and signal variants return int status. (Figure 4)
- Kernel primitive types use different names from the user ones (`kmutex_t`, `kcondvar_t`, `krwlock_t`, `ksema_t`) so applications that read internal kernel data structures do not confuse them. (Figure 4, footnote 1)

## Mutual Exclusion Lock Implementation
- Mutexes prevent races on shared data and are by far the most heavily used primitive. (Mutex Implementation)
- Mutexes are meant to be held for short intervals; e.g., a critical system mutex should not be held while waiting for disk I/O. (Mutex Implementation)
- Mutexes are not recursive (the owner cannot call `mutex_enter()` again on the same lock), and the thread that holds a mutex must be the one to release it. These rules are enforced to promote good practice and avoid deadlocks. (Mutex Implementation)
- When `mutex_enter` finds the lock set, the blocking action depends on the type passed to `mutex_init` and stored in the mutex. (Mutex Implementation)
- The default policy is called adaptive (type `MUTEX_DEFAULT`): it spins by polling the owner's status while the owner (recorded at acquisition) remains running on a processor, and sleeps once the owner stops running. This gives fast response and low overhead for simple contention. (Mutex Implementation) [The policy is now stated in the note's Eykholt callout; the fast-response, low-overhead rationale is not.]
- To avoid taking a lock while inspecting the owner's status, the spinner determines it indirectly: it spins while the current-thread pointer of any CPU points to the owner. (Mutex Implementation, footnote 2) [Now stated in the note's Eykholt callout, so not beyond the notes.]
- On uniprocessors adaptive mutexes always sleep, since the owner cannot be running. (Mutex Implementation, footnote 3) [Now stated in the note's Eykholt callout, so not beyond the notes.]
- `MUTEX_SPIN` takes as its argument the interrupt level to disable while the mutex is held. It is rarely used because adaptive mutexes are generally more efficient. (Mutex Implementation)
- Device drivers must use `MUTEX_DRIVER`, whose argument is a Sun-DDI-defined opaque value (currently essentially an interrupt priority). It selects spin if that priority is above the "thread level", adaptive otherwise. (Mutex Implementation)
- Fast-path trick: non-adaptive mutexes use a separate primitive lock field, and the field the adaptive type uses is kept permanently locked. `mutex_enter()` therefore always tries the adaptive lock first and considers other types only if that fails. (Mutex Implementation)

## Turnstiles vs Queues in Synchronization Objects
- Every synchronization object needs a way to find the threads suspended on it. Because many system structures embed synchronization objects, their storage cost must stay small, so the queue header is not stored in the object. (Turnstiles)
- Instead, two bytes in the object locate a turnstile structure containing the sleep queue header and the priority inheritance information [Khanna 1992]. The notes say nothing about turnstiles. (Turnstiles)
- Turnstiles are preallocated so that there are always more turnstiles than active threads. (Turnstiles)
- Rejected alternative: choose a sleep queue from an array by hashing the object's address, essentially what traditional `sleep()` did. Turnstiles were preferred for more predictable real-time behavior, since a turnstile is never shared with other locks, whereas hashed sleep queues sometimes are. (Turnstiles)


## Interrupts as Threads
- Other MP kernels (Ultrix [Hamilton 1988], multithreaded SVR4 [Peacock 1992]) have several synchronization primitives with the same semantics (e.g., mutual exclusion) that explicitly either sleep or spin. (Interrupts as Threads)
- With spin mutexes shared with interrupt handlers, the interrupt priority level must be raised before acquiring and lowered after releasing, high enough to keep out any handler that uses the object; otherwise deadlock. The notes describe this as masking a signal/interrupt, not raising the interrupt priority level. (Interrupts as Threads)
- Drawback 1: raising and lowering interrupt priority can be expensive, especially on architectures with external interrupt controllers, and mutexes are heavily used. (Interrupts as Threads)
- Drawback 2: in a modular kernel, subsystems are interdependent, and requests from interrupt handlers (e.g., mapping kernel memory, memory allocation) can touch many subsystems. So many subsystems' mutexes must protect themselves at relatively high priority, which keeps interrupt priority high for long periods and imposes the raise/lower cost on every acquire/release. (Interrupts as Threads)
- Drawback 3: interrupt handlers must live in a constrained environment that avoids any kernel function that might sleep, even briefly. (Interrupts as Threads)
- SunOS 5.0 treats most interrupts (not all) as asynchronously created and dispatched high-priority threads, which may sleep and use the standard primitives. The lecture presents it as universal (the note's Paper callout adds the exception) and does not mention their priority. (Interrupts as Threads) [The "most, not all" part is now stated in the note's Eykholt callout; the high priority and asynchronous creation and dispatch are not.]
- Putting threads to sleep is done in software and must be protected from interrupts if interrupts are to sleep or wake other threads. The kernel uses a primitive spin lock protected by raised priority, one of the few bounded sections where interrupts are locked out. Traditional UNIX ([Leffler 1989], [Bach 1986]) also protects the dispatcher by locking out interrupts, usually all of them. (Interrupts as Threads)
- The modifiable "thread level": interrupts above it are not handled as threads and are treated like non-portable "firmware" (e.g., simulating DMA via programmed I/O). These handlers can synchronize only via spin mutexes and software interrupts. (Interrupts as Threads) [The threshold and the spin-mutex/software-interrupt restriction are now stated in the note's Eykholt callout; the "firmware" characterization and the DMA example are not.]
- If thread level is set to the maximum priority, all interrupts are locked out during dispatching. Where the firmware cannot tolerate even this short dispatcher lockout, thread level can be lowered, typically to the interrupt level of the scheduling clock. (Interrupts as Threads) [Now stated in the note's Eykholt callout, so not beyond the notes.]

## Implementing Interrupts as Threads
- Traditional UNIX (and earlier SunOS): the interrupted process is held captive (pinned) until the interrupt returns; handlers run on the interrupted process's kernel stack or a separate interrupt stack; the handler must finish and get off the stack before anything else runs on that processor; the kernel synchronizes with handlers by blocking interrupts in critical sections. (Implementing Interrupts as Threads) [Running on the interrupted process's kernel stack or a separate interrupt stack as the traditional scheme is now stated in the note's Eykholt callout; the rest is not.]
- SunOS 5.0 preallocates interrupt threads that are already partly initialized, because a full thread creation per interrupt is impractical. On an interrupt it does the minimum work to move onto the interrupt thread's stack and make it the current thread. (Implementing Interrupts as Threads) [Now stated in the note's Eykholt callout and the note body (Interrupts as Threads, pre-created interrupt threads), so not beyond the notes; "partly" rather than fully initialized is the Pre-initialization item under Notes vs paper discrepancies.]
- At that point the two threads are not fully separated: the interrupt thread is not yet a full-fledged thread (cannot be descheduled), and the interrupted thread is pinned until the interrupt thread returns or blocks and cannot proceed on another CPU. On return, the interrupted thread's state is restored. (Implementing Interrupts as Threads) [The pinning until the interrupt thread returns or blocks is now stated in the note's Eykholt callout; the rest is not.]
- Interrupts may nest: an interrupt thread can itself be interrupted and pinned by another interrupt thread. (Implementing Interrupts as Threads)
- If the interrupt thread blocks on a synchronization variable (mutex or CV), it saves state ("passivates") to become a full thread runnable on any CPU, then control returns to the pinned thread. Most of the full-thread cost is paid only when it must block due to contention. (Implementing Interrupts as Threads) [That it becomes a full thread only if it blocks is now stated in the note's Eykholt callout; the "passivation" term, running on any CPU, and the return to the pinned thread are not.]
- On SPARC the passivation cost includes flushing the entire register file; this is done only if the handler sleeps, not during uncontended handling. (Implementing Interrupts as Threads, footnote 4)
- While an interrupt thread is in progress, its level and all lower-priority interrupts are blocked by the normal priority mechanism. If it blocks, they stay disabled, because the handler may not be reentrant at the block point or may still be doing high-priority work that lower-priority work must not interrupt. (Implementing Interrupts as Threads)
- A blocked interrupt thread stays bound to the CPU it started on, as an implementation convenience and to guarantee an interrupt thread is always available when an interrupt occurs (the authors note this may change). (Implementing Interrupts as Threads)
- A flag in the cpu structure records that an interrupt at that level has blocked, and the minimum interrupt level is noted. Whenever the interrupt level changes, the CPU's base interrupt level is checked, and the actual priority level is never allowed below it. (Implementing Interrupts as Threads)
- `release_interrupt()` lets an interrupt thread continue as a normal high-priority thread: it saves the pinned thread's state and clears the blocked indication, letting the CPU lower its interrupt priority level. (Implementing Interrupts as Threads)
- Rejected alternative [Barnett 1992]: bounded first-level handlers capture device state and wake a waiting second-level interrupt thread for the rest. Disadvantages: device drivers must be restructured, and a full context switch to the second-level thread is always required. SunOS gives full thread behavior with no driver restructuring and little extra cost when uncontended. (Implementing Interrupts as Threads) [Now stated in the note's Eykholt callout, except the [Barnett 1992] attribution, so not beyond the notes.]

## Interrupt Thread Cost
- About 40 extra SPARC instructions per interrupt taken versus about 12 saved on the mutex enter/exit path; the net gain holds only as long as interrupts do not block too frequently. The notes give the numbers but not this caveat. (Interrupt Thread Cost)
- Conversion of an interrupt into a "real" thread is done only when there is lock contention. (Interrupt Thread Cost) [Now stated in the note's Eykholt callout, so not beyond the notes.]
- Memory cost: one interrupt thread is preallocated per potentially active interrupt level below thread level, per CPU, plus one system-wide interrupt thread for the clock. SPARC has nine interrupt levels that can use threads. Each thread needs a stack and data structure, roughly 8 KB, so memory cost can be high. (Interrupt Thread Cost, footnote 5)
- Since all levels are unlikely to be active at once, a smaller per-CPU pool could be used, blocking all further below-thread-level interrupts when the pool is empty, capping simultaneous active interrupts. (Interrupt Thread Cost)

## Clock Interrupt
- The clock interrupt fires 100 times per second on Sun SPARC. (Clock Interrupt, footnote 6)
- There is a single clock interrupt thread for the whole system, not one per CPU, and the clock handler invokes it only if it is not already active. (Clock Interrupt)
- The clock thread can be delayed more than one tick by blocking on a mutex or by higher-level interrupts. If a tick arrives while it is active, the interrupt is cleared and a counter incremented; before returning, the clock thread checks the counter, decrements it, and repeats clock processing. (Clock Interrupt)
- This is rare in practice, usually caused by heavy higher-level interrupt activity, and can also happen while debugging. (Clock Interrupt)


## Kernel Locking Strategy
- The kernel uses data-based locking almost exclusively: each mutex and rw lock protects a set of shared data, as opposed to protecting routines (monitors). Every piece of shared data is protected by some synchronization object. (Kernel Locking Strategy)
- Locking in virtual memory, file system, STREAMS, and device drivers was covered in [Kleiman 1992]; this paper elaborates only on device drivers because they are closely tied to interrupt threads. (Kernel Locking Strategy)

## Non-MT Driver Support
- MT-unsafe drivers are those not modified to protect themselves against concurrency (no locking of their own). (Non-MT Driver Support)
- As interim support, wrappers acquire a single global mutex, `unsafe_driver`, so only one MT-unsafe driver is active at a time. (Non-MT Driver Support)
- Drivers can be entered through explicit entry points, interrupts, and call-backs; each entry must acquire `unsafe_driver` if the driver is unsafe. Example: when an MT-unsafe driver uses `timeout()`, the callout structure is marked so `unsafe_driver` is held during the later function call. (Non-MT Driver Support)
- MT-unsafe drivers may still use old `sleep()`/`wakeup()`. `sleep()` releases `unsafe_driver` after the thread is asleep and reacquires it before returning. (Non-MT Driver Support)
- The `longjmp()` feature of `sleep()` is kept: if a thread sleeping with a dispatch value greater than PZERO is signalled, it longjmps to a `setjmp()` done in the unsafe-driver entry wrapper, which returns EINTR to the driver's caller. (Non-MT Driver Support)
- `sleep()` checks that its caller is an MT-unsafe driver and panics otherwise; it is unsafe to use from a driver that does its own locking. (Non-MT Driver Support)
- Simple locking is easy to add, so almost all drivers have some of their own. Those are called MT-safe regardless of granularity; "MT-hot" is used by some developers for drivers with fine-grained locking. (Non-MT Driver Support)

### Figure 5: Unsafe Driver Wrapper
- Figure 5 shows calls and interrupts entering the MT-unsafe driver through a locking wrapper, with a signal path that longjmps from the driver back to the wrapper. (Figure 5)

## Lock Hierarchy Violation Detection
- Instead of defining a system lock hierarchy a priori, the team built `locknest`, a lint-like static analysis tool that reads C source, builds call graphs, and reports locking cycles (lock-ordering violations). (Lock Hierarchy Violation Detection)
- They credit it with helping early implementation debugging and probably reducing time spent debugging deadlocks. A similar tool (Sema) is described in [Korty 1989]. (Lock Hierarchy Violation Detection)

## Deadlock Detection
- Side benefit of priority inheritance: deadlocks from hierarchy violations are usually detected at run time too. (Deadlock Detection)
- It works well for mutexes and write-held rw locks, but cannot always find deadlocks involving read-held rw locks because there is no complete list of reader threads. Condition-variable deadlocks are not detected. (Deadlock Detection)

## SVR4/MP DKI Locking Primitives
- While SunOS driver interfaces were being built, UNIX International and USL were defining the SVR4 Multiprocessor DDI/DKI (Device Driver Interface / Driver-Kernel Interface) with a different set of locking primitives based on the traditional interrupt-blocking model. (SVR4/MP DKI)
- SunOS 5.0 implements those interfaces, to the extent then defined, on top of its own locking primitives and ignores any spin semantics, so such drivers port easily. Native SunOS drivers normally use SunOS primitives. (SVR4/MP DKI)

## Implementation Technology
- The paper describes development techniques that made the implementation easier to get working; kernel time slicing is the one detailed. (Implementation Technology)

## Kernel Time Slicing
- Because the kernel is fully preemptible, code was added to the clock interrupt handler to preempt whatever thread it interrupted, making kernel threads time-slice. This gives nearly arbitrary code interleavings even on a uniprocessor. (Kernel Time Slicing)
- Raising the clock interrupt rate made this more effective at exposing windows where data was unprotected. It found locking bugs on uniprocessor hardware before MP hardware existed, and remained useful afterward because uniprocessors far outnumbered multiprocessors. (Kernel Time Slicing)
- It is intended only as a debugging feature, because it has some, though slight, performance cost. (Kernel Time Slicing)

## Summary
- SunOS 5.0 is a multithreaded, symmetric multiprocessor version of the SVR4 kernel. Primary features: fully preemptible real-time kernel; high concurrency on SMPs; user thread support; interrupts handled as independent threads; adaptive mutexes. (Summary)
- The kernel and user-level thread models are almost identical: scheduling kernel threads onto CPUs is analogous to the library scheduling user threads onto LWPs. (Summary)
- Threads structuring the kernel has "mostly good effects" but they can be overused. Costs: stacks are large and must be on separate pages if stack-overrun protection is wanted; context switching is still expensive. (Summary)
- Some things are still better implemented with callouts and other "zero-weight" processes, though threads are a good structuring paradigm for the kernel. (Summary)

## References
- Published at Summer '92 USENIX, June 8-12, 1992, San Antonio, TX; authors from SunSoft, Inc. (header)
- [Khanna 1992] "Realtime Scheduling in SunOS 5.0" (USENIX Winter 1992) describes the real-time features, priority inheritance, and turnstiles referred to throughout. (References)
- [Kleiman 1992] "Symmetric Multiprocessing in Solaris 2.0" (COMPCON Spring 1992) covers VM, FS, STREAMS, and driver locking. (References)
- [Powell 1991] "SunOS Multi-thread Architecture" (USENIX Winter 1991) describes the user-level MT architecture; [Stein 1992] "Implementing Lightweight Threads" (USENIX Summer 1992) describes the user-level threads package. (References)
- [Barnett 1992] "Kernel Threads and their Performance Benefits" (Lynx Real-Time Systems) is the source of the rejected two-level interrupt design. (References)
- [Korty 1989] "Sema: a Lint-Like Tool for Analyzing Semaphore Usage in a Multithreaded Unix Kernel" (USENIX Winter 1989) does static lock hierarchy analysis. (References)
- [Hamilton 1988] experimental symmetric MP Ultrix kernel; [Peacock 1992] experiences multithreading System V Release 4 (SEDMS III); [Leffler 1989] 4.3BSD design; [Bach 1986] Design of the UNIX OS. (References)

## Author Information
- Ten SunSoft authors: Eykholt (technical leader, OS-Multithreading group; previously Amdahl UTS multiprocessing and the Amdahl 580 CPU logic), Kleiman (architect of multithreading in SunOS; co-developer of NFS, Vnodes, and the original SunOS SPARC port), Barton (previously Zilog, Parallel Computers, CounterPoint, Telestream), Faulkner (Physics PhD, ex-Bell Labs, UNIX kernel work since 1976, compiler and debugger development, a principal in developing /proc for SVR4), Shivalingiah (OS-Virtual Memory group), Smith (OS-Multithreading group; previously Amdahl Design Automation), Stein (developer of the SunOS Multi-thread Architecture), Voll (OS-Multithreading group; previously Amdahl and Cygnet Systems), Weeks (at Sun since 1986; previously Xerox), and Williams (OS-Multithreading group; previously American Information Systems, ONYX, Tri-Comp, Hughes Aircraft Radar Systems). (Author Information)
- Titles, education, and tenure: Eykholt is a Senior Staff Engineer (MSEE 1978, BSEE 1977, Purdue); Kleiman is a Distinguished Engineer in SunSoft's Operating Systems Technology Department (M.S. EE Stanford 1978, B.S. EECS MIT 1977; UNIX and workstation architecture since 1977, first at Bell Labs, then Sun); Barton (BA CIS, UC Santa Cruz 1982; four years at Sun); Faulkner is a Senior Staff Engineer (B.S. Physics N. C. State 1963, Ph.D. Physics Princeton 1967, then Bell Labs); Shivalingiah is a Staff Engineer (M.S. CS UT Arlington 1983, B.S. Electronics UVCE India 1981; three years at Sun); Smith (B.S. CS UC Santa Barbara 1986); Stein (BS CS Wisconsin 1981); Voll (B.S. UC Santa Barbara 1981; "routinely destroys his home directory"); Weeks (B.A. CS UC Berkeley 1984); Williams is a Staff Engineer (S.B. EECS MIT 1980; over six years at Sun). Contact e-mail addresses and phone numbers are given; Eykholt's address is SunSoft, M/S MTV5-40, 2550 Garcia Avenue, Mountain View, CA 94043. (Author Information)

## Notes vs paper discrepancies
Each item was checked against the paper, the lecture as reconstructed from independent student note sets (no lecture transcript was retrievable), and third-party references; sources are listed under "Discrepancy sources". Verdicts: PAPER CONFIRMED, NOTES WRONG (the notes depart from the paper and the lecture does not support them); LECTURE FRAMING (the notes reproduce the lecture and the paper differs); NOT A REAL DISCREPANCY.
- Adaptive mutex criterion: the notes say the mutex also tracks critical-section length to choose spin vs block. In the paper the adaptive policy depends only on whether the owner is running on a CPU. (Mutex Implementation) [Now stated in the note's Eykholt callout.]
  - Verdict: LECTURE FRAMING, the lecture says to spin for short and block for long critical sections, and third parties (illumos mutex.c, McDougall & Mauro) side with the paper: the only runtime test is whether the owner is running, and short hold times are a design assumption.
- Where an interrupt runs: the notes say that "if the handler routine contains no locks, it cannot block, so we can safely run it on the stack of the interrupted thread" and attribute this rule to the paper, which does not state it. In the paper the handler moves onto a preallocated interrupt thread's stack immediately. Running on the interrupted process's stack is the traditional scheme being replaced; the interrupted thread is pinned, not borrowed. (Implementing Interrupts as Threads) [Now stated in the note's Eykholt callout.]
  - Verdict: LECTURE FRAMING, the lecture gives the same "no locks, cannot block, run on the interrupted thread's stack" rule, and third parties (illumos intr.c, downey.io) side with the paper: the handler always switches to the interrupt thread's own stack.
- Top/bottom half: the notes describe a top half in the interrupted context followed by a bottom half in a created thread. The paper rejects that two-level design (Barnett) because it needs driver restructuring and always costs a context switch. SunOS runs the whole handler in the interrupt thread and promotes it to a full thread only if it blocks. (Implementing Interrupts as Threads) [Now stated in the note's Eykholt callout.]
  - Verdict: LECTURE FRAMING, the lecture presents top/bottom halves as the common technique (as in Linux), and third parties (illumos, Oracle Writing Device Drivers) side with the paper for thread-level interrupts, using a two-level split only for high-level interrupts.
- What the 12 instructions save: the original notes said a signal no longer needs to be disabled around mutex lock/unlock (the current note says the interrupt mask). The paper states only the figure, but its context (the spin-mutex drawbacks in Interrupts as Threads) is the cost of raising and lowering the interrupt priority level around each mutex. Interrupts, not signals. (Interrupt Thread Cost, Interrupts as Threads)
  - Verdict: PAPER CONFIRMED, NOTES WRONG, the lecture says the interrupt mask no longer changes on each mutex lock/unlock, and third parties (Kleiman & Eykholt 1995, downey.io) also say interrupt masking, so "signal" was the notes' own error, since corrected.
- The 40 instructions: the notes attribute them to "performing checks and potentially creating a new thread". Interrupt threads are preallocated, so none is created per interrupt; the 40 instructions are the overhead of taking an interrupt, and promotion to a full thread happens only on contention. (Interrupt Thread Cost) [Now stated in the note's Eykholt callout.]
  - Verdict: LECTURE FRAMING, the lecture attributes the 40 instructions to checks and possibly creating a thread, and third parties (illumos intr.c) side with the paper: preallocated threads are taken from a free list and nothing is created per interrupt.
- CPU structure: the notes list a "list of kernel level threads". The paper lists the current thread, that CPU's idle thread, and dispatching/interrupt info; the per-process and system-wide thread lists hang off proc and thread structures. (Data Structures) [Now stated in the note's Eykholt callout.]
  - Verdict: LECTURE FRAMING, the lecture lists "the other kernel-level threads" in the CPU structure, and third parties (illumos cpuvar.h and thread.h) mostly side with the paper: per-CPU run queues and interrupt-thread pools exist, but not a general thread list.
- Swappable stack: the notes say each kernel thread structure "points to the lightweight process and the stack, which is swappable", unqualified. Only LWP-backed threads have a swappable kernel stack (allocated with the LWP); system threads' stacks and thread structures are non-swappable. (Data Structures, System Threads)
  - Verdict: NOT A REAL DISCREPANCY, the lecture describes Figure 2 (a user process) the same way, and illumos and Oracle's Solaris docs confirm the LWP and its stack are swappable for LWP-backed threads; only system threads are left out.
- LWP pointer cardinality: the original notes said the kernel thread holds "pointers to associated LWPs" (plural); the current note says "the associated LWP" (singular). In the paper a kernel thread has at most one associated LWP, and system and interrupt threads have none. (Data Structures, Overview)
  - Verdict: PAPER CONFIRMED, NOTES WRONG, the lecture says "the associated LWP" (singular), and third parties (illumos kthread_t's single t_lwp, downey.io) agree, so the plural was the notes' wording, since corrected.
- Pre-initialization: the notes say the kernel "pre-creates and pre-initializes thread structures for the interrupt routines". The paper says interrupt threads are only partly initialized; the rest of the state is saved (passivation) only if the thread blocks. (Implementing Interrupts as Threads)
  - Verdict: NOT A REAL DISCREPANCY, the lecture also says pre-create and pre-initialize, and illumos and McDougall & Mauro show preallocation removing creation from the fast path, so "pre-initialized" against "partly initialized" is a difference of degree.
- Universality: the notes imply all interrupts become threads. In the paper only interrupts at or below the "thread level" do; higher ones remain firmware-style handlers limited to spin mutexes and software interrupts. (Interrupts as Threads) [Now stated in the note's Eykholt callout.]
  - Verdict: PAPER CONFIRMED, NOTES WRONG (by omission), the lecture names the paper's priority-level threshold but declares it out of scope, and third parties (McDougall & Mauro, illumos, Oracle Writing Device Drivers) confirm high-level interrupts are not threads.

## Covered in the notes
- Kernel vs user-level threads and 1:1, M:1, M:N mappings; Solaris supports M:N and 1:1, with user threads optionally bound to an LWP.
- LWPs as kernel-visible per-thread state and the library's virtual CPUs.
- proc contents: kernel thread list, address space, user credentials, signal handlers.
- LWP contents: user registers, system call arguments, resource usage, signal masks; LWP data is swappable.
- Kernel thread structure is non-swappable and holds kernel registers, stack pointer, scheduling info, LWP/CPU pointers.
- cpu structure holds the current thread and dispatching/interrupt info; SPARC dedicates a register to the current thread.
- Thread switches within a process avoid changing address mappings (threads-and-concurrency).
- Threads of a process share the address space and other resources such as files (threads-and-concurrency).
- CV wait/signal/broadcast and the readers/writer problem (threads-and-concurrency).
- Adaptive mutex basics: spin if the owner runs on another CPU, else block; MP only; owner recorded.
- Interrupts as threads to avoid handler/mutex deadlock; a blocked interrupt thread waits like any other thread; preallocated interrupt threads.
- 40-instruction interrupt overhead vs 12-instruction per-mutex saving; net win because mutex operations are far more frequent (optimize the common case).


## Discrepancy sources
- <https://www.usenix.org/legacy/publications/library/proceedings/sa92/eykholt.pdf> (paper; mirror <http://static.usenix.org/publications/library/proceedings/sa92/eykholt.pdf>)
- <https://github.com/awpala/my-omscs-notes/blob/main/cs-6200/05-P2L4-thread-design-considerations.md> (raw: <https://raw.githubusercontent.com/awpala/my-omscs-notes/main/cs-6200/05-P2L4-thread-design-considerations.md>)
- <https://github.com/tewidis/GIOS> (markdown/thread_design_considerations.md)
- <https://github.com/Guochiuan/CS6200-notes>
- <https://github.com/bayernscience/OMSCS-CS6200>
- <https://downey.io/notes/omscs/cs6200/multithreading-in-solaris/>
- <https://www.omscs-notes.com/operating-systems/thread-design-considerations/> (the notes under review)
- <https://dokumen.pub/graduate-introduction-to-operating-systems-cs-6200-midterm-exam-review-notes-fallnbsped.html> (Kudrayvtsev midterm review; checked)
- <https://raw.githubusercontent.com/illumos/illumos-gate/master/usr/src/uts/common/os/mutex.c>
- <https://raw.githubusercontent.com/illumos/illumos-gate/master/usr/src/uts/i86pc/os/intr.c>
- <https://raw.githubusercontent.com/illumos/illumos-gate/master/usr/src/uts/common/sys/thread.h>
- <https://raw.githubusercontent.com/illumos/illumos-gate/master/usr/src/uts/common/sys/cpuvar.h>
- <https://www.filibeto.org/aduritz/truetrue/solaris10/si/solaris_internals_2001.pdf> (McDougall & Mauro, Solaris Internals tutorial, USENIX 2001)
- <https://api.openalex.org/works/W2111763551> and <https://doi.org/10.1145/202213.202217> (Kleiman & Eykholt, Interrupts as Threads, 1995; abstract only)
- <https://docs.oracle.com/cd/E19253-01/816-4854/interrupt-15678/index.html> (Oracle, Writing Device Drivers, ch. 8)
- <https://docs.oracle.com/cd/E23824_01/html/821-1451/spconcepts-30492.html> (Oracle Solaris Administration: Common Tasks)
- <https://en.wikipedia.org/wiki/Interrupt_handler>
- Not accessible: <https://www.coursehero.com/file/38454639/P2L4-ThreadDesignConsiderationsdocx/>, <https://quizlet.com/324419686/p2l4-thread-design-considerations-flash-cards/>
