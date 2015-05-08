#pragma once

#include <iostream>

#include "GL\glew.h"
#include "GL\freeglut.h"
#include "vec3.hpp"
#include "glm\glm.hpp"

#include "ShaderLoader.h"
#include "ObjFileParser.h"

using namespace glm;
using namespace Core;

GLuint program;

void renderScene(void) {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glClearColor(1.0, 0.0, 0.0, 1.0);

	glUseProgram(program);
	glDrawArrays(GL_TRIANGLES, 0, 3);

	glutSwapBuffers();
}

void init(void) {
	glEnable(GL_DEPTH_TEST);
	ShaderLoader shaderLoader;
	program = shaderLoader.CreateProgram("test_vs.glsl", "test_fs.glsl");
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

	vec3 p = vec3(0.0f, 0.0f, 0.0f);
	
	std::cout << "Stuff here: " << std::endl;
	ObjFileParser tfp("model_test.obj");
	//std::vector<std::string> list = tfp.ParseLine();
	//for (std::vector<std::string>::size_type i = 0; i < list.size(); ++i) {
	//	std::cout << list[i].c_str() << std::endl;
	//}
	////std::string s;
	////while (!(s = tfp.ReadLine()).empty())
	////	std::cout << s.c_str() << std::endl;
	//tfp.ParseLine();

}

int main(int argc, char **argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(500, 500);//optional
	glutInitWindowSize(800, 600); //optional
	glutCreateWindow("OpenGL First Window");
	glEnable(GL_DEPTH_TEST);
	glutDisplayFunc(renderScene);

	GLenum error = glewInit();
	if (GLEW_OK != error)
		std::cout << "Um... what?" << std::endl;

	if (glewIsSupported("GL_VERSION_4_4")) {
		std::cout << "GLEW version 4.4 supported." << std::endl;
	} else {
		std::cout << "GLEW version 4.4 not supported." << std::endl;
	}

	init();

	glutMainLoop();
	return 0;
}
