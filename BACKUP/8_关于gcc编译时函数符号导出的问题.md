# [关于gcc编译时函数符号导出的问题](https://github.com/Urchinzhou/gitblog/issues/8)

背景：在 Android P liblog 模块中增加一个功能，涉及外部函数调用。如在 `A.c` 中定义函数 `fun`，在 `A.h` 中声明函数 `fun`，在 `B.c` 中包含 `A.h` 后调用 `fun`，文件名、路径等均没有问题，但编译时会触发 `error:undefined reference to `。

分析：函数显然是定义了的，提示未定义应该是出于某种原因未找到。后发现 `logprint.c` 文件中部分函数带有前缀 `LIBLOG_ABI_PUBLIC`，该宏定义为 `#define LIBLOG_ABI_PUBLIC __attribute__((visibility("default")))`，作用是设置符号的可见性属性，查看 liblog 的 Android.bp 文件，发现编译选项设置为

```c
cflags: [
        "-Werror",
        "-fvisibility=hidden",
  ......
  ]
```

可见性属性会覆盖编译时通过 `-fvisibility` 选项指定的值，`default` 可见性属性会使符号在所有情况下都被输出，`hidden` 可见性属性会隐藏相应的符号。

结论：该模块在编译时，通过编译选项 `"-fvisibility=hidden"` 将符号的默认可见性属性设置为不可见，因此，对于源文件中没有显示声明为可见的函数或变量，无法被共享库的其它文件访问，从而导致编译时触发 `error:undefined reference to `，解决办法是将需要对外共享的函数、变量的可见性属性标识为 `default`。

参考阅读：

[控制符号的可见性](https://my.huhoo.net/archives/2010/03/post_52.html)