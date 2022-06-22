# Matrix Simulator
A simulator to generate 0-1 matrices with various options to control the spread of zeros in the matrix.

## Quick usage
You can run the simulator with default parameters as
```bash
python3 script-gen_0_1_matrix.py
```
This will generate a 0-1 matrix with 20 rows, 10 columns and 30% of missing data (i.e. 0's in a matrix). All employed parameters and their values are listed in the log file. The matrix is written in default output file `output_file.txt`

To print help run
```bash
python3 script-gen_0_1_matrix.py -h
```
## Output files
The simulator outputs the following two files
* `<output_file_prefix>.txt` - contains generated matrix

Format: 
The first row is the number of rows followed by the number of columns. Subsequent rows start with the row name followed by matrix row.

Example:
```bash
10 5
sp1 1 1 1 1 0
sp2 1 1 1 0 1
sp3 0 1 1 0 1
sp4 1 1 1 1 0
sp5 1 1 0 1 1
sp6 1 1 0 0 0
sp7 1 1 1 0 0
sp8 1 0 1 1 1
sp9 0 0 0 1 0
sp10 0 0 1 0 0
```

* `<output_file_prefix>.log` - contains information about values of parameters and summary of the matrix in terms of row/column sum frequencies. Such summaries are used to avoid generating isomorphic matrices (i.e. identical with respect to row and/or column shuffles) (see below).

Example:
```
----------------------------------------------------------------------------------------------------
Matrix generation
----------------------------------------------------------------------------------------------------
Command line: script-gen_0_1_matrix.py -n 10 -k 5 -u 20 -m 40
----------------------------------------------------------------------------------------------------
Printing parameter values:
----------------------------------------------------------------------------------------------------
o:output_file
n:10
k:5
m:40.0
u:20.0
up:[0.33 0.33 0.33]
r0:1
r1:2
c0:1
c1:4
rf:[60 10 30]
rp:[0.1 0.6 0.3]
cf:[60 10 30]
cp:[0.1 0.6 0.3]
i:None
t:5
----------------------------------------------------------------------------------------------------
Matrix Summary:
----------------------------------------------------------------------------------------------------
n k #0 %0 row_sum_freq col_sum_freq col_row_sum_1_freq
10 5 20 40.0 [0 2 1 2 5 0][0 0 0 0 1 1 0 3 0 0 0][3 2 0]
----------------------------------------------------------------------------------------------------
```

## Parameters
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


## Detailed description

**Generating matrix**
1. The simulator starts with a nxk matrix of 1's.
2. If u>0, then in u rows all entries are assigned with 0's. Then for each row one column is sampled according to up sampling proba:wqbilities and the corresponding entry is assigned with 1.
3. If the % of missing data is not equal to m, then next row constraint on minimal number of zeros, r0, will be assured. The simulator goes through each of n-u rows, samples r0 columns with sampling probabilities cp and assigns coresponding entries to zeros.
4. If the % of missing data is not equal to m, then next column constraint on minimal number of zeros, c0, will be assured. The simulator goes through each column, computes the number x of 0 in the column and if x < c0, samples c0-x rows with sampling probabilities rp and assigns coresponding entries to zeros.
5. If the % of missing data is not equal to m, the remaining zeros are assinged by sampling a pair row & column, if the entry equals to 1, the entry is assigned wth 0, if the entry is 0, the pair is resampled. This step continues until all zeros are allocated and m equals to the % of zeros in the matrix, or until a zero cannot be allocated without violating constraints on minimal number of 1's in each row and column.

**Assuring minimal number of 1's in each row and column**

Rows and columns, which are at the boundary of constraints (i.e. row sum = r1, column sum = c1) are excluded from sampling and assigning additional zeros.

**Parameter boundaries**

* *The % of missing data, m, does not match the % of zeros in simulated matrix.* Parameters on minimal number of zeros and ones in rows and columns, as well as the number of rows with minimal information (i.e. row sum = 1), parameter u, constrain minimal and maximal % of zeros, m, that need to be allocated to satisfy these constraints. Thus, at the boundaries, it can happen that user-defined m is different from the % of zeros in the simulated matrix.

* *Sampling probabilities are ignored.*

TODO 

**Isomorphic matrices**

TODO

## Application
The simulator was used in Phylogenomics to simulate presence-absence species per locus matrices with missing data, i.e. when genetic sequence of some locus is not present for a species.

## Citation
If you use this simulator, please cite the following article:

* **Olga Chernomor, Christiane Elgert, Arnd von Haeseler** (in prep) "Identifying equally scoring trees in phylogenomics with incomplete data using Gentrius"
