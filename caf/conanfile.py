from conans import ConanFile, CMake


class CAFConan(ConanFile):
    name = "caf"
    version = "0.15.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    # No exports necessary

    def source(self):
        self.run("git clone https://github.com/actor-framework/actor-framework.git")

    def build(self):
        cmake = CMake(self.settings)
        shared_definition = "" if self.options["shared"] else "-DCAF_BUILD_STATIC_ONLY=yes"
        self.run('cmake %s/actor-framework %s %s' %
                 (self.conanfile_directory, cmake.command_line, shared_definition))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.lib", dst="lib", src="lib")
        self.copy("*.dylib", dst="lib", src="lib")
        self.copy("*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["caf_io", "caf_core"]
