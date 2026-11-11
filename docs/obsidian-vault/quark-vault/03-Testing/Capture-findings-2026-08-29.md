---
title: "Capture findings 2026-08-29"
tags: [testing, captures]
status: canonical
---

# Quark Anticheat — Validation Capture Findings, 2026-08-29

**Purpose.** This document reports what a set of validation runs of the Quark Anticheat
prototype actually produced. It is written for a reader with no access to the repository,
the capture files, or any prior discussion. Every factual claim below is either quoted
from a capture file (named at the point of quotation) or attributed to a source file and
line number.

**Scope discipline.** Where the captures do not show something, this document says so and
stops. It does not substitute expected behaviour derived from source code, and it does not
import results from the project's earlier test record
(`docs/vm_test_environment.md`). Statements derived from reading source rather than from
observation are labelled **(source-derived)** every time they appear.

**One finding governs the reading of everything else, so it is stated first.**

---

## 0. Governing finding: the captured binaries were not built from the repository source

Three message strings appear in the captures that **do not exist anywhere in the
repository's C or Rust source**:

| String appearing in captures | Present in repo source? |
|---|---|
| `Refusing to confirm protection for PID <n>: kernel module registration failed.` | No |
| `kernel-level protection was not confirmed (daemon is reachable, but Ring 0 registration failed -- is quark_kernel.ko loaded?)` | No |
| `Refusing to continue unprotected.` | No |

Verified by searching all `*.c`, `*.h`, and `*.rs` files in the repository for each
string; all three return no matches. The repository's only SDK fatal message is at
`sdk/quark_sdk.c:92` and reads `[QUARK-SDK] FATAL: lost connection to the Quark Anticheat
daemon.` — a different message for a different condition. The repository's daemon
(`quark_daemon/src/main.rs`) contains no refusal logic at all.

**Consequence.** The captures were produced by a build that is **ahead of the repository
checkout** and contains a fail-closed behaviour the repository does not have: the daemon
refuses to confirm protection when kernel-module registration fails. This behaviour is
what caused Condition A below to produce no defence. Any description of the daemon written
from the repository source will not match these captures.

The exact build is **not identifiable**: `environment.txt` records `git_commit:` and
`git_branch:` as empty (see section 6). Establishing which revision produced these captures
requires separate confirmation from the machine that ran them.

---

## 1. Inventory

Capture files were found in two top-level directories, `captures/` and `captures (1)/`.
These are overlapping copies. Four run directories exist in total.

### 1.1 The authoritative run

**`captures (1)/captures/20260829-003354/`** — the only complete run. All quotations in
this document come from here unless stated otherwise.

| File | Bytes | Contents |
|---|---|---|
| `environment.txt` | 1189 | Host, kernel, distro, CPU, memory, toolchain versions, harness parameters |
| `results.csv` | 1070 | One row per repetition. **Malformed for two of three conditions — see section 7.1** |
| `summary.txt` | 473 | Aggregate. **Reports only Condition B; the other two were silently dropped — see section 7.1** |
| `none.1` … `none.5` `.cheat` | 157 each | Attacker stdout/stderr, no-defence condition |
| `none.1` … `none.5` `.game` | 746 each | Target process stdout/stderr, no-defence condition |
| `none.1` … `none.5` `.dmesg` | **0 each** | Empty. No kernel messages, consistent with no module loaded |
| `A.1` … `A.15` `.cheat` | 157–158 | Attacker output, Condition A |
| `A.1` … `A.15` `.daemon` | 555–558 | Daemon output, Condition A |
| `A.1` … `A.15` `.game` | 859–861 | Target output, Condition A |
| `A.1` … `A.15` `.dmesg` | **0 each** | Empty |
| `B.1` … `B.10` `.cheat` | 279 each | Attacker output, Condition B |
| `B.1` … `B.10` `.daemon` | 972 each | Daemon output, Condition B |
| `B.1` … `B.10` `.dmesg` | 724 each | Kernel ring buffer, Condition B |
| `B.1` … `B.10` `.game` | 743 each | Target output, Condition B |
| `negctl.with_module.cheat` | 279 | Attacker against a live PID, module loaded |
| `negctl.without_module.cheat` | 158 | Same attacker, same PID, same address, module unloaded |
| `negctl.daemon` | 972 | Daemon output during the negative control |
| `negctl.dmesg` | 795 | Kernel ring buffer during the negative control |
| `negctl.game` | 497 | Target output during the negative control |
| `watchdog.daemon` | 558 | Daemon output during the watchdog probe |
| `watchdog.game` | 614 | Target output during the watchdog probe |

### 1.2 Other run directories found

- **`captures (1)/captures/20260829-003006/`** — aborted. `results.csv` contains only its
  header row. `B.1.daemon` (91 bytes) contains one line:
  `Failed to bind socket: Os { code: 98, kind: AddrInUse, message: "Address already in use" }`.
  No usable data.
- **`captures (1)/captures/20260829-003028/`** and **`.../20260829-003328/`** — one
  Condition B repetition each, both successful, both independent of each other (`diff -rq`
  reports every file differs). Their results agree with the ten Condition B repetitions in
  the authoritative run. Usable as supporting replicates.
- **`captures/`** (top level) — a **truncated duplicate**. It contains the same three
  earlier runs, but its copy of `20260829-003354/` holds only `none.1` through `none.4` and
  no Condition A, Condition B, negative-control, or watchdog files. Its `results.csv` (223
  bytes) is correspondingly short. **Do not use this directory.** It appears to be an
  incomplete copy of the authoritative run.

### 1.3 Files named in the capture request that do not exist

`cap_none.txt`, `cap_modeA.txt`, `cap_modeB.txt`, `cap_modeB_daemon.log`, and
`cap_modeB_dmesg.txt` **do not exist** in the working tree. Neither do loose `game.log`,
`cheat.log`, or `daemon.log` files. All captured data is inside the run directories listed
above.

---

## 2. Per-condition findings

The three conditions, as configured by the capture harness:

- **No defence** — no daemon, no kernel module.
- **Condition A** — daemon running, kernel module *not* loaded.
- **Condition B** — daemon running, kernel module loaded.

All three target the mock game (`game_target/game`), attacked by `cheat/cheat`.

**A note on quoting the attacker's output.** In the attacker's captures the lines are not
in chronological order. The error is written to stderr (unbuffered) and the progress lines
to stdout (block-buffered when redirected to a file), so the error appears *first* in the
file even though it occurred after the "Opening" line. Quotations below preserve file order
and this note should accompany any excerpt.

### 2.1 No defence — 5 repetitions

**Attacker's write succeeded in 5 of 5.** Verified: `grep -l 'Value: 9999' none.*.game`
matches all five.

From `none.1.cheat`, complete file:

```
[CHEAT] Opening /proc/8675/mem for writing...
[CHEAT] Writing new value 9999 to address 0x4030BC...
[CHEAT] SUCCESS! Wrote 4 bytes. Target variable updated.
```

From `none.1.game`, trimmed to the two state prints (elisions marked):

```
[QUARK-SDK] connection to daemon failed: No such file or directory
[GAME] Connecting to Quark Anticheat...
[GAME] WARNING: Quark Anticheat Daemon not detected. Running without protection.

--- [GAME STATE] ---
PID:            8675
Health address: 0x4030bc -> Value: 100
[... score line and menu prompt elided ...]

--- [GAME STATE] ---
PID:            8675
Health address: 0x4030bc -> Value: 9999
[... score line and menu prompt elided ...]
```

**Target process outcome: survived.** The second state print is after the attack, and the
process was still accepting commands. `none.*.dmesg` are 0 bytes — no kernel involvement.

### 2.2 Condition A — 15 repetitions — no defence occurred

**This condition did not exercise userspace detection. The daemon refused to register the
target, so no variables were monitored and no detection was possible.**

From `A.1.daemon`, complete file:

```
==================================================
🛡️🛡️  QUARK ANTICHEAT DAEMON ACTIVE  🛡️🛡️
Listening on Unix socket: /tmp/quark.sock
==================================================
[QUARK-DAEMON] Client connected.
[QUARK-DAEMON] Registering game process with PID: 9229
[QUARK-DAEMON] Registering PID 9229 to Ring 0 Module...
[QUARK-DAEMON] Kernel Registration stderr: [QUARK-CLI] Error creating netlink socket: Protocol not supported

[QUARK-DAEMON] Refusing to confirm protection for PID 9229: kernel module registration failed.
```

Counted across all fifteen repetitions:

| Observation | Count |
|---|---|
| `Refusing to confirm protection` present | 15 of 15 |
| `Protocol not supported` present | 15 of 15 |
| `Registering target variable` present | **0 of 15** |
| `[QUARK-MONITOR]` thread messages present | **0 of 15** |
| Target reached `Value: 9999` | 15 of 15 |

`Protocol not supported` is the netlink socket creation failing because no module is
listening on the protocol — the expected consequence of Condition A's configuration. The
daemon then declined to proceed.

The attacker's write succeeded, identically to the no-defence condition. From `A.1.cheat`,
complete file:

```
[CHEAT] Opening /proc/9229/mem for writing...
[CHEAT] Writing new value 9999 to address 0x4030BC...
[CHEAT] SUCCESS! Wrote 4 bytes. Target variable updated.
```

From `A.1.game`, trimmed:

```
[QUARK-SDK] FATAL: kernel-level protection was not confirmed (daemon is reachable, but Ring 0 registration failed -- is quark_kernel.ko loaded?). Refusing to continue unprotected.
[GAME] Connecting to Quark Anticheat...
[GAME] WARNING: Quark Anticheat Daemon not detected. Running without protection.
[... first state print, Value: 100, elided ...]

--- [GAME STATE] ---
PID:            9229
Health address: 0x4030bc -> Value: 9999
[... menu prompt elided ...]
```

**Target process outcome: survived, unprotected, successfully attacked, in 15 of 15.**

**No tamper detection and no SIGKILL occurred in any repetition of any condition.**
Verified: searching every capture file for `TAMPERING`, `Terminating target`, `Killed`, and
`killed` returns no matches anywhere in the capture set.

### 2.3 Condition B — 10 repetitions — attack prevented in 10 of 10

**The attacker's `open()` was denied in 10 of 10 repetitions**, and the target's value was
unchanged.

From `B.1.cheat`, complete file (note the ordering caveat above — the error line is first
in the file but occurred second):

```
[CHEAT] Error: Failed to open /proc/PID/mem. Are you sure the PID is correct and you have permission?: Permission denied
[CHEAT] Hint: The target process must permit debugging (prctl PR_SET_PTRACER) if Yama ptrace_scope is enabled.
[CHEAT] Opening /proc/12235/mem for writing...
```

The attacker exited with status **1** in all ten repetitions (`cheat_exit` column of
`results.csv`), which is the failure path at `cheat/cheat.c:35-38`. The error text is
`perror` output; the underlying errno is `EACCES`, reported as `Permission denied`. The
attacker never reached its write call — no `Writing new value` or `SUCCESS` line appears in
any Condition B capture.

From `B.1.game`, trimmed:

```
[GAME] Connecting to Quark Anticheat...
[QUARK-SDK] Successfully initialized and linked to Quark Daemon (PID: 12235)
[GAME] Monitored variables registered with Quark Anticheat Daemon.

--- [GAME STATE] ---
PID:            12235
Health address: 0x4030bc -> Value: 100
[... score line and menu prompt elided ...]

--- [GAME STATE] ---
PID:            12235
Health address: 0x4030bc -> Value: 100
[... score line and menu prompt elided ...]
```

**Target process outcome: survived and unaffected.** Health reads 100 both before and after
the attack in all ten repetitions (`health` column of `results.csv` is `100` for every
Condition B row).

Defensive component logs, from `B.1.daemon`, complete file:

```
==================================================
🛡️🛡️  QUARK ANTICHEAT DAEMON ACTIVE  🛡️🛡️
Listening on Unix socket: /tmp/quark.sock
==================================================
[QUARK-DAEMON] Client connected.
[QUARK-DAEMON] Registering game process with PID: 12235
[QUARK-DAEMON] Registering PID 12235 to Ring 0 Module...
[QUARK-DAEMON] Kernel Registration output: [QUARK-CLI] Sending command 1 for PID 12235 to kernel...
[QUARK-CLI] Command sent successfully.
[QUARK-DAEMON] Registering target variable: 'health' at Address: 0x4030BC (size: 4 bytes)
[QUARK-DAEMON] Registering target variable: 'score' at Address: 0x40310C (size: 4 bytes)
[QUARK-MONITOR] Thread started. Monitoring /proc/12235/mem
[QUARK-MONITOR] Warning: Could not open /proc/12235/mem: Os { code: 13, kind: PermissionDenied, message: "Permission denied" }
[QUARK-MONITOR] Thread terminated with error: Os { code: 13, kind: PermissionDenied, message: "Permission denied" }
```

### 2.4 Negative control — same process, same address, module toggled

The strongest single control in the capture set. One target process (PID 15441) was
attacked twice at the same address, with the kernel module loaded and then unloaded.

`negctl.with_module.cheat`, complete file:

```
[CHEAT] Error: Failed to open /proc/PID/mem. Are you sure the PID is correct and you have permission?: Permission denied
[CHEAT] Hint: The target process must permit debugging (prctl PR_SET_PTRACER) if Yama ptrace_scope is enabled.
[CHEAT] Opening /proc/15441/mem for writing...
```

`negctl.without_module.cheat`, complete file:

```
[CHEAT] Opening /proc/15441/mem for writing...
[CHEAT] Writing new value 9999 to address 0x4030BC...
[CHEAT] SUCCESS! Wrote 4 bytes. Target variable updated.
```

`negctl.dmesg`, complete file:

```
[ 2366.837576] [QUARK-KERNEL] Initializing Quark Anticheat Kernel Module...
[ 2366.837586] [QUARK-KERNEL] Netlink socket created successfully.
[ 2366.839025] [QUARK-KERNEL] Successfully registered kretprobe on ptrace_may_access.
[ 2367.459103] [QUARK-KERNEL] Process 15441 is now protected by Quark.
[ 2367.460276] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 15441 by PID 15416!
[ 2367.460290] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 15441 by PID 15416!
[ 2367.560510] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 15441 by PID 15449!
[ 2368.647875] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 15441 by PID 15493!
[ 2368.671120] [QUARK-KERNEL] Exiting Quark Anticheat Kernel Module...
```

Same process, same address, same attacker binary; only the module differs.

### 2.5 Watchdog probe — inconclusive, no watchdog behaviour captured

The probe did not test what it was intended to test. Because the kernel module was not
loaded for this probe, the daemon refused registration and the target never became a
supervised client.

`watchdog.daemon`, complete file:

```
==================================================
🛡️🛡️  QUARK ANTICHEAT DAEMON ACTIVE  🛡️🛡️
Listening on Unix socket: /tmp/quark.sock
==================================================
[QUARK-DAEMON] Client connected.
[QUARK-DAEMON] Registering game process with PID: 15569
[QUARK-DAEMON] Registering PID 15569 to Ring 0 Module...
[QUARK-DAEMON] Kernel Registration stderr: [QUARK-CLI] Error creating netlink socket: Protocol not supported

[QUARK-DAEMON] Refusing to confirm protection for PID 15569: kernel module registration failed.
```

`watchdog.game` shows the target running unprotected and never registering. **No watchdog
firing, no `_exit(137)`, and no daemon-disconnect behaviour is present in these captures.**

---

## 3. Mutual exclusion evidence

**Both sides are captured, in all ten Condition B repetitions.**

### 3.1 Daemon side — observed

The daemon's own monitor thread was denied access to the target's memory. From
`B.1.daemon`:

```
[QUARK-MONITOR] Thread started. Monitoring /proc/12235/mem
[QUARK-MONITOR] Warning: Could not open /proc/12235/mem: Os { code: 13, kind: PermissionDenied, message: "Permission denied" }
[QUARK-MONITOR] Thread terminated with error: Os { code: 13, kind: PermissionDenied, message: "Permission denied" }
```

This appears in **10 of 10** Condition B daemon captures (`monitor_blocked` column of
`results.csv` is `1` for every Condition B row). `code: 13` is `EACCES`.

The thread terminated. It did not retry, and no further `[QUARK-MONITOR]` output follows in
any Condition B capture.

### 3.2 Kernel side — observed

The kernel logged blocks against PIDs other than the attacker's. From `B.1.dmesg`,
complete file:

```
[ 2278.422764] [QUARK-KERNEL] Initializing Quark Anticheat Kernel Module...
[ 2278.422774] [QUARK-KERNEL] Netlink socket created successfully.
[ 2278.423750] [QUARK-KERNEL] Successfully registered kretprobe on ptrace_may_access.
[ 2279.049414] [QUARK-KERNEL] Process 12235 is now protected by Quark.
[ 2279.051122] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 12235 by PID 12216!
[ 2279.051137] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 12235 by PID 12216!
[ 2279.151297] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 12235 by PID 12243!
[ 2280.246967] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process 12235 by PID 12280!
```

Four alerts, three distinct blocked PIDs, against a protected target of 12235. Only one of
those three PIDs can be the attacker. The block is therefore not attacker-specific, and
this is observed, not inferred.

---

## 4. Kernel alert lines

### 4.1 Full untruncated lines

Every `[QUARK-KERNEL ALERT]` line in the capture set carries the attacking PID. The format
is fixed:

```
[ <monotonic seconds> ] [QUARK-KERNEL ALERT] Blocked memory/ptrace access to protected process <target_pid> by PID <attacker_pid>!
```

### 4.2 Alert count and PID distribution, all ten Condition B repetitions

Every repetition produced exactly **four alerts** across exactly **three distinct blocked
PIDs**, with one PID blocked twice:

| Rep | Target PID | Blocked PIDs (in log order) |
|---|---|---|
| B.1 | 12235 | 12216, 12216, 12243, 12280 |
| B.2 | 12513 | 12496, 12496, 12520, 12561 |
| B.3 | 12796 | 12780, 12780, 12806, 12847 |
| B.4 | 13088 | 13071, 13071, 13096, 13138 |
| B.5 | 13388 | 13367, 13367, 13397, 13442 |
| B.6 | 13698 | 13678, 13678, 13707, 13753 |
| B.7 | 14035 | 14011, 14011, 14044, 14088 |
| B.8 | 14362 | 14339, 14339, 14370, 14460 |
| B.9 | 14739 | 14719, 14719, 14748, 14796 |
| B.10 | 15084 | 15062, 15062, 15093, 15148 |

The negative control (section 2.4) shows the same four-alert, three-PID pattern.

### 4.3 Which process each PID corresponds to

**The captures do not record the daemon's own PID or the attacker's PID directly**, so
attribution is partly inference. What is observable versus inferred:

- **Observable:** the target PID (printed by the target itself and named in the alert), and
  that three distinct non-target PIDs were blocked.
- **Observable:** the attacker's captures name only the target PID, never the attacker's
  own.

Attribution consistent with the captures, but **inferred, not observed**:

1. The first PID (blocked twice, e.g. 12216) is numerically lower than the target and was
   blocked ~1.7 ms after protection was established. The daemon started before the target,
   so a lower PID is consistent with the daemon's main thread. It was blocked **twice**,
   and the daemon log shows **two** variables registered (`health` and `score`) immediately
   before — consistent with one denied read per variable.
2. The second PID (e.g. 12243) is higher than the target and was blocked ~102 ms after
   protection. Computed from `B.1.dmesg`: `2279.151297 - 2279.049414 = 0.101883 s`. The
   daemon log records exactly one monitor-thread denial. **(source-derived note:** the
   daemon's monitor thread sleeps 100 ms before its first access, at
   `quark_daemon/src/main.rs:246`, which matches the observed 102 ms.**)**
3. The third PID (e.g. 12280) was blocked ~1.2 s later, consistent with when the harness
   launched the attacker.

A point worth flagging: if PIDs 12216 and 12243 are both the daemon, they are **different
PIDs for the same process**. The kernel module resolves the calling task with
`task_pid_vnr(current)` (`kernel/quark_kernel.c:120` region), which for a thread yields
that thread's own id rather than the thread-group id. **This is a plausible explanation for
the two distinct daemon-side PIDs, but it is not established by the captures** — confirming
it requires recording the daemon's PID and thread ids during a run, which was not done.

---

## 5. Timing

### 5.1 What timestamps exist

**Only the kernel captures carry timestamps.** `B.*.dmesg` and `negctl.dmesg` use the
standard kernel ring-buffer format: seconds since boot with **microsecond resolution**
(6 decimal places), for example `[ 2278.422764]`.

**No other capture carries any timestamp.** The daemon, target, and attacker outputs
(`.daemon`, `.game`, `.cheat`) contain no time information at any resolution. The
`none.*.dmesg` and `A.*.dmesg` files are **0 bytes** — no kernel messages were generated,
consistent with no module being loaded.

`environment.txt` records one wall-clock timestamp for the run as a whole:
`date_utc: 2026-08-29T03:33:54Z`. It does not timestamp individual repetitions.

### 5.2 Is detection latency computable?

**No, for two independent reasons.**

First, **no detection occurred.** Condition A produced zero tamper detections and zero
SIGKILLs across 15 repetitions (section 2.2). There is no event to measure. The
`latency_ms` column of `results.csv` reads `NA` for every row of every condition, and
`summary.txt` reports `no valid samples` for latency.

Second, even had detection occurred, **the captures carry no timestamps on the userspace
side.** The daemon's alert output and the attacker's output are both untimestamped, so the
interval between the write landing and any subsequent kill could not be computed from these
files.

**What would be needed.** A capture in which (a) the daemon registers variables and its
monitor thread runs — which, given the fail-closed behaviour in section 0, appears to
require the kernel module loaded, in which case the monitor thread is itself blocked
(section 3) — and (b) timestamps exist on both the attacker's write completion and the
daemon's detection. Neither condition is met by any file in this capture set. This document
does not estimate the value.

### 5.3 Intervals that *are* computable

From the kernel timestamps in Condition B only, and only within a single repetition. In
`B.1.dmesg`: module init to kretprobe registration is `2278.423750 - 2278.422764 =
0.000986 s`; protection established to the first block is `2279.051122 - 2279.049414 =
0.001708 s`; protection established to the ~102 ms block is `0.101883 s`.

These describe when events occurred relative to one another in the kernel log. **They are
not a defence latency measurement.** In Condition B the denial happens inside the
attacker's own `open()` call, so there is no interval between attack and response to
measure.

---

## 6. Environment as captured

All values below are quoted from `environment.txt` in the authoritative run directory.
Nothing here is taken from any other machine.

```
date_utc:        2026-08-29T03:33:54Z
host:            nobara-pc

uname_r:         7.0.9-200.nobara.fc43.x86_64
uname_a:         Linux nobara-pc 7.0.9-200.nobara.fc43.x86_64 #1 SMP PREEMPT_DYNAMIC Sun May 17 16:46:25 UTC 2026 x86_64 GNU/Linux
os_release:      Nobara Linux 44 (KDE Plasma Desktop Edition)
glibc:           ldd (GNU libc) 2.43

CONFIG_KPROBES:          CONFIG_KPROBES=y
CONFIG_KRETPROBES:       CONFIG_KRETPROBES=y
CONFIG_BPF_LSM:          CONFIG_BPF_LSM=y
CONFIG_SECURITY_YAMA:    CONFIG_SECURITY_YAMA=y
yama_ptrace_scope: 0

cpus:            5
governor:        n/a
model:           12th Gen Intel(R) Core(TM) i7-1265U
mem_total:       8122084 kB

gcc:             gcc (GCC) 16.2.1 20260819 (Red Hat 16.2.1-2)
cargo:           cargo 1.97.1 (c980f4866 2026-06-30) (Fedora 1.97.1-1.fc44)
rustc:           rustc 1.97.1 (8bab26f4f 2026-07-14) (Fedora 1.97.1-1.fc44)

git_commit:      
git_branch:      
git_dirty:       YES
```

### Values requiring separate confirmation

- **`git_commit` and `git_branch` are empty.** The exact source revision that produced
  these binaries is **not recorded**. Given section 0, this is the most consequential gap
  in the environment record. `git_dirty: YES` was captured, but without a base commit it
  identifies nothing.
- **`governor: n/a`** — the CPU frequency governor could not be read. Not available for the
  methodology.
- **The kernel is a Fedora 43 build (`fc43`) while the OS reports Nobara Linux 44.** Both
  are as captured. This is a mixed state, not a transcription error, and is noted again in
  section 7.
- **`yama_ptrace_scope: 0`** — permissive. Relevant because it means Yama was *not*
  restricting `/proc/<pid>/mem` access during these runs, so the Condition B denials cannot
  be attributed to Yama. The negative control (section 2.4) independently confirms this.
- **`CONFIG_BPF_LSM=y`** — the kernel supports BPF LSM. Recorded for completeness; nothing
  in the captures indicates it was used.
- **No RAM/CPU figure for the target process** was captured. There is no `ps` output, no
  CPU-utilisation sample, and no memory measurement in any file.

---

## 7. Discrepancies and unexpected results

Reported prominently, as requested. Items 7.1 and 7.2 affect how the results may be
described; 7.3 affects the harness output itself.

### 7.1 Harness defect — `results.csv` is malformed and `summary.txt` is incomplete

**`results.csv` rows for the no-defence and Condition A runs are split across two physical
lines.** Example, the first data row as it appears in the file:

```
1,none,0,0,0,1,0,1,0,0
0,9999,NA,1
```

This is one logical row broken in two. The `kernel_blocks` field contains an embedded
newline and the literal text `0\n0`. All 5 no-defence rows and all 15 Condition A rows are
affected. The 10 Condition B rows are **not** affected and are well-formed.

**Cause**, from the harness source (`capture.sh`): the field is computed as
`grep -c '...' "$tag.dmesg" || echo 0`. When the dmesg capture is empty, `grep -c` prints
`0` *and* exits with status 1, so the `|| echo 0` fallback also fires, emitting a second
`0`. Condition B is unaffected because `grep` found 4 matches and exited 0.

**Consequence: `summary.txt` silently omits two of the three conditions.** Its aggregation
filters on a validity column that the broken rows no longer have in the expected position,
so the no-defence and Condition A results were dropped without warning. The summary reads:

```
mode    reps   landed  detected   denied    alive  mon_block
B         10        0         0       10       10         10
```

**`summary.txt` must not be quoted as a complete result.** The per-condition counts in
section 2 of this document were recomputed directly from the individual capture files, not
from the CSV or the summary.

### 7.2 Condition A does not exist as a defended mode in the captured build

This is the substantive finding, and it follows from section 0. The captured daemon
refuses to register a target when kernel-module registration fails. Since Condition A is
*defined* by the module being absent, the daemon refused in 15 of 15 repetitions, never
registered any variable, and never started a monitor thread.

**Consequences for how the results may be described:**

- There is **no observed data on userspace polling detection** in this capture set — not a
  slow detection, not a partial one. The mechanism never ran.
- The three conditions are **not** "undefended / userspace-defended / kernel-defended". As
  captured they are "undefended / undefended-by-refusal / kernel-defended". The no-defence
  and Condition A rows are behaviourally identical in outcome: write lands, target survives.
- The project documentation describes a two-mode design. `docs/funcionamiento_codigo.md`
  section 2.1 describes userspace verification as an operative mode. That description
  matches the repository source but **does not match the captured build's behaviour.**

### 7.3 The SDK announces a fail-closed policy but the target continues running

In every Condition A repetition the SDK printed:

```
[QUARK-SDK] FATAL: kernel-level protection was not confirmed (daemon is reachable, but Ring 0 registration failed -- is quark_kernel.ko loaded?). Refusing to continue unprotected.
```

and the target then **continued running, was successfully attacked, and survived** — in 15
of 15. The message states a refusal that did not occur.

The immediately following line in the same capture is the target's own:

```
[GAME] WARNING: Quark Anticheat Daemon not detected. Running without protection.
```

**(source-derived)** that line is the `quark_sdk_init() != 0` branch at
`game_target/game.c:40`, which logs and proceeds. So the SDK signalled failure by return
value and the target chose to continue. Whether the SDK was *intended* to terminate the
process cannot be determined from the captures; what is observed is that the announced
refusal had no effect on this target.

### 7.4 The target binary is not position-independent

The target's `health` variable is at **`0x4030bc` in every repetition of every condition**,
across at least 30 distinct process PIDs. A position-independent executable under ASLR
would place it at a different address each run.

This is unremarkable as a test artefact but matters for two reasons: any statement that the
design is indifferent to ASLR is **not exercised by these captures**, and the attacker was
supplied a fixed address that would not be stable against a PIE build. The captures do not
record the compiler flags used.

### 7.5 Kernel and distribution are from different Fedora generations

`uname_r` reports `7.0.9-200.nobara.fc43.x86_64` while `os_release` reports `Nobara Linux
44`. Both as captured. Report both verbatim rather than reconciling them.

### 7.6 `quark_cli` reports success without confirmation

In Condition B the daemon logged:

```
[QUARK-DAEMON] Kernel Registration output: [QUARK-CLI] Sending command 1 for PID 12235 to kernel...
[QUARK-CLI] Command sent successfully.
```

**(source-derived)** this message is printed at `quark_daemon/quark_cli.c:70`, immediately
after `sendto()` returns, and no reply is ever read. It therefore indicates that a netlink
message was transmitted, not that the kernel registered the PID. The independent
confirmation is the kernel's own line, `[QUARK-KERNEL] Process 12235 is now protected by
Quark.`, which is present in all ten Condition B dmesg captures. Cite the kernel line, not
the CLI line.

### 7.7 An earlier run failed on a port conflict

`captures (1)/captures/20260829-003006/B.1.daemon` contains only:

```
Failed to bind socket: Os { code: 98, kind: AddrInUse, message: "Address already in use" }
```

The run produced no data. Noted for completeness; it indicates a stale socket or a
still-running daemon at that moment, and has no bearing on the later runs.

---

## 8. Provenance table

Legend: **Observed** — supported by a quoted line in these captures. **Documented only** —
asserted in project documentation or implied by source, with no supporting capture.
**Absent** — neither observed nor applicable.

| Row | No defence (n=5) | Condition A (n=15) | Condition B (n=10) |
|---|---|---|---|
| **Write lands** | **Observed** — yes, 5/5. `none.1.cheat` `SUCCESS! Wrote 4 bytes.`; `none.1.game` `Value: 9999` | **Observed** — yes, 15/15. `A.1.cheat` `SUCCESS! Wrote 4 bytes.`; `A.1.game` `Value: 9999` | **Observed** — no, 0/10. `B.1.cheat` `Permission denied`; no write line present |
| **Detected** | **Absent** — no detector configured | **Observed absent** — 0/15. No `[QUARK-MONITOR]` and no `Registering target variable` in any `A.*.daemon` | **Absent** — prevention, not detection; nothing to detect |
| **Prevented** | **Absent** | **Observed absent** — 0/15 | **Observed** — yes, 10/10. `B.*.cheat` exit status 1; `B.*.dmesg` `[QUARK-KERNEL ALERT] Blocked memory/ptrace access…` |
| **Latency** | **Absent** | **Absent** — no detection event occurred; `latency_ms` is `NA` in all rows | **Absent** — denial is synchronous within `open()`; no interval exists to measure |
| **Target outcome** | **Observed** — survived, 5/5. Second state print present, `Value: 9999` | **Observed** — survived, 15/15. Second state print present, `Value: 9999` | **Observed** — survived unaffected, 10/10. `Value: 100` before and after |
| **Mutual exclusion (daemon side)** | **Absent** | **Absent** — monitor thread never started | **Observed** — 10/10. `B.*.daemon` `[QUARK-MONITOR] Warning: Could not open /proc/<pid>/mem: Os { code: 13, … }` |
| **Mutual exclusion (kernel side)** | **Absent** | **Absent** — `A.*.dmesg` are 0 bytes | **Observed** — 10/10. Four alerts, three distinct blocked PIDs, only one of which can be the attacker |
| **Attacker PID in alert line** | **Absent** | **Absent** | **Observed** — every alert carries `by PID <n>` |
| **Negative control** | — | — | **Observed** — one PID, one address: denied with module (`negctl.with_module.cheat`), succeeded without (`negctl.without_module.cheat`) |
| **Watchdog / fail-closed on daemon loss** | **Absent** | **Absent** | **Absent** — probe never reached a supervised state; see section 2.5 |
| **Evasion / bypass** | **Absent** | **Absent** | **Absent** — no bypass was attempted in any capture |

### Cells that are documented only, with no capture support

For completeness, these appear in project documentation but have **no supporting line in
this capture set** and are marked accordingly above: userspace polling detection at a 50 ms
interval; SIGKILL mitigation on value mismatch; watchdog termination with `_exit(137)` on
daemon loss; and any measurement of CPU or memory overhead.

---

## 9. Summary of what these captures do and do not support

**Supported by quoted capture lines:**

- Kernel-level prevention works and is reproducible: 10 of 10 repetitions denied the
  attacker at `open()` with `EACCES`, plus 2 further single-repetition runs
  (`20260829-003028`, `20260829-003328`) agreeing independently.
- The target was unaffected: value 100 before and after, process alive, 10 of 10.
- The denial is attributable to the module and not to Yama or another OS restriction:
  demonstrated by the negative control on a single live PID, and corroborated by
  `yama_ptrace_scope: 0`.
- The block is not attacker-specific: three distinct PIDs blocked per repetition, with the
  daemon's own monitor thread denied and logging that denial on its own side.
- Kernel alert lines carry the attacking PID in full.
- Without protection the attack succeeds: 5 of 5.

**Not supported, and not to be asserted from this capture set:**

- Any figure for userspace detection latency. No detection occurred and no userspace
  timestamps exist.
- Any claim that userspace polling detection functions in the captured build. It never ran.
- Any watchdog or fail-closed-on-daemon-loss behaviour. Not exercised.
- Any overhead measurement. Not captured.
- Any bypass or evasion result. Not attempted.
- The identity of the source revision under test. Not recorded.


## Update 2026-11-11 — agent:claude — origen probable del build capturado

- **REPLACES** — «The exact build is **not identifiable**» (§0) → las tres cadenas de §0 están en el commit `2624ae4` ("fix: refuse to report success until kernel-level protection is confirmed", 2026-08-29 00:14:56 -03:00 = 03:14:56 UTC). `environment.txt` de la corrida autoritativa registra `date_utc: 2026-08-29T03:33:54Z`, 19 minutos después. Verificado con `git show 2624ae4 | grep -c` → 2 coincidencias. Conclusión: el build capturado **probablemente** incluye ese commit; la identidad exacta sigue **UNVERIFIED** (no hay `git_commit` en la captura, y pudo haber cambios sin commitear).
- **ADDED** — Esto explica §7.2 y §7.3: el comportamiento fail-closed ya estaba implementado en el SDK/daemon capturados pero no en la rama `BAR-example-test` donde estaba el harness.
- Las demás conclusiones de este documento no se modifican.
