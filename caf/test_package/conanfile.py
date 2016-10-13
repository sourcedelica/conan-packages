from conans import ConanFile, CMake
from conans.util.files import save
import os
import sys

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

    def build(self):
        # TODO - copy tests from package source to tests dir
        """
        rm -rf sparse-caf
        mkdir sparse-caf
        cd sparse-caf
        git init
        git remote add origin https://github.com/actor-framework/actor-framework.git
        git config core.sparseCheckout true
        save(".git/info/sparse-checkout", "libcaf_test")
        save(".git/info/sparse-checkout", "libcaf_core/test", True)
        save(".git/info/sparse-checkout", "libcaf_io/test", True)
        git pull origin %s --depth 1 % version
        # copy files from sparse-caf
        """
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)


    def test(self):
        self.run(os.sep.join([".","bin", "caf-test"]))
