# [Conan](http://conan.io) recipe for [CAF](http://actor-framework.org)

## Setup

### GCC 5.1+

CAF compiles with the default C++ ABI.

Verify which version of the C++ ABI your compiler is using by default:

```
g++ --version -v 2>&1 | grep -- --with-default-libstdcxx-abi
```

Edit `~/.conan/conan.conf` and change `compiler.libcxx` depending on the
value of `--with-default-libstdcxx-abi`:

| ABI value | Conan `libcxx` |
|:----------|:---------------|
| `new`     | `libstdc++11`  |
| `old`     | `libstdc++`    |

You may need to run the `conan` command once to generate it.

## Building a new version of the package

1. Edit `conanfile.py` and `test_package/conanfile.py` and change the
   version attribute
2. Run `conan test_package`

The last step will build CAF and install the package in your local Conan
repository under `~/.conan/data`.

## Uploading the package to `conan.io`
```
conan upload --all caf/version@user/channel
```
where _version_ is the new version number, _user_ is the `conan.io` user 
that your packages live under, and _channel_ is one of `testing`, `beta`,
`development`, `stable`, etc.

After the package is uploaded successfully you should commit and push 
the changes to the two `conanfile.py` files to Github.