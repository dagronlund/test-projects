#include "RenderingModelData.h"

using namespace Core;

RenderingModelData::RenderingModelData(int *indices, float *vertices, float *normals,
	float *texCoords)
{
	this->indices = indices;
	this->vertices = vertices;
	this->normals = normals;
	this->texCoords = texCoords;
}

RenderingModelData::~RenderingModelData(void)
{
	delete indices;
	delete vertices;
	delete normals;
	delete texCoords;
}

int *RenderingModelData::GetIndices(void)
{
	return indices;
}

float *RenderingModelData::GetVertices(void)
{
	return vertices;
}

float *RenderingModelData::GetNormals(void)
{
	return normals;
}

float *RenderingModelData::GetTexCoords(void)
{
	return texCoords;
}

