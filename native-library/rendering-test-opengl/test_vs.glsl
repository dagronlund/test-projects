#version 430 core

layout(location = 0) in vec3 in_position;
uniform mat4 vpMat;
 
void main()
{
	gl_Position = vpMat * vec4(in_position, 1.0);
}
