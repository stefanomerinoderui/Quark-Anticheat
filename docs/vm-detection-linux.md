# VM and Hypervisor Detection on Linux (Anti-Cheat Reference)

Last updated: 2026-11-16

This document describes techniques for detecting that a Linux program is running inside a virtual machine, or on top of a hidden hypervisor, using timing, memory behavior, CPU identification, and system artifacts. It is written for anti-cheat development and defensive testing. Each section explains what the check does, why it works, how to implement it on Linux, how it fails, and how an adversary might defeat it.

Pafish and Al-Khaser (both Windows-only) are used as the conceptual catalog. Section 8 maps their check categories to Linux equivalents.

---

## 1. Scope and threat model

| Case | Description | Typical relevance to anti-cheat |
|---|---|---|
| Guest VM | Game runs inside a VM (QEMU/KVM, VirtualBox, VMware, Hyper-V, Xen, cloud). | Policy decision: ban, flag, or allow. Often used with GPU passthrough (VFIO). |
| Hidden hypervisor | A thin hypervisor runs beneath the OS and hides itself (hypervisor-based cheats, memory-hiding via EPT). | Highest value target. The OS sees "bare metal" unless you measure. |
| Nested virtualization | A VM inside a VM. | Raises timing cost sharply; complicates baselines. |
| Container | Docker, Podman, LXC. Shares the host kernel. | Not a VM. CPUID and timing look like the host. Detect separately (cgroups, namespaces). |
| Emulation | QEMU TCG, Rosetta-like layers, Box64/FEX. | Different signal set (instruction timing is far slower, CPUID leaf 0x40000000 reports "TCGTCGTCGTCG" for QEMU TCG). |

Key principle: client-side checks run in an environment the attacker controls. Every check below can be defeated by someone who controls the hypervisor or the kernel. Use them as one layer inside a scoring system that also uses server-side signals and hardware attestation (section 10 and 12).

---

## 2. Quick reference matrix

| Method | Detects | Reliability | Easy to spoof | Needs root |
|---|---|---|---|---|
| CPUID leaf 1 ECX bit 31 (hypervisor present) | Guest VM | High on default configs | Yes (flag can be cleared) | No |
| CPUID leaf 0x40000000 vendor string | Which hypervisor | High on default configs | Yes | No |
| CPUID latency vs. reference instruction | Any hypervisor, including hidden | Medium | Hard, but TSC offsetting masks part of it | No |
| TSC delta vs. PMU cycle counter | Hidden VM exits | Medium to high where a vPMU exists | Hard | No (depends on `perf_event_paranoid`) |
| TSC vs. independent clock (server time) | TSC manipulation | Medium | Medium | No |
| Steal time in `/proc/stat` | Guest on an oversubscribed host | Low (soft signal) | Hard | No |
| Cache hierarchy measured vs. reported | Spoofed CPU topology | Medium | Medium | No |
| TLB/EPT page walk cost | Nested paging | Low to medium | N/A (hardware effect) | No |
| DMI/SMBIOS strings | Common VMs | High on default configs | Easy | Partly |
| PCI vendor/device IDs | Virtual devices | High on default configs | Easy to medium | No |
| Block device and NIC identity | Virtual disks, NICs, MAC OUIs | High on default configs | Easy | No |
| Kernel modules, guest agents | Guest tools installed | Medium | Easy | No |
| ACPI table OEM IDs | Common VMs | High on default configs | Medium | Yes |
| MSR reads | Missing or odd MSRs | Medium | Medium | Yes |
| Missing thermal, cpufreq, RAPL, IOMMU groups | Absence of real hardware | Medium | Medium | No |

"Default configs" means the hypervisor has not been deliberately hardened. A hardened guest (section 7.12) defeats the static checks and leaves only the timing and consistency checks.

---

## 3. CPUID-based detection

CPUID is unprivileged on x86 and is always intercepted by Intel VT-x and AMD-V hypervisors, so the hypervisor fully controls what the guest sees and also pays a VM exit on every execution. That makes it both an information source and a timing probe.

### 3.1 Hypervisor present bit

`CPUID.1:ECX[31]` is set by hypervisors to advertise their presence. Linux exposes it as the `hypervisor` flag in `/proc/cpuinfo` and `lscpu` reports it as "Hypervisor vendor". A hardened guest clears it (QEMU/KVM can do this with CPU model flags), so a clear bit proves nothing.

### 3.2 Hypervisor vendor string (leaf 0x40000000)

If the present bit is set, `CPUID.0x40000000` returns the maximum hypervisor leaf in EAX and a 12-byte vendor signature in EBX, ECX, EDX (in that order).

| Signature | Hypervisor |
|---|---|
| `KVMKVMKVM\0\0\0` | KVM (also used by VirtualBox on Linux guests with the KVM paravirt provider) |
| `Microsoft Hv` | Hyper-V, WSL2, Azure, Windows with VBS (also used by KVM when Hyper-V enlightenments are enabled) |
| `VMwareVMware` | VMware |
| `XenVMMXenVMM` | Xen |
| `VBoxVBoxVBox` | VirtualBox (when its own interface is used) |
| `TCGTCGTCGTCG` | QEMU in TCG (software emulation) mode |
| `bhyve bhyve ` | bhyve |
| `prl hyperv  ` | Parallels |
| `ACRNACRNACRN` | ACRN |

Caveats:
- A KVM guest can present `Microsoft Hv` (or any custom string) through `hv_vendor_id`, so the vendor string tells you what the guest was told, not necessarily the true hypervisor.
- On bare metal, leaf `0x40000000` is undefined (many CPUs return the highest basic leaf's data). Only interpret it if the present bit is set, or treat an unexpected value as an anomaly.
- Leaf `0x40000001` EAX is `Hv#1` for the Hyper-V interface and carries KVM paravirtual feature bits for KVM.

### 3.3 Consistency checks on other leaves

Even when the hypervisor bit is hidden, a guest CPU model is often inconsistent:

- Brand string (leaves `0x80000002` to `0x80000004`): `QEMU Virtual CPU`, `Common KVM processor`, `QEMU64`.
- Family/model/stepping that does not match a real SKU, or a model name that does not match the reported feature flags (for example a recent model without features that model always has).
- Leaf 4 (cache parameters) and leaf `0xB`/`0x1F` (topology): odd socket/core/thread layouts such as N sockets with 1 core each, cache sizes that are round numbers, no shared L3.
- Leaf `0x15` (TSC/crystal ratio) and `0x16` (frequencies): zero in most guests, but also zero on older real CPUs, so this is a weak signal.
- Leaf `0x80000008` (physical address bits): 40 bits is a common QEMU default; real CPUs commonly report 39, 42, 43, 46, or 48 depending on the model.
- Leaf 7 feature flags: a guest may hide or add features compared with the same model on real hardware.
- Cross-source consistency: compare the CPUID instruction directly against `/proc/cpuinfo`, `lscpu`, and `/sys/devices/system/cpu`. A spoofer that edits only one source (for example a mount-namespace bind mount over `/proc/cpuinfo`) leaves a mismatch.

### 3.4 Microcode revision

`/proc/cpuinfo` shows `microcode : 0x...`. KVM guests commonly report a trivially small value such as `0x1` unless the host value is passed through. Real machines report a firmware-dependent value in the hundreds of millions range or a recognizable hex revision. This is a cheap heuristic with a modest false-positive rate (AMD and some distros report 0x0).

---

## 4. Timing-based detection

### 4.1 Why timing works

Intel VT-x unconditionally intercepts `CPUID`, `GETSEC`, `INVD`, `XSETBV`, and the VMX instruction family. AMD-V intercepts `CPUID` and several others. Other instructions (`RDTSC`, `RDMSR`, `WRMSR`, `HLT`, `PAUSE`, `INVLPG`, CR accesses) trap only if the hypervisor configures them to. From Linux userspace, `CPUID` is the main always-trapping instruction available to you, which is why most userland timing checks revolve around it.

A VM exit plus re-entry costs far more than the instruction itself. As an order of magnitude: native `CPUID` takes on the order of 100 to 250 cycles; under a hardware hypervisor it commonly costs on the order of 1,000 to several thousand cycles; nested virtualization is far higher. These numbers vary a lot by CPU generation, mitigations, and hypervisor, so never hard-code them. Calibrate.

### 4.2 CPUID versus a reference instruction

Measure `CPUID` latency and compare it with a non-trapping reference sequence (for example a dependent `imul` chain) measured the same way. The ratio is more portable than absolute cycles because it cancels out much of the CPU model and frequency difference. A well-known variant uses `FYL2XP1` as the reference.

Implementation notes for Linux userspace:
- Pin the thread with `sched_setaffinity` so the TSC read and the CPUID run on one core.
- Bracket `RDTSC` with `LFENCE` (or use `RDTSCP`, but RDTSCP can be disabled or trapped in some guests).
- Warm up first, then collect thousands of samples.
- Use the minimum and low percentiles (p5, p50) rather than the mean. Interrupts, scheduling, and SMIs inflate individual samples.
- Optionally raise priority (`SCHED_FIFO` needs `CAP_SYS_NICE`) and `mlockall` to reduce page-fault noise.

A reference implementation is in Appendix A.

### 4.3 Kernel-side timing (cleanest signal)

A kernel module can measure with interrupts and preemption disabled, which removes most noise:

```c
unsigned long flags;
u32 a, b, c, d;
u64 t0, t1;

preempt_disable();
local_irq_save(flags);
t0 = rdtsc_ordered();
cpuid(0, &a, &b, &c, &d);
t1 = rdtsc_ordered();
local_irq_restore(flags);
preempt_enable();
```

NMIs and SMIs can still interrupt, so keep multiple samples. Kernel modules need signing under Secure Boot or kernel lockdown. eBPF cannot execute CPUID, so it cannot replace this.

### 4.4 TSC cycles versus PMU cycles

Many hypervisors try to hide VM exit cost by adjusting the TSC (offsetting or scaling) so that guest-visible time does not advance during exits. This defeats naive `CPUID`-vs-reference timing. A second counter can expose it:

- Use `perf_event_open` with `PERF_TYPE_HARDWARE` / `PERF_COUNT_HW_CPU_CYCLES`, `exclude_kernel=1`.
- Run a batch (for example 20,000) of `CPUID` calls and read both TSC and the cycle counter before and after.
- Run the same batch with a reference instruction.
- Compute `tsc/cycles` for each run. On bare metal both ratios are about the same, so their quotient is close to 1.0. If exit time is included in TSC but excluded from the guest's virtualized PMU, the CPUID ratio is much larger than the reference ratio.

Caveats:
- It depends on the hypervisor exposing a vPMU. In many setups it does not (`perf_event_open` fails with `ENOENT` or `EOPNOTSUPP`). PMU absence is a soft signal on its own, since containers and locked-down kernels also block it.
- `kernel.perf_event_paranoid` of 3 (a distro patch on some systems) blocks unprivileged use. Lower values permit user-only counting for your own process.
- Some hypervisors count host cycles during exits, which brings the ratio back to 1.0. In that case the absolute CPUID cost is still high, so keep both numbers.

A reference implementation is in Appendix B.

### 4.5 TSC versus an independent clock

On a Linux guest, `CLOCK_MONOTONIC_RAW` is often derived from the same TSC or from `kvm-clock`, so comparing TSC with it is circular. Useful comparisons need an independent time source:

- Server time: send timestamps to a server and compare elapsed time over seconds to minutes against local TSC deltas. This is the strongest option and cannot be faked by a local hypervisor.
- Other hardware clocks: HPET or ACPI PM timer (`/sys/devices/system/clocksource/clocksource0/available_clocksource`, switching clocksources needs root and is invasive).
- Frequency sanity: measure TSC frequency over a known external interval, then check against `CPUID.15H/16H`, the `tsc_known_freq` flag, and the model's expected base clock.
- Cross-core TSC offsets: read the TSC on several pinned cores. Real hardware keeps them synchronized (`constant_tsc`, `nonstop_tsc`, invariant TSC in `CPUID.80000007H:EDX[8]`); misconfigured virtual CPUs may drift.

### 4.6 Sleep and timer behavior

Some sandboxes accelerate or skip sleeps. Request `nanosleep` of a known duration and confirm with an external timestamp that the wall time really elapsed. A mismatch indicates a manipulated clock or a sandbox.

### 4.7 Steal time and scheduling jitter

- `/proc/stat` CPU line: the 8th numeric field is steal time. A nonzero value means a hypervisor took CPU time from this guest. Only paravirtual steal-time reporting (KVM, Xen, some Hyper-V) populates it. It tells you a guest exists, not that a hidden hypervisor exists.
- Tight-loop jitter: run a loop with nothing but `RDTSC` reads and record gaps. Spikes of hundreds to thousands of cycles at regular intervals are common in guests (timer-tick exits, host scheduling). Bare metal also produces spikes (interrupts, SMIs), so this is a weak statistical signal.

### 4.8 Timing noise sources to control

| Source | Mitigation |
|---|---|
| Interrupts, scheduler | Pin CPU, high priority, many samples, take low percentiles; kernel-side: disable IRQs |
| Frequency scaling and turbo | Compare ratios, not absolute cycles; stay on one core |
| SMT sibling load | Note thread topology; discard runs with a busy sibling if you can see it |
| SMIs | Cannot be controlled; use percentiles |
| Page faults | Warm up, `mlockall` |
| Mitigations (retpoline, IBRS) | Affect syscalls more than `CPUID`; still record the kernel version |

---

## 5. Memory-based detection

### 5.1 Memory size, layout, and hotplug

- `MemTotal` in `/proc/meminfo`, the physical memory map in `/sys/firmware/memmap/*` and `/proc/iomem` (addresses are zeroed for unprivileged users), and the early e820 map from `dmesg`.
- Warning signs: round power-of-two sizes (4096 MiB, 8192 MiB), no firmware-reserved ranges that real boards have (ME, GPU stolen memory), a PCI hole placed at the classic 0x80000000 or 0xC0000000 boundaries, and few reserved regions.
- Low RAM (under 4 GB) or very few cores is a weak signal for modern gaming PCs.
- Ballooning: the `virtio_balloon`, `vmw_balloon`, `hv_balloon`, and Xen balloon drivers; `/sys/bus/virtio/drivers/virtio_balloon`; `MemTotal` or free memory changing without any local allocation.
- Memory hotplug: `/sys/devices/system/memory/` blocks added at runtime are common in cloud guests and rare on desktops.
- NUMA: a single node with an odd CPU/memory ratio, or missing `/sys/devices/system/node`.

All of these are easy to configure away in a hardened VM.

### 5.2 Nested paging (EPT/NPT) cost

With two-dimensional paging, a guest TLB miss needs a nested page walk, so it costs more than on bare metal. Experiment design:

1. `mmap` a large buffer (1 to 4 GB), larger than TLB reach.
2. Access it randomly with a page-sized stride. Measure average latency per access.
3. Repeat with `madvise(MADV_NOHUGEPAGE)` and with `madvise(MADV_HUGEPAGE)` (transparent huge pages).
4. Compare the 4K-versus-2M latency ratio against the expected value for the CPU model.

Limitations: if the host backs guest memory with huge pages, the nested walk shortens and the effect shrinks. This is a statistical, noisy signal and works best as one input in a score.

### 5.3 Cache hierarchy measured versus reported

Spoofed topology data in CPUID and sysfs cannot change what the cache really does.

- Pointer-chase through working sets from 4 KB to 256 MB and locate the latency steps (L1, L2, L3, DRAM).
- Compare the plateaus with `/sys/devices/system/cpu/cpu0/cache/index*/size` and `CPUID.4`.
- A mismatch means the topology was invented. Real values will also show the true host CPU class, which you can compare with the claimed model.

### 5.4 First-touch fault cost

Touching never-used guest-physical pages triggers an EPT violation that the host must resolve, producing a bimodal latency distribution (tens of microseconds on the slow path). In long-running guests most memory is already backed, so this is a weak signal that works best shortly after boot.

### 5.5 Page deduplication (KSM) timing

Host-side KSM merges identical pages across guests. Writing to a merged page triggers copy-on-write with measurably higher latency. This is slow to measure (minutes), host-config dependent, and not recommended for anti-cheat; it is listed for completeness.

### 5.6 Hypervisor memory hiding through EPT

Hypervisor-based cheats hide memory by changing EPT permissions (for example, separate pages for execute and read). Accesses that hit the "wrong view" cause VM exits. Defensive ideas:
- Compare instruction-fetch view and data-read view of critical code pages (hash what you execute versus what you read).
- Look for latency outliers on specific pages when switching between read and execute access.
- Combine with the CPUID/PMU timing above, since hooks that cause exits also add measurable latency elsewhere.

---

## 6. Static artifact checks on Linux

These are the Linux counterparts to Pafish and Al-Khaser registry, file, driver, and process checks. They are cheap, but they are only reliable against default configurations. Read files with raw syscalls where you can (section 9).

### 6.1 DMI and SMBIOS

Files in `/sys/class/dmi/id/`: `sys_vendor`, `product_name`, `product_version`, `bios_vendor`, `bios_version`, `board_vendor`, `board_name`, `chassis_vendor`, `chassis_type`. Most are world-readable. `product_uuid`, `product_serial`, and `board_serial` need root. The raw table is `/sys/firmware/dmi/tables/DMI` (root).

| Hypervisor | Typical values |
|---|---|
| QEMU/KVM | `sys_vendor`: `QEMU`; `product_name`: `Standard PC (Q35 + ICH9, 2009)` or `Standard PC (i440FX + PIIX, 1996)`; `bios_vendor`: `SeaBIOS` or `EDK II` (OVMF) |
| RHEL KVM | `sys_vendor`: `Red Hat`; `product_name`: `KVM` |
| VirtualBox | `sys_vendor`: `innotek GmbH` (or `Oracle Corporation`); `product_name`: `VirtualBox` |
| VMware | `sys_vendor`: `VMware, Inc.`; `product_name`: `VMware Virtual Platform` or `VMware7,1` |
| Hyper-V | `sys_vendor`: `Microsoft Corporation`; `product_name`: `Virtual Machine` |
| Xen | `sys_vendor`: `Xen`; `product_name`: `HVM domU` |
| Parallels | `sys_vendor`: `Parallels Software International Inc.` |
| Google Cloud | `sys_vendor`: `Google`; `product_name`: `Google Compute Engine` |
| AWS Nitro | `sys_vendor` and `bios_vendor`: `Amazon EC2`; `product_name`: instance type |

`EDK II` alone is not a VM signal, since it is also the base of many real UEFI firmwares.

### 6.2 PCI devices

Enumerate `/sys/bus/pci/devices/*/{vendor,device,class}` (no root needed).

| Vendor ID | Owner | Notes |
|---|---|---|
| `0x1af4` | Red Hat (virtio) | virtio-net, virtio-blk, virtio-gpu, balloon |
| `0x1b36` | Red Hat (QEMU devices) | QXL `1b36:0100`, PCIe root ports, xHCI |
| `0x1234` | QEMU/Bochs VGA | `1234:1111` is the standard VGA |
| `0x15ad` | VMware | SVGA, vmxnet3 |
| `0x80ee` | VirtualBox | VBoxGuest, VGA |
| `0x1414` | Microsoft | Hyper-V devices |
| `0x5853` | Xen | platform device |
| `0x1ab8` | Parallels | |
| `0x1d0f` | Amazon | ENA, NVMe on Nitro |

Emulated Intel chipsets are a giveaway: `8086:1237` (i440FX host bridge), `8086:7000` (PIIX3), `8086:29c0` (Q35 host bridge), `8086:2918` (ICH9 LPC). Also look at topology: a real PC has dozens of devices and IOMMU groups; a minimal guest has a handful.

With GPU passthrough (VFIO), the GPU is real but the rest of the PCI tree is virtual, so check all devices, not just the GPU.

### 6.3 Disks, NICs, GPUs

- Block devices: `/sys/block/*/device/{vendor,model}` (`QEMU HARDDISK`, `VBOX HARDDISK`, `VMware Virtual disk`, `Virtual Disk`); device names `vda`, `xvda`; `QEMU DVD-ROM`.
- NIC drivers: symlink `/sys/class/net/*/device/driver` pointing to `virtio_net`, `e1000` (QEMU default), `vmxnet3`, `hv_netvsc`, `xen-netfront`.
- MAC OUIs (`/sys/class/net/*/address`): `52:54:00` QEMU/KVM, `08:00:27` VirtualBox, `00:0C:29` / `00:50:56` / `00:05:69` VMware, `00:15:5D` Hyper-V, `00:16:3E` Xen, `00:1C:42` Parallels. A locally administered bit set on a physical-looking NIC is also suspicious.
- DRM drivers (`/sys/class/drm/card*/device/driver`): `virtio_gpu`, `vmwgfx`, `bochs-drm`, `qxl`, `vboxvideo`.

### 6.4 Kernel modules and drivers

`/proc/modules`, `/sys/module/`, `/sys/bus/virtio/`, `/sys/bus/vmbus/`.

- virtio: `virtio_pci`, `virtio_net`, `virtio_blk`, `virtio_scsi`, `virtio_balloon`, `virtio_console`, `virtio_gpu`, `9pnet_virtio`
- VirtualBox: `vboxguest`, `vboxsf`, `vboxvideo`
- VMware: `vmw_balloon`, `vmw_vmci`, `vmwgfx`, `vmxnet3`, `vmw_pvscsi`
- Hyper-V: `hv_vmbus`, `hv_netvsc`, `hv_storvsc`, `hv_utils`, `hv_balloon`
- Xen: `xen_blkfront`, `xen_netfront`, `xen-balloon`
- QEMU graphics: `qxl`, `bochs`

Built-in drivers do not appear in `/proc/modules`, so also check `/sys/bus/*`.

### 6.5 Guest agents and processes

Scan `/proc/*/comm` and `/proc/*/cmdline`: `qemu-ga`, `spice-vdagent(d)`, `VBoxService`, `VBoxClient`, `vmtoolsd`, `vmware-user`, `hv_kvp_daemon`, `hv_vss_daemon`, `hv_fcopy_daemon`, `xe-daemon`, `cloud-init`, `google_guest_agent`, `amazon-ssm-agent`. Easy to remove.

### 6.6 Kernel and sysfs reports

- `/sys/hypervisor/type` and `/sys/hypervisor/uuid` (Xen; EC2 Xen instances show a UUID beginning with `ec2`).
- `dmesg` or `/var/log/kern.log`: `Hypervisor detected: KVM`, `clocksource: Switched to clocksource kvm-clock`. `kernel.dmesg_restrict` may block unprivileged reads.
- Clocksource: `/sys/devices/system/clocksource/clocksource0/current_clocksource` shows `kvm-clock`, `hyperv_clocksource_tsc_page`, or `xen` on paravirtualized guests.
- `systemd-detect-virt --vm` and `virt-what` bundle many of these checks (DMI, CPUID, `/proc/xen`, device tree, `/sys/hypervisor`). Reading their source is a quick way to see what a mature implementation checks.

### 6.7 ACPI tables

`/sys/firmware/acpi/tables/` (root). Check the OEM ID and OEM Table ID in `FACP`, `DSDT`, `SSDT`, and `APIC`:

| Hypervisor | OEM ID / Table ID |
|---|---|
| QEMU/SeaBIOS/OVMF | `BOCHS ` / `BXPC    ` |
| VirtualBox | `VBOX  ` |
| VMware | `VMWARE` |
| Xen | `Xen` |
| Hyper-V | `VRTUAL` / `MICROSFT` |

### 6.7b MSRs

With root and the `msr` module loaded, read `/dev/cpu/N/msr`. Useful MSRs: `IA32_FEATURE_CONTROL` (0x3A), `IA32_VMX_*` (0x480 and up), `IA32_PLATFORM_INFO` (0xCE), `IA32_MPERF`/`IA32_APERF` (0xE7/0xE8), RAPL energy (0x611). Guests commonly fail these with an I/O error because the MSR is not exposed. Kernel lockdown can block the msr device. Treat results as soft signals.

### 6.8 Missing hardware features

Real desktops and laptops usually have:
- `/sys/class/thermal/thermal_zone*`, `/sys/class/hwmon/*`
- `/sys/devices/system/cpu/cpu0/cpufreq` (frequency scaling)
- `/sys/class/powercap` (RAPL) on Intel/AMD
- `/sys/kernel/iommu_groups/*` (IOMMU active)
- A battery or AC adapter on laptops
- Input devices under `/dev/input/` with real vendor strings (`/proc/bus/input/devices`)
- Normal uptime and user activity

A minimal VM lacks most of these. Because each is easy to emulate or fake, use them as a feature count, not a verdict. Note that bare-metal servers and some SBCs also lack them.

### 6.9 Display and input realism

Check screen resolution and mode lists (DRM, `xrandr`, Wayland output info), pointer movement over time (`XQueryPointer` or libinput), keyboard/mouse device names, and idle time. Sandboxes often run at 800x600 or 1024x768 with no input activity.

### 6.10 Environment and identity

Hostnames and usernames matching analysis patterns (`sandbox`, `malware`, `vm`, `test`), tiny disks (under 60 GB), very short uptime, and very low process counts. All trivially changeable, so weight them low.

---

## 7. Hidden hypervisor detection and the hardened guest

### 7.1 What a hardened environment hides

Typical VFIO-style guests and hypervisor cheats try to remove: the hypervisor CPUID bit and vendor string, DMI/SMBIOS and ACPI identifiers, virtual PCI devices, guest agents and modules, MAC OUIs, and timing differences (TSC offsetting, trapping RDTSC). That defeats sections 3.1, 3.2, and 6 almost completely.

### 7.2 What remains hard to hide

- The real cost of VM exits (CPUID, MSR accesses on trapped ranges, EPT violations). Hiding it needs either TSC manipulation (detectable with the PMU or an external clock) or very low-overhead exits.
- Hardware-level behavior: cache sizes, memory latency, and TLB costs that do not match claimed topology.
- Inconsistencies between sources (CPUID instruction vs `/proc/cpuinfo` vs DMI vs measured behavior).
- Missing real hardware features (thermal, cpufreq, IOMMU groups, microcode revision plausibility).
- Server-side behavior: input patterns, aim statistics, network timing.
- Boot integrity: TPM measurements, Secure Boot state, IMA logs, remote attestation.

### 7.3 Detection strategy

1. Collect raw features, not booleans (timings, distributions, strings, counts).
2. Compare the claimed CPU model to measured behavior (cache sizes, latencies).
3. Use two clocks (TSC and PMU, or TSC and server time) so no single manipulated counter hides everything.
4. Require independent categories to agree before acting.
5. Make the server the decision maker.

---

## 8. Mapping Pafish and Al-Khaser checks to Linux

Pafish (`a0rtega/pafish`) and Al-Khaser (`LordNoteworthy/al-khaser`) are Windows-only. Their categories map as follows.

| Windows check | Linux equivalent |
|---|---|
| Registry keys of VM vendors | `/sys/class/dmi/id/*`, `/sys/bus/*`, `/proc/cpuinfo`, `/proc/modules` |
| Vendor files and drivers (`VBoxMouse.sys`, `vmmouse.sys`) | Kernel modules and device nodes (`/dev/vboxguest`, `/dev/vmci`, `/dev/vport*`, `/dev/hvc*`) |
| Vendor processes (`vboxservice.exe`, `vmtoolsd.exe`) | `VBoxService`, `vmtoolsd`, `qemu-ga`, `spice-vdagent`, `hv_*_daemon` |
| Window classes, mouse movement | X11/Wayland pointer activity, input devices |
| MAC prefixes, adapter names | `/sys/class/net/*/address`, driver symlinks |
| Device names (`\\.\VBoxMiniRdrDN`) | `/dev/*`, `/sys/bus/pci`, `/sys/block/*/device/model` |
| WMI queries (`Win32_ComputerSystem`) | DMI files in sysfs |
| SMBIOS and ACPI firmware tables | `/sys/firmware/dmi/tables/DMI`, `/sys/firmware/acpi/tables/*` |
| CPUID hypervisor bit and vendor | Same instruction, same leaves |
| RDTSC delta, RDTSC+CPUID delta | Same, with Linux pinning and perf-counter cross-check |
| `Sleep` acceleration | `nanosleep`/`clock_nanosleep` against an external clock |
| Disk size, RAM size, core count | `/proc/meminfo`, `/sys/block/*/size`, `/sys/devices/system/cpu` |
| Uptime, username, file paths | `/proc/uptime`, `$USER`, home directory contents |
| `IsDebuggerPresent`, PEB flags | `TracerPid` in `/proc/self/status`, `ptrace(PTRACE_TRACEME)` behavior |
| API hook checks (Cuckoo hooks) | `LD_PRELOAD`, `/etc/ld.so.preload`, `/proc/self/maps` anomalies, libc prologue integrity |

VMAware (`kernelwernel/VMAware`) is a modern C++ library that implements many of these checks with a scoring approach and runs on Linux. Verify its current technique list in the repository before depending on it.

---

## 9. Hardening the detector on Linux

Your checker runs in an environment the attacker controls. Common Linux tampering methods and countermeasures:

| Attack | Countermeasure |
|---|---|
| `LD_PRELOAD` or `/etc/ld.so.preload` hooks on libc (`open`, `read`, `fopen`) | Use raw syscalls through inline assembly or a statically linked helper; check the environment and `/proc/self/maps` for unexpected libraries |
| Bind mounts, overlayfs, or FUSE over `/sys/class/dmi/id` and `/proc/cpuinfo` | Parse `/proc/self/mountinfo` for overlays on those paths; compare the file results with CPUID and measured behavior |
| Mount or user namespaces presenting a fake `/proc` and `/sys` | Compare namespace IDs (`/proc/self/ns/*`) with PID 1 where permitted; cross-check with raw instruction results |
| `ptrace`, seccomp-bpf, or `strace` interposing on syscalls | Check `TracerPid` and `Seccomp` in `/proc/self/status`; time your own syscalls for interception overhead |
| Patched or debugged checker binary | Integrity checks on your own code (self-hash of `.text`), obfuscation, split logic across threads |
| Emulated `/dev/cpu/*/msr` | Treat MSR results as soft; cross-validate with timing |

General rules:
- Prefer sources that cannot be faked from userspace (the CPUID instruction, TSC, PMU) over files in `/proc` and `/sys`.
- Cross-check every file-derived value against an instruction-derived or measured value.
- Randomize check order, sample counts, and thresholds. Do not ship a single boolean "is VM" function that can be patched to return false.
- Ship raw measurements to the server and decide there.
- Accept the limit: an attacker who controls the host kernel or hypervisor can defeat any client-side check. Server-side analytics and hardware attestation (TPM 2.0 measured boot with remote attestation, Secure Boot, IMA) raise the cost the most.

---

## 10. False positives and legitimate environments

| Environment | What you see | Notes |
|---|---|---|
| WSL2 | `Microsoft Hv`, `microsoft-standard-WSL2` in `/proc/version` | Real Linux kernel under Hyper-V; common for developers |
| Windows host with VBS/HVCI (guest or native Windows) | Hyper-V root partition: hypervisor bit set, CPUID always traps | Applies to Windows clients; a baseline from non-VBS machines will misjudge them |
| Cloud instances (AWS Nitro, GCP, Azure) | Vendor DMI strings, virtio/NVMe/ENA devices | Typically not gaming clients; policy decision |
| Containers (Docker, Podman, LXC) | Same CPUID/DMI as the host | Not a VM; detect via `/proc/1/cgroup`, `/.dockerenv`, namespaces if relevant |
| Proton/Wine | Windows-style APIs reporting emulated data | Wine-layer checks see emulated Windows; underlying hardware is real. Native Linux checks apply to a native client or helper |
| Linux gamers with VFIO or dual-GPU setups | Real GPU, virtual everything else | Policy decision, not necessarily cheating |
| Hybrid-core CPUs, laptops, SBCs, Steam Deck | Unusual topologies, missing thermal/cpufreq on some boards | Calibrate on real devices, not just desktops |

Decide the policy before choosing thresholds: do you ban all VMs, flag only suspicious ones, or only detect hidden hypervisors? Detecting a hidden hypervisor is the strongest and least controversial goal.

---

## 11. Scoring and decision design

Group signals into categories, and weight them by reliability:

| Category | Examples | Weight |
|---|---|---|
| Hard identity | Hypervisor bit plus known vendor string, DMI/PCI/ACPI vendor match | High (but only against default configs) |
| Hard behavior | High CPUID latency with confirming PMU/external clock mismatch | High |
| Soft behavior | Steal time, jitter, TLB ratio, cache mismatch | Low to medium |
| Soft environment | Missing thermal/cpufreq, odd microcode, low RAM, short uptime | Low |
| Consistency | CPUID vs `/proc/cpuinfo` vs DMI mismatch, bind mounts on `/proc` or `/sys` | Medium to high (indicates tampering) |

Guidelines:
- Require agreement from at least two independent categories before taking action.
- Treat tampering indicators (inconsistent sources, bind mounts, hooks) as signals in their own right.
- Learn per-CPU-model thresholds from telemetry on known-good machines instead of hard-coding cycle counts.
- Use hysteresis and repeat the measurement over time. Do not ban on a single run.
- Keep the data minimal and hash identifiers, since hardware fingerprinting has privacy and legal implications.

---

## 12. Calibration and test plan

Build a test matrix and measure each check in every cell:

1. Bare metal (several CPU generations, Intel and AMD, desktop and laptop).
2. Linux guest under KVM/QEMU with default config.
3. Linux guest under KVM/QEMU hardened (hypervisor bit hidden, SMBIOS and ACPI customized, MAC changed, TSC adjustments).
4. VirtualBox and VMware guests.
5. WSL2.
6. Cloud instances.
7. Nested virtualization.
8. Hypervisor-based cheat prototype in your lab (if you build one for testing).

For each check record the full distribution (min, p5, p50, p95), the kernel version, CPU model, and mitigations. Compute true and false positive rates per check and for the combined score. Re-run after kernel updates and new CPU releases, since latencies drift. Keep the test harness in version control so regressions are caught early.

Use Pafish and Al-Khaser in the Windows side of your lab, and `systemd-detect-virt`, `virt-what`, and VMAware on Linux, as independent references to see what they flag in each environment.

---

## Appendix A: CPUID timing probe (userspace)

```c
// vmcheck_timing.c
// Build: gcc -O2 -o vmcheck_timing vmcheck_timing.c
#define _GNU_SOURCE
#include <cpuid.h>
#include <inttypes.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <x86intrin.h>

#define SAMPLES 5000

static int cmp_u64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
    return (x > y) - (x < y);
}

static inline uint64_t tsc_fenced(void) {
    _mm_lfence();
    uint64_t t = __rdtsc();
    _mm_lfence();
    return t;
}

static uint64_t sample_cpuid(void) {
    unsigned a, b, c, d;
    uint64_t t0 = tsc_fenced();
    __cpuid(0, a, b, c, d);
    uint64_t t1 = tsc_fenced();
    (void)a; (void)b; (void)c; (void)d;
    return t1 - t0;
}

static uint64_t sample_ref(void) {
    uint64_t x = 3;
    uint64_t t0 = tsc_fenced();
    for (int i = 0; i < 64; i++)
        __asm__ volatile("imul %0, %0" : "+r"(x));   // dependent chain, no VM exit
    uint64_t t1 = tsc_fenced();
    return t1 - t0;
}

int main(void) {
    int cpu = sched_getcpu();
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(cpu >= 0 ? cpu : 0, &set);
    sched_setaffinity(0, sizeof set, &set);

    unsigned a, b, c, d;
    __cpuid(1, a, b, c, d);
    int hv = (c >> 31) & 1;
    char vendor[13] = "";
    if (hv) {
        __cpuid(0x40000000, a, b, c, d);
        memcpy(vendor, &b, 4);
        memcpy(vendor + 4, &c, 4);
        memcpy(vendor + 8, &d, 4);
        vendor[12] = 0;
    }
    printf("hypervisor bit: %d, vendor: '%s'\n", hv, vendor);

    static uint64_t cp[SAMPLES], rf[SAMPLES];
    for (int i = 0; i < 200; i++) { sample_cpuid(); sample_ref(); }   // warm up
    for (int i = 0; i < SAMPLES; i++) { cp[i] = sample_cpuid(); rf[i] = sample_ref(); }

    qsort(cp, SAMPLES, sizeof *cp, cmp_u64);
    qsort(rf, SAMPLES, sizeof *rf, cmp_u64);

    printf("cpuid cycles: min=%" PRIu64 " p50=%" PRIu64 " p95=%" PRIu64 "\n",
           cp[0], cp[SAMPLES / 2], cp[SAMPLES * 95 / 100]);
    printf("ref   cycles: min=%" PRIu64 " p50=%" PRIu64 " p95=%" PRIu64 "\n",
           rf[0], rf[SAMPLES / 2], rf[SAMPLES * 95 / 100]);
    printf("ratio cpuid/ref (p50): %.2f\n", (double)cp[SAMPLES / 2] / (double)rf[SAMPLES / 2]);
    return 0;
}
```

Interpretation: compare the numbers against baselines from your test matrix. Do not use a fixed threshold across machines.

## Appendix B: TSC versus PMU cycle probe

```c
// vmcheck_pmu.c
// Build: gcc -O2 -o vmcheck_pmu vmcheck_pmu.c
#define _GNU_SOURCE
#include <cpuid.h>
#include <errno.h>
#include <inttypes.h>
#include <linux/perf_event.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <x86intrin.h>

#define BATCH 20000

static int open_cycles(void) {
    struct perf_event_attr pe;
    memset(&pe, 0, sizeof pe);
    pe.type = PERF_TYPE_HARDWARE;
    pe.size = sizeof pe;
    pe.config = PERF_COUNT_HW_CPU_CYCLES;
    pe.disabled = 1;
    pe.exclude_kernel = 1;
    pe.exclude_hv = 1;
    return (int)syscall(SYS_perf_event_open, &pe, 0, -1, -1, 0);
}

static int run(int fd, int use_cpuid, uint64_t *tsc, uint64_t *cyc) {
    unsigned a, b, c, d;
    uint64_t x = 3, c0 = 0, c1 = 0;

    if (read(fd, &c0, sizeof c0) != sizeof c0) return -1;
    _mm_lfence();
    uint64_t t0 = __rdtsc();
    _mm_lfence();
    for (int i = 0; i < BATCH; i++) {
        if (use_cpuid) { __cpuid(0, a, b, c, d); }
        else           { __asm__ volatile("imul %0, %0" : "+r"(x)); }
    }
    _mm_lfence();
    uint64_t t1 = __rdtsc();
    if (read(fd, &c1, sizeof c1) != sizeof c1) return -1;

    *tsc = t1 - t0;
    *cyc = c1 - c0;
    (void)a; (void)b; (void)c; (void)d; (void)x;
    return 0;
}

int main(void) {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);
    sched_setaffinity(0, sizeof set, &set);

    int fd = open_cycles();
    if (fd < 0) {
        printf("PMU cycle counter unavailable (errno=%d). Soft signal only.\n", errno);
        return 1;
    }
    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);

    uint64_t tsc_ref, cyc_ref, tsc_cpuid, cyc_cpuid;
    for (int i = 0; i < 3; i++) {                 // warm up
        run(fd, 0, &tsc_ref, &cyc_ref);
        run(fd, 1, &tsc_cpuid, &cyc_cpuid);
    }
    if (run(fd, 0, &tsc_ref, &cyc_ref) || run(fd, 1, &tsc_cpuid, &cyc_cpuid)) {
        puts("read failed");
        return 1;
    }

    double r_ref   = (double)tsc_ref   / (double)cyc_ref;
    double r_cpuid = (double)tsc_cpuid / (double)cyc_cpuid;

    printf("per CPUID: tsc=%.1f cycles, pmu=%.1f cycles\n",
           (double)tsc_cpuid / BATCH, (double)cyc_cpuid / BATCH);
    printf("tsc/pmu ref=%.3f cpuid=%.3f quotient=%.2f (about 1.0 on bare metal)\n",
           r_ref, r_cpuid, r_cpuid / r_ref);
    return 0;
}
```

Interpretation: a quotient near 1.0 with a low absolute CPUID cost matches bare metal. A high TSC cost per CPUID with a much lower PMU cost indicates exits hidden from the guest's cycle counter. A high cost in both indicates a visible VM exit. A missing PMU is a soft signal only.

## Appendix C: Artifact collection snippet

```bash
#!/usr/bin/env bash
# Prints the most common VM indicators for manual inspection and test-matrix baselines.
echo "== CPU =="
grep -m1 'model name' /proc/cpuinfo
grep -m1 'microcode'  /proc/cpuinfo
grep -m1 -o 'hypervisor' /proc/cpuinfo
lscpu | grep -i -E 'hypervisor|virtualization'
echo "== DMI =="
for f in sys_vendor product_name product_version bios_vendor bios_version board_vendor board_name chassis_type; do
  printf '%s: ' "$f"; cat /sys/class/dmi/id/$f 2>/dev/null || echo n/a
done
echo "== Clocksource =="
cat /sys/devices/system/clocksource/clocksource0/current_clocksource
echo "== Steal (8th field) =="
awk '/^cpu /{print $9}' /proc/stat
echo "== PCI vendor:device =="
for d in /sys/bus/pci/devices/*; do
  echo "$(basename "$d") $(cat "$d/vendor") $(cat "$d/device")"
done
echo "== Block models =="
for d in /sys/block/*/device; do echo "$d: $(cat $d/vendor 2>/dev/null) $(cat $d/model 2>/dev/null)"; done
echo "== NICs =="
for n in /sys/class/net/*; do
  echo "$(basename "$n") $(cat "$n/address") driver=$(basename "$(readlink -f "$n/device/driver" 2>/dev/null)")"
done
echo "== Modules =="
lsmod | grep -E 'virtio|vbox|vmw|hv_|xen|qxl|bochs'
echo "== Hardware realism =="
ls /sys/class/thermal 2>/dev/null | head
ls /sys/devices/system/cpu/cpu0/cpufreq 2>/dev/null | head -3
ls /sys/class/powercap 2>/dev/null | head -3
ls /sys/kernel/iommu_groups 2>/dev/null | head -3
echo "== Tools =="
systemd-detect-virt --vm 2>/dev/null
echo "== Tamper hints =="
grep -E ' /proc | /sys ' /proc/self/mountinfo
grep -E 'TracerPid|Seccomp' /proc/self/status
echo "LD_PRELOAD=$LD_PRELOAD"; cat /etc/ld.so.preload 2>/dev/null
```

---

## References

- Intel SDM Volume 3 (VMX, VM exits, CPUID, TSC) and AMD APM Volume 2 (SVM)
- Linux kernel documentation: `Documentation/virt/kvm/x86/cpuid.rst`, `Documentation/virt/kvm/x86/msr.rst`, `Documentation/admin-guide/sysctl/kernel.rst` (`perf_event_paranoid`)
- Microsoft Hypervisor Top-Level Functional Specification (Hyper-V CPUID leaves)
- `a0rtega/pafish`: Windows sandbox and VM detection test tool
- `LordNoteworthy/al-khaser`: Windows evasion technique test suite
- `kernelwernel/VMAware`: cross-platform VM detection library
- `systemd-detect-virt` and `virt-what`: reference implementations of artifact-based detection on Linux
