project(CAFReusePackage)
cmake_minimum_required(VERSION 3.5.1)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++1z")
#set(CMAKE_BINARY_DIR /Users/eric/PycharmProjects/conan-recipes/caf/test_package/build/e2cfbe22535234e76cb415e6154e331c12e858d4)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB_RECURSE tests "tests/src/*.cpp")
add_executable(caf-test
             ${tests}
             tests/caf/test/unit_test.hpp
             tests/caf/test/unit_test_impl.hpp)
target_include_directories(caf-test PUBLIC tests)
target_link_libraries(caf-test
                    ${LD_FLAGS}
                    ${CONAN_LIBS}
                    ${PTHREAD_LIBRARIES})
