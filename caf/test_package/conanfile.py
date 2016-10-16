try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from conans import ConanFile, CMake
from conans.errors import ConanException
from conans.util.files import save
import os
import sys
import pdb


class CAFReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    version = '0.15.1'
    username = 'sourcedelica'  # FIXME
    channel = 'testing'        # FIXME
    requires = "caf/%s@%s/%s" % (version, username, channel)
    default_options = "caf:shared=False"
    generators = "cmake"

    def config_options(self):
        self.has_libcxx = "libcxx" in self.settings.compiler.fields
        print("has_libcxx=" , self.has_libcxx)

    # TODO: remove this when https://github.com/conan-io/conan/issues/564 is fixed
    def set_abi(self):
        """CAF builds with the default GCC ABI - use it for the package"""
        output = StringIO()
        self.run("g++ --version -v", output)
        contents = output.getvalue()
        use_libcxx11 = '--with-default-libstdcxx-abi=new' in contents
        libcxx = 'libstdc++11' if use_libcxx11 else 'libstdc++'
        self.settings.compiler.libcxx = libcxx
        self.output.info("test_package setting compiler.libcxx=%s" % libcxx)

    def build(self):
        self.copy_tests()
        if self.settings.compiler == 'gcc' and float(self.settings.compiler.version.value) >= 5.1:
            self.set_abi()

        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def copy_tests(self):
        tests_dir = "%s/tests" % self.conanfile_directory
        repo_url = "https://github.com/actor-framework/actor-framework.git"
        self.run("rm -rf %s" % tests_dir)
        self.run("git init %s" % tests_dir)
        self.run("cd %s && git remote add origin %s" % (tests_dir, repo_url))
        self.run("cd %s && git config core.sparseCheckout true" % tests_dir)
        sparse_checkout = "%s/.git/info/sparse-checkout" % tests_dir
        save(sparse_checkout, "libcaf_test\n")
        save(sparse_checkout, "libcaf_io/test\n", True)
        self.run("cd %s && git pull origin %s --depth 1" % (tests_dir, self.version))

    def test(self):
        self.run(os.sep.join([".", "bin", "caf-test"]))
