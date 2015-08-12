#pragma once

#include <iostream>
#include <time.h>

#include "GL\glew.h"
#include "GL\freeglut.h"

#include "glm\vec3.hpp"
#include "glm\glm.hpp"
#include "glm\gtc\matrix_transform.hpp"

#include "ShaderLoader.h"
#include "ObjFileParser.h"

#pragma comment(lib, "glew32.lib")
#define _CRT_SECURE_NO_WARNINGS

using namespace glm;
using namespace Core;

GLuint program;
GLuint vbo;
GLuint vao;
GLuint indexBuffer;
int indicesCount;

float pitch = 0;
float yaw = 0;
float z = 0;
float x = 0;

void keyPress(unsigned char key, int mouseX, int mouseY)
{
	if (key == 'w')
	{
		z += .1f;
		std::cout << z << std::endl;
	}
	else if (key == 's')
	{
		z -= .1f;
		std::cout << z << std::endl;
	}
	else if (key == 'a')
	{
		x -= .1;
		std::cout << x << std::endl;
	}
	else if (key == 'd')
	{
		x += .1;
		std::cout << x << std::endl;
	}

	glutPostRedisplay();
}

mat4 cameraMatrix()
{
	mat4 projection = perspective(45.0f, 4.0f / 3.0f, 0.1f, 100.f);
	mat4 view = translate(mat4(1.0f), vec3(-x, 0.0f, z));
	//view = rotate(view, pitch, vec3(-1.0f, 0.0f, 0.0f));
	//view = rotate(view, yaw, vec3(0.0f, 1.0f, 0.0f));
	//glm::mat4 Model = glm::scale(glm::mat4(1.0f), glm::vec3(0.5f));
	//return projection * view;
	return projection * view;
}

void init(void) 
{
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_DEBUG_OUTPUT);
	ShaderLoader shaderLoader;
	program = shaderLoader.CreateProgram("test_vs.glsl", "test_fs.glsl");
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

	ObjFileParser tfp("triangle.3d");
	RenderingModelData *data = tfp.GetRenderingData();
	
	glGenVertexArrays(1, &vao);
	glBindVertexArray(vao);

	glGenBuffers(1, &vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, data->GetVertices()->size() * sizeof(float), 
		data->GetVertices()->data(), GL_STATIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, (void*)0);

	glGenBuffers(1, &indexBuffer);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, data->GetIndices()->size() * sizeof(unsigned int), 
		data->GetIndices()->data(), GL_STATIC_DRAW);
	indicesCount = data->GetIndices()->size();
}

void renderScene(void)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glClearColor(0.0, 0.0, 0.0, 1.0);

	glBindVertexArray(vao);
	glUseProgram(program);
	GLuint matId = glGetUniformLocation(program, "vpMat");
	mat4 cMat = cameraMatrix();
	glUniformMatrix4fv(matId, 1, GL_FALSE, &cameraMatrix()[0][0]);

	//glDrawArrays(GL_TRIANGLES, 0, 3);

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer);


	glDrawElements(GL_TRIANGLES, indicesCount, GL_UNSIGNED_INT, (void*)0);


	glutSwapBuffers();

	std::cout << "Drawn." << std::endl;
}

int main(int argc, char **argv) 
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(500, 500); //optional
	glutInitWindowSize(800, 600); //optional
	glutCreateWindow("Test");
	glutDisplayFunc(renderScene);
	glutKeyboardFunc(keyPress);

	if (GLEW_OK != glewInit()) 
	{
		std::cout << "GLEW Error" << std::endl;
	}
		
	if (glewIsSupported("GL_VERSION_4_3")) 
	{
		std::cout << "OpenGL 4.3 supported" << std::endl;
	}

	init();

	glutMainLoop();
	return 0;
}
