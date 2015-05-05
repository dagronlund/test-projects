#pragma once

#include "GL\glew.h"
#include "GL\freeglut.h"
#include <iostream>

namespace Core {
	
	class ShaderLoader {
	private:
		std::string ReadShader(char *fileName);
		GLuint CreateShader(GLenum shaderType, std::string source, char *shaderName);
		int CheckShaderLog(GLuint shader);
		int CheckProgramLog(GLuint shader);

	public:
		ShaderLoader(void);
		~ShaderLoader(void);
		GLuint CreateProgram(char * vertexShaderFileName, char * fragmentShaderFileName);
	};
}