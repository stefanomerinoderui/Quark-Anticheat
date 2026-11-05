obj-m += quark_kernel.o

KDIR ?= /lib/modules/$(shell uname -r)/build

# Kernels built with clang (e.g. CachyOS) require building modules with LLVM too.
ifneq ($(shell grep -s '^CONFIG_CC_IS_CLANG=y' $(KDIR)/.config),)
LLVM_FLAG = LLVM=1
endif

# Build using the running kernel build system.
#
# `all` builds the release module: VM detection is enforced unconditionally,
# and the code path that would bypass it is not compiled in at all.
#
# `testing` additionally defines QUARK_TESTING_BUILD, which compiles in the
# VM-check bypass -- needed on hosts that are themselves hypervisor guests
# (e.g. this project's own VM test rig), never intended for a real release.
all:
	make -C $(KDIR) M=$(CURDIR) $(LLVM_FLAG) modules

testing:
	make -C $(KDIR) M=$(CURDIR) $(LLVM_FLAG) modules ccflags-y="-DQUARK_TESTING_BUILD"

clean:
	make -C $(KDIR) M=$(CURDIR) $(LLVM_FLAG) clean
