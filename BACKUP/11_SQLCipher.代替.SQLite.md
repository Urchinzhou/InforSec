# [SQLCipher 代替 SQLite](https://github.com/Urchinzhou/gitblog/issues/11)

SQLCipher 是基于 SQLite 的安全扩展，加解密行为对应用层透明，可使用标准 SQLite API 执行数据库操作，移植简单，以页为单位进行加解密操作，效率高，开销比 SQLite 多 5% 左右。

### 安全特性

- 加密算法使用 AES-256 CBC模式；
- 使用口令初始化数据库，实际加密密钥根据口令派生产生，相同口令派生出的密钥不同；
- 以页为单位加解密，默认页大小 4096 Bytes，可调整优化；
- 对每一页写的时候，文末会附带消息验证码，用于读取时校验；
- 加密算法由 OpenSSL libcrypto 等开源库支持；

### 业务流程

<img src="https://s3.ax1x.com/2021/01/28/y94yrj.md.png" width=500 alt="flow" align=center />

### 效果对比

- SQLite

<img src="https://s3.ax1x.com/2021/01/29/yCo7B4.png" alt="yCo7B4.png" border="0"/>

- SQLCipher

<img src="https://s3.ax1x.com/2021/01/29/yCTev8.png" alt="yCTev8.png" border="0" />

### 应用示例（Android）

- [Using SQLCipher for Android With Room](https://github.com/sqlcipher/android-database-sqlcipher#using-sqlcipher-for-android-with-room)
- [Using SQLCipher for Android's Native API](https://github.com/sqlcipher/android-database-sqlcipher#using-sqlcipher-for-androids-native-api)

### FAQ：

[如何使用 SQLCipher 加密明文 SQLite 数据库](https://discuss.zetetic.net/t/how-to-encrypt-a-plaintext-sqlite-database-to-use-sqlcipher-and-avoid-file-is-encrypted-or-is-not-a-database-errors/868)

