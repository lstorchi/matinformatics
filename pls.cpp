#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

#include <basstat_inc.h>
#include <common.hpp>

double Average(std::vector<float> v)
{  
  double sum = 0.0;
  for (int i=0; i<v.size(); i++)
    sum += v[i];
                
  return sum/v.size();
}

double Deviation(std::vector<float> v, double ave)
{
  double E=0;
  for(int i=0;i<v.size();i++)
    E+=(v[i] - ave)*(v[i] - ave);

  return sqrt(1.0/v.size()*E);
}

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
  int num_of_components = 1;
  int validate = 1;
  std::string at = "MYT_";

  float zeroval;
  std::vector<float> coeff;

  build_and_validate_pls (at, obj_name_v, yv, xv, 
    numofobjs, num_of_components, validate, zeroval, coeff);

  std::vector<float> diff;
  for (int i=0; i<numofobjs; ++i)
  {
    std::cout << obj_name_v[i] << " " << yv[i] << " ";
    float esty = zeroval;
    for (int j=0; j<(int)coeff.size(); ++j)
      esty += coeff[j] * xv[i][j];
    std::cout << esty << std::endl;
    diff.push_back(fabsf(yv[i]-esty));
  }

  double avg = Average(diff); 
  double std = Deviation(diff, avg);

  std::cout << avg << " +/- " << std << std::endl;

  return 0;
}
