try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from conans import ConanFile


class CAFConan(ConanFile):
    name = "caf"
    version = '0.15.1'
    url = "https://github.com/sourcedelica/conan-recipes/tree/master/caf"
    license = "BSD-3-Clause"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    source_dir = "actor-framework"

    def config_options(self):
        if self.settings.compiler == 'gcc' and float(self.settings.compiler.version.value) >= 5.1:
            self.set_abi()

    def source(self):
        self.run("git clone https://github.com/actor-framework/actor-framework.git")
        self.run("cd %s && git checkout -b %s.x %s" % (self.source_dir, self.version, self.version))

    def build(self):
        static_suffix = "" if self.options.shared else "-only"
        configure = \
            "./configure --no-python --no-examples --no-opencl --no-tools --no-unit-tests --build-static%s" % \
            static_suffix
        self.run("cd %s && %s" % (self.source_dir, configure))
        self.run("cd %s && make" % self.source_dir)

    def package(self):
        self.copy("*.hpp",   dst="include/caf", src="%s/libcaf_core/caf" % self.source_dir)
        self.copy("*.hpp",   dst="include/caf", src="%s/libcaf_io/caf" % self.source_dir)
        self.copy("*.dylib", dst="lib",         src="%s/build/lib" % self.source_dir)
        self.copy("*.a",     dst="lib",         src="%s/build/lib" % self.source_dir)

    def package_info(self):
        self.cpp_info.libs = ["caf_io_static", "caf_core_static"]

    # TODO: remove this when https://github.com/conan-io/conan/issues/564 is fixed
    def set_abi(self):
        """CAF builds with the default GCC ABI.  Find out what it is."""
        output = StringIO()
        self.run("g++ --version -v", output)
        contents = output.getvalue()
        use_libcxx11 = '--with-default-libstdcxx-abi=new' in contents
        libcxx = 'libstdc++11' if use_libcxx11 else 'libstdc++'
        self.settings.compiler.libcxx = libcxx
        self.output.info("Setting compiler.libcxx=%s" % libcxx)
