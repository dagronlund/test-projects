#version 430 core

layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 normal;

uniform mat4 mvpMatrix;
uniform mat4 mvMatrix;
uniform mat3 nMatrix;

out vec3 v;
out vec3 n;

void main()
{
	v = vec3(mvMatrix * vec4(vertex, 1.0));
	n = normalize(nMatrix * normal);
	gl_Position = mvpMatrix * vec4(vertex, 1.0);
}
