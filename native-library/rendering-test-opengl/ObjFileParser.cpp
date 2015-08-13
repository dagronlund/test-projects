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
	vector<int> faces;
	data = new RenderingModelData();
	
	string line;
	while (!fileStream.eof())
	{
		getline(fileStream, line, '\n');
		vector<string> list = SeparateLine(line);
		if (list.size() == 0 || list[0] == "" || list[0].find('#') == 0) // Line is empty or comment
		{
		}
		else if (list[0] == "v") // Line is vertex
		{
			ParseVector(list, *data->GetVertices());
		}
		else if (list[0] == "vn") // Line is normal
		{
			ParseVector(list, *data->GetNormals());
		}
		else if (list[0] == "vt") // Line is texture coordinate
		{
			ParseVector(list, *data->GetTexCoords());
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
	}

	FillRenderingData(faces);
}

void ObjFileParser::FillRenderingData(vector<int> &faces)
{
	if (status == ObjFileFaceStatus::VERTEX) 
	{
		*data->GetIndices() = faces;
	}
	else if (status == ObjFileFaceStatus::VERTEX_TEXTURE) 
	{
		RenderingModelData *newData = new RenderingModelData();
		for (int i = 0; i < data->GetIndices()->size() / 6; i++) 
		{
			int offset = i * 6;

			int vi = (*data->GetIndices())[offset];
			newData->GetVertices()->push_back((*data->GetVertices())[vi]);
			vi = (*data->GetIndices())[offset + 2];
			newData->GetVertices()->push_back((*data->GetVertices())[vi]);
			vi = (*data->GetIndices())[offset + 4];
			newData->GetVertices()->push_back((*data->GetVertices())[vi]);
			
			int ti = (*data->GetIndices())[offset + 1];
			newData->GetVertices()->push_back((*data->GetTexCoords())[ti]);
			ti = (*data->GetIndices())[offset + 3];
			newData->GetVertices()->push_back((*data->GetTexCoords())[ti]);
			ti = (*data->GetIndices())[offset + 5];
			newData->GetVertices()->push_back((*data->GetTexCoords())[ti]);
		
			newData->GetIndices()->push_back(i);
		}
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
	if (status == newStatus || status == ObjFileFaceStatus::UNKNOWN)
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