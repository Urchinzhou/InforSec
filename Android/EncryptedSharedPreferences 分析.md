# EncryptedSharedPreferenes 分析

[EncryptedSharedPreferences 源码](https://github.com/androidx/androidx/blob/androidx-master-dev/security/crypto/src/main/java/androidx/security/crypto/EncryptedSharedPreferences.java)

EncryptedSharedPreferenes 是 androidx 下安全组件中的加密类，实现`SharedPreferences`的键值对加密。

对它的分析，主要涉及以下几点：

- 密钥从哪儿来，存哪儿去
- 所用加密算法是什么
- 工程实现流程
- 内部源码分析

