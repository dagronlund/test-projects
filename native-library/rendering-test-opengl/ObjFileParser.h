#pragma once

#include <iostream>
#include <fstream>
#include <vector>

namespace Core {
	
	class ObjFileParser {
	private:
		std::ifstream fileStream;

		std::string ReadLine();
		std::vector<std::string> SeparateLine();
		bool ParseLine();

	public:
		ObjFileParser(char *fileName);
		~ObjFileParser(void);
	};
}
