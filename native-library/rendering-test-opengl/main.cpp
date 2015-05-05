#pragma once

#include "GL\glew.h"
#include "GL\freeglut.h"
#include "ShaderLoader.h"
#include "gmtl\Vec.h"

#include <iostream>

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

	gmtl::Vec3f v;
	
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
		std::cout << "Um... fuck?" << std::endl;

	if (glewIsSupported("GL_VERSION_4_4")) {
		std::cout << "GLEW version 4.4 supported." << std::endl;
	} else {
		std::cout << "GLEW version 4.4 not supported." << std::endl;
	}

	init();

	glutMainLoop();
	return 0;
}