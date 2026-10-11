---
id: operating-systems-papers-beyond-notes-popek-goldberg
title: "Popek & Goldberg, Formal Requirements for Virtualizable Third Generation Architectures: Beyond the Notes"
course: operating-systems
lecture: papers-beyond-notes-popek-goldberg
---

# Popek & Goldberg: everything not in the notes

Everything in the paper that the lecture notes do not state, plus the places where the paper contradicts or sharpens them; validated against the paper text. The reference point is the lecture notes: the `virtualization.md` note now carries `> **Paper (Popek & Goldberg):**` callouts for the lecture-framing discrepancies listed under "Notes vs paper discrepancies", so some gaps below are now annotated in the note. Paper: <https://s3.amazonaws.com/content.udacity-data.com/courses/ud923/references/ud923-popek-goldberg-paper.pdf>.

The paper appeared in Communications of the ACM, Volume 17, Number 7, July 1974, pages 412-421, and is a revised version of a paper from the Fourth ACM Symposium on Operating Systems Principles, 1973. Authors: Gerald J. Popek (UCLA) and Robert P. Goldberg (Honeywell Information Systems and Harvard). Citations below give the section heading and, where useful, the printed page number.

**OCR caveat.** The Udacity-hosted text is an OCR of the 1974 typescript and is noticeably garbled in the formal passages. The notation for the behavior-sensitivity definition is mangled (stray glyphs such as "del r", "elr @ x", "@," for the shift operator, "psw" lowercased, "1/0" for I/O, "ppp-10"/"pnp-10"/"DEC pPpp-10" for DEC PDP-10, "ppp-11" for PDP-11, "LBar"/"Lpsw" for register-load mnemonics, "yrst 1" / "JRST 1" for the PDP-10 JRSTF-style return-to-user instruction, "1BM" for IBM). Where this file states a formal definition it has been reconstructed and cross-checked against the Wikipedia "Popek and Goldberg virtualization requirements" summary and the standard restatement in course notes (Rutgers CS553, Harvard CS161); any residual uncertainty is flagged inline.

## Abstract and key words
- Virtual machine systems had been implemented on a limited number of third-generation systems, the paper's example being CP-67 on the IBM 360/67. (abstract)
- From earlier empirical studies it was already known that some third-generation machines, the paper's example being the DEC PDP-10, cannot support a virtual machine system. The paper's job is to replace that empirical knowledge with a formal, checkable condition. (abstract)
- Key words and CR categories are listed: operating system, third generation architecture, sensitive instruction, formal requirements, abstract model, proof, virtual machine, virtual memory, hypervisor, virtual machine monitor; CR categories 4.32, 4.35, 5.21, 5.22. The term "hypervisor" is already present in 1974. (abstract)
- Funding: U.S. Atomic Energy Commission and the U.S. Air Force (Electronic Systems Division, Hanscom Field). (front matter)

## Section 1: Virtual machine concepts
- The paper's one-sentence definition, which the lecture quotes: a virtual machine is "an efficient, isolated duplicate of the real machine." (Section 1) [Stated in the note body (virtualization.md, section Defining Virtualization), so not beyond the notes.]
- The three VMM characteristics are stated as an *essentially identical* environment, *efficiency*, and *complete resource control*. The lecture renames these fidelity, performance, and safety/isolation; the paper's wording is the original. (Section 1) [The lecture's names are in the note body and the paper's Section 5 names (equivalence, efficiency, resource control) are in the note's Popek & Goldberg callout; the Section 1 wording is not.]
- "Essentially identical" is defined precisely: any program run under the VMM has an effect identical to running on the bare machine, with two explicit exceptions, differences from resource availability (for example, a VM given less memory) and differences from timing dependencies (because of the intervening software and other concurrent VMs). (Section 1) [The identical effect and its two exceptions (timing, resource availability) are now stated in the note's Popek & Goldberg callout; the parenthetical examples are not.]
- The identical-environment requirement is what excludes an ordinary time-sharing operating system from being a VMM. (Section 1) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes.]
- Efficiency is defined operationally: a statistically dominant subset of the virtual processor's instructions must execute directly on the real processor with no VMM intervention. This explicitly rules out traditional emulators and complete software interpreters (simulators) from being VMMs. The lecture's "VirtualBox is a VM but the JVM and an emulator are not" quiz is exactly this point. (Section 1) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes.]
- Resource control is defined by two conditions: (1) a program running in the created environment cannot access any resource not explicitly allocated to it, and (2) under certain circumstances the VMM can regain control of resources already allocated. (Section 1) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes.]
- The paper distinguishes the virtual machine (the environment created) from the VMM (the software creating it), and notes a VMM is not necessarily a time-sharing system, though it may be. (Section 1)
- Isolation is defined as implied by the identical-effect requirement holding regardless of other activity on the real computer. (Section 1)
- The paper separates the virtual machine concept from virtual memory: virtual memory (via segmentation and paging) is only one possible ingredient of a virtual machine, which also has a virtual processor and possibly other virtual devices. (Section 1)

## Section 2: A model of third generation machines
- The model is an idealized third-generation machine like the IBM 360, Honeywell 6000, or DEC PDP-10, with a processor and linear, uniformly addressable memory. (Section 2)
- Simplifying assumption: I/O instructions and interrupts are assumed not to exist in the formal model, though the paper says they can be added as extensions. The entire theory is built without I/O, which the lecture never mentions. (Section 2)
- The processor has two modes only, supervisor and user; the full instruction set is available in supervisor mode but not in user mode. This two-mode model predates the four-ring x86 world the lecture describes. (Section 2)
- Memory is addressed through a relocation-bounds register R = (l, b): l is the base (relative address 0 maps to absolute l), b is the absolute size of the virtual memory (not the largest valid address). To address all of memory, set relocation 0 and bounds q - 1. (Section 2)
- Address development rule: for an instruction producing address a, if a + l >= q then memory trap, else if a >= b then memory trap, else use E[a + l]. (Section 2)
- Machine state has exactly four components, S = (E, M, P, R): executable storage E (size q), processor mode M in {s, u}, program counter P (relative to R), and relocation-bounds register R. (Section 2)
- The triple (M, P, R) is the program status word (PSW), assumed to fit in one storage location for proof convenience; E[0] holds the old PSW and E[1] the new PSW. (Section 2)
- An instruction is modeled as a function i: C to C over the finite set of states C. (Section 2)
- The relocation register is assumed active in both supervisor and user mode, a slight departure from most real relocation systems, chosen for simplicity and stated not to affect the result. (Section 2)
- Trap definition: an instruction traps when it leaves storage unchanged except that E[0] receives the PSW in effect before the instruction and the next PSW is taken from E[1]; typically the new mode is supervisor and R = (0, q-1). A trap atomically saves state and transfers control to a prespecified routine. (Section 2)
- The definition could be relaxed to allow the trap to take effect immediately after or some instructions later, as long as state is recorded reversibly. (Section 2)
- A *memory trap* is a trap caused by an instruction trying to develop an address beyond the bounds in R or beyond physical memory. (Section 2)

## Section 3: Instruction behavior (the instruction classification)
- *Privileged* instruction: i is privileged iff for any pair of states that differ only in mode (one supervisor, one user) and neither memory-traps, the user-mode execution traps and the supervisor-mode execution does not. This is the "privileged instruction trap." (Section 3) [Now stated informally in the note's Popek & Goldberg callout (traps in user mode but not in supervisor mode); the formal pair-of-states condition is not.]
- The paper insists a privileged instruction must *trap* in user mode; merely NOP-ing it without trapping does not count, and would be better called a "user mode NOP." The lecture's loose phrase "privileged instructions that do not trap" (for the 17 x86 instructions) is at odds with this definition. (Section 3) [That a privileged instruction must trap and that the lecture's phrase is loose are now stated in the note's Popek & Goldberg callout; the "user mode NOP" term is not.]
- Privileged instructions are a property of the machine, independent of virtualization, readable from the principles of operation. (Section 3)
- Example privileged instructions: System/360 LPSW (load PSW); Honeywell 6000 LBAR and DEC PDP-10 DATAO APR (load relocation/base register). (Section 3)
- *Control sensitive* instruction: i is control sensitive if there is a state where executing i (without memory-trapping) either changes the amount of memory resources available or changes the processor mode without going through the memory-trap sequence. The example privileged instructions above are also control sensitive; another is the PDP-10 return-to-user-mode instruction. (Section 3) [The definition is now stated in the note's Popek & Goldberg callout; the examples are not.]
- *Behavior sensitive* instruction: i is behavior sensitive if its effect (the resulting memory contents or program counter) depends on the value of the relocation-bounds register (its location in real memory) or on the processor mode. The paper splits this into *location sensitivity* (behavior depends on real-memory location) and *mode sensitivity* (behavior depends on mode). (Section 3) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes.]
- Example behavior-sensitive instructions: location sensitive, IBM 360/67 LRA (load real address); mode sensitive, DEC PDP-11/45 MFPI (move from previous instruction space), which forms its effective address from mode-dependent information. (Section 3)
- *Sensitive* = control sensitive or behavior sensitive; an instruction that is not sensitive is *innocuous*. The lecture uses "privileged" throughout and never introduces the sensitive/innocuous vocabulary, which is the paper's central contribution. (Section 3) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes (the note no longer lacks this vocabulary).]
- Footnotes refine the model: machines whose ADD/DIVIDE trap on exceptions should have those traps excluded from the control-sensitivity definition (footnote 2); the processor is deliberately not treated as a resource, so a HALT may execute directly, which would be unacceptable under VM time-sharing (footnote 3); the behavior-sensitivity result still holds if restricted to the mode case, since relocation changes in supervisor mode do not affect user-mode VM code (footnote 5). (Section 3)

## Section 4: The virtual machine monitor (the construction)
- The VMM is a *control program* CP = (D, A, {v_i}) with three module groups: a *dispatcher* D whose first instruction sits at the hardware trap target; an *allocator* A that decides which resources a VM gets and keeps VMs and the VMM separate (and keeps multiple VMs from sharing the same resource); and a set of *interpreter* routines {v_i}, one per privileged instruction, each simulating the trapped instruction's effect. The lecture's "trap-and-emulate" is exactly this; the dispatcher/allocator/interpreter decomposition is not in the notes. (Section 4) [The dispatcher / allocator / interpreter decomposition is now stated in the note's Popek & Goldberg callout; the allocator's job of keeping the VMM and multiple VMs apart is not.]
- The allocator is invoked by the dispatcher whenever a privileged instruction would change the machine resources of the VM (the primary example being an attempt to reset the relocation-bounds register R). (Section 4) [That the allocator is invoked whenever a trapped instruction would change a VM's resources is now stated in the note's callout; the dispatcher's role and the relocation-register example are not.]
- By convention the control program runs in supervisor mode and all other programs run in user mode; one control-program location records the simulated mode of the virtual machine. (Section 4)

## Section 5: The virtual machine properties (formal restatement)
- The three properties are restated formally for an arbitrary program running with the control program resident:
  - *Efficiency*: all innocuous instructions execute directly on the hardware with no VMM intervention. (Section 5)
  - *Resource control*: it must be impossible for the program to affect the system resources available to it; the allocator is invoked on any attempt. (Section 5)
  - *Equivalence*: any program K performs indistinguishably from running without the control program, with the two exceptions of timing and resource availability. (Section 5) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes.]
- The resource-availability exception is handled by reframing the VM as a *smaller* version of the real machine (logically identical, with fewer resources); equivalence is then guaranteed against a smaller real machine. (Section 5)
- Formal definition of a VMM: any control program satisfying efficiency, resource control, and equivalence. The virtual machine is then the environment a program sees under that VMM. (Section 5)

## Section 5-6: Theorem 1 and its proof
- **Theorem 1**: "For any conventional third generation computer, a virtual machine monitor may be constructed if the set of sensitive instructions for that computer is a subset of the set of privileged instructions." This is the result the whole lecture rests on, stated exactly. (Section 5-6) [Now stated in the note's Popek & Goldberg callout, so not beyond the notes.]
- The theorem is a *sufficient* condition, not necessary, and is noted as easy to check and easy for hardware designers to use as a design requirement. (Section 6)
- The equivalence proof uses a *virtual machine map* f: C_0 to C_1, a one-one homomorphism from the states of the real machine (without VMM) to the states with VMM, with respect to all finite instruction sequences; its left inverse is g. (Section 6)
- A concrete *standard VM map* is given: the control program occupies the first k locations of physical memory, a VM occupies the next w locations with k + w <= q, and the map fixes the relocation to shift guest addresses by k, forces user mode, and so on. (Section 6)
- Equivalence is defined via *halting*: starting the two machines in S1 and f(S1), the environments are equivalent iff whenever the real machine halts in S2, the virtual machine halts in f(S2). Halts (not instruction counts) are the comparison points because the VMM may interpret an instruction with a long sequence. (Section 6)
- Proof sketch: construct the CP; the only non-obvious part is providing interpreter routines for all privileged instructions, which is shown to exist by an *existence argument*, a (possibly enormous) state-transition table per privileged instruction, made finite by limiting the size w of real memory. The paper stresses this is a last resort and that real systems use far simpler routines. (Section 6)
- Resource control and efficiency are "trivially dispensed with" given the subset condition; only equivalence needs real work, done via Lemmas 1-3 in the appendix. (Section 6)
- The paper explicitly discusses why the *necessity* direction fails in general: a machine with location-sensitive instructions may still be virtualizable if the VMM sits in high memory and lets guests run unrelocated; and an instruction that is not strictly privileged but still traps on an undesirable action (for example, one that can only *decrease* the bounds from user mode) can be acceptable. (Section 6)

## Section 7: Recursive virtualization
- **Theorem 2**: a conventional third-generation computer is *recursively virtualizable* if it is (a) virtualizable and (b) a VMM without timing dependencies can be constructed for it. Recursive virtualization means running a copy of the VMM under itself, repeatedly, until resources (memory) are exhausted. None of this is in the notes. (Section 7)
- The only programs excluded from the "identically performing" class are resource-bound or timing-dependent ones; memory is the only resource bound in the skeletal model, and it just limits recursion depth. (Section 7)

## Section 8: Hybrid virtual machines (HVM)
- Because very few third-generation architectures were actually virtualizable, the paper relaxes the definition to a *hybrid virtual machine* (HVM), which interprets more instructions and so is less efficient but applies to more machines. (Section 8)
- To state the relaxed condition, sensitivity is split by mode: an instruction is *user sensitive* if it is control or behavior sensitive in some user-mode state, and *supervisor sensitive* if so in some supervisor-mode state. (Section 8)
- **Theorem 3**: an HVM monitor can be constructed for any conventional third-generation machine in which the set of *user-sensitive* instructions is a subset of the privileged instructions. In an HVM monitor, all instructions executed in virtual supervisor mode are interpreted; otherwise it is like a VMM. (Section 8)
- Worked example: the DEC PDP-10 return-to-user-mode instruction (rendered "yrst 1" / "JRST 1" in the OCR, the JRSTF-family instruction) is supervisor-control-sensitive but not privileged, so the PDP-10 cannot host a VMM; but since all its user-sensitive instructions are privileged, it can host an HVM monitor. This is the formal version of the "PDP-10 cannot be virtualized" claim from the abstract. (Section 8)

## Section 9: Conclusion
- The paper positions itself against prior authors who had only *speculated* about architectural characteristics; the formal approach pins down the exact mechanisms and requirements. (Section 9)
- The results were used at UCLA to evaluate the DEC PDP-11/45 and to make modifications so a virtual machine system could be constructed on it. (Section 9)
- The paper lists simplifications it made (no I/O resources or instructions, no asynchronous events, simple memory mapping) and claims empirically that these can be added as straightforward extensions. (Section 9)
- It notes "very recent" proposals for architectures that directly support virtual machines without the usual VMM interpretive overhead, and says the formal techniques can verify such claims, a 1974 anticipation of hardware virtualization. (Section 9)

## Appendix: lemmas
- **Lemma 1**: innocuous instructions, executed directly by the VM system, obey the equivalence property (follows from the innocuous definition and the VM map). (Appendix)
- **Lemma 2**: sensitive instructions, interpreted by the VM system, obey the equivalence property (follows from all sensitive instructions trapping, correct interpretation, and the VM map). (Appendix)
- **Lemma 3**: if all single instructions obey equivalence, any finite instruction sequence does, proven by induction on sequence length using the homomorphism property of the VM map. (Appendix)

## References of note
- The reference list includes Goldberg's own prior work (the 1972 Harvard PhD thesis "Architectural principles for virtual computer systems"; the 1971 Hawaii "Hardware requirements for virtual machine systems"), Buzen and Gagliardi on the evolution of virtual machine architecture (NCC 1973), the IBM VM/370 Planning Guide (1972), and Galley on PDP-10 virtual machines. (References)

## Covered in the notes
- The one-sentence definition "an efficient, isolated duplicate of the real machine", and that virtualization is enabled by a VMM.
- The three VMM responsibilities, under the lecture's names fidelity, performance, and safety/isolation (the paper's equivalence/efficiency/resource control).
- That a statistically dominant subset of instructions runs directly on the hardware (the efficiency property), which the note states as "guest instructions are executed directly by the hardware" and the VMM not interfering with every instruction.
- Trap-and-emulate as the core CPU-virtualization mechanism (the paper's dispatcher plus per-instruction interpreter routines).
- The idea that privileged operations trap to the hypervisor, which emulates them invisibly to the guest.
- That the VirtualBox-style system VM is a virtual machine while the JVM and a console emulator are not (the paper's exclusion of interpreters/emulators via the efficiency property).

## Notes vs paper discrepancies
Each item was checked against the paper text and at least one third-party source; sources are listed under "Discrepancy sources". Verdicts follow the fedorova/birrell convention: LECTURE FRAMING (keep the lecture wording, annotate with a callout); NOTES WRONG (fixed in place); NOT A REAL DISCREPANCY.

- The note (reproducing the lecture) describes the 17 x86 instructions as "privileged (required ring 0), but didn't cause a trap." Under the paper's own definition a privileged instruction *must* trap in user mode, so these are precisely *sensitive but not privileged* instructions. Annotated with a Popek & Goldberg callout in the "x86 Virtualization in the Past" section.
  - Verdict: LECTURE FRAMING. The lecture's phrasing is the exam-facing one and the course uses "privileged" loosely, but it contradicts the paper's vocabulary, so the callout restates it precisely. Confirmed by the Popek-Goldberg definitions (Section 3), the Wikipedia summary, Harvard CS161 (sensitive-but-not-privileged), and the StackOverflow consensus that "not all of x86's sensitive instructions are privileged."
- The note gives the VMM's three properties only under the lecture's names (fidelity, performance, safety). The paper's formal names (equivalence, efficiency, resource control) and their precise definitions, especially that efficiency is what excludes emulators, are additive. Annotated with a callout in "Defining Virtualization".
  - Verdict: NOT A REAL DISCREPANCY. The note is not wrong, just informal; the callout adds the paper's formal statements. Verified against Section 1 and Section 5.
- The note states trap-and-emulate without the dispatcher/allocator/interpreter decomposition or the sensitive/control-sensitive/behavior-sensitive classification. These are the paper's core and are added as callouts in "Processor Virtualization".
  - Verdict: NOT A REAL DISCREPANCY. The lecture compresses the formal theory for teaching; the callouts supply the classification and Theorem 1, verified against Sections 3-6, the Rutgers CS553 restatement, and the UCSB EPT-FreeBSD slides.
- The "17" count. The lecture presents it as a fact without a source; the paper does not contain it (the paper has no instruction count for x86, which did not exist in 1974). The count is from Robin and Irvine, USENIX Security 2000. The callout attributes it correctly.
  - Verdict: NOT A REAL DISCREPANCY, but a missing attribution now supplied. Verified against Robin and Irvine's abstract ("approximately 250 instructions of the Intel Pentium platform").

## Discrepancy sources
- <https://en.wikipedia.org/wiki/Popek_and_Goldberg_virtualization_requirements> (restates privileged/control-sensitive/behavior-sensitive and the sensitive-subset-of-privileged theorem; used to reconstruct the OCR-garbled formal definitions)
- <https://people.cs.rutgers.edu/~sn624/553-S25/lectures/10-system-virtualization.pdf> (Rutgers CS553: "when the sensitive instructions are a subset of the privileged instructions, a hardware architecture can be fully virtualized through trap-and-emulate")
- <https://read.seas.harvard.edu/cs161/2018/lectures/lecture25/> (Harvard CS161: privileged instruction must trap in user mode; sensitive vs user-sensitive definitions)
- <https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/ept-freebsd.pdf> (UCSB: "to make an architecture virtualizable, all sensitive instructions should be privileged instructions")
- <https://faculty.nps.edu/irvine/Publications/Publications2000/VMM_Usenix00.pdf> (Robin and Irvine, "Analysis of the Intel Pentium's Ability to Support a Secure Virtual Machine Monitor", USENIX Security 2000; source of the 17 sensitive-unprivileged x86 instructions out of ~250)
- <https://ccl.cse.nd.edu/blog/2010/the-virtualization-theorem-ignored-for-three-decades/> (plain-language restatement of the theorem and the requirement that all sensitive operations trap)
