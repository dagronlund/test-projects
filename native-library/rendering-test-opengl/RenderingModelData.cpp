#include "RenderingModelData.h"

using namespace std;
using namespace Core;

RenderingModelData::RenderingModelData()
{
}

RenderingModelData::~RenderingModelData(void)
{
}

vector<int>* RenderingModelData::GetIndices(void)
{
	return &indices;
}

vector<float>* RenderingModelData::GetVertices(void)
{
	return &vertices;
}

vector<float>* RenderingModelData::GetNormals(void)
{
	return &normals;
}

vector<float>* RenderingModelData::GetTexCoords(void)
{
	return &texCoords;
}

