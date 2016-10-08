from conans import ConanFile, CMake


class CAFConan(ConanFile):
    name = "caf"
    version = "0.15.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    source_dir = "actor-framework"
    # No exports necessary

    def source(self):
        self.run("git clone https://github.com/actor-framework/actor-framework.git")
        self.run("cd %s && git checkout %s" % (self.source_dir, self.version))

    def build(self):
        cmake = CMake(self.settings)
        off = "-DCAF_NO_EXAMPLES=yes -DCAF_NO_TOOLS=yes -DCAF_NO_UNIT_TESTS=yes -DCAF_NO_OPENCL=yes -DCAF_NO_PYTHON=yes"
        shared_definition = "-DCAF_BUILD_STATIC=yes" if self.options.shared \
            else "-DCAF_BUILD_STATIC_ONLY=yes"
        self.run('cmake %s/%s %s %s %s' %
                 (self.conanfile_directory, self.source_dir, cmake.command_line, shared_definition, off))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.hpp", dst="include/caf", src="actor-framework/libcaf_core/caf")
        self.copy("*.hpp", dst="include/caf", src="actor-framework/libcaf_io/caf")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.dylib", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["caf_io", "caf_core"]