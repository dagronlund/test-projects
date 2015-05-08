#include "ObjFileParser.h"

#include <sstream>

using namespace std;
using namespace Core;

string TrimString(string s) {
	size_t startpos = s.find_first_not_of(" \t");
	size_t endpos = s.find_last_not_of(" \t");
	if (startpos != string::npos && endpos != string::npos)
		return s.substr(startpos, endpos + 1);
	else
		return string();
}

ObjFileParser::ObjFileParser(char *fileName) {
	fileStream = ifstream(fileName);
}

ObjFileParser::~ObjFileParser(void) {
}

string ObjFileParser::ReadLine() {
	string line;
	getline(fileStream, line);
	return line;
}

vector<string> ObjFileParser::SeparateLine() {
	vector<string> list;
	string line = TrimString(ReadLine()); // Read line and clean it
	if (line.empty()) // If line is empty, return empty list
		return list;
	size_t delimiter = line.find(' '); // Find first space
	while (!line.empty()) { // While string still exists
		if (delimiter == string::npos) { // If no spaces left...
			list.push_back(line); // Add what remains to list
			line = string(); // Empty line to end loop
		} else { // Space found in line
			list.push_back(line.substr(0, delimiter)); // Add first word to list
			line = TrimString(line.substr(delimiter + 1)); // Remove first word and clean
			delimiter = line.find(' '); // Find first space, again
		}
	}
	return list;
}

bool ObjFileParser::ParseLine() {

	return false;
}