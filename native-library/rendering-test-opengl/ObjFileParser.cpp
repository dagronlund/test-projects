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
	ParseFile();
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

void ObjFileParser::ParseFile() 
{
	// Temporary data storage
	vector<float> vertices;
	vector<float> normals;
	vector<float> texCoords;
	vector<int> faces;

	string line = ReadLine();
	while (!line.empty())
	{
		vector<string> list = SeparateLine(line);
		if (list[0] == "" || list[0].find('#') == 0) // Line is empty or comment
		{
		}
		else if (list[0] == "v") // Line is vertex
		{
			ParseVector(list, vertices);
		}
		else if (list[0] == "vn") // Line is normal
		{
			ParseVector(list, normals);
		}
		else if (list[0] == "vt") // Line is texture coordinate
		{
			ParseVector(list, texCoords);
		}
		else if (list[0] == "f") // Line is face
		{
			ParseFace(list, faces);
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
			throw exception("Unexpected character encountered in model file.");
		}
		line = ReadLine();
	}

}

void ObjFileParser::FillRenderingData(vector<float> &vertices, vector<float> &texCoords, 
	vector<float> &normals, vector<int> &faces)
{
	if (status == ObjFileFaceStatus::VERTEX) 
	{
		int *indicesCopy = new int[faces.size()];
		std::copy(faces.begin(), faces.end(), indicesCopy);

		float *verticesCopy = new float[vertices.size()];
		std::copy(vertices.begin(), vertices.end(), verticesCopy);

		data = new RenderingModelData(indicesCopy, verticesCopy, NULL, NULL);
	}
	else if (status == ObjFileFaceStatus::VERTEX_TEXTURE) 
	{

	}
}

void ObjFileParser::ParseVector(const vector<string> &list, 
	vector<float> &vectors)
{
	vectors.push_back(std::stof(list[1])); // x
	vectors.push_back(std::stof(list[2])); // y
	if (list.size() == 4) // z is optional for textures
	{
		vectors.push_back(std::stof(list[3])); // z
	}
}

void ObjFileParser::ParseFaceComponent(const string &component,
	vector<int> &faces) 
{
	size_t first = component.find('/');
	
	if (first == -1) // Vertex Only 
	{
		faces.push_back(stoi(component) - 1);
		AssertFaceStatus(ObjFileFaceStatus::VERTEX);
	}
	else
	{
		size_t second = component.find('/', first + 1);

		if (second == -1) // Vertex, Texture 
		{
			faces.push_back(stoi(component.substr(0, first)) - 1);
			faces.push_back(stoi(component.substr(first + 1)) - 1);
			AssertFaceStatus(ObjFileFaceStatus::VERTEX_TEXTURE);
		}
		else if (second == first + 1) // Vertex, Normal
		{
			faces.push_back(stoi(component.substr(0, first)) - 1);
			faces.push_back(stoi(component.substr(second + 1)) - 1);
			AssertFaceStatus(ObjFileFaceStatus::VERTEX_NORMAL);
		}
		else // Vertex, Texture, Normal
		{
			faces.push_back(stoi(component.substr(0, first)) - 1);
			faces.push_back(stoi(component.substr(first + 1, second - (first + 1))) - 1);
			faces.push_back(stoi(component.substr(second + 1)) - 1);
			AssertFaceStatus(ObjFileFaceStatus::VERTEX_TEXTURE_NORMAL);
		}
	}
}

void ObjFileParser::ParseFace(const vector<string> &list,
	vector<int> &faces) 
{
	ParseFaceComponent(list[1], faces);
	ParseFaceComponent(list[2], faces);
	ParseFaceComponent(list[3], faces);
	if (list.size() > 4) // Four Corners Provided
	{
		ParseFaceComponent(list[3], faces);
		ParseFaceComponent(list[4], faces);
		ParseFaceComponent(list[1], faces);
	}
}

void ObjFileParser::AssertFaceStatus(ObjFileFaceStatus newStatus) 
{
	if (status == newStatus)
	{
	}
	else if (status == ObjFileFaceStatus::UNKNOWN) 
	{
		status = newStatus;
	}
	else
	{
		throw exception("Faces provided are in an inconsistent format.");
	}
}

RenderingModelData* ObjFileParser::GetRenderingData() 
{
	return data;
}