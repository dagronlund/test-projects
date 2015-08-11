#pragma once

namespace Core 
{

	class RenderingModelData
	{
	private:
		int *indices;
		float *vertices;
		float *normals;
		float *texCoords;

	public:
		RenderingModelData(int *indices, float *vertices, float *normals,
			float *texCoords);
		~RenderingModelData(void);

		int *GetIndices(void);
		float *GetVertices(void);
		float *GetNormals(void);
		float *GetTexCoords(void);
	};
}


