try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from conans import ConanFile
from conans.errors import ConanException
import os
import sys

version_env = "CONAN_PACKAGE_VERSION"
version_str = os.getenv(version_env)
if not version_str:
    sys.stderr.write("%s not set\n" % version_env)
    sys.exit(1)


class CAFConan(ConanFile):
    name = "caf"
    url = "https://github.com/sourcedelica/conan-recipes/tree/master/caf"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    source_dir = "actor-framework"
    version = version_str

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

    def set_abi(self):
        """CAF builds with the default GCC ABI.  """
        output = StringIO()
        self.run("g++ --version -v", output)
        contents = output.getvalue()
        use_libcxx11 = '--with-default-libstdcxx-abi=new' in contents
        libcxx = 'libstdc++11' if use_libcxx11 else 'libstdc++'
        self.settings.compiler.libcxx = libcxx
	self.output.info("Setting compiler.libcxx=%s" % libcxx)
