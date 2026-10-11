---
id: operating-systems-papers-beyond-notes-pai
title: "Pai et al., Flash: Beyond the Notes"
course: operating-systems
lecture: papers-beyond-notes-pai
---

# Pai et al. (Flash): everything not in the notes

Everything in the paper that the original lecture notes do not state, plus places where the paper contradicts them; validated against the paper text. The reference point is the original lecture notes: the notes now carry `> **Paper (...):**` callouts for the lecture-framing discrepancies listed under "Notes vs paper discrepancies", so some gaps below are now annotated in the notes. Paper: <https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-pai-paper.pdf>.

## Front matter
- Published in the Proceedings of the 1999 USENIX Annual Technical Conference, Monterey, California, June 6-11, 1999. Authors: Vivek S. Pai (Department of Electrical and Computer Engineering), Peter Druschel and Willy Zwaenepoel (Department of Computer Science), Rice University. (Front matter)

## Abstract
- AMPED is presented as combining the high performance of SPED servers on cached workloads with the performance of MP and MT servers on disk-bound workloads, using only facilities available in all modern operating systems (portability claim). The notes describe AMPED's portability but not this "best of both" framing in terms of cached vs disk-bound workloads. (Abstract)
- Architectures are evaluated within a single implementation explicitly "to quantify the impact of a server's concurrency architecture on its performance." (Abstract)
- Flash is compared with two widely used servers, Apache and Zeus; headline result: Flash matches or exceeds existing servers by up to 50% across a wide range of real workloads. The notes give no numbers. (Abstract)
- The paper also presents results quantifying the contribution of individual Flash optimizations (developed in 6.3). (Abstract)

## 1 Introduction
- Motivation for portability and performance: portable high-performance servers reduce the hardware cost of meeting a given demand and allow switching hardware platforms and OSes based on cost, availability or performance. (1)
- Servers reach thousands of requests per second by caching frequently requested content in main memory despite long disk latency. (1)
- Core problem statement: Web data sets typically exceed main memory, so a high-performance server must overlap serving cached requests with concurrent disk operations fetching uncached content. (1)
- SPED servers give excellent performance on cached workloads; Zeus and the original Harvest/Squid proxy caches are SPED. Footnote: Zeus can be configured to run multiple SPED processes, particularly on multiprocessors. (1) [Zeus being SPED is now stated in the note body and the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology); Harvest/Squid and the footnote are not.]
- On workloads exceeding the server cache, MP or MT servers usually perform best. Apache used MP on UNIX and MT on Windows NT. (1)
- Flash "nearly matches" SPED on cached workloads while matching or exceeding MP/MT on disk-intensive workloads, and uses only standard APIs. (1)
- AMPED behaves like SPED when requested documents are cached and like MP/MT when requests must be satisfied from disk. (1)
- Evaluation scope stated up front: qualitative and quantitative comparison of AMPED, SPED, MP, MT in a single implementation, plus comparison with Apache and Zeus on real workloads from server logs and on two operating systems. (1)
- The paper's roadmap expands AMPED as "asynchronous multi-process event-driven" in one place (vs "asymmetric" elsewhere), an inconsistency in the paper itself. (1)

## Figure 1: Simplified Request Processing Steps
- Figure 1 shows the sequence Start, Accept Conn, Read Request, Find File, Send Header, Read File/Send Data, End, explicitly labelled "simplified." (Fig. 1)

## 2 Background
- HTTP clients contact the server over TCP: the client opens a TCP connection and sends an HTTP request header specifying the content. (2)
- Static content is stored as disk files; dynamic content is generated on request by auxiliary application programs on the server. The server sends an HTTP response header followed by the data, if applicable, on the client's TCP connection. (2)
- The discussion is restricted to HTTP/1.0 static content on UNIX-like OSes, but all architectures handle dynamic content, and the steps are similar for HTTP/1.1 and Windows NT. (2)
- Accept step: an accept on the server's listen socket creates a new socket for the client connection. (2)
- Read request step: read the HTTP request header from the socket and parse it for the URL and options. (2)
- Find file step: check that the file exists and the client has permissions, and obtain the file's size and last-modification time for the response header. (2)
- Read file / send data: for larger files only part is read and sent at a time, and the two steps repeat until all content is transmitted. (2)
- Every step can block, with specific calls named: socket reads/accepts block if data has not arrived; socket writes block when TCP send buffers are full due to limited network capacity; stat() and open() block until disk accesses complete; read() or touching a memory-mapped region blocks while data is read from disk. The notes classify steps as CPU/network/disk but do not name blocking calls or conditions. (2)
- Conclusion of the background: a high-performance server must interleave the sequential steps of many requests to overlap CPU processing with disk and network; the architecture determines the interleaving strategy. Performance also depends on optimizations such as caching. (2)

## 3 Server Architectures
- The paper treats exactly four architectures: AMPED (proposed) plus existing SPED, MP, MT. (3) [Now stated in the note body (thread-performance-considerations.md, section Experimental Methodology: the comparison is between MP, MT, SPED and AMPED), so not beyond the notes.]

## 3.1 Multi-process
- Each MP process performs all steps of one HTTP request before accepting a new one; servers typically use 20-200 processes. (3.1) [One request at a time per process is now stated in the note body (thread-performance-considerations.md, section Concurrency In The Event-Driven Model); the 20-200 process count is not.]
- Overlap of disk, CPU and network happens naturally because the OS switches to a runnable process when the active one blocks. (3.1)
- Because each process has a private address space, no synchronization is needed to handle different requests. Footnote: the OS still synchronizes internally to accept connections, since the accept queue is shared. The notes mention costly shared state across processes but not the absence of application-level synchronization. (3.1) [The absence of synchronization in MP is now stated in the note's Pai callout (thread-performance-considerations.md, section Best Case Numbers); the accept-queue footnote is not.]
- Downside: optimizations relying on global information, such as a shared cache of valid URLs, are harder in MP. (3.1)

## Figure 2: Multi-Process
- Figure 2 shows Process 1 through Process N, each running the full pipeline sequentially for one request at a time. (Fig. 2)

## Figure 3: Multi-Threaded
- Nothing beyond the notes (the notes' MT diagram shows the same structure).

## 3.2 Multi-threaded
- Each MT thread accepts a new request only after finishing all steps of the current one, mirroring MP's use of a process. (3.2) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology), so not beyond the notes.]
- MT requires kernel threads: when one thread blocks on I/O, other runnable threads in the same address space must remain eligible to run. OSes with only user-level thread libraries, e.g. FreeBSD 2.2.6, cannot effectively support MT servers. The notes say only that MT depends on OS thread support. (3.2)

## 3.3 Single-process event-driven
- SPED uses non-blocking system calls for asynchronous I/O and BSD select or System V poll to detect completed operations. (3.3) [The use of select/poll is now stated in the note body (thread-performance-considerations.md, section Event-Driven Model: How?); the non-blocking calls and the BSD/System V attribution are not.]
- SPED as a state machine: it performs one basic step of one request at a time, interleaving steps of many requests. Each iteration does a select for completed I/O events (new connection arrivals, completed file operations, client sockets that received data or have send-buffer space); for a ready event it completes the corresponding step and initiates the next. (3.3) [Now stated in the note body (thread-performance-considerations.md, sections Event-Driven Model and Concurrency In The Event-Driven Model), so not beyond the notes.]
- The SPED problem: many OSes lack suitable asynchronous disk support. Non-blocking read/write works on sockets and pipes but may block on disk files; both FreeBSD 2.2.6 and Solaris 2.6 behave this way, and the authors believe most UNIX versions do. (3.3)
- Many UNIXes have true async disk I/O APIs, but they are not integrated with select, so network and disk completions cannot be checked together efficiently; open and stat may still block. Existing SPED servers therefore do not use these APIs, and file reads that miss the file cache block the main thread, losing concurrency. (3.3)

## Figure 4: Single Process Event Driven
- Figure 4 shows one process whose event dispatcher drives all steps (accept, read request, find file, send header/read file/send data) for all requests, including disk activity. (Fig. 4)

## 3.4 Asymmetric Multi-Process Event-Driven
- By default the main event-driven process handles all steps; only when a disk operation is necessary (a file "not likely to be in the main memory file cache") does it instruct a helper over an IPC channel such as a pipe. The helper's completion notification arrives via IPC and is detected through select like any other I/O event. (3.4) [Now stated in the note body (thread-performance-considerations.md, sections Helper Threads And Processes and Flash Web Server) and the note's Pai callout (Flash Web Server), so not beyond the notes.]
- AMPED aims to keep SPED's efficiency on everything except disk reads while avoiding SPED's problem with inadequate async disk support, using only widely available OS support. (3.4)
- UNIX APIs used: non-blocking read, write and accept on sockets and pipes; select for completion; mmap to access file data; mincore to check whether a file is in memory. (3.4) [mmap, mincore, pipes and select are now stated in the note body (thread-performance-considerations.md, sections Event-Driven Model: How? and Flash Web Server); the non-blocking read, write and accept calls are not.]
- Zero-copy with process helpers: both the main process and the helper mmap the requested file; the helper touches all pages in its mapping, then notifies the main process that it can transmit without risk of blocking. Using mmap lets helpers initiate disk reads without additional data copying. (3.4) [The mmap, touch and notify mechanism is now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server); the no-additional-copy benefit is not.]

## Figure 5: Asymmetric Multi-Process Event Driven
- Figure 5 shows one event-driven process with an event dispatcher plus Helper 1 through Helper k; the caption says helpers handle "some disk operations." (Fig. 5)

## 4 Design comparison
- Section 4 is an explicitly qualitative comparison of performance characteristics and possible optimizations across the architectures. (4)

## 4.1 Performance characteristics
- Disk operations: in MP and MT only the process or thread causing disk activity blocks; in AMPED only a helper blocks and the server keeps handling requests, the extra cost being IPC between server and helpers; in SPED all user-level processing stops whenever any request needs the disk. (4.1) [The AMPED and SPED blocking behavior is now stated in the note body (thread-performance-considerations.md, sections Helper Threads And Processes and CS Trace); the MP/MT case and the IPC cost are not.]
- Memory effects: memory consumption reduces space for the filesystem cache. SPED is smallest (one process, one stack). MT adds memory and kernel resources proportional to the number of threads, i.e. the maximum number of concurrent requests. AMPED helpers add overhead but have small application-level memory demands and are needed only per concurrent disk operation, not per concurrent request. MP pays a full process per concurrent request, with substantial memory and kernel overhead. (4.1) [That AMPED needs a helper per concurrent blocking I/O rather than an entity per concurrent request is now stated in the note body (thread-performance-considerations.md, section Helper Threads And Processes); the full ordering with SPED smallest and MT proportional to threads is not.]
- Disk utilization: the number of concurrent disk requests determines whether a server can benefit from multiple disks and disk head scheduling. MP/MT can issue one disk request per process/thread, AMPED one per helper; SPED can issue only one at a time and gets neither benefit. (4.1)

## 4.2 Cost/Benefits of optimizations & features
- The architecture affects the feasibility and profitability of optimizations and features; compared qualitatively. (4.2)
- Information gathering (for accounting and performance): MP needs IPC to consolidate data; MT needs per-thread statistics with periodic consolidation or fine-grained synchronization on globals; SPED and AMPED process all requests centrally, needing no synchronization or IPC for shared state. (4.2)
- Application-level caching stores previous results (e.g. response headers, file mappings) but competes with the filesystem cache for physical memory, so it must be applied carefully. (4.2)
- MP uses per-process caches to avoid IPC and synchronization, which increases compulsory misses and wastes memory; MT uses one cache but must synchronize accesses/updates to avoid races; SPED and AMPED use a single cache without synchronization. (4.2)
- Long-lived connections arise from slow-link clients (modems) and HTTP/1.1 persistent connections and commit server resources for the connection's duration. In SPED/AMPED the cost is a file descriptor, application-level connection information and some kernel state; MT and MP add a thread or process per connection. (4.2)

## 5 Flash implementation
- Flash is described as a high-performance AMPED implementation using aggressive caching and other techniques. (5)

## 5.1 Overview
- Flash uses a single non-blocking server process assisted by helper processes; the server process handles all client interaction, interaction with CGI applications, and control of helpers. Helpers perform all actions that may cause synchronous disk activity. (5.1) [That helpers handle only blocking disk I/O and the main process does everything else is now stated in the note body (thread-performance-considerations.md, section Helper Threads And Processes); the CGI interaction is not.]
- Helpers are separate processes rather than kernel threads specifically to stay portable to OSes without kernel threads, such as FreeBSD 2.2.6. (5.1) [Now stated in the note body (thread-performance-considerations.md, section Helper Threads And Processes), except the FreeBSD 2.2.6 example.]
- The server is divided into modules for the request steps of Section 2 and modules for caching. (5.1)
- Three caches: filename (pathname) translations, response headers, and file mappings. The notes cover pathname and header caching and generic file caching, but not the mapped-file cache as a distinct cache. (5.1) [Now stated in the note body (thread-performance-considerations.md, sections Flash Web Server and Impact of Optimizations, which name pathname, mmap file and header caching), so not beyond the notes; the bullet's claim about the mapped-file cache is outdated.]
- Helpers do two jobs: pathname translation and bringing disk blocks into memory. They are spawned dynamically by the server, kept in reserve when idle, operate synchronously, and handle one request at a time. (5.1)
- To minimize IPC, helpers return only a completion notification, not file content they loaded. (5.1)

## 5.2 Pathname Translation Caching
- The cache maps requested names (e.g. "/~bob") to actual disk files (e.g. /home/users/bob/public_html/index.html). (5.2)
- It lets Flash avoid the pathname translation helpers on most requests, reducing processing and the number of translation helpers needed, so the cache's memory is recovered through less memory used by helper processes. (5.2)

## 5.3 Response Header Caching
- The response header contains information about the file and the server. Because it is tied to the file, the header cache needs no separate invalidation: when the mapping cache detects a changed file, the header is regenerated. (5.3)

## 5.4 Mapped Files
- Flash caches memory-mapped files to reduce map/unmap operations. mmap avoids extra data copying and double-buffering but costs system calls to create and remove mappings; keeping unused mappings increases kernel bookkeeping and degrades performance. (5.4)
- The cache works on file "chunks": small files are one chunk, large files many. Mappings are unmapped lazily when too much data is mapped; inactive chunks sit on an LRU free list and are unmapped when the list grows too large. (5.4)
- LRU is chosen to approximate the OS "clock" page replacement algorithm, so Flash maps only what is likely in memory. All mapped pages are tested for residency with mincore() before use. (5.4) [Residency testing with mincore() before use is now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server); the LRU/clock rationale is not.]

## 5.5 Byte Position Alignment
- writev() sends multiple discontiguous memory regions in one call; high-performance servers use it to send the header followed by file data. (5.5) [That writev() sends the header followed by file data is now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server); the general definition is not.]
- When the OS copies writev regions into a contiguous kernel buffer, a header whose length is not a multiple of the machine word size makes every subsequent region's copy misaligned; the extra cost is proportional to the data copied. (5.5) [The misalignment is now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server); the cost proportional to the data copied is not.]
- Flash aligns response headers on 32-byte boundaries and pads their lengths to multiples of 32 bytes by adding characters to variable-length header fields (e.g. server name). 32 bytes rather than word size targets systems with 32-byte cache lines that may be optimized for copies on cache boundaries. The notes' "optimizations that take advantage of the networking hardware and the network interface card" (DMA alignment, scatter-gather) does not describe this. (5.5) [Padding headers to multiples of 32 bytes for 32-byte cache lines is now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server), so the bullet's last sentence is outdated; the 32-byte boundary alignment and the padding via variable-length fields are not.]

## 5.6 Dynamic Content Generation
- For a dynamic request, the server forwards it via a pipe to the corresponding CGI-bin process, forking one if none exists. Output is read from the CGI pipe descriptor and transmitted like static content. (5.6)
- CGI processes are kept persistent, amortizing creation cost over many requests, similar to FastCGI. Because CGI runs in separate processes, it can block on disk or compute arbitrarily long without affecting the server. (5.6)

## 5.7 Memory Residency Testing
- mincore() is available in most modern UNIXes. On OSes without it but with mlock() (e.g. Compaq Tru64 UNIX, formerly Digital Unix), Flash could lock pages and control its own file cache, eliminating residency testing. (5.7)
- With neither, a feedback heuristic could run the clock algorithm to predict which cached pages are resident, adapting to available file-cache memory using performance counters for page faults and/or disk accesses. (5.7)

## 6 Performance Evaluation
- Three goals: compare architectures on real workloads; compare Flash with Apache and Zeus on synthetic and real workloads; quantify the impact of Flash's optimizations. (6)
- To eliminate implementation differences, the same Flash code base builds four servers: Flash (AMPED), Flash-MT, Flash-MP, Flash-SPED, created by replacing Flash's event/helper dispatch mechanism; all else, including optimizations, is identical. The notes list the systems but not this method or rationale. (6) [That all compared implementations except Apache share Flash's optimizations over otherwise identical code is now stated in the note body (thread-performance-considerations.md, section Experimental Methodology); building them by replacing only the dispatch mechanism is not.]
- Reference points: Zeus v1.30 (SPED) and Apache v1.3.1 (MP). (6) [Zeus v1.30 as SPED is now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology); Apache v1.3.1 is not.]
- Flash-MP and Apache use 32 server processes; Flash-MT uses 64 threads. (6) [The 64 Flash-MT threads are now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology); the 32 processes are not.]
- Zeus runs as a single process for synthetic tests and in a vendor-advised two-process configuration for real-workload tests; since SPED Zeus can block on disk, two processes help even on a uniprocessor by overlapping computation and disk I/O. (6) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology), so not beyond the notes.]
- Flash and Flash-MT: 128 MB mapped-file cache limit, 6000-entry pathname cache. Each Flash-MP process: 4 MB mapped-file cache, 200-entry pathname cache, smaller because caches are replicated per process. (6)
- OSes: Solaris 2.6 and FreeBSD 2.2.6. Hardware: 333 MHz Pentium II, 128 MB memory, multiple 100 Mbit/s Ethernet interfaces; switched Fast Ethernet to the client machines. (6)
- Client software: an event-driven program simulating multiple HTTP clients (Banga and Druschel); each simulated client issues requests as fast as the server can handle them. (6)

## 6.1 Synthetic Workload
- Clients repeatedly request the same file, with file size varied per test; the file stays cached, so servers run at highest capacity. (6.1) [Now stated in the note body (thread-performance-considerations.md, section Best Case Numbers), so not beyond the notes.]
- Left graphs plot total output bandwidth vs file size; right graphs plot connection rate for small files separately. Run on Solaris (Fig. 6) and FreeBSD (Fig. 7). The notes show one bandwidth plot only. (6.1)
- Finding: architecture choice has little impact on a trivial cached workload. (6.1) [Now stated in the note body (thread-performance-considerations.md, section Best Case Numbers: all implementations had similar results), so not beyond the notes.]
- Flash variants compare favorably to Zeus, affirming the absolute performance of the Flash implementation. (6.1)
- Apache is significantly lower on both OSes and over the entire range of file sizes; the paper hedges that Zeus "presumably" also uses aggressive optimizations. (6.1)
- Zeus's anomaly on FreeBSD for file sizes between 10 and 100 KB appears to stem from the byte alignment problem of 5.5. (6.1) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Best Case Numbers), so not beyond the notes.]
- All servers perform substantially better on FreeBSD than Solaris; relative performance is not strongly affected by the OS. (6.1)

## Figure 6: Solaris single file test
- Lines: SPED, Flash, Zeus, MT, MP, Apache. Bandwidth axis 0-120 Mb/s over 0-200 KB file sizes; connection rate axis 0-1200 req/s over 0-20 KB. Caption: architecture seems to have little impact; aggressive optimizations in Flash and Zeus make them outperform Apache. (Fig. 6)

## Figure 7: FreeBSD single file test
- Lines: SPED, Flash, Zeus, MP, Apache (no MT, since FreeBSD 2.2.6 lacks kernel threads). Bandwidth axis 0-250 Mb/s over 0-200 KB; connection rate axis 0-3500 req/s over 0-20 KB. (Fig. 7)
- Caption: FreeBSD's higher network performance magnifies the gap between Apache and the rest compared with Solaris; the Zeus curve shape between 10 and 100 KB is likely the byte alignment problem. (Fig. 7)

## 6.2 Trace-based experiments
- Motivation: the single-file test indicates maximum cached performance but little about real workloads, so request streams are generated by replaying access logs from real servers. (6.2)
- Owlnet trace detail: a Rice server hosting personal Web pages for about 4500 students and staff. CS trace: Rice Computer Science department server. Fig. 8 results are on Solaris. (6.2)
- Comparison with Flash-MP shows Apache's lowest-place result is only partly due to its MP architecture and mostly due to lack of aggressive optimizations. (6.2)
- Owlnet's smaller data set gives better cache locality, so Flash-SPED does relatively much better on it, while MP does well on the more disk-intensive CS trace. (6.2) [Now stated in the note body (thread-performance-considerations.md, sections Owlnet Trace and CS Trace), so not beyond the notes.]
- Owlnet has high locality but a smaller average transfer size than CS, so bandwidth numbers end up roughly comparable. (6.2)
- Second experiment (absent from the notes): Rice ECE department access logs truncated to achieve a given data set size, replayed in a loop by clients, giving a range of data set (and working set) sizes from 15 to 150 MB. (6.2, Figs. 9-10)
- Both trace experiments use two client machines with 32 clients each. (6.2)
- Results on FreeBSD (Fig. 9) and Solaris (Fig. 10), metric total output bandwidth. Requests/sec is not used because truncation changes the request size distribution, making requests/sec fluctuate, while bandwidth is less sensitive. (6.2)
- All servers decline as the data set grows, with a significant drop when the working set exceeds the effective main-memory cache; beyond that they are essentially disk-bound. (6.2)
- Flash is very competitive with Flash-SPED on cached workloads and meets or exceeds MP on disk-bound workloads, confirming AMPED combines the best of the other architectures; this was the central design goal. (6.2) [The comparison is now stated in the note's Pai callout and body (thread-performance-considerations.md, section Summary of Performance Results); the "central design goal" framing is not.]
- SPED's quick deterioration as disk activity rises confirms Section 4's reasoning; SPED-based Zeus shows the same behavior, though its absolute performance is below the Flash-derived servers. (6.2)
- Flash-MP falls significantly short of the other architectures on cached workloads, likely due to its smaller per-process user-level caches. (6.2)
- OS choice matters: Solaris results are up to 50% lower than FreeBSD; the OS also affects relative performance, but trends are less clear. (6.2)
- Flash beats MP disk-bound because it is more memory-efficient and causes less context switching: it needs only enough helpers to keep the disk busy rather than a process per connection, and helpers need little application memory, so fewer and smaller processes leave more memory for the filesystem cache. The notes give only the memory point. (6.2) [Now stated in the note body (thread-performance-considerations.md, section Summary of Performance Results), which gives both the memory and the context-switching reasons, so not beyond the notes; the bullet's last sentence is outdated.]
- Zeus on FreeBSD drops only after the data set exceeds 100 MB, earlier for others, apparently because Zeus prioritizes small-document requests, starving large ones under full load and shrinking its effective working set; Solaris's lower overall performance masks this. (6.2)
- Zeus's two-process configuration gives it a slight advantage over single-process Flash-SPED, since one process can serve while the other blocks on disk. (6.2) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology), so not beyond the notes.]
- No Flash-MT results on FreeBSD 2.2.6 because it lacks kernel threads. (6.2)

## Figure 8: Performance on Rice Server Traces/Solaris
- Two bar charts (CS trace, Owlnet trace), each 0-40 Mb/s, with bars for Apache, MP, MT, SPED, Flash; Zeus is not included. (Fig. 8)

## Figure 9: FreeBSD Real Workload
- Bandwidth (0-200 Mb/s) vs data set size 15-150 MB for SPED, Flash, Zeus, MP, Apache. Caption: SPED suits cached workloads; when the working set fits in cache Flash mimics Flash-SPED; Flash-SPED drops drastically on disk-bound workloads. (Fig. 9)

## Figure 10: Solaris Real Workload
- Bandwidth (axis 30-80 Mb/s) vs data set size 15-150 MB for SPED, Flash, Zeus, MT, MP, Apache. (Fig. 10)
- Caption: Flash-MT is comparable to Flash for both in-core and disk-bound workloads, achieved only by carefully minimizing lock contention, which added code complexity; without it, disk-bound results resembled Flash-SPED. (Fig. 10)

## 6.3 Flash Performance Breakdown
- Setup identical to the FreeBSD single-file test (cached document of a given size); measures throughput for all combinations of the three main optimizations: pathname translation caching, mapped-file caching, response header caching. (6.3)
- Each optimization significantly improves throughput for cached content; pathname translation caching gives the largest benefit. (6.3)
- Because each optimization removes a per-request cost, the impact is strongest for small documents. (6.3)

## Figure 11: Flash Performance Breakdown
- Connection rate (axis to 3500 req/s) vs file size 0-20 KB, eight lines: all (Flash), path & mmap, path & resp, path only, mmap & resp, mmap only, resp only, no caching. (Fig. 11)
- Caption: without optimizations, Flash's small-file performance would drop by half. (Fig. 11)

## 6.4 Performance under WAN conditions
- The whole experiment is absent from the notes. LAN benchmarks miss that real clients use WANs, whose limited bandwidth and packet loss increase HTTP connection duration; at a given request rate a real server therefore handles many more concurrent connections than in a LAN test (Mogul). (6.4)
- The number of concurrent connections can significantly affect server performance (Banga and Druschel). (6.4)
- Method: persistent connections simulate long-lived WAN connections on the LAN testbed; ECE logs replayed with a 90 MB data set to expose limited file-cache effects; Solaris; varying number of simultaneous clients. (6.4)
- SPED, AMPED and MT initially rise with more connections, likely from added concurrency and aggregation effects, e.g. more completed I/O events per select call amortizing its overhead. (6.4)
- Beyond 200 concurrent connections SPED and AMPED flatten, MT declines gradually due to per-thread switching and space overhead, and MP declines significantly due to per-process overhead. (6.4)

## Figure 12: Adding clients
- Bandwidth (axis to 120 Mb/s) vs 0-500 simultaneous clients for SPED, Flash, MT, MP (no Zeus or Apache). Caption: low per-client overheads of MT, SPED and AMPED give stable performance; multiple application-level caches and per-process overheads make MP drop. (Fig. 12)

## 7 Related Work
- Several researchers have analyzed the processing costs of the individual HTTP request-serving steps and proposed improvements. (7)
- James Hu et al. analyze Web server optimizations, comparing a multi-threaded architecture with a thread-pool architecture on UNIX and Windows NT using the WebStone benchmark. (7)
- Nahum et al. compare high-performance approaches with new socket APIs on single-file tests and other benchmarks. (7)
- Yiming Hu et al. analyze an earlier Apache and implement optimizations that help especially small requests. (7)
- Yates et al. measure the demands a server places on the OS for various workload types and service rates. (7)
- Banga et al. examine OS support for event-driven servers and propose new APIs to remove bottlenecks with large numbers of concurrent connections (resource containers). (7)
- AMPED resembles Thoth's "multi-process structuring" (Thoth being a portable operating system and environment): groups of processes ("teams") cooperate by passing messages; one process waits synchronously for an activity and reports it to an event-driven server. Flash's disk helpers play that role for disk completions. (7)
- Harvest/Squid also combines an event-driven server with helper processes: it keeps its own DNS cache and uses "dnsserver" processes for gethostbyname() calls, so a blocking DNS lookup affects only the dnsserver process. Unlike Flash, Harvest uses select() for non-blocking file access, which most UNIXes falsely report as non-blocking; Harvest also tries to reduce disk metadata operations. (7)
- Caching policies: Arlitt et al. derive policies from server logs and cross-server similarities; Cao et al.'s Greedy DualSize uses access frequency and file size for replacement; other work characterizes Web workloads (Crovella and Bestavros self-similarity; Manley and Seltzer). (7)
- Copy avoidance, motivated by data copying in the OS being a significant cost for large files: Thadani et al. propose an API to read and send memory-mapped files without copying; IO-Lite extends fbufs to unify filesystem, networking, IPC and application buffers; Engler et al.'s Cheetah server uses exokernel interaction to eliminate copying and streamline small requests; Lava applies similar techniques in a microkernel. (7)
- Multi-machine approaches: multiple server nodes in parallel (e.g. DNS load balancing, Cisco LocalDirector, IBM eNetwork dispatcher, ONE-IP, cluster-based services, locality-aware request distribution) and sharing memory across machines (cooperative caching, global memory management, cooperative prefetching and caching). (7)

## 8 Conclusion
- Quantified final claims: Flash exceeds Zeus by up to 30% and Apache by up to 50% on real workloads, and nearly matches or exceeds other architectures across a wide range of realistic workloads. (8)
- Restates that architectures were implemented from the same code base to evaluate the concurrency architecture's impact, and that optimization contributions were measured. (8)

## Acknowledgments
- Thanks Erich Nahum, Jeff Mogul and anonymous reviewers for comments; Michael Pearlman for the Solaris testbed configuration; Zeus Technology for its server software and Damian Reeves for feedback and technical assistance with it. Flash derives some infrastructure from Jef Poskanzer's thttpd server. Funded by NSF grants, a Texas TATP grant and an IBM Partnership Award. (Acknowledgments)

## References
- 32 references; Apache [1] and Zeus [32] are cited by URL; the client load generator is Banga and Druschel, "Measuring the capacity of a Web server" (USITS 1997) [3]; the WAN connection-duration claim cites Mogul's DEC WRL report [24]. (References)

## Notes vs paper discrepancies
Each item was checked against the paper, the lecture as reconstructed from independent student note sets and lecture slide screenshots (no lecture transcript was retrievable), and third-party references; sources are listed under "Discrepancy sources". Verdicts: PAPER CONFIRMED, NOTES WRONG (the notes depart from the paper and the lecture does not support them); LECTURE FRAMING (the notes reproduce the lecture and the paper differs); NOT A REAL DISCREPANCY.
- Memory footprint ordering: the lecture and the note say Flash has a smaller memory footprint than the MT and MP implementations (and the note adds that SPED and AMPED Flash have comparable footprints). The paper gives the full ordering: SPED has the smallest (one process, one stack); AMPED adds small helpers. Flash wins disk-bound because it is smaller than MP/MT while not blocking like SPED. (4.1, 6.2)
  - Verdict: NOT A REAL DISCREPANCY, the lecture slide says "smaller mem footprint" (relative to MT/MP), which the note reports faithfully, and the Princeton COS518 presentation gives the paper's ordering with SPED smallest.
- Lecture says SPED "smokes" Flash on cached data (slide: "SPED >> AMPED Flash"). The paper says Flash-SPED "slightly outperforms" Flash and Flash is "very competitive" with it. (6.1, 6.2) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Summary of Performance Results).]
  - Verdict: LECTURE FRAMING, the summary slide says "SPED >> AMPED Flash" when data is in cache, and third parties (MIT 6.824, Mazieres's notes, Princeton COS518) side with the paper that SPED and AMPED are roughly tied.
- Lecture places Zeus's anomaly as a drop after about 125 KB. The paper locates it on FreeBSD between 10 and 100 KB and attributes it to the writev byte-alignment problem. (6.1, Fig. 7) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Best Case Numbers).]
  - Verdict: LECTURE FRAMING, the lecture shows the Solaris graph (where Zeus dips near 125-150 KB) and says only "Zeus has anomaly", and no third party discusses the Zeus curve, so the figure is a reading of the displayed graph rather than the anomaly the paper describes.
- Lecture describes Zeus as a "SPED implementation with two processes." It was single-process for synthetic tests and two-process only for real-trace tests. (6) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology).]
  - Verdict: LECTURE FRAMING, the slide lists "Zeus (SPED w/ 2 processes)", and third parties (Mazieres's notes, MIT 6.824) describe Zeus as SPED, consistent with the paper's per-experiment configuration.
- Lecture describes the compared MT implementation as boss/workers. The paper's MT model has each thread handle one request through all its steps, analogous to a process in MP (3.2, Fig. 3); Flash-MT uses 64 threads and no boss thread is described (6). [Now stated in the note's Pai callout (thread-performance-considerations.md, section Experimental Methodology).]
  - Verdict: LECTURE FRAMING, the slide lists "MT (boss-worker)", and third parties (Princeton COS518, MIT 6.824) side with the paper's per-request threads.
- Lecture's mincore/mmap sequence (as reproduced in the notes: "The helper reads the file in memory via `mmap` and then the dispatcher checks via `mincore`") is reversed. The main process checks residency with mincore first; only if pages are not resident is a helper dispatched, which mmaps and touches the pages, then notifies. (3.4, 5.4) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server).]
  - Verdict: LECTURE FRAMING, the slide lists the mmap bullet before the mincore bullet (whose "to decide local handler or helper" clause implies the check comes first), and third parties (Mazieres's notes, MIT 6.824) side with the paper's check-first order.
- Lecture attributes the MT/MP lag on the single-file test to "the extra synchronization requirements and the cost of context switching." The paper attributes it to extra kernel overhead (context switching, etc.) only; Flash-MP's private address spaces need no synchronization. (3.1, 6.1) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Best Case Numbers).]
  - Verdict: LECTURE FRAMING, the slides say "MT/MP extra sync & context switching", and third parties are silent or mildly side with the paper, which names only kernel overhead for this result (synchronization is a real cost for MT, not MP).
- The note, following the lecture, says Flash "makes some optimizations that take advantage of the networking hardware and the network interface card" (DMA alignment, scatter-gather). The paper's corresponding optimization (5.5) targets OS kernel copy alignment and CPU cache lines, not network hardware. (5.5) [Now stated in the note's Pai callout (thread-performance-considerations.md, section Flash Web Server).]
  - Verdict: LECTURE FRAMING, the slide lists "alignment for DMA" and "DMA w/ scatter-gather", and third parties (Princeton COS518, Mazieres's notes) side with the paper's header padding for aligned copies, with no mention of DMA or network hardware.

## Covered in the notes
- Basic request steps and their CPU/network/disk character; MP, MT and event-driven models with basic pros and cons (memory footprint, context switches, synchronization, OS thread support).
- MT threads each perform all steps and share state, requiring synchronization; SPED avoids context switching and synchronization in a single thread of control.
- SPED, AMPED and AMTED concepts (helpers as threads or processes); helpers emulate async I/O; helper communication via pipes/sockets so select/poll still work; helpers as processes when the kernel lacks threads, giving portability.
- Flash uses mmap, mincore and pipes; pathname-translation and response-header caching; caching of data and computation.
- Experimental design: systems compared, CS vs Owlnet traces (large vs fits in memory), synthetic single-file best case, bandwidth and connection-rate metrics vs file size.
- Qualitative results: similar single-file results with SPED slightly ahead due to the residency check (also the cause of the cached-workload gap in trace results), MT/MP lagging from context switching, Flash highest on both traces, Apache lowest for lack of optimizations, Flash best on traces, SPED collapsing on the disk-bound CS trace, optimizations raising connection rate.


## Discrepancy sources
- <https://www.usenix.org/conference/1999-usenix-annual-technical-conference/flash-efficient-and-portable-web-server> (USENIX 1999 paper page)
- <https://www.usenix.org/legacy/events/usenix99/full_papers/pai/pai.pdf> (USENIX 1999 paper PDF)
- <https://dl.acm.org/doi/10.5555/1268708.1268723> (ACM DL entry)
- <https://github.com/ivyivylynn/OS_Study_Notes> and <https://raw.githubusercontent.com/ivyivylynn/OS_Study_Notes/master/P2L5.md> (lecture slide screenshots under <https://raw.githubusercontent.com/ivyivylynn/OS_Study_Notes/master/images/P2L5/>: 30e7689c.png, 39009f50.png, 58d7712e.png, 2d014ac1.png, 3bad5a59.png, d0bb1117.png, 883154e3.png, be178580.png)
- <https://github.com/stevenxchung/Introduction-to-Operating-Systems> and <https://raw.githubusercontent.com/stevenxchung/Introduction-to-Operating-Systems/master/Lesson%2009%20-%20Thread%20Performance%20Considerations/lesson-09-notes.md>
- <https://github.com/tewidis/GIOS> (markdown/thread_performance_considerations.md)
- <https://github.com/lkrych/gios_notes> (lectures/p2_l5_thread_performance_considerations.md)
- <https://www.omscs-notes.com/operating-systems/thread-performance-considerations/> (the notes as published; not independent)
- <https://pdos.csail.mit.edu/archive/6.824-2001/lecnotes/flash.txt>, <https://pdos.csail.mit.edu/archive/6.824-2004/handouts/flash.txt>, <https://pdos.csail.mit.edu/archive/6.824-2005/handouts/flash.txt>, <https://pdos.csail.mit.edu/archive/6.824-2006/notes/flash.txt> (MIT 6.824 Flash lecture notes)
- <http://www.scs.stanford.edu/nyu/03sp/notes/l4d.txt> (Mazieres, NYU Flash notes, Stanford-hosted)
- <https://www.cs.princeton.edu/courses/archive/fall15/cos518/studpres/flash.pdf> (Princeton COS518 student presentation)
- <http://www.sosp.org/2001/papers/welsh.pdf> (SEDA, SOSP 2001)
- <https://en.wikipedia.org/wiki/C10k_problem> (checked; no Flash-specific content)
