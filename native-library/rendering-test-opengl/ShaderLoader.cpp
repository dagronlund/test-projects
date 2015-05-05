#include "ShaderLoader.h"
#include <iostream>
#include <fstream>
#include <vector>

using namespace Core;

ShaderLoader::ShaderLoader(void) {

}

ShaderLoader::~ShaderLoader(void) {

}

std::string ShaderLoader::ReadShader(char *fileName) {
	std::string shaderCode;
	std::ifstream file(fileName, std::ios::in);

	if (!file.good()) {
		std::cout << "Can't read file: " << fileName << std::endl;
		std::terminate();
	}

	file.seekg(0, std::ios::end);
	shaderCode.resize((unsigned int)file.tellg());
	file.seekg(0, std::ios::beg);
	file.read(&shaderCode[0], shaderCode.size());
	file.close();

	return shaderCode;
}

int ShaderLoader::CheckShaderLog(GLuint shader) {
	int result = 0;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &result);

	if (result == GL_FALSE) {
		int logSize = 0;
		glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &logSize);

		std::string log;
		log.resize(logSize);
		glGetShaderInfoLog(shader, logSize, NULL, &log[0]);

		std::cout << "Compile FAILED with message: " << &log[0] << std::endl;
	}
	return result;
}

int ShaderLoader::CheckProgramLog(GLuint program) {
	int result = 0;
	glGetProgramiv(program, GL_LINK_STATUS, &result);
	
	if (result == GL_FALSE) {
		int logSize = 0;
		glGetProgramiv(program, GL_INFO_LOG_LENGTH, &logSize);
		
		std::string log;
		log.resize(logSize);
		glGetProgramInfoLog(program, logSize, NULL, &log[0]);
		
		std::cout << "Link FAILED with message: " << &log[0] << std::endl;
	}
	return result;
}

GLuint ShaderLoader::CreateShader(GLenum shaderType, std::string source, char *shaderName) {
	int compileResult = 0;

	GLuint shader = glCreateShader(shaderType);
	const char *shaderCodePointer = source.c_str();
	const int shaderCodeSize = source.size();
	glShaderSource(shader, 1, &shaderCodePointer, &shaderCodeSize);
	glCompileShader(shader);
	glGetShaderiv(shader, GL_COMPILE_STATUS, &compileResult);

	if (CheckShaderLog(shader) == GL_FALSE)
		std::terminate();

	return shader;
}

GLuint ShaderLoader::CreateProgram(char *vsFileName, char *fsFileName) {
	std::string vsCode = ReadShader(vsFileName);
	std::string fsCode = ReadShader(fsFileName);

	GLuint vsShader = CreateShader(GL_VERTEX_SHADER, vsCode, "VertexShader");
	GLuint fsShader = CreateShader(GL_FRAGMENT_SHADER, fsCode, "FragmentShader");

	GLuint program = glCreateProgram();
	glAttachShader(program, vsShader);
	glAttachShader(program, fsShader);
	glLinkProgram(program);

	if (CheckProgramLog(program) == GL_FALSE)
		std::terminate();

	return program;
}