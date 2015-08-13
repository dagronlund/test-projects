#version 430 core
out vec4 color;

in vec3 v;
in vec3 n;

void main(void)
{
	//color = vec4(n, 1.0);
	color = vec4(0.0, 1.0, 0.0, 1.0) * max(dot(normalize(-v), n), 0.0);
}