## Matrix simulation

## Description


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
