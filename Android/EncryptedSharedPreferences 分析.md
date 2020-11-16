# EncryptedSharedPreferenes 分析

[EncryptedSharedPreferences 源码](https://github.com/androidx/androidx/blob/androidx-master-dev/security/crypto/src/main/java/androidx/security/crypto/EncryptedSharedPreferences.java)

EncryptedSharedPreferenes 是 androidx 下安全组件中的加密类，实现`SharedPreferences`的键值对加密。

对它的分析，主要涉及以下几点：

- 密钥管理
- 加密算法
- 工程实现
- 源码分析

开发者文档中提供了`SharedPreferences`加密键值对的实例代码，其中使用`MasterKeys`来进行密钥管理，而在 [MasterKeys](https://developer.android.com/reference/androidx/security/crypto/MasterKeys?hl=zh-cn) 的文档中提示该类已废弃，应使用`MasterKey.Builder`来管理主密钥，示例如下

```java
 // this is equivalent to using deprecated MasterKeys.AES256_GCM_SPEC
 KeyGenParameterSpec spec = new KeyGenParameterSpec.Builder(
         MASTER_KEY_ALIAS,
         KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
         .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
         .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
         .setKeySize(KEY_SIZE)
         .build();
 MasterKey masterKey = new MasterKey.Builder(MainActivity.this)
         .setKeyGenParameterSpec(spec)
         .build();
 EncryptedSharedPreferences.create(
         MainActivity.this,
         "your-app-preferences-name",
         masterKey, // masterKey created above
         EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
         EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM);
```

### 密钥管理

`KeyGenParameterSpec`是`android.security.keystore`中的类，用于指定密钥的参数，相当于先制定一个规范，规范中指明密钥别名、密钥用途、加密模式等密钥属性，然后在生成密钥的时候直接使用指定的规范。我们重点需要关注的是，主密钥的生成和存储，也就是下面调用的`MasterKey.Builder`方法。

`MasterKey.Builder`就是用于生成`MasterKey`的构建器，最终生成密钥的方法是构建器里的`build()`，那么在`build()`里面做了什么事情，需要深入到[源码](https://github.com/androidx/androidx/blob/androidx-master-dev/security/crypto/src/main/java/androidx/security/crypto/MasterKey.java)里面去看看。

```java
/**
* Builds a {@link MasterKey} from this builder.
* @return The master key.
*/
@NonNull
public MasterKey build() throws GeneralSecurityException, IOException {
	if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
		return buildOnM();
	} else {
		return new MasterKey(mKeyAlias, null);
	}
}

private MasterKey buildOnM() throws GeneralSecurityException, IOException {
  ...
  if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P && mRequestStrongBoxBacked) {
    if (mContext.getPackageManager().hasSystemFeature(
      PackageManager.FEATURE_STRONGBOX_KEYSTORE)) {
      builder.setIsStrongBoxBacked(true);
    }
  }
  mKeyGenParameterSpec = builder.build();//完成KeyGenParameterSpec的构建
  ...
  @SuppressWarnings("deprecation")
    String keyAlias = MasterKeys.getOrCreate(mKeyGenParameterSpec);//按照Spec指定的参数创建密钥
  return new MasterKey(keyAlias, mKeyGenParameterSpec);
}
```

我们以 Android 9.0 为参考，`build`中调用的是 `buildOnM()`，而在`buildOnM()`中会检查系统是否支持基于硬件的 StrongBox Keystore，如果支持，则调用`setIsStrongBoxBacked(true)`以设置该密钥由 StrongBox 安全芯片保护，至此密钥参数设置的最后一步完成，并返回一个`KeyGenParameterSpec`的实例，`build()`内容很简单，直接返回一个`KeyGenParameterSpec`实例，如下

```
public KeyGenParameterSpec build() {
	return new KeyGenParameterSpec(
    mKeystoreAlias,
    mNamespace,
    mKeySize,
    ......
    mIsStrongBoxBacked,
    mUserConfirmationRequired,
    mUnlockedDeviceRequired,
    mCriticalToDeviceEncryption);
  }
}
```

而后返回到`buildOnM()`中，调用`MasterKeys.getOrCreate(mKeyGenParameterSpec)`创建主密钥并返回密钥别名字符串，然后逐级返回上层调用方法。

