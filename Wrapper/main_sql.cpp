#include "AbcSmc.h"

#include <gsl/gsl_rng.h>
#include <gsl/gsl_statistics_double.h>
#include <math.h>
#include <unistd.h>

using namespace std;
const gsl_rng* RNG = gsl_rng_alloc(gsl_rng_taus2);

void usage() {
    cerr << "\n\tUsage: ./abc_sql abc_config_sql.json --process\n\n";
}


int main(int argc, char* argv[]) {
    if (not (argc == 3) ) {
        usage();
        exit(100);
    }

    if ( strcmp(argv[2], "--process") == 0  ) { 
        AbcSmc* abc = new AbcSmc();
        abc->parse_config(string(argv[1]));
        gsl_rng_set(RNG, time(NULL) * getpid()); // seed the rng using sys time and the process id
        abc->process_database(RNG);
    } else {
        usage(); 
        exit(101);
    }

    return 0;
}
