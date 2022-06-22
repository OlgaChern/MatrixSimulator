##Parameters

The simulator accepts the following parameters:

*Print help:*
* `-h, --help`            show this help message and exit

*Prefix of the output files:*
* `-o <file_name>`        output files prefix

*Matrix size:*
* `-n <num>`              number of rows
* `-k <num>`              number of cols

*Missing entries:*
* `-m <num>`              % of zeros to be allocated

*Rows with minimal info (i.e. row sum = 1):*
* `-u <num>`              % of rows with row sum = 1
* `-up <num> <num> <num>` vector of length 3, defines probabilities for 3 column categories to contain 1's in rows with row sum = 1

*Constraints on rows:*
* `-r0 <num>`             minimum number of 0's in a row
* `-r1 <num>`             minimum number of 1's in a row

*Constraints on columns:*
* `-c0 <num>`             minimum number of 0's in a col
* `-c1 <num>`             minimum number of 1's in a col

*Control row sampling probabilities:*
* `-rf <num> <num> <num>` vector of length 3, defines sizes (in %) for 3 row categories
* `-rp <num> <num> <num>` vector of length 3, defines probabilities for 3 row categories

*Control column sampling probabilities:*
* `-cf <num> <num> <num>` vector of length 3, defines sizes (in %) for 3 col categories
* `-cp <num> <num> <num>` vector of length 3, defines probabilities for 3 col categories

*Dealing with isomorphic matrices:*
* `-i <file_name>`        input file should contain information about other available matrices and will be used for a basic isomorphism check, if you have more than one matrix. If
                        matrix generation was successful, this file will be updated with an information about new matrix.
* `-t <num>` number of trials to perform, in case matrix is equivalent to some existing one (info passed via -i) or if some warnings were occured

