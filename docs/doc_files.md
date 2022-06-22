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

 












The matrix summary is provided in terms of row/column sum frequencies. Such summaries can be used, for instance, to avoid generating isomorphic matrices (i.e. identical with respect to row and/or column shuffles) (see below).
