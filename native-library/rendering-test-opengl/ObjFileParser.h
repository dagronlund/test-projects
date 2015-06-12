#pragma once

#include <iostream>
#include <fstream>
#include <vector>

namespace Core 
{
	
	class ObjFileParser 
	{
	private:
		std::ifstream fileStream;

		std::string ReadLine();
		std::vector<std::string> SeparateLine(std::string line);
		bool ParseLine();

		void ParseVector(const std::vector<std::string> &list,
			std::vector<float> &vectors);
		void ParseFace(const std::vector<std::string> &list,
			std::vector<int> &faces);

	public:
		ObjFileParser(char *fileName);
		~ObjFileParser(void);
	};
}
