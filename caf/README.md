Conan recipe for [CAF](http://actor-framework.org)
==================================================

TODO
----
- I copied the tests for 0.15.1 manually into `test_package/tests`.  This needs to be automated by `test_package/conanfile.py`.

CAF build parameters
--------------------

```
Libcaf version:    0.15.1

Build type:        Release
Build static:      no
Build static only: yes
Runtime checks:    no
Log level:         none
With mem. mgmt.:   yes
With exceptions:   yes

Build I/O module:  yes
Build tools:       no
Build examples:    no
Build unit tests:  no
Build benchmarks:  no
Build opencl:      no
Build Python:      no

CXX:               /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++
CXXFLAGS:          -std=c++11 -Wextra -Wall -pedantic -ftemplate-depth=512 -ftemplate-backtrace-limit=0 -stdlib=libc++ -fPIC -O3 -DNDEBUG
```