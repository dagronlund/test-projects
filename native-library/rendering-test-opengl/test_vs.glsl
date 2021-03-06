#version 430 core

layout(location = 0) in vec3 vertex;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec3 texCoord;

uniform mat4 mvpMatrix;
uniform mat4 mvMatrix;
uniform mat3 nMatrix;

out vec3 v;
out vec3 t;
out vec3 n;
out float depth;

void main()
{
	v = vec3(mvMatrix * vec4(vertex, 1.0));
	n = normalize(nMatrix * normal);
	t = texCoord;
	depth = (mvMatrix * vec4(vertex, 1.0)).z / -500;
	gl_Position = mvpMatrix * vec4(vertex, 1.0);
}
