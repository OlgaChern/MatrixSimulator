## Output files

### <output_file_prefix>.txt
This file contains generated matrix.

*Format:*

The first row is the number of rows followed by the number of columns. Subsequent rows start with the row name followed by matrix row.

*Example:*

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

### <output_file_prefix>.log
This file contains information about values of parameters and matrix summary.

*Example:*

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


**Matrix Summary**

Here, we will describe the matrix summary on the above example.

*Basic info:*
* `n = 10` - the number of rows  
* `k = 5`  - the number of columns
* `#0 = 20` - the number of zeros in the matrix
* `%0 = 60%` - the % of zeros out of all `n x k` matrix entries

*Rows and columns sum summaries:*
* `row_sum_freq: [0 2 1 2 5 0]` - the length of the vector is k+1. Each entry corresponds to the number of rows with row sum = i-1, where i is the position in the vector.

Position in the vector | Row sum | Number of rows with corresponding sum
--- | --- | ---
**i** | **i-1** | **row counts**
1 | 0 | 0
2 | 1 | 2
3 | 2 | 1
4 | 3 | 2
5 | 4 | 5
6 | 5 | 0

* `col_sum_freq: [0 0 0 0 1 1 0 3 0 0 0]`

*Columns involved in rows with minimal information (row sum = 1):*
* `col_row_sum_1_freq: [3 2 0]`
