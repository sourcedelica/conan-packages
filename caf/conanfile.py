import StringIO
from conans import ConanFile, CMake
import os
import sys
import pdb

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
    source_dir = "actor-framework"
    version = version_str

    def config(self):
        print("config")
        if self.settings.compiler == 'gcc' and float(self.settings.compiler.version.value) >= 5.1:
            self.check_abi()

    def source(self):
        print("source")
        self.run("git clone https://github.com/actor-framework/actor-framework.git")
        self.run("cd %s && git checkout -b %s.x %s" % (self.source_dir, self.version, self.version))

    def build(self):
        print("build")
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

    def check_abi(self):
        abi_check_source = """
            #include <iostream>
            int main(int argc, char **argv) {
                std::cout << _GLIBCXX_USE_CXX11_ABI;
            }
        """
        source_filename = os.tmpnam() + ".cpp"
        with open(source_filename, "w+") as tmp_file:
            tmp_file.write(abi_check_source)

        exe_filename = os.tmpnam()
        self.run("g++ %s -o %s" % (source_filename, exe_filename))

        output = StringIO.StringIO()
        self.run("%s" % exe_filename, output)
        contents = output.getvalue()
        output.close()

        os.remove(source_filename)
        os.remove(exe_filename)

        libcxx = self.settings.compiler.libcxx
        if contents == '1' and libcxx != 'libstdc++11':
            raise Exception("You must use the option -s compiler.libcxx=libstdc++11")
        if contents == '0' and libcxx != 'libstdc++':
            raise Exception("You must use the option -s compiler.libcxx=libstdc++")
