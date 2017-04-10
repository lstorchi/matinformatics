#include <cstring>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <sstream>
#include <sys/stat.h>

#include <cmath>

#include <getopt.h>
#include <unistd.h>

#include <vector>
#include <map>

#include <basstat_inc.h>

#include <algorithm> 
#include <functional> 
#include <cctype>
#include <locale>
#include <sstream>
#include <iterator>

#include "common.hpp"

bool file_exists(const std::string& filename)
{
  struct stat buf;
  if (stat(filename.c_str(), &buf) != -1)
    return true;
                    
  return false;
}

static inline std::string &ltrim(std::string &s) 
{
  s.erase(s.begin(), std::find_if(s.begin(), 
        s.end(), std::not1(std::ptr_fun<int, int>(std::isspace))));
  return s;
}

static inline std::string &rtrim(std::string &s) 
{
  s.erase(std::find_if(s.rbegin(), s.rend(), 
        std::not1(std::ptr_fun<int, int>(std::isspace))).base(), 
      s.end());
  return s;
}

// trim from both ends
static inline std::string &trim(std::string &s) 
{
  return ltrim(rtrim(s));
}

int fill_matrix (Matrix & x, Matrix & y, std::vector<float> & yv, 
    std::vector<std::vector<float> > & xv)
{
  int nobj = (int) yv.size();

  lsAllocMatrix (&x, nobj, (int) (xv.size() * xv[0].size()));
  lsAllocMatrix (&y, nobj, 1);
  for (int i=0; i<nobj; ++i)
  {
    y.data[i][0] = yv[i];
    for (int j=0; j<(int)xv[i].size(); ++j)
      x.data[i][j] = xv[i][j];
  }
 
  return nobj;
}

int build_pls (Matrix & x, Matrix & y, int num_of_components, 
    float * sdec, double * r2, LV * plscoeff)
{
  float vx, vxac, sy;
  int comp, i;
  
  TLV tlv;
  
  vxac  = 0.00;
  
  lsCheckMissing (&x, -99.00);
  lsCheckMissing (&y, -99.00);
  
  lsAutoscaleMatrix (&y);
  lsAutoscaleMatrix (&x);
  
  lsAllocTLV (&tlv, &x, &y);
  lsInitTLV (&tlv, &x, &y);
  
  for (comp=0; comp<=num_of_components; comp++) 
  {
    lsAllocLV (&plscoeff[comp], &x, &y);
    
    lsExtractLV  (&x, &y, &plscoeff[comp]);
    lsDeflatePLS (&x, &y, &plscoeff[comp], &tlv, (comp+1));
  
    vx = 100.0 * (plscoeff[comp].VarX/tlv.VarX0);
    vxac += vx;
    sy = plscoeff[comp].SSYe[0]/tlv.SSY0[0];
  
    for (i=comp; i<=num_of_components; i++)
      r2[i] += (double) sy;
    
    sdec[comp] = sqrt((tlv.SSYp[0]-plscoeff[comp].SSYe[0])/x.nobj);
    sdec[comp] /= y.weights[0];
  }
  
  lsFreeTLV (&tlv);
 
  return 0;
}

void validate_pls (Matrix & x, Matrix & y, float * q2, float * sdep, 
    int numofcomp, bool userg) 
{

  int i, comp;
  float ** ssy, ssy0;

  ssy = new float* [numofcomp+1];
  for (i=0; i<=numofcomp; i++) 
  {
    ssy[i] = new float;
    ssy[i][0] = 0.0;
  }
  
  ssy0 = 0.0;
    
  lsCheckMissing(&x,-99.00);
  lsCheckMissing(&y,-99.00);

  if ( (x.nmis + y.nmis) > 0 ) {
    lsSetMissing (&x, -99.00);
    lsSetMissing (&y, -99.00);
  }

  lsSetAverages (&y);

  for (i=0; i<y.nobj; i++) 
    ssy0 += sqr (y.data[i][0] - y.averages[0]);

  if (userg)
    lsValidateRG (&x, &y, numofcomp+1, 5, 20, 1, ssy, 
        NULL, NULL, NULL); 
  else
    lsValidateLOO (&x,&y,numofcomp+1,1,ssy,
       NULL, NULL, NULL);

  for (comp=0; comp<=numofcomp; comp++) {
    q2[comp] = 1.00 - (ssy[comp][0]/ssy0);
    sdep[comp] = sqrt(ssy[comp][0]/(float)x.nobj);
  }

  for (i=0; i<=numofcomp; i++)
    delete ssy[i];
  delete[] ssy;

  return;
}

bool build_and_validate_pls (std::string & at, 
    std::vector<std::string> & obj_name_v,
    std::vector<float> & yv, 
    std::vector<std::vector<float> > & xv, 
    int numofobjs, int num_of_components,
    int validation)
{

  Matrix x, y;
  fill_matrix (x, y, yv, xv);

  std::stringstream ss;

  if (numofobjs > 3)
  {
    float * q2 = new float [num_of_components + 1];
    float * sdep = new float [num_of_components + 1];
    float * sdec = new float [num_of_components + 1];
    double * r2 = new double [num_of_components + 1];
    
    LV * plscoeff = new LV [num_of_components + 1];
                                                   
    for (int i=0; i<num_of_components + 1; i++) 
    {
      q2[i] = 0.0;
      sdep[i] = 0.0;
      sdec[i] = 0.0;
      r2[i] = 0.0;
    }
    
    build_pls (x, y, num_of_components, sdec, r2, plscoeff);
  
    fill_matrix (x, y, yv, xv);
  
    if (validation != 0)
    {
      bool userg = (validation == 1);
      validate_pls (x, y, q2, sdep, num_of_components, userg);
  
      std::stringstream ssp0;
      ssp0 << at << "parameters.txt";
      if (access( ssp0.str().c_str(), F_OK ) != -1)
        std::remove(ssp0.str().c_str());
      std::ofstream fout0 (ssp0.str().c_str(), std::ios::app);
  
      fout0 << "n r2 q2 sdep" << std::endl;
      for (int j=0; j<=num_of_components; j++)
        fout0 << j+1 << " " << r2[j] << " " << 
          q2[j] << " " << sdep[j] << std::endl;
   
      fout0.close();
                                                         
      std::cout << "n r2 q2 sdep" << std::endl;
      for (int j=0; j<=num_of_components; j++)
        std::cout << j+1 << " " << r2[j] << " " << 
          q2[j] << " " << sdep[j] << std::endl;
      
    }
    else 
    {
      std::stringstream ssp0;
      ssp0 << at << "parameters.txt";
      if (access( ssp0.str().c_str(), F_OK ) != -1)
        std::remove(ssp0.str().c_str());
      std::ofstream fout0 (ssp0.str().c_str(), std::ios::app);
  
      fout0 << "n r2 q2 sdep" << std::endl;
      for (int j=0; j<=num_of_components; j++)
        fout0 << j+1 << " " << r2[j] << " " << 
          q2[j] << " " << sdep[j] << std::endl;
   
      fout0.close();
                                                         
      std::cout << "n r2 q2 sdep" << std::endl;
      for (int j=0; j<=num_of_components; j++)
        std::cout << j+1 << " " << r2[j] << " " << 
          q2[j] << " " << sdep[j] << std::endl;
  
    }
  
    lsSetWeights (&x);
    lsSetWeights (&y);

    std::map<std::string, float> minval_map;
    std::string fname = "min_emin_values.txt";
    if (file_exists(fname.c_str()))
    {
      std::ifstream myfile(fname.c_str(), std::ios::in);
      std::string line;
      while (std::getline(myfile, line))
      {
        std::vector<std::string> tokens;
        std::istringstream iss(line);
        std::copy(std::istream_iterator<std::string>(iss),
                  std::istream_iterator<std::string>(),
                  std::back_inserter(tokens));
        if (tokens.size() == 2)
          minval_map[tokens[0]] = atoi(tokens[1].c_str());
        else
          std::cout << "error in file " << fname << " : " << 
            line << std::endl;
      }
  
      myfile.close();
    }
  
    // computing b0
    float zeroval = 0.0;
    std::vector<float> coeff;
    int max = num_of_components;
    for (int k=0; k<x.nvar; k++) 
    {
      coeff.push_back(plscoeff[max].b[0][k]*x.weights[k]/y.weights[0]);
      zeroval -= plscoeff[max].b[0][k]*x.weights[k]*x.averages[k]; 
    }
    zeroval /= y.weights[0];
    zeroval += y.averages[0];
    
    int counter = 0;
    std::cout << "Print Coeff plscoeff.txt... " << std::endl;
    
    std::stringstream ssp;
    ssp << at << "plscoeff.txt";
    if (access( ssp.str().c_str(), F_OK ) != -1)
      std::remove(ssp.str().c_str());
    std::ofstream fout (ssp.str().c_str(), std::ios::app);
   
    fout << at << std::endl;
    fout << std::scientific;
    fout << zeroval << std::endl;
    fout << num_of_components << std::endl;
    fout << numofobjs << std::endl;
    fout << sdec[num_of_components] << std::endl;
    fout << coeff.size() << std::endl;
    std::vector<float>::iterator it = coeff.begin();
    for (; it != coeff.end(); ++it)
    {
      ++counter;
      fout.width(18); fout.precision(11);
      fout << *it << std::endl;
      /*if (counter%5 == 0)
          fout << std::endl;*/
    }
    //fout << std::endl;
    
    fout.close();
    
    lsFreeMatrix (&x); 
    lsFreeMatrix (&y);
    
    for (int j=0; j<num_of_components + 1; j++) 
      lsFreeLV (&plscoeff[j]);
    
    delete [] plscoeff;
                            
    delete [] q2;
    delete [] sdep;
    delete [] sdec;
    delete [] r2;
  }
  else
  {
    std::cout << "Print Coeff fake plscoeff.txt... " << std::endl;
    
    std::stringstream ssp;
    ssp << at << "plscoeff.txt";
    if (access( ssp.str().c_str(), F_OK ) != -1)
      std::remove(ssp.str().c_str());
    std::ofstream fout (ssp.str().c_str(), std::ios::app);
  
    float zeroval = 0.0;
   
    fout << at << std::endl;
    fout << std::scientific;
    fout << zeroval << std::endl;
    fout << num_of_components << std::endl;
    fout << numofobjs << std::endl;
    fout << zeroval << std::endl;
    fout << "0" << std::endl;
    
    fout.close();
  }

  return true;
}

void tokenize (const std::string & str, std::vector<std::string> & tokens,
    const std::string & delimiters)
{
  // Skip delimiters at beginning.
  std::string::size_type lastPos = 
    str.find_first_not_of(delimiters, 0);
  std::string::size_type pos = 
    str.find_first_of(delimiters, lastPos);
  
  while (std::string::npos != pos || 
      std::string::npos != lastPos)
  {
    tokens.push_back(str.substr(lastPos, pos - lastPos));
    lastPos = str.find_first_not_of(delimiters, pos);
    pos = str.find_first_of(delimiters, lastPos);
  }
}
