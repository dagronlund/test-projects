#pragma once

#include <iostream>
#include <time.h>

#include "GL\glew.h"
#include "GL\freeglut.h"

#include "glm\vec3.hpp"
#include "glm\glm.hpp"
#include "glm\gtc\matrix_transform.hpp"

#include "lodepng.h"

#include "ShaderLoader.h"
#include "ObjFileParser.h"

#pragma comment(lib, "glew32.lib")
#define _CRT_SECURE_NO_WARNINGS

using namespace glm;
using namespace Core;

GLuint program;
GLuint vao;
GLuint indexBuffer;
int indicesCount;

float pitch = 0;
float yaw = 0;
float z = -150;
float x = 0;
int renderType = 3;

void keyPress(unsigned char key, int mouseX, int mouseY)
{
	if (key == 'w')
	{
		z += 1;
		std::cout << z << std::endl;
	}
	else if (key == 's')
	{
		z -= 1;
		std::cout << z << std::endl;
	}
	else if (key == 'a')
	{
		x -= 1;
		std::cout << x << std::endl;
	}
	else if (key == 'd')
	{
		x += 1;
		std::cout << x << std::endl;
	}
	else if (key == ' ')
	{
		renderType++;
		if (renderType > 3)
		{
			renderType = 0;
		}
	}

	glutPostRedisplay();
}

mat4 GetProjectionMatrix()
{
	return perspective(45.0f, 4.0f / 3.0f, 0.1f, 500.0f);
}

mat4 GetViewMatrix()
{
	return translate(mat4(1.0f), vec3(-x, 0.0f, z));
}

mat4 GetCameraMatrix()
{
	return GetProjectionMatrix() * GetViewMatrix();
}

void init(void) 
{
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_DEBUG_OUTPUT);
	ShaderLoader shaderLoader;
	program = shaderLoader.CreateProgram("test_vs.glsl", "test_fs.glsl");
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

	ObjFileParser tfp("teapot_textures.3d");
	RenderingModelData *data = tfp.GetRenderingData();
	
	glGenVertexArrays(1, &vao);
	glBindVertexArray(vao);

	GLuint vertexBuffer;
	glGenBuffers(1, &vertexBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer);
	glBufferData(GL_ARRAY_BUFFER, data->GetVertices()->size() * sizeof(float), 
		data->GetVertices()->data(), GL_STATIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, (void*)0);

	GLuint normalBuffer;
	glGenBuffers(1, &normalBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, normalBuffer);
	glBufferData(GL_ARRAY_BUFFER, data->GetNormals()->size() * sizeof(float),
		data->GetNormals()->data(), GL_STATIC_DRAW);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, (void*)0);

	GLuint texCoordBuffer;
	glGenBuffers(1, &texCoordBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, texCoordBuffer);
	glBufferData(GL_ARRAY_BUFFER, data->GetTexCoords()->size() * sizeof(float),
		data->GetTexCoords()->data(), GL_STATIC_DRAW);
	glEnableVertexAttribArray(2);
	glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sizeof(float) * 3, (void*)0);

	glGenBuffers(1, &indexBuffer);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, data->GetIndices()->size() * sizeof(unsigned int), 
		data->GetIndices()->data(), GL_STATIC_DRAW);
	indicesCount = data->GetIndices()->size();

	std::vector<unsigned char> image;
	unsigned int width, height;
	unsigned int error = lodepng::decode(image, width, height, "texture.png");
	std::cout << error << std::endl;

	GLuint texture;
	glGenTextures(1, &texture);
	glBindTexture(GL_TEXTURE_2D, texture);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image.data());
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
}

void renderScene(void)
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glClearColor(0.0, 0.0, 0.0, 1.0);

	glBindVertexArray(vao);
	glUseProgram(program);

	glUniformMatrix4fv(glGetUniformLocation(program, "mvpMatrix"), 
		1, GL_FALSE, &GetCameraMatrix()[0][0]);

	glUniformMatrix4fv(glGetUniformLocation(program, "mvMatrix"),
		1, GL_FALSE, &GetViewMatrix()[0][0]);

	glUniformMatrix3fv(glGetUniformLocation(program, "nMatrix"),
		1, GL_FALSE, &transpose(inverse(mat3(GetViewMatrix())))[0][0]);

	glUniform1i(glGetUniformLocation(program, "renderType"), renderType);

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
