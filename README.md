For building with llvm toolchain (tested with 3.4.2, 3.8, 3.9)
```
make ARCH=x86_64 CC=clang defconfig
make ARCH=x86_64 CC=clang
```

Optionally:
```
HOSTCC=clang KBUILD_OUTPUT=build-dir
```

Now `allyesconfig` is fine, except KASAN.


------------

Make sure enable `CONFIG_X86_INTEL_MPX` in the `.config` file. To enable the MPX ISs.

