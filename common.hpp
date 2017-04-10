bool file_exists(const std::string& filename);

int fill_matrix (Matrix & x, Matrix & y, std::vector<float> & emin_v, 
    std::vector<struct pka_mats> & finger_v);

int build_pls (Matrix & x, Matrix & y, int num_of_components, 
    float * sdec, double * r2, LV * plscoeff);

void validate_pls (Matrix & x, Matrix & y, float * q2, float * sdep, 
    int numofcomp, bool userg);

void tokenize (const std::string & str, std::vector<std::string> & tokens,
    const std::string & delimiters = " ");

bool build_and_validate_pls (std::string & at, 
    std::vector<std::string> & obj_name_v,
    std::vector<float> & yv, 
    std::vector<std::vector<float> > & xv, 
    int numofobjs, int num_of_components,
    int validation, float & zeroval, 
    std::vector<float> & coeff);
