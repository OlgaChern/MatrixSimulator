# Matrix Simulator
A simulator to generate 0-1 matrices with various options to control the spread of zeros in the matrix.

It starts with a matrix of ones and then allocates the required number of zeros in the matrix according to the user-defined parameters. One can control the amount of zeros (their % out of all matrix entries) and the spread across the matrix using sampling row/column probabilities and % of rows with row sum equals to one (rows with minimal information) and also the distribution of such ones across columns. The constraints on rows and columns are imposed via minimal number of zeros and ones in each row/column, i.e. constraints on row and column sums.

For the generated matrix the simulator provides also matrix summary in terms of row and column sum counts. These summaries can be used to discard matrices, which are identical after row and/or column shuffling.

Read more about the steps of matrix simulation [>>>](./docs/doc_workflow.md)

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
* `<output_file_prefix>.log` - contains information about values of parameters and matrix summary

Detailed description of output files [>>>](./docs/doc_files.md)

## Input file
The simulator accepts one optional input file. This file should contain matrix summaries of previously generated matrices (or it should be an empty file). This file will be also updated by adding matrix summary of currently generated matrix. The matrix summaries can be used to avoid generating  matrices, that are identical with respect to row and/or column shuffling. This is useful, if one wants to generate many **different** random matrices with the same input parameters. 

Detailed description of input file [>>>](./docs/doc_files.md)

## Parameters
Detailed description of all parameters [>>>](./docs/doc_param.md)

## Application
The simulator was used in Phylogenomics to simulate presence-absence species per locus matrices with missing data, i.e. when genetic sequence of some locus is not present for a species.

## Citation
If you use this simulator, please cite the following article:
* **Olga Chernomor, Christiane Elgert, Arnd von Haeseler** (2023) "Identifying equally scoring trees in phylogenomics with incomplete data using Gentrius", bioRxiv (preprint), https://doi.org/10.1101/2023.01.19.524678
