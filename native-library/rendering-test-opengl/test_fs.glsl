#version 430 core
out vec4 color;

uniform int renderType;
uniform sampler2D textureSampler;

in vec3 v;
in vec3 t;
in vec3 n;
in float depth;

void main(void)
{
	if (renderType == 0)
	{
		//color = vec4(0.0, 1.0, 0.0, 1.0);
		color = texture(textureSampler, t.xy);
	}
	else if (renderType == 1)
	{
		color = vec4(n, 1.0);
	}
	else if (renderType == 2)
	{
		color = vec4(depth, depth, depth, 1.0);
	}
	else if (renderType == 3)
	{
		color = vec4(0.0, 1.0, 0.0, 1.0) * .25 + vec4(0.0, 1.0, 0.0, 1.0) * max(dot(normalize(-v), n), 0.0) * .75;
	}
}
