#include "ObjFileParser.h"

#include <sstream>

using namespace std;
using namespace Core;

string TrimString(string s) 
{
	size_t startpos = s.find_first_not_of(" \t");
	size_t endpos = s.find_last_not_of(" \t");
	if (startpos != string::npos && endpos != string::npos)
		return s.substr(startpos, endpos + 1);
	else
		return string();
}

ObjFileParser::ObjFileParser(char *fileName) 
{
	fileStream = ifstream(fileName);
}

ObjFileParser::~ObjFileParser(void) 
{
}

string ObjFileParser::ReadLine() 
{
	string line;
	getline(fileStream, line);
	return line;
}

vector<string> ObjFileParser::SeparateLine(string line) 
{
	vector<string> list;
	line = TrimString(line); // Read line and clean it
	size_t delimiter = line.find(' '); // Find first space
	while (!line.empty()) // While string still exists
	{ 
		if (delimiter == string::npos) // If no spaces left...
		{ 
			list.push_back(line); // Add what remains to list
			line = string(); // Empty line to end loop
		} 
		else // Space found in line
		{ 
			list.push_back(line.substr(0, delimiter)); // Add first word to list
			line = TrimString(line.substr(delimiter + 1)); // Remove first word and clean
			delimiter = line.find(' '); // Find first space, again
		}
	}
	return list;
}

bool ObjFileParser::ParseLine() 
{
	// Temporary data storage
	vector<float> vertices();

	string line = ReadLine();
	while (!line.empty())
	{
		vector<string> list = SeparateLine(line);
		if (list[0] == "" || list[0].find('#') == 0) // Line is empty or comment
		{
		}
		else if (list[0] == "v") // Line is vertex
		{
		}
		else if (list[0] == "vn") // Line is normal
		{
		}
		else if (list[0] == "vt") // Line is texture coordinate
		{
		}
		else if (list[0] == "f") // Line is face
		{
		}
		else if (list[0] == "o") // Line defines object
		{
		}
		else if (list[0] == "g") // Line defines group
		{
		}
		else if (list[0] == "mtllib") // Line add material library
		{
		}
		else if (list[0] == "usemtl") // Line uses material library
		{
		}
		else // Line contains unknown start sequence
		{
		}
		line = ReadLine();
	}
}

void ObjFileParser::ParseVertex(vector<string> &list, vector<float> &vertices) 
{
	float f = std::stof(list[0]);

}