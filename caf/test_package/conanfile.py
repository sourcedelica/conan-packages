try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from conans import ConanFile, CMake
from conans.errors import ConanException
from conans.util.files import save
from conans.client.output import ConanOutput
import os
import sys


def env(name, default=None):
    value = os.environ.get(name, default)
    if not value:
        out = ConanOutput(sys.stdout, True)
        out.error("You must set the %s environment variable" % name)
        sys.exit(1)
    return value


class CAFReuseConan(ConanFile):
    version  = env('CAF_CONAN_VERSION')
    username = env('CAF_CONAN_USERNAME', 'sourcedelica')  # FIXME
    channel  = env('CAF_CONAN_CHANNEL', 'testing')        # FIXME

    requires = "caf/%s@%s/%s" % (version, username, channel)
    settings = "os", "compiler", "build_type", "arch"
    default_options = "caf:shared=False"
    generators = "cmake"

    def build(self):
        if self.settings.compiler == 'gcc' and float(self.settings.compiler.version.value) >= 5.1:
            if self.settings.compiler.libcxx != 'libstdc++11':
                raise ConanException("You must use the setting compiler.libcxx=libstdc++11")
        self.copy_tests()

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
