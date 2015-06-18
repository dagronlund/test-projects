#pragma once

#include <iostream>
#include <fstream>
#include <vector>

#include "RenderingModelData.h"

namespace Core 
{
	enum class ObjFileFaceStatus {
		UNKNOWN, VERTEX_ONLY, VERTEX_TEXTURE, VERTEX_NORMAL, VERTEX_TEXTURE_NORMAL
	};

	class ObjFileParser 
	{
	private:
		std::ifstream fileStream;
		ObjFileFaceStatus status = ObjFileFaceStatus::UNKNOWN;
		RenderingModelData *data;

		std::string ReadLine();
		std::vector<std::string> SeparateLine(std::string line);
		void ParseFile();

		void ParseVector(const std::vector<std::string> &list,
			std::vector<float> &vectors);
		void ParseFace(const std::vector<std::string> &list,
			std::vector<int> &faces);
		void ParseFaceComponent(const std::string &component, 
			std::vector<int> &faces);
		void AssertFaceStatus(ObjFileFaceStatus newStatus);

	public:
		ObjFileParser(char *fileName);
		~ObjFileParser(void);
		RenderingModelData* GetRenderingData();
	};
}
