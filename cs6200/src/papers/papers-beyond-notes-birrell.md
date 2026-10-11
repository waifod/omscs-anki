---
id: operating-systems-papers-beyond-notes-birrell
title: "Birrell, An Introduction to Programming with Threads: Beyond the Notes"
course: operating-systems
lecture: papers-beyond-notes-birrell
---

# Birrell: everything not in the notes

Everything in the paper that the original lecture notes do not state, plus places where the paper contradicts them; validated against the paper text. The reference point is the original lecture notes: the notes now carry `> **Paper (...):**` callouts for the lecture-framing discrepancies listed under "Notes vs paper discrepancies", so some gaps below are now annotated in the notes. Paper: <https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-birrell-paper.pdf>.

Page numbers are the paper's printed page numbers (SRC Research Report 35, January 6, 1989).

## Front matter (abstract, contents)
- The paper is SRC Research Report 35 from Digital Equipment Corporation's Systems Research Center (Palo Alto), dated January 6, 1989, by Andrew D. Birrell. (cover)
- Abstract: a threads facility gives a program multiple simultaneous points of execution that synchronize through shared memory; the paper describes each primitive and then gives a tutorial per primitive with advice, warnings about what goes wrong, and hints for avoiding pitfalls. It is aimed at experienced programmers wanting practical expertise. (abstract)
- Classification: CR categories D.1.4 (Concurrent Programming), D.3.3 (Concurrent programming structures), D.4.1 (Process Management); general terms Design, Languages, Performance; additional key words Threads, Concurrency, Multi-processing, Synchronization. (abstract)
- Copyright Digital Equipment Corporation 1989: copying for non-profit educational and research purposes is permitted without fee if copies acknowledge SRC, the authors and contributors, and the copyright notice; commercial copying requires a paid license. (front matter)
- Structure of the paper: one tutorial section per primitive (Mutex, Condition variable, Fork, Alert), then additional techniques, building programs, and an appendix comparing other thread designs. (contents)
- The contents page numbers do not match the body's printed page numbers after the Mutex section: contents gives Condition variable 14, Fork 22, Alert 27, Additional techniques 28, Building 30, Concluding remarks 31, References 31, Appendix 33, while the body places them at 13, 21, 25, 26, 28, 29, 29, 31. This file uses the body numbering. (contents)

## Introduction
- Many experimental operating systems and some commercial ones had recently added concurrency support; the most popular mechanism is multiple lightweight threads within a single address space, used from within a single program. (p.1)
- Concurrent programming has techniques and pitfalls absent from sequential programming; many techniques are obvious only with hindsight. (p.1)
- Deadlock is called "a pleasant sort of bug" because the program stops with all the evidence intact; other pitfalls take the form of insidious performance penalties. (p.1)
- Goal: give an experienced sequential programmer enough hints to build a substantial multi-threaded program that works correctly, efficiently, and with a minimum of surprises. (p.1)
- Definition: a thread is "a single sequential flow of control"; in a high-level language it is programmed with procedures whose calls follow the traditional stack discipline. Within one thread there is a single point of execution at any instant, and the programmer needs to learn nothing new to use a single thread. (p.1)
- With multiple threads the programmer can mostly view them as executing simultaneously, as if there were as many processors as threads, but must occasionally remember that they might not all actually run simultaneously. (p.1)
- The programmer decides when and where to create threads, or accepts such decisions made by implementers of library packages or runtime systems. (p.1)
- "Single address space" means the addressing hardware is configured so all threads can read and write the same memory locations; in a high-level language this corresponds to off-stack (global) variables being shared, while each thread runs on its own call stack with its own local variables. (p.1)
- Definition of "lightweight": thread creation, existence, destruction and synchronization are cheap enough that the programmer will use them for all concurrency needs. (p.1)
- Footnote 1: Birrell uses "process" only for a single flow of control associated one-to-one with an address space, since that seemed the most common usage. (p.1)
- The paper is self-described as selective (only the most important primitives; omits features such as per-thread context information), biased (built around the design choices of the Topaz system at SRC), and idiosyncratic (based on the author's ten years of personal experience). (p.1-2)
- Examples are in Modula-2+ (Algol/Pascal family) and are meant to illustrate concurrency points only; do not use the algorithms in real programs. (p.2)
- Threads are not a tool for automatic parallel decomposition (a compiler turning a sequential program into multiprocessor code); that is a different art the paper does not cover. (p.2)

## Why use concurrency?
- Four forces push toward concurrency: (1) multiprocessors; (2) driving slow devices (disks, networks, terminals, printers); (3) human users, who can do two or three things at once and expect the computer to as well; (4) distributed systems with shared network servers (file server, spooling print server). (p.2)
- The multiprocess alternative (separate address spaces) is expensive to set up and inter-address-space communication is often costly "even in the presence of shared segments." (p.2)
- Lightweight threads were observed to work well on systems with up to about 10 processors, not 1000. (p.2)
- Slow devices are programmed by treating every device request as sequential (it suspends only the invoking thread until completion) while other threads do useful work. (p.2)
- Window systems typically run each user-invoked action (e.g. a mouse click) in a separate thread, so multiple actions run in parallel; the window system itself probably also uses a thread to watch the mouse, the mouse being another slow device. (p.2)
- Servers use multiple threads to handle client requests in parallel instead of artificially serializing them or creating one server process per client "at great expense." (p.2)
- Concurrency can be added deliberately to reduce latency (defined as the elapsed time between calling a procedure and its return): work that does not affect the result is deferred to another thread. Example: return from a balanced-tree insert/delete before re-balancing and re-balance in a separate thread. (p.3)
- If the deferred-work thread runs at lower priority, the work happens when the system is less busy (e.g. waiting for user input). This is valuable even on a uniprocessor: the same total work, but better responsiveness. (p.3)

## The design of a thread facility
- Thread systems offer similar facilities with much diversity in detail; there are four major mechanisms: thread creation, mutual exclusion, waiting for events, and a way to get a thread out of an unwanted long-term wait. The notes cover only the first three. (p.3) [Partly stated in the note body (threads-and-concurrency.md, section Basic Thread Mechanisms): the note says Birrell also describes mechanisms for waking threads from a wait state; the four-mechanism list is not stated.]
- The paper is organized around the SRC thread facility, whose semantics were formally specified in [4] (Birrell, Guttag, Horning, Levin, SOSP 1987). (p.3)

## Thread creation
- SRC interface: `TYPE Thread; TYPE Forkee = PROCEDURE(REFANY): REFANY; PROCEDURE Fork(proc: Forkee; arg: REFANY): Thread; PROCEDURE Join(thread: Thread): REFANY;`. REFANY is a dynamically typed pointer to garbage-collected storage (footnote 2). (p.3)
- Fork starts the new thread executing asynchronously at an invocation of the procedure; when that procedure returns, the thread dies. (p.3)
- Example: `t := Fork(a, x); p := b(y); q := Join(t);` runs a(x) and b(y) in parallel and assigns a(x)'s result to q. (p.4)
- Join is not called much at SRC, and some thread facilities do not provide it at all: most forked threads are permanent daemon threads, have no results, or communicate results through some other synchronization arrangement. (p.4) [Now stated in the note's Birrell callouts (threads-and-concurrency.md, Thread Creation; threads-case-study-pthreads.md, PThread Creation), except the "have no results" reason.]
- If a thread's initial procedure has returned and nobody ever calls Join on it, the thread "quietly evaporates." (p.4) [Now stated in the note's Birrell callout (threads-case-study-pthreads.md, PThread Creation), so not beyond the notes.]

## Mutual exclusion
- The simplest form of thread interaction is shared memory, i.e. global variables in a high-level language. (p.4)
- SRC expresses mutual exclusion with the data type `Mutex` and the language construct `LOCK mutex DO ... statements ... END`, which locks, runs the statements, then unlocks. (p.4)
- A mutex has two states, locked and unlocked, and is initially unlocked. A thread inside the LOCK clause is said to "hold" the mutex; a second thread trying to lock it blocks, enqueued on the mutex, until it is unlocked. (p.4)
- Associating a set of variables with a mutex and accessing them only while holding it is the basis of monitors, first described by Tony Hoare [9]. (p.4)
- Example: `LOCK m DO newElement^.next := head; head := newElement; END;` protects pushing onto a linked list whose head is the global `head`. (p.4)
- With a global mutex, at most one thread is inside the LOCK clause at any instant. With a mutex stored in a record, the correct statement is "at most one thread executes with that mutex held": the mutex protects the other fields of the same record, so different records can be accessed in parallel. (p.4-5) [Partly stated in the note's Birrell callout (threads-case-study-pthreads.md, PThread Mutexes): per-record mutexes allow more parallelism; the "at most one thread executes with that mutex held" statement is not.]

## Condition variables
- A mutex can be viewed as a simple resource scheduling mechanism: the resource is the shared memory accessed in the LOCK clause and the policy is one thread at a time. Condition variables exist to express more complicated scheduling policies, by letting a thread block until some event happens. (p.5)
- SRC interface: `TYPE Condition; PROCEDURE Wait(m: Mutex; c: Condition); PROCEDURE Signal(c: Condition); PROCEDURE Broadcast(c: Condition);`. (p.5) [Now stated in the note body (threads-case-study-pthreads.md, section PThread Condition Variables), except the Modula-2+ declarations.]
- A monitor consists of some data, a mutex, and zero or more condition variables; a given condition variable is always used with the same mutex and its data. (p.5)
- Signal does nothing unless some thread is blocked on the condition variable (a signal with no waiter is not remembered); if there are waiters it awakens at least one, but possibly more than one. (p.5) [Partly stated in the note's Birrell callout (threads-and-concurrency.md, Condition Variables): at least one, possibly more; the no-waiter case is not.]
- Footnote 3: the atomic unlock-and-block in Wait avoids the "wake-up waiting" race, citing Saltzer [13] (MIT thesis, 1966). (p.5)
- Usage pattern: lock the mutex and examine the shared data; if the resource is available continue, otherwise call Wait; the thread that later makes the resource available calls Signal or Broadcast. Example: `LOCK m DO WHILE head = NIL DO Thread.Wait(m, nonEmpty) END; topElement := head; head := head^.next; END;` with the adder calling `Thread.Signal(nonEmpty)` inside its LOCK clause. (p.5-6)

## Alerts
- Purpose: interrupt a particular thread so it backs out of a long-term wait or computation. Interface: `EXCEPTION Alerted; PROCEDURE Alert(t: Thread); PROCEDURE AlertWait(m: Mutex, c: Condition); PROCEDURE TestAlert(): BOOLEAN;`. The notes mention alerts only in passing (threads-and-concurrency.md, Basic Thread Mechanisms: Birrell also describes mechanisms for waking threads from a wait state). (p.6)
- Each thread has an "alert-pending" boolean, initially false. AlertWait behaves like Wait, except that if alert-pending is true it does not block: it clears the flag, re-locks m and raises Alerted. (p.6)
- Alert(t) on a thread blocked in AlertWait wakes it; it re-locks the mutex and then raises Alerted. Alert(t) on a thread not blocked in AlertWait (including one blocked in plain Wait) only sets its alert-pending flag. (p.6)
- TestAlert atomically tests and clears the calling thread's alert-pending boolean. (p.6)
- Modula-2+ exceptions should be thought of as a non-ignorable return code. (p.6)
- Example: a GetChar routine blocked on keyboard input should return when another thread decides the input is no longer wanted (user clicks CANCEL). Signalling its condition variable is not possible if that variable is hidden under layers of abstraction, so the CANCEL thread calls `Thread.Alert(t)` and GetChar contains `TRY WHILE empty DO Thread.AlertWait(m, nonEmpty) END; RETURN NextChar() EXCEPT Thread.Alerted: RETURN EndOfFile END;`. (p.6-7)
- "Alerts are complicated, and their use produces complicated programs." (p.7)

## Using a Mutex: accessing shared data
- The basic rule is stated for *mutable* shared data: all shared mutable data must be associated with some mutex and accessed only by a thread holding it. The notes say "shared state" without the mutable qualifier (immutable data needs no lock; see p.11). (p.7)

## Unprotected data
- Example: `VAR table: ARRAY [0..999] OF REFANY; VAR i: [0..1000];` with `Insert(r)` doing `(1) table[i] := r; (2) i := i+1;` for non-NIL r; table initially all NIL and i = 0. (p.7)
- Interleaving A(1), B(1), A(2), B(2) of Insert(x) and Insert(y) leaves y in the table, loses x, and, since (2) ran twice, leaves an orphaned empty (NIL) slot. Fix: wrap (1) and (2) in `LOCK m DO ... END`, which enforces serialization. (p.7-8)
- Effects of unsynchronized access can be bizarre because they depend on precise timing, and timing is usually non-deterministic due to page faults, real-time timer facilities, or actual multiprocessor asynchrony. (p.8)
- Ideally the language would help, e.g. syntax preventing access to variables until the appropriate mutex is locked, but most languages did not offer this; meanwhile you need programmer discipline and careful use of searching and browsing tools. (p.8)
- Coarse-grain locking (e.g. one mutex for all the global state of a module) makes unprotected-data bugs rarer but causes other problems (lock conflicts, later). Advice: make mutex use "as simple as possible, but no simpler"; adopt more elaborate arrangements only if sure the benefits outweigh the risks, not because the program looks nicer. (p.8)

## Invariants
- Think of a mutex as protecting the invariant of its data: a boolean function of the data that is true whenever the mutex is not held. A thread that locks the mutex starts with the invariant true and must restore it before releasing the mutex, including before calling Wait, since Wait unlocks. (p.8)
- Table example invariant: i is the index of the first NIL element and all elements beyond i are NIL. The variables in the invariant are accessed only with the mutex held, and the invariant is false between the two assignments; it is guaranteed only when the mutex is not held. (p.8)
- Write invariants down explicitly; if they are too complicated to write down, you are probably doing something wrong. They can be informal or in a formal specification language such as Larch [7], which was used to specify the SRC threads facility [4]. (p.8-9)
- Also write down in the program which mutex protects which data items. (p.9) [Now stated in the note body (threads-and-concurrency.md, section Common Pitfalls), so not beyond the notes.]

## Cheating
- The "always lock" rule rests on a model where thread actions are arbitrarily interleaved. Programmers are tempted to skip the mutex for very simple data (one integer or boolean) because the mutex has significant overhead and they "know" the access is a single atomic instruction. (p.9)
- Skipping the lock probably works only if the variable is word aligned, the machine is a uniprocessor, and the compiler generates the obvious instructions and does not cache the variable in a register. Otherwise you may get wrong answers, or worse, usually right and occasionally wrong. Machine-independent correct code must use a synchronization technique approved by the language. (p.9)
- Footnote 4: there is a strong argument for letting programmers exploit instruction atomicity to avoid a LOCK clause, but it is hard to define such a feature efficiently and machine-independently. (p.9)
- Definition of a "hint": a cheap way of getting information that is either correct or causes you to invoke a more expensive, correct way of getting it. Unsynchronized reads can be used as hints. (p.9)
- Hint example (double-checked initialization): `IF NOT initDone THEN LOCK m DO IF NOT initDone THEN Initialize(); initDone := TRUE; END; END; END;`. Correct only if initDone starts FALSE, an unlocked read cannot cause a runtime error, and an unlocked read of FALSE returns FALSE; reading a stale FALSE merely costs taking the lock. Do this only after verifying the language guarantees these assumptions. (p.9)

## Deadlocks involving only mutexes
- The simplest deadlock is a thread trying to lock a mutex it already holds; some systems explicitly allow a thread to continue in that case (recursive locking; see Sun, p.33). (p.10)
- Lock order is stated as a partial order: for any pair {M1, M2}, every thread needing both locks them in the same order. This "completely avoids" deadlocks involving only mutexes, but not other deadlocks that arise with condition variables. (p.10)
- Partitioning technique: thread B wanting M1 may actually need data disjoint from what A accesses under M1; protect that disjoint data with a new mutex M3, giving the order M1 before M2 before M3. This only exists to enable a partial order. (p.10)
- Pursuing this partitioning makes locking more complicated and unsynchronized access more likely; "Having your program deadlock is almost always a preferable risk to having your program give the wrong answer." (p.10)

## Poor performance through lock conflicts
- Once all data is protected and the granularity is fine enough not to deadlock, the remaining mutex problems are all performance problems. (p.10)
- Holding a mutex can stop another thread from progressing. That is fine if the holder uses all the machine's resources, but if the holder stops progressing while holding it (blocks on another mutex, takes a page fault, waits for I/O), total throughput drops. Worse on a multiprocessor, where a blocked thread may leave a processor idle. Lock conflicts must be rare events. (p.10)
- Finer granularity reduces conflicts but adds complexity; "There is no way out of this dilemma" and it is a tradeoff inherent in concurrent computation. (p.10)
- Open-files example: a single mutex for open/close/read/write would prevent writes to separate files proceeding in parallel. Better: `globalLock` protects `globalTable` in Open, and `TYPE File = REF RECORD m: Thread.Mutex; ... END` with `Write(f, ...)` doing `LOCK f^.m DO ... END`. (p.11) [Partly stated in the note's Birrell callout (threads-case-study-pthreads.md, PThread Mutexes): one lock per open file plus one for the global table; the code is not.]
- Different parts of one record can be protected by different mutexes, and immutable fields of a record need no protection at all. (p.11)
- Packed-field hazard: if fields packed into one memory word (not separately accessible by atomic memory operations) are protected by different mutexes, concurrent read-modify-write of the whole word by two threads can corrupt the other field. Be especially careful if overriding the language's default record layout; the language probably will not prevent this. (p.11)
- The scheduler is the part of the thread implementation (often in the OS) that decides which non-blocked threads get a processor, usually by priority; priorities may be fixed or dynamic, programmer-assigned or computed, and often the algorithm is unspecified. (p.11)
- Priority inversion scenario (Birrell does not use that name), uniprocessor, A high, B medium, C low: C runs and locks M; B wakes and preempts C; B starts a very long computation; A wakes and preempts B; A tries to lock M and blocks; the processor returns to B. The high-priority thread cannot progress while a medium one uses the CPU, and the state is stable until C gets CPU time to unlock M. (p.11-12) [Partly stated in the note body (scheduling.md, section Priority Inversion): the generic high/medium/low mutex scenario and the name; Birrell's version, where B's very long computation makes the state stable until C gets CPU time, is not.]
- Programmer workaround: C raises its priority before locking M, which is inconvenient because it requires knowing, per mutex, which other priorities might be involved. Real fix belongs to the thread implementer: while A is blocked on M, the scheduler should treat M's holder as having at least A's priority (priority inheritance). The SRC implementation does not do this. (p.12) [Partly stated in the note body (scheduling.md, section Priority Inversion): boosting the mutex owner's priority; the programmer workaround and that SRC does not do it are not.]

## Releasing the mutex within a LOCK clause
- Motivation: unlock before calling down into a lower-level abstraction that will block or run long, to avoid delaying other threads. SRC provides raw `Acquire(m)` and `Release(m)` in a lower-level, less-advertised interface. (p.12)
- Dangers: the calls must be correctly bracketed even when exceptions occur, and the monitor data may change while unlocked. If Release is called inside a flow-control construct (e.g. a conditional), the program counter encodes a decision based on old monitor state that may no longer be valid. SRC discourages this paradigm. (p.12)
- Mutex hand-off to a forked thread: holding a mutex, fork a thread to continue working on the protected data while the parent stops touching it, by locking with Acquire(m) and calling Release(m) in the child. This is dangerous and hard to verify, and it fails on facilities that track which thread holds a mutex. Birrell recommends against it. (p.12-13)

## Using a Condition variable: scheduling shared resources
- A condition variable is for scheduling how multiple threads access a shared resource when one-at-a-time mutual exclusion is not sufficient. (p.13)
- Example: producers and consumers share an unbounded buffer, a linked list rooted at `head`, protected by m; consumers block on `nonEmpty` when it is empty. `Consume`: `LOCK m DO WHILE head = NIL DO Thread.Wait(m, nonEmpty) END; topElement := head; head := head^.next; END; RETURN topElement`. `Produce`: `LOCK m DO newElement^.next := head; head := newElement; Thread.Signal(nonEmpty); END`. Because the buffer is unbounded, producers never wait and one condition variable suffices (contrast the notes' bounded buffer with c_prod and c_cons). (p.13)
- General pattern Birrell "strongly recommends" for all condition variable uses: `WHILE NOT expression DO Thread.Wait(m,c) END;`. (p.13)
- Reason 1: Signal does not guarantee the awoken thread is next to lock the mutex; another consumer may lock it, remove the element, and unlock before the awoken thread gets the mutex. (p.14) [Now stated in the note body (threads-and-concurrency.md, section Condition Variable API, condition variable quiz), so not beyond the notes.]
- Footnote 5: these are not Hoare's condition variables [9]. Hoare's design guarantees enough to make the re-test redundant, but SRC's design is preferred because it permits a much simpler implementation and the extra check is usually cheap. (These semantics are what is usually called Mesa-style; the paper lists Lampson and Redell's Mesa paper [10] in the references.) (p.14)
- Reason 2, specific to SRC: Signal may (rarely) wake more than one thread, permitted because it allowed more efficient code for Wait and Signal. (p.14) [Partly stated in the note's Birrell callout (threads-and-concurrency.md, Condition Variables): Signal can rarely wake several, a reason for the while loop; the efficiency justification is not.]
- Main reason: with the loop it is immediately clear that the expression holds before the following statements; without it, this could be verified only by examining every place that might signal the condition variable. The convention allows verifying correctness by local inspection, which is always preferable to global inspection. (p.14)
- Final advantage: extra wake-ups are benign, so coding to wake only the right threads becomes a performance question rather than a correctness one (though at least the correct threads must still be woken). (p.14)

## Using "Broadcast"
- Signal is for when at most one thread can usefully be awoken; Broadcast wakes all threads that have called Wait. Under the re-check convention, replacing any Signal with Broadcast never changes correctness. (p.14) [Now stated in the note body (threads-and-concurrency.md, section Common Pitfalls), so not beyond the notes.]
- Two uses of Broadcast: (1) simplicity: wake several threads even though not all can progress, so you can be less careful about separating wait reasons into different condition variables, trading slightly poorer performance for simplicity; (2) genuine need: the newly available resource can be used by multiple threads. (p.14) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Condition Variable API), so not beyond the notes.]
- Shared/exclusive (readers/writers) locking is the named example of (2): reads may proceed concurrently (correct and faster), but a modifying thread needs exclusive access. Callers bracket reads with AcquireShared/ReleaseShared and writes with AcquireExclusive/ReleaseExclusive. (p.14) [Partly stated in the note's Birrell callout (threads-and-concurrency.md, Condition Variable API): readers are the standard example; the AcquireShared/ReleaseShared/AcquireExclusive/ReleaseExclusive interface is not.]
- First version, one condition variable c and counter i (positive: number of active readers; negative: active writer; zero: free): `AcquireExclusive: LOCK m DO WHILE i # 0 DO Wait(m,c) END; i := -1 END`; `AcquireShared: LOCK m DO WHILE i < 0 DO Wait(m,c) END; i := i+1 END`; `ReleaseExclusive: LOCK m DO i := 0; Broadcast(c) END`; `ReleaseShared: LOCK m DO i := i-1; IF i = 0 THEN Signal(c) END END`. (p.15) [The counter encoding is stated in the note body (threads-and-concurrency.md, section Readers/Writer Problem, resource_counter); the one-condition-variable code is not.]
- Broadcast in ReleaseExclusive is convenient because the terminating writer need not know how many readers can proceed. It is only a convenience: keep a count of waiting readers and call Signal that many times; Broadcast just uses information the thread implementation already has. (p.15)
- This first encoding "exemplifies many of the problems" with condition variables, and the following subsections revise it step by step. (p.15-16)

## Spurious wake-ups
- Birrell's definition: waking threads that cannot make useful progress, caused by using Broadcast where Signal suffices, or by having threads wait on one condition variable for different reasons. (p.16) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Spurious Wake-ups), so not beyond the notes.]
- In the one-CV readers/writers code, ReleaseExclusive's Broadcast wakes readers and writers; if a reader locks the mutex first, it increments i and the woken writer cannot progress until ReleaseShared. The cost is extra time in the thread scheduler, "typically an expensive place to be." (p.16)
- If such wake-ups will be common, and unless the scheduler is unusually efficient, split waiters onto two condition variables: a terminating reader signals only the writers' CV, and a terminating writer signals one of the two, depending on which is non-empty. (p.16) [Partly stated: the terminating writer's choice of class is in the note's Birrell callout (threads-and-concurrency.md, Readers/Writer Example); the conditions (wake-ups common, scheduler not unusually efficient) are not.]
- Refined version: `VAR cR, cW: Condition; VAR readWaiters: INTEGER`. AcquireExclusive waits on cW while `i # 0`. AcquireShared does `readWaiters := readWaiters+1; WHILE i < 0 DO Wait(m,cR) END; readWaiters := readWaiters-1; i := i+1`. ReleaseExclusive: `i := 0; IF readWaiters > 0 THEN Broadcast(cR) ELSE Signal(cW) END`. ReleaseShared: `i := i-1; IF i = 0 THEN Signal(cW) END`. (p.16-17) [ReleaseExclusive's behavior is now stated in the note's Birrell callout (threads-and-concurrency.md, Readers/Writer Example); the readWaiters bookkeeping is not.]

## Spurious lock conflicts
- Birrell's name for what the notes call spurious wake-ups: a terminating reader calls Signal while still holding the mutex; on a multiprocessor the woken writer runs a few instructions in Wait and blocks on the still-held mutex, and a few microseconds later the reader unlocks it. Cost: two extra re-schedule operations, "a significant expense." On a uniprocessor this is often not a problem. (p.17) [The name and the case are now stated in the note's Birrell callout (threads-and-concurrency.md, Spurious Wake-ups); the multiprocessor/uniprocessor contrast and the two-reschedule cost are not.]
- Fix (`doSignal`): since the reader does not touch protected data after Signal, move the Signal past the end of the LOCK clause while keeping the access to i protected: `LOCK m DO i := i-1; doSignal := (i=0); END; IF doSignal THEN Thread.Signal(cW) END;`. The condition is evaluated under the lock; only the signal moves out. (p.17) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Spurious Wake-ups), so not beyond the notes.]
- Harder case: a terminating writer's Broadcast is issued with the mutex held, and in addition only one woken reader at a time can lock the mutex to re-check and increment i, so on a multiprocessor the other woken readers tend to block on the mutex (unlikely on a uniprocessor). (p.17-18)
- Fix: ReleaseExclusive Signals one reader instead of Broadcasting, and each reader wakes the next by calling `Thread.Signal(cR)` after its LOCK clause in AcquireShared (a chained wake-up). (p.18)

## Starvation
- Fairness: for mutexes the thread implementation handles it, typically first-in-first-out within each priority level; mostly the same for condition variables, but sometimes the programmer must get involved. Starvation, where a thread never makes progress, is the most extreme unfairness. (p.18)
- Writer starvation in the readers/writers code under heavy read load: A acquires shared (i=1), B acquires (i=2), A releases (i=1), C acquires (i=2), B releases (i=1), and so on. There is always an active reader, i never reaches 0, and writers stay blocked forever. (p.18)
- Fix: add `writeWaiters`; AcquireExclusive increments it before its wait loop and decrements it after. In AcquireShared, after `readWaiters := readWaiters+1`, `IF writeWaiters > 0 THEN Thread.Signal(cW); Thread.Wait(m,cR); END;` then the usual `WHILE i < 0` loop, and `Thread.Signal(cR)` after the LOCK clause. A new reader thus defers once to a blocked writer. (p.18-19)
- "There is no limit to how complicated this can become"; exercise restraint and add such scheduling features only if the actual load on the resource requires them. (p.19)

## Complexity
- The readers/writers solution grew from 15 lines in the procedure bodies to 30, with quite subtle correctness reasoning. (p.19)
- Whether to handle spurious wake-ups, lock conflicts and starvation depends on the threads implementation's performance, whether you run on a multiprocessor, and the expected load; if the resource is mostly not in use, adopt the simplest coding style. (p.19)
- Rule of thumb: moving Signal beyond the end of the LOCK clause is usually easy and worth it; the other enhancements usually are not, but ignore them only after explicitly considering whether your situation needs them. (p.19)

## Deadlock
- Condition variables can deadlock too: A acquires resource (1), B acquires (2), A waits on (2)'s condition variable, B waits on (1)'s. Remedy: a partial order on resources managed by condition variables (e.g. (1) before (2)), so B may not try to acquire (1) while holding (2). (p.19-20)
- Nested monitor problem: `Get: LOCK a DO LOCK b DO WHILE NOT ready DO Thread.Wait(b,c) END END END`; `Give: LOCK a DO LOCK b DO ready := TRUE; Thread.Signal(c) END END`. Get's Wait releases b but keeps a, so Give blocks on a and never signals. The example is trivial (a protects no data) but the pattern occurs. (p.20)
- It usually arises when a mutex is locked at one abstraction level and the code calls down into a lower level that, unknown to the higher level, blocks, and the block can be released only by a thread that needs the higher-level mutex. Calling down while holding a mutex is risky unless you fully understand when the callee might block. (p.20)
- Fixes: explicitly unlock before calling down (with the dangers described on p.12), or better, end the LOCK clause before calling down. Literature: Haddon, "Nested monitor calls" [8]. (p.20-21)

## Using Fork: working in parallel
- Recap of reasons to fork: use a multiprocessor, do useful work while waiting for a slow device, satisfy users by working on several actions at once, serve multiple network clients simultaneously, and defer work to a less busy time. (p.21)
- A straightforward application might have one thread for the main computation, one writing output to a file, one waiting for or responding to user input, and one in the background cleaning up data structures (e.g. re-balancing a tree). Several SRC library packages fork threads internally. (p.21)
- Drive slow devices with synchronous library calls that suspend only the calling thread; older asynchronous schemes (interrupts, Unix signals, VMS ASTs) are unnecessary. To avoid waiting, invoke the device call in a separate thread; for multiple outstanding requests, use multiple threads. (p.21)
- If the OS still delivers asynchronous events through the older mechanisms, the thread runtime library should convert them into more appropriate mechanisms; examples are the Topaz system call design [11] and the exception and trapping machinery of Sun's lightweight process library [14,15]. (p.21)
- Interactive responsiveness: it is "particularly infuriating" if the display goes dead because a database query is slow. Some window systems always call the program in a separate thread; others call it synchronously with the input event, in which case you must decide whether to do the action synchronously or fork. (p.21)
- Forking UI work requires great care reading interactive state (current selection, contents of editable text areas) because it can change once you run asynchronously; each window system handles this differently and Birrell had "not yet seen a totally satisfactory design." (p.21)
- Network servers: with RPC [3] the server runtime forks threads internally and runs each concurrent incoming call in its own thread, with no work for you. With connection-oriented protocols (e.g. file transfer over TCP), fork one thread per incoming connection. A client that does not want to wait for a server reply calls it from a separate thread. (p.21-22)
- Deferring work, simplest variant: once the procedure has computed its result, fork a thread for the rest and return, reducing latency in the hope that the deferred work is cheaper later (e.g. a processor goes idle). Downsides: possibly large numbers of threads, and the cost of Fork every time. (p.22)
- Preferred: a single housekeeping thread fed with requests; better still if it needs no information beyond "there is work," e.g. maintaining a data structure in optimal form when the main threads get correct answers anyway. The housekeeper can merge similar requests into one action or run no more often than a chosen periodic interval. (p.22)
- On a multiprocessor, deciding when and what to fork is too problem-specific for general advice; pipelining is the one general technique offered. (p.22)

## Pipelining
- A pipeline is a chain of producer-consumer relationships: A only enqueues a request in a buffer, B takes it, does part of the work, enqueues it in a second buffer, C does the rest. The three threads run in parallel except when synchronizing on buffers, so this uses up to three processors. (p.22)
- At best a pipeline gives almost linear speed-up and fully uses a multiprocessor. It is also useful on a uniprocessor if each stage hits real-time delays (page faults, device handling, network communication). (p.22)
- Code example: `PaintChar(ch)` allocates a RasterList node, appends it under `LOCK m` (`rasterTail^.next := this; rasterTail := this`), then calls `Thread.Signal(c1)` outside the LOCK and returns. `Rasterize` loops: under m, `WHILE last^.next = NIL DO Wait(m, c1) END; last := last^.next`; converts the char with `Font.Map`; appends a PaintList node under m; `Signal(c2)`. `Painter` similarly waits on c2 and calls `Display.PaintBitmap`. (p.22-24)
- Implementation details of the example: buffers are unbounded linked lists tracked by tail pointers `rasterTail`/`paintTail`, initialized to dummy elements to simplify the code; each consumer keeps its own `last` pointer instead of removing nodes; one mutex m protects both buffers, with condition variables c1 and c2; the stages are started with `Thread.Fork(Rasterize, rasterTail); Thread.Fork(Painter, paintTail)`. (p.22-24)
- The example's code is internally inconsistent: `PaintList` is declared with a field `r: Bitmap`, but Rasterize assigns `this^.bitmap` and Painter reads `last^.bitmap`. (p.22-24)
- Problem 2: the number of stages statically determines the amount of concurrency. That is fine if you know the processor count and exactly where real-time delays occur, but a problem in flexible or portable environments. (p.24)
- Despite these problems, Birrell calls pipelining a powerful technique with wide applicability. (p.24)

## The impact of your environment
- The OS must not suspend the entire address space when one thread blocks for I/O or a page fault, and the OS and libraries must permit calls from multiple threads in parallel. A well-designed environment exposes its facilities as synchronous calls that block only the calling thread [11]. (p.24)
- Know four performance parameters of your implementation: cost of creating a thread, cost of keeping a blocked thread in existence, cost of a context switch, and cost of a LOCK clause when the mutex is not locked. They determine how far adding threads is feasible. (p.24)

## Potential problems with adding threads
- Careless thread addition can make the program slower. With significantly more ready threads than processors, performance usually degrades: schedulers are slow at general rescheduling. Getting a thread onto an idle processor is fast; queueing it and later swapping it in for another thread is expensive. (p.24)
- More running threads are also more likely to conflict over mutexes and over resources managed by condition variables. (p.24)
- This matters mainly for threads added for performance (parallel actions, deferring work, using multiprocessors), less for threads added for program structure (slow devices, fast mouse response, RPC invocations). (p.24-25)
- The warning applies only to ready threads. Blocked threads cost only scheduler data structures and a stack; SRC programs often have many blocked threads (50 is not uncommon in application programs), and there are usually hundreds blocked inside the OS even on personal workstations. (p.25)
- Thread creation and termination are not cheap. Implementations cache a few terminated thread "carcasses" to avoid stack creation per fork, yet a Fork still costs about two or three re-scheduling decisions, so do not fork too small a computation. A useful measure of a multiprocessor thread implementation is the smallest computation for which forking is profitable. (p.25)
- SRC experience on a 5-way multiprocessor: programmers were as likely to err by creating too few threads as too many. (p.25)

## Using Alert: diverting the flow of control
- Alerts terminate a long-running computation or long-term wait. Examples: on a multiprocessor, fork several competing algorithms for the same problem and abort the rest when the first finishes; abort a long database query when the user clicks CANCEL. (p.25)
- SRC convention: every procedure in a public interface that might incur a long computation or long-term wait should be alertable: long computations call TestAlert occasionally and long waits use AlertWait instead of Wait. "Long" means long enough to upset a human user. (p.25)
- Benefit: the user can always regain control of the application. Cost: callers must be prepared for Alerted to propagate out of these procedures. The convention is applied less rigorously when an entry point only occasionally causes a long wait. (p.25)
- Second SRC convention: alert a thread only if you forked it; e.g. a package must not alert a caller's thread that happens to be executing inside the package. This lets an alert mean "terminate completely." (p.25)
- Alerts, like any asynchronous interrupt mechanism (e.g. Apollo's task_$signal), are intrusive: a straightforward flow of control in one thread can be diverted by another thread, which defeats verification by local inspection. Unless used with great restraint they make programs unreadable, unmaintainable, and perhaps incorrect. (p.25)
- Alternatives: if you know which condition variable the thread is blocked on, set a boolean flag and signal that condition variable; a package can offer extra entry points whose purpose is to prod a thread blocked inside it. (p.26)
- Alerts are most useful when you do not know exactly where the target is blocked (in any of several packages, or on any of several condition variables in one package); there an alert is the best solution. Even when alternatives exist, alerts may be preferable as a single unified way to provoke thread termination. (p.26)
- There was no consensus among thread facility designers on this problem; each solution had its own problems. (p.26)

## Additional techniques
- Most thread programming paradigms are simple; this section covers a few useful but much less obvious ones. (p.26)

## Up-calls
- Layered abstractions (higher levels call only lower levels, peers do not call each other, all actions initiated at the top) carry over to concurrency: threads honor abstraction boundaries, and permanent daemon threads inside an abstraction call only lower levels. The layering forms a partial order sufficient to prevent mutex deadlocks with no extra care. (p.26)
- Pure top-down layering fails when actions affecting high levels originate low: network packet reception, user input, and spontaneous state changes in peripherals such as disks and tapes. (p.26)
- Network receive has three or more dispatch layers (OSI data link, network, transport). Keeping top-down calls costs a context switch per layer, because the thread wanting data from its transport connection cannot be the one that dispatches an incoming Ethernet packet: the packet may belong to another connection, another protocol (UDP vs TCP), or another protocol family (DECnet vs IP). Implementations that kept this layering had "uniformly bad performance," dominated by context switches. (p.26)
- Up-calls (Clark [5]): a pool of threads receives data-link packets; the receiving thread dispatches on Ethernet protocol type and calls up to the network layer (DECnet or IP), dispatches again, calls up to transport (TCP), and finally dispatches to the connection; in some systems this extends into the application. No unnecessary context switches; all the top-performing network implementations are structured this way. (p.26-27)
- Costs: each layer needs an up-call interface in addition to its down-call interface, and synchronization gets more delicate. In a top-down system holding a layer's mutex while calling down is fine (barring nested-monitor blocking), but with up-calls an up-calling thread holding a lower-level mutex that locks a higher-level one violates the lock order and can deadlock on mutexes alone. Avoid holding a mutex while making an up-call, "easier said than done." (p.27)

## Version stamps
- Problem: a lower-level thread may invalidate information a higher-level thread has cached, e.g. a disk volume changes through hardware problems or removal and replacement. Up-calls can invalidate higher-level cache structures but not state held locally by a thread; at worst a thread reads from the cache and the data becomes invalid before its call to the lower level happens. (p.27)
- Technique: the low level keeps a counter with the true data, incremented on every change (assume it never overflows); every copy handed up carries the current counter value and is cached with it; calls down that depend on earlier data pass the counter back; the low level compares and, on mismatch, returns an exception so the caller reconsiders (sometimes the exception carries the new data). Also useful for cached data across a distributed system. (p.27)

## Work crews
- "An embarrassment of parallelism": a program can expose far more concurrency than the machine accommodates, e.g. a compiler with a thread per procedure or even per statement. One thread per action makes the scheduler inefficient, causes numerous lock conflicts, or exhausts memory for stacks. (p.27-28)
- Options: fork with more restraint, or use an abstraction that controls forking: Vandevoorde and Roberts' work crews [17] enqueue requests for asynchronous activity served by a fixed pool of threads. The complexity lies in managing requests, synchronizing between them, and coordinating results. (p.28)
- "Lazy forking": an unexplored SRC proposal to implement Fork so it defers actually creating the thread until a processor is available to run it. (p.28)

## Building your program
- A successful program must be useful, correct, live and efficient, and concurrency affects each. (p.28)
- Useful: design library interfaces assuming multi-threaded callers. All entry points must be thread re-entrant (callable by multiple threads simultaneously), even if each just locks a central mutex; never return results in shared global variables or global statically allocated storage; calls should be synchronous, with callers using other threads for overlap. Follow this even without current multi-threaded clients. (p.28)
- Correct: if the program produces an answer, it is the one its specification defines. The environment gives little help beyond sequential tools; be fastidious about associating each piece of data with one and only one mutex ("If you don't pay constant attention to this, your task will be hopeless"), and with the re-check-after-Wait style you are unlikely to go wrong. (p.28)
- Live: the program eventually produces an answer; the alternatives are infinite loops ("I can't help you with infinite loops") or deadlock. Deadlocks should be easy to detect with a symbolic debugger that at least enumerates threads and shows each stack. (p.28)
- Desirable debugger features: filtering thread enumeration (threads with a stack frame in a given module, threads blocked on a given mutex or condition variable) and, ideally, finding which thread holds a given mutex. (p.28-29)
- Efficient: the program makes good use of resources and answers quickly. Performance bugs are the most insidious because you may not notice them. Needed statistics: lock conflicts (how often threads blocked on each mutex and how long they waited) and concurrency levels (average number of ready threads, or the percentage of time n threads were ready). (p.29)
- Do not emphasize efficiency at the expense of correctness: it is much easier to make a correct program efficient than an efficient program correct. (p.29)

## Concluding remarks
- Birrell argues concurrent programming is neither exotic nor difficult; you need good primitives and suitable libraries, basic caution and carefulness, an armory of useful techniques, and knowledge of the common pitfalls. (p.29)
- Butler Lampson, Mike Schroeder, Bob Stewart and Bob Taylor prompted the paper. (p.29)

## References
- 17 references, including: Hoare, "Monitors: an operating system structuring concept" (CACM 1974) [9]; Lampson and Redell, "Experience with processes and monitors in Mesa" (CACM 1980) [10], listed but not visibly cited in the body; Saltzer's 1966 MIT thesis on traffic control [13] (wake-up waiting); Haddon, "Nested monitor calls" (OSR 1977) [8]; Clark, "The structuring of systems using up-calls" (SOSP 1985) [5]; Birrell and Nelson, "Implementing remote procedure calls" (TOCS 1984) [3]; Birrell, Guttag, Horning and Levin, formal specification of multiprocessor synchronization primitives (SOSP 1987) [4]. (p.29-30)
- Remaining references: Accetta et al., Mach (USENIX 1986) [1]; Apollo CPS reference (1987) [2]; Cooper and Draves, C Threads (CMU-CS-88-154) [6]; Guttag, Horning and Wing, Larch (IEEE Software 1985) [7]; McJones and Swart, evolving the UNIX interface for multi-threaded programs (USENIX 1989, the Topaz system calls) [11]; Rovner, Modula-2+ (IEEE Software 1986) [12]; Sun OS 4.0 manual and System Services Overview [14,15]; Tevanian et al., Mach threads and the Unix kernel (USENIX 1987) [16]; Vandevoorde and Roberts, Workcrews (submitted) [17]. (p.29-30)

## Appendix: other thread designs
- The SRC design is similar to several publicly available designs; the appendix compares Apollo, Sun and Mach, with hints on when their differences are useful or dangerous, and assumes familiarity with their documentation; readers should check that documentation before relying on the appendix, and Birrell apologizes in advance for any misrepresentation. (p.31)
- Every design has mechanisms the paper skips: facilities for affecting scheduling (adjusting priorities, hints on when preemption would be useful), per-thread context information (SRC and Sun), and a "conditional lock" operation on a mutex (all of them). (p.31)
- All these systems are equivalent in power: each can reproduce the others' facilities by programming on top of them, and any concurrent problem can be solved with any of them; differences only make some paradigms (good or bad) easier and others harder. (p.31)
- Equivalence table. Sun 4.0: Fork = `lwp_create`, Mutex = `mon_t`, LOCK/END = `mon_enter`/`mon_exit`, Condition = `cv_t`, Wait = `cv_wait`, Broadcast = `cv_broadcast`, Signal = `cv_notify`, no Join, no Alert. Mach C threads: `cthread_fork`, `cthread_join`, `mutex_t`, `mutex_lock`/`mutex_unlock`, `condition_t`, `condition_wait`, `condition_broadcast`, `condition_signal`, no Alert. Apollo Domain CPS: `task_$create`, `task_$release`, `task_$handle_t`, `mutex_$lock`/`mutex_$unlock`, `ec2_$eventcount_t`, `ec2_$wait`, `ec2_$advance` (Broadcast), no Signal, Alert = `task_$signal`. The text extraction leaves the alignment of `task_$release`/`task_$handle_t` against Join/Mutex ambiguous. An empty entry means Birrell saw no reasonably equivalent facility. (p.31)

## Apollo Domain Concurrent Programming Support (CPS)
- `mutex_$lock` accepts a timeout. Legitimate use: switch to an alternative algorithm when a mutex is held too long, useful if lock conflicts are common; but you should normally make conflicts rare and short via fine-grained locking, each mutex protecting only the data you intend to touch. (p.31-32)
- Using the timeout to detect or recover from deadlocks is discouraged: deadlocks are bugs to be found with a debugger and programmed away. (p.32)
- Level 2 eventcounts serve the purpose of condition variables: lock the mutex, inspect data, read the eventcount with `ec2_$read`, unlock, then `ec2_$wait` until it is advanced; this matches SRC Wait plus Broadcast. Reading the eventcount while still holding the mutex gives the same atomicity SRC guarantees in Wait, and this is how SRC implements Wait's atomicity. (p.32)
- Eventcounts are not tied to a mutex or its data, so threads can block and wake without synchronizing over shared data; this is rarely what you want, since you normally wake a thread because you just changed data it cares about. (p.32)
- Lost-wakeup sequence: (1) A looks at the data and decides to block; (2) A unlocks the mutex; (3) B locks the mutex and changes the data; (4) B calls `ec2_$advance`; (5) A calls `ec2_$read`; (6) A calls `ec2_$wait`. A is never woken. Step 5 was meant to precede step 4, and to guarantee that A must do (5) before (2). (p.32)
- `ec2_$wait` can wait on multiple eventcounts, occasionally convenient; without it you need one thread per awaited condition. It introduces no new problems beyond implementation complexity and possible performance penalties. (p.32)
- `task_$signal` produces a fault at an arbitrary point in the target thread (unless it has inhibited faults), in contrast to SRC's polled alerts (AlertWait/TestAlert). Interrupting a thread holding a mutex would leave shared data unpredictable, so Apollo inhibits faults while a mutex is locked. (p.32)
- Tradeoff: polling makes control flow visible in the source; interrupting anywhere outside LOCK clauses makes termination more certain, since forgetting a TestAlert call cannot break it. Both are valid and the ideal design would support both. (p.32)

## Sun's lightweight process library
- Sun OS 4.0 provides "lightweight processes" as a library; they are not true threads, since only one runs at a time within an address space, but creation and synchronization look like real threads. (p.33)
- Sun allows recursive mutex locking (a holder can call, possibly recursively, a procedure that locks the same mutex); in SRC this deadlocks. It is fine if the monitor invariant was restored before the call; if the call is really a bug (you forgot the callee uses the same data), you silently get wrong answers. Splitting the computation across threads can turn a former recursive acquisition into an acquisition by another thread, i.e. a deadlock. (p.33)
- Sun has no alert mechanism, but threads can handle asynchronous Unix signals via `agt_create`; some signals serve the purpose of alerts. Alerts are "not really a fundamental part of threads," just a convenience. (p.33)
- Sun also offers message passing between threads. Most designers view message passing as an alternative to shared-memory synchronization, not an adjunct; Birrell advises against using both in one program, except as needed for Sun's message system to handle Unix signals. (p.33)

## Threads in Mach
- The table's Mach entries come from Eric Cooper's C library interface to Mach threads [6]; it closely resembles SRC's, the only noticeable omission is alerting, and there are no substantive differences. (p.33)

## Notes vs paper discrepancies
Each item was checked against the paper, the lecture as reconstructed from independent student note sets (no lecture transcript was retrievable), and third-party references; sources are listed under "Discrepancy sources". Verdicts: PAPER CONFIRMED, NOTES WRONG (the notes depart from the paper and the lecture does not support them); LECTURE FRAMING (the notes reproduce the lecture and the paper differs); NOT A REAL DISCREPANCY.
- "Spurious wake-up" means different things. The notes use it for a thread woken by a Signal/Broadcast issued while the signaller still holds the mutex, so it immediately blocks on the mutex. Birrell calls that a "spurious lock conflict" and reserves "spurious wake-up" for waking threads that cannot make progress at all (Broadcast where Signal suffices, or several wait reasons sharing one CV). (p.16-17) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Spurious Wake-ups).]
  - Verdict: LECTURE FRAMING, the lecture uses the readers/writer example to define a spurious wake-up as signalling while holding the mutex, and third parties (POSIX, Wikipedia, OSTEP) side with the paper, whose meaning is close to the standard one.
- The threads notes say a conditional signal must stay inside the mutex because the condition reads shared state. Birrell's `doSignal` pattern evaluates the condition under the lock and signals after the LOCK clause, so only the test needs the mutex. (The pthreads notes' "notify after unlocking" tip agrees with Birrell, so the two note files are inconsistent with each other.) (p.17) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Spurious Wake-ups).]
  - Verdict: LECTURE FRAMING, the lecture says the reader cannot unlock before signalling, and third parties (POSIX, Lampson & Redell) side with the paper that only the shared-state test needs the lock; OSTEP's hold-the-lock rule is a simplicity guideline.
- The notes' writer exit both Broadcasts read_phase and Signals write_phase. Birrell's refined version wakes only one class (Broadcast cR if readWaiters > 0, else Signal cW); waking both is a source of what he calls spurious wake-ups. Not wrong, but less efficient. (p.16-17) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Readers/Writer Example).]
  - Verdict: LECTURE FRAMING, the lecture's writer wakes both classes in arbitrary order, and third parties (POSIX, Lampson & Redell, OSTEP) treat that as correct but costlier, which is the paper's efficiency point.
- The pthreads notes say "One mechanism not considered by Birrell is detachable threads", and the threads notes say a forking thread must not exit before its child and present join as the mechanism. Birrell says Join is rarely used at SRC, some facilities lack it, and an unjoined finished thread "quietly evaporates", which is effectively detached-by-default. Birrell does not discuss what happens to children when the parent exits. (p.4) [Now stated in the note's Birrell callouts (threads-and-concurrency.md, Thread Creation; threads-case-study-pthreads.md, PThread Creation).]
  - Verdict: LECTURE FRAMING, the lecture says detachable threads are not in Birrell and that early parent exit leaves zombies, and third parties (POSIX, Linux man pages) side with the paper: detach only means auto-reclaim, and surviving main's exit needs pthread_exit, not detachment.
- The pthreads tip "mutex scope must be global" conflicts with Birrell's per-object mutexes stored in records (one mutex per open file), which allow more parallelism. The lecture tip presumably means visible to all threads that use it. (p.4-5, p.11) [Now stated in the note's Birrell callout (threads-case-study-pthreads.md, PThread Mutexes).]
  - Verdict: LECTURE FRAMING, the lecture says the mutex must be visible to all threads and not local to one function, and third parties (POSIX, OSTEP, Lampson & Redell) side with the paper that per-object mutexes in shared heap structures are standard.
- The notes say broadcast "may not always be super useful" because woken threads still take the mutex one at a time. Birrell gives two legitimate uses (simplicity, and resources usable by many waiters, such as readers, who proceed concurrently after leaving the critical section). (p.14) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Condition Variable API).]
  - Verdict: LECTURE FRAMING, the lecture calls Broadcast a tenuous use because only one thread re-acquires the mutex at a time, and third parties (POSIX, Lampson & Redell, OSTEP) side with the paper that Broadcast is right when several waiters can proceed.
- The notes list deadlock detection and recovery as an option. Birrell treats deadlocks as bugs to find with a debugger and remove, and discourages lock timeouts for recovery. Different emphasis, not a factual conflict. (p.28, p.32)
  - Verdict: NOT A REAL DISCREPANCY, the lecture lists prevention, detection and recovery, and the ostrich algorithm, and OSTEP also presents detect-and-recover as legitimate, so Birrell's stance is advice for application programmers rather than a conflicting fact.
- The notes describe Signal as waking "a waiting thread"; Birrell's Signal wakes at least one and possibly more, which is part of why the while loop is required. (p.5, p.14) [Now stated in the note's Birrell callout (threads-and-concurrency.md, Condition Variables).]
  - Verdict: LECTURE FRAMING, the lecture says Signal wakes one thread and justifies the while loop only by intervening threads, and third parties (POSIX, OSTEP) side with the paper's "at least one".
- The notes say compilers "may generate warnings/errors" for forgotten locks; Birrell (1989) says most languages do not yet offer such help and you need discipline plus searching and browsing tools. A difference of era more than of fact. (p.8)
  - Verdict: NOT A REAL DISCREPANCY, the lecture says some compilers can warn, and Clang's Thread Safety Analysis shows modern compilers can, given annotations, so both statements are true for their era.
- The notes balance a pipeline by assigning more threads to the slow stage. Birrell's pipeline has one thread per stage, balanced by hand-tuning how much work each stage does, and he notes the stage count statically fixes the degree of concurrency. Different remedies, not a contradiction. (p.24)
  - Verdict: NOT A REAL DISCREPANCY, the lecture assigns more pool threads to the slowest stage, and Intel oneTBB's parallel pipeline filters show both that remedy and Birrell's stage-balance concern are standard.

## Covered in the notes
- Threads share an address space; each has its own stack and registers.
- Threads are cheaper than processes to set up and to communicate between (IPC cost).
- Overlapping I/O waits on a uniprocessor; multiprocessor parallel speed-up.
- Fork(proc, arg) creating a thread, and Join blocking until the child finishes and returning its result.
- Mutex semantics: lock, critical section, blocking on a held mutex; LOCK-clause vs explicit unlock styles.
- Lost-update race (notes use a linked-list insert instead of Birrell's table).
- Condition variable API: Wait(m, c), Signal, Broadcast; Wait atomically releases the mutex and re-acquires it on wake.
- Re-checking the predicate in a while loop because another thread may get the mutex first.
- Producer/consumer with a mutex and condition variables.
- Readers/writers with a proxy counter (positive readers, -1 writer, 0 free); last reader Signals a writer (no Broadcast, since at most one writer can proceed), Broadcast for readers.
- Broadcast in place of Signal is safe for correctness; Signal in place of Broadcast is not.
- Signalling while holding the mutex causes woken threads to block on the mutex; signal after unlocking (Birrell's spurious lock conflict, notes' spurious wake-up).
- Two-mutex deadlock from opposite acquisition orders; fix by lock ordering.
- One mutex per piece of shared data, used consistently; document which mutex protects what.
- Pipelining: stages as threads, shared buffers between stages, balancing stage work; throughput limited by the slowest stage and keeping the pipeline balanced over time requires re-balancing (Birrell's problem 1: equal stages need hand tuning and re-tuning as the program changes).
- Thread pools vs creating a thread per task (boss/workers).
- Many-to-one user threads block the whole process on a blocking call (Birrell's environment requirement).
- Trylock exists (pthreads), matching Birrell's "conditional lock" mention.


## Discrepancy sources
- <https://github.com/awpala/my-omscs-notes> (cs-6200/03-P2L2-threads-and-concurrency.md, cs-6200/04-P2L3-threads-case-study-pthreads.md)
- <https://raw.githubusercontent.com/awpala/my-omscs-notes/HEAD/cs-6200/04-P2L3-threads-case-study-pthreads.md>
- <https://github.com/Guochiuan/CS6200-notes> (P2L2 Threads and Concurrency.md, P2L3 PThreads.md)
- <https://github.com/lkrych/gios_notes> (lectures/threads_and_concurrency/3-Threads_and_Concurrency.md, lectures/pthreads/4-Threads_Case_Study-PThreads.md)
- <https://github.com/tewidis/GIOS> (markdown/threads_and_concurrency.md, markdown/pthreads.md)
- <https://github.com/hpca01/GIOS> (checked; a copy of the omscs-notes file, not counted as independent)
- <https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_cond_signal.html>
- <https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_exit.html>
- <https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_detach.html>
- <https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_init.html>
- <https://man7.org/linux/man-pages/man3/pthread_join.3.html>
- <https://man7.org/linux/man-pages/man3/pthread_create.3.html>
- <https://en.wikipedia.org/wiki/Spurious_wakeup>
- <https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf> (OSTEP ch.30, Condition Variables)
- <https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks-usage.pdf> (OSTEP ch.29, Lock-based Concurrent Data Structures)
- <https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf> (OSTEP ch.32, Common Concurrency Problems)
- <https://people.eecs.berkeley.edu/~brewer/cs262/Mesa.pdf> (Lampson & Redell, Experience with Processes and Monitors in Mesa, 1980)
- <https://clang.llvm.org/docs/ThreadSafetyAnalysis.html>
- <https://www.intel.com/content/www/us/en/docs/onetbb/developer-guide-api-reference/2023-1/working-on-the-assembly-line-parallel-pipeline.html>
- <https://www.intel.com/content/www/us/en/docs/onetbb/developer-guide-api-reference/2022-1/throughput-of-pipeline.html>
- <https://api.github.com/search/repositories?q=gios+notes> (used to locate student note repositories)
