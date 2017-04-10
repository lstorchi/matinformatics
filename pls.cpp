#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

#include <basstat_inc.h>
#include <common.hpp>

int main (int argc, char ** argv)
{
  if (argc != 2)
  {
    std::cerr << "usage: " << argv[0] << " filename " << std::endl;
    return 1;
  }

  std::vector<std::string> obj_name_v;
  std::vector<std::vector<float> > xv;
  std::vector<float> yv;

  std::cout << "Read file..." << std::endl;

  unsigned int dim = 0;
  std::ifstream infile(argv[1]);
  std::string line;
  while (std::getline(infile, line))
  {
    std::vector<std::string> tokens;
    tokenize (line, tokens);

    if (dim != 0)
    {
      if (tokens.size() != dim)
      {
        std::cerr << "dimension error" << std::endl;
        return 1;
      }
    }

    if (tokens.size() >= 3)
    {
      obj_name_v.push_back(tokens[0]); 

      std::vector<float> x;
      for (int i=1; i<(int)(tokens.size()-1); ++i)
        x.push_back(atof(tokens[i].c_str()));
      xv.push_back(x);

      yv.push_back(atof(tokens[(int)(tokens.size()-1)].c_str()));
    }
  }

  infile.close();

  std::cout << "Start PLS..." << std::endl;

  int numofobjs = (int) xv.size();
  int num_of_components = 3;
  std::string at = "MYT_";

  build_and_validate_pls (at, obj_name_v, yv, xv, 
    numofobjs, num_of_components, 0);

  return 0;
}
