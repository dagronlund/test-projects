#pragma once

#include <vector>

namespace Core 
{

	class RenderingModelData
	{
	private:
		std::vector<int> indices;
		std::vector<float> vertices;
		std::vector<float> texCoords;
		std::vector<float> normals;

	public:
		RenderingModelData();
		~RenderingModelData(void);

		std::vector<int>* GetIndices(void);
		std::vector<float>* GetVertices(void);
		std::vector<float>* GetNormals(void);
		std::vector<float>* GetTexCoords(void);
	};
}
