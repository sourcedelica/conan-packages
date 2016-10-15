try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from conans import ConanFile, CMake
from conans.util.files import save
import os
import sys
import pdb

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "sourcedelica")
version_env = "CONAN_PACKAGE_VERSION"
version_str = os.getenv(version_env)
if not version_str:
    sys.stderr.write("%s not set\n" % version_env)
    sys.exit(1)


class CAFReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    version = version_str
    requires = "caf/%s@%s/%s" % (version, username, channel)
    default_options = "caf:shared=False"
    generators = "cmake"

    def config_options(self):
        self.has_libcxx = "libcxx" in self.settings.compiler.fields
        print("has_libcxx=" , self.has_libcxx)

    def set_abi(self):
        """CAF builds with the default GCC ABI.  """
        output = StringIO()
        self.run("g++ --version -v", output)
        contents = output.getvalue()
        use_libcxx11 = '--with-default-libstdcxx-abi=new' in contents
        libcxx = 'libstdc++11' if use_libcxx11 else 'libstdc++'
        self.settings.compiler.libcxx = libcxx
        self.output.info("test_package setting compiler.libcxx=%s" % libcxx)

    def build(self):
        self.copy_tests()
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
