from conans import ConanFile, CMake, tools

class HumbleloggingConan(ConanFile):
	name = "humblelogging"
	version = "3.0.3"
	license = "THE BEER-WARE LICENSE"
	url = "https://github.com/insaneFactory/conan-humblelogging"
	description = "HumbleLogging is a lightweight C++ logging framework. It aims to be extendible, easy to understand and as fast as possible."
	settings = "os", "compiler", "build_type", "arch"
	options = {
		"shared": [True, False],
		"fPIC": [True, False]
	}
	default_options = {
		"shared": False,
		"fPIC": True
	}
	tool_requires = "cmake/3.22.3"
	generators = "cmake"

	def configure(self):
		if self.settings.os == "Windows":
			del self.options.fPIC

	def source(self):
		self.run("git clone https://github.com/mfreiholz/humblelogging.git")
		self.run("cd humblelogging && git fetch --all --tags --prune && git checkout tags/v" + self.version)
		# This small hack might be useful to guarantee proper /MT /MD linkage
		# in MSVC if the packaged project doesn't have variables to set it
		# properly
		tools.replace_in_file("humblelogging/CMakeLists.txt", "project(humblelogging)",
					  '''project(humblelogging)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

	def build(self):
		cmake = CMake(self)
		cmake.definitions["BuildShared"] = "ON" if self.options.shared else "OFF"
		cmake.configure(source_folder="humblelogging")
		cmake.build()

	def package(self):
		self.copy("*.h", dst="include", src="humblelogging/include", keep_path=True)
		self.copy("*humblelogging.lib", dst="lib", keep_path=False)
		self.copy("*.dll", dst="bin", keep_path=False)
		self.copy("*.so", dst="lib", keep_path=False)
		self.copy("*.dylib", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)

	def package_info(self):
		self.cpp_info.libs = ["humblelogging"]
