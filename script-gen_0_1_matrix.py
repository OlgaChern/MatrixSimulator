#/usr/bin/python3
#------------------------------------------------------------
import sys
import argparse
import numpy as np
import os.path
from os import path
#------------------------------------------------------------
def cat_sizes(total,cat_percent):
    """
    Compute the sizes of row/col categories
    
    Parameters
    ----------
    total: int
        number of entities to be assigned into different categories
    cat_percent: ndarray
        percentages of entities in each category
        
    Returns
    -------
    sz: ndarray
        vector of sizes for all categories
    """
    sz=np.array([])
    for i in range(len(cat_percent)-1):
        sz=np.append(sz,round(total*cat_percent[i]/100))

    sz=np.append(sz,total-sum(sz))
    #print("Printing sizes of categories:",sz)
    return sz
    
#--------------------------------------------------------------------
#----->>>>>>>>> COLUMN/ROW check
#------------------------------------------------------------
def check_allowed_vec(probs,mj,j,min_ones,probs_alt):
    """
    Check, if column/row of interest is allowed
    
    Parameters
    ----------
    probs: ndarray
        probability vector for columns/rows; 0 probability -> col/row is not allowed anymore to be modified by introduing more 0's
        
    mj: ndarray
        a col/row from a 0-1 matrix
        
    j: int
        id of the col/row in the original matrix
        
    min_ones: int
        number of minimum 1's that should be present in col/ros, this defines the rule if a col/row is still allowed to be modified; specify min_ones=4 for columns and min_ones=2 for rows
        
    Returns
    -------
    change_tag: bool
        True if a column is not anymore allowed to be modified, i.e. the probability vector was modified to assign 0 probability to the column and normalised

    """
    
    change_tag=False
    allowed_entries=np.nonzero(np.logical_and(np.array(mj==1),np.array(probs_alt>0)))[0].size
    if sum(mj)==min_ones or allowed_entries==0:
        probs[j]=0
        if sum(probs)!=0:
            for i in range(len(probs)):
                probs[i]=probs[i]/sum(probs)
        change_tag=True
        #print("PROBS_CHANGED:",np.array2string(probs, max_line_width=10000))
    return change_tag
#------------------------------------------------------------
#----->>>>>>>>> COLUMNS:
# functions to assure that columns are still allowed to be modified by adding further 0's
#------------------------------------------------------------
def check_allowed_col_rec(col_probs,row_probs,m,j,r1,c1):
    """
    Check, if COLUMN of interest is still allowed, if not start recursive check over ROWs with ones in this column
    
    Parameters
    ----------
    col_probs: ndarray
        probability vector for columns; 0 probability -> col is not allowed anymore to be modified by introduing more 0's
    row_probs: ndarray
        probability vector for rows; 0 probability -> row is not allowed anymore to be modified by introduing more 0's
    m: ndarray
        0-1 matrix
    j: int
        id of COLUMN in matrix m
    """

    res=check_allowed_vec(col_probs,m[:,j],j,c1,row_probs)
    
    if res:
        rows_with_ones=np.nonzero(m[:,j]==1)[0]
        for i in rows_with_ones:
            if row_probs[i]!=0:
                check_allowed_row_rec(col_probs,row_probs,m,i,r1,c1)

#------------------------------------------------------------
#----->>>>>>>>> ROWs:
# functions to assure that rows are still allowed  to be modified by adding further 0's
#------------------------------------------------------------
def check_allowed_row_rec(col_probs,row_probs,m,j,r1,c1):
    """
    Check, if ROW of interest is still allowed, if not start recursive check over COLUMNs with ones in this row
    
    Parameters
    ----------
    col_probs: ndarray
        probability vector for columns; 0 probability -> col is not allowed anymore to be modified by introduing more 0's
    row_probs: ndarray
        probability vector for rows; 0 probability -> row is not allowed anymore to be modified by introduing more 0's
    m: ndarray
        0-1 matrix
    j: int
        id of ROW in matrix m
        
    """
    
    res=check_allowed_vec(row_probs,np.array(m[j,:]).reshape(-1),j,r1,col_probs)
    
    if res:
        col_with_ones=np.nonzero(m[j,:]==1)[0]
        for i in col_with_ones:
            if col_probs[i]!=0:
                check_allowed_col_rec(col_probs,row_probs,m,i,r1,c1)

#------------------------------------------------------------
def check_allowed_pair_rec(col_probs,row_probs,m,i,j,r1,c1):
    """
    Check, if after setting m[i,j]=0, ith ROW and jth COLUMN are still allowed to be modified by introducing new 0 into respective row/column. If not check recursively other involved columns and rows
    
    Parameters
    ----------
    col_probs: ndarray
        probability vector for columns; 0 probability -> col is not allowed anymore to be modified by introduing more 0's
    row_probs: ndarray
        probability vector for rows; 0 probability -> row is not allowed anymore to be modified by introduing more 0's
    m: ndarray
        0-1 matrix
    i: int
        id of ROW in matrix m
    j: int
        id of COLUMN in matrix m
        
    """
    check_allowed_row_rec(col_probs,row_probs,m,i,r1,c1)
    check_allowed_col_rec(col_probs,row_probs,m,j,r1,c1)
#------------------------------------------------------------
def check_allowed_thorough(col_probs,row_probs,m,r1,c1):
    """
    Check, if after setting m[i,j]=0, rows and columns are still allowed to be modified. This is a thorough check: all rows and all columns.

    Parameters
    ----------
    col_probs: ndarray
        probability vector for columns; 0 probability -> col is not allowed anymore to be modified by introduing more 0's
    row_probs: ndarray
        probability vector for rows; 0 probability -> row is not allowed anymore to be modified by introduing more 0's
    m: ndarray
        0-1 matrix
    """

    check=True
    while check:
        #print("row_probs_1:",np.array2string(row_probs, max_line_width=10000))
        #print("col_probs_1:",np.array2string(col_probs, max_line_width=10000))
        row_probs_zeros_1=len(np.nonzero(row_probs==0)[0])
        col_probs_zeros_1=len(np.nonzero(col_probs==0)[0])
        #print(row_probs_zeros_1,col_probs_zeros_1)

        for i in np.nonzero(row_probs!=0)[0]:
            check_allowed_vec(row_probs,m[i,:],i,r1,col_probs)

        for j in np.nonzero(col_probs!=0)[0]:
            check_allowed_vec(col_probs,m[:,j].reshape(-1),j,c1,row_probs)

        #print("row_probs_2:",np.array2string(row_probs, max_line_width=10000))
        #print("col_probs_2:",np.array2string(col_probs, max_line_width=10000))
        row_probs_zeros_2=len(np.nonzero(row_probs==0)[0])
        col_probs_zeros_2=len(np.nonzero(col_probs==0)[0])
        #print(row_probs_zeros_2,col_probs_zeros_2)


        check=False
        if row_probs_zeros_1!=row_probs_zeros_2 or col_probs_zeros_1!=col_probs_zeros_2:
            check=True


#------------------------------------------------------------
def sample_index(probs,mj):
    """
    Choosing column/row index among allowed ones for an input vector (row/column) mj.
    
    Parameters
    ----------
    probs: ndarray
        probability vector for columns/rows; 0 probability -> column/row is not allowed anymore to be modified by introduing more 0's. IMPORTANT: probabilities should correspond to the index you are sampling: sampling column index -> col_probs, sampling row index -> row_probs.
        
    mj: ndarray
        a col/row from a 0-1 matrix. IMPORTANT: if sampling column index -> mj must be a row from m, sampling row index -> mj must be a column from m
        
    Returns
    -------
    id: int
        Sampled col/row index
    """
    
    probs_aux=np.array(probs)
    
    allowed_entries=np.logical_and(np.array(mj==1),np.array(probs>0))
    probs_aux[np.logical_not(allowed_entries)]=0
    probs_aux=probs_aux/sum(probs_aux)

    id=np.random.choice(len(probs_aux),1,p=probs_aux)
    
    return int(id)
    
    
def sample_indices(col_probs,row_probs,m):
    """
    Choosing column and row indices among allowed ones.
    
    Parameters
    ----------
    col_probs: ndarray
        updated vector of column probabilities
    row_probs: ndarray
        updated vector of row probabilities
    m: ndarray
        0-1 matrix
        
    Returns
    -------
    i: int
        Sampled row index
    j: int
        Sampled col index
        
    Notes
    -------
        Note, that the results are passed via tuple
    """
    
    j=np.random.choice(m.shape[1],1,p=col_probs/sum(col_probs))
    i=sample_index(row_probs,np.array(m[:,j]).reshape(-1))
    
    return (int(i),int(j))
    
#============================================================
def parse_parameters():
    """Parsing arguments passed to the script"""
    
    #parser = argparse.ArgumentParser(description='Generate 0-1 matrix',exit_on_error=True)
    parser = argparse.ArgumentParser(description='Generate 0-1 matrix')
    
    # parameters------------------------------------------------------
    parser.add_argument("-i",help="input file should contain information about other available matrices and will be used for a basic isomorphism check, if you have more than one matrix. If matrix generation was successful, this file will be updated with an information about new matrix.",metavar="<file_name>")
    parser.add_argument("-o",help="output file prefix",default="output_file",metavar="<file_name>")
    
    parser.add_argument("-n",help="number of rows",type=int,default=20,metavar="<num>")
    parser.add_argument("-k",help="number of cols",type=int,default=10,metavar="<num>")
    parser.add_argument("-m",help="%% of zeros to be allocated",type=float,default=30,metavar="<num>")

    parser.add_argument("-u",help="%% of rows with sum of elements = 1",type=float,default=0,metavar="<num>")
    
    parser.add_argument("-up",nargs=3,help="vector of length 3, defines probabilities for 3 column categories to contain 1's in rows, which sum up to 1",type=float,default=[0.33,0.33,0.33],metavar="<num>")
    
    parser.add_argument("-r0",help="minimum number of 0's in a row",type=int,default=1,metavar="<num>")
    parser.add_argument("-r1",help="minimum number of 1's in a row",type=int,default=2,metavar="<num>")
    parser.add_argument("-c0",help="minimum number of 0's in a col",type=int,default=1,metavar="<num>")
    parser.add_argument("-c1",help="minimum number of 1's in a col",type=int,default=4,metavar="<num>")
    
    parser.add_argument("-rf",nargs=3,help="vector of length 3, defines sizes (in %%) for 3 row categories",default=[60,10,30],type=float,metavar="<num>")
    parser.add_argument("-rp",nargs=3,help="vector of length 3, defines probabilities for 3 row categories",default=[0.1,0.6,0.3],type=float,metavar="<num>")
    
    parser.add_argument("-cf",nargs=3,help="vector of length 3, defines sizes (in %%) for 3 col categories",default=[60,10,30],type=float,metavar="<num>")
    parser.add_argument("-cp",nargs=3,help="vector of length 3, defines probabilities for 3 col categories",default=[0.1,0.6,0.3],type=float,metavar="<num>")
    
    parser.add_argument("-t",help="number of trials to perform, in case matrix is equivalent to some existing one (info passed via -i) or if some warnings were occured",type=int,default=5,metavar="<num>")
    
    # parsing arguments----------------------------------------------------
    args = parser.parse_args(sys.argv[1:])
    #----------------------------------------------------------------------
    args.up=np.array(args.up)
    args.rf=np.array(args.rf)
    args.rp=np.array(args.rp)
    args.cf=np.array(args.cf)
    args.cp=np.array(args.cp)
    #----------------------------------------------------------------------
    #print("="*50)
    #print("Printing input parameters:")
    #print("="*50)
    d=vars(args)
    file=open(args.o+".log","w")
    file.write("="*50+'\n')
    file.write("Printing input parameters:"+'\n')
    file.write("="*50+'\n')
    for i in d.keys():
        #print(i+":",d[i])
        file.write(str(i)+":"+str(d[i])+'\n')
    file.write("="*50+'\n')
    file.close()
    #----------------------------------------------------------------------
    generate_0_1_matrix(d["n"],d["k"],d["m"],d["u"],d["up"],d["r0"],d["r1"],d["c0"],d["c1"],d["rf"],d["rp"],d["cf"],d["cp"],d["t"],outfile=d["o"],infile=d["i"])
    
def parameter_sanity_check(n,k,m,u,up,r0,r1,c0,c1,rf,rp,cf,cp,t,outfile,infile):
    """
    Check if all parameters are within expected ranges.
    """
    forbidden_ch=["\\"," ",":","*","?","\"","<",">","|"]
    #----------------------------------------------------------------------
    if infile:
        for i in infile:
            if i in forbidden_ch:
                sys.exit("INPUT_ERROR: infile: not allowed character in the input file name. File names should not contain the following characters: "+"'"+"' '".join(forbidden_ch)+"'")
	# if files does not exist, you should use it to write info about current matrix..
        if not path.exists(infile):
            print("WARNING: file ",infile," does not exists, i.e. no information is available for a basic isomorphism check. However, the file name will be used to output information about the matrix, generated in this run. This information can be further used for isomorphism check for other matrices.")
        #    sys.exit("INPUT_ERROR: infile '"+infile+"' does not exist!")
    #----------------------------------------------------------------------
    for i in outfile:
        if i in forbidden_ch:
            sys.exit("INPUT_ERROR: outfile: not allowed character in output file name. File names should not contain the following characters: "+"'"+"' '".join(forbidden_ch)+"'")
    #----------------------------------------------------------------------
    if n<5:
        sys.exit("INPUT_ERROR: n corresponds to the number of rows in a matrix to be generated, currently the required minimum is at least 5!")
    #----------------------------------------------------------------------
    if k<3:
        sys.exit("INPUT_ERROR: k corresponds to the number of columns in a matrix to be generated, currently the required minimum is at least 3!")
    #----------------------------------------------------------------------
    if np.logical_or(m<0,m>100):
        sys.exit("INPUT_ERROR: m corresponds to percentage and should be within [0,100] range!")
    #----------------------------------------------------------------------
    if np.logical_or(u<0,u>100):
        sys.exit("INPUT_ERROR: u corresponds to percentage and should be within [0,100] range!")
    #----------------------------------------------------------------------
    if np.count_nonzero(np.logical_or(up<0,up>1))>0:
        sys.exit("INPUT_ERROR: probabilities of column categories (up) should be within [0,1] range!")
    elif sum(up)!=1:
        print("WARNING: probabilities of column categories (up) do not sum up to 1! They will be normalized..")
        up=up/sum(up)
    #----------------------------------------------------------------------
    if np.logical_or(r0<0,r0>k):
        sys.exit("INPUT_ERROR: r0 (min number of 0's in a row) should be in range between 0 and k!")
    #----------------------------------------------------------------------
    if np.logical_or(r1<0,r1>k):
        sys.exit("INPUT_ERROR: r1 (min number of 1's in a row) should be in range between 0 and k!")
    #----------------------------------------------------------------------
    if r0>k-r1:
        sys.exit("INPUT_ERROR: condition r0>k-r1 is violated! Incompatible combination of parameters!")
    #----------------------------------------------------------------------
    if np.logical_or(c0<0,c0>n):
        sys.exit("INPUT_ERROR: c0 (min number of 0's in a column) should be in range between 0 and n!")
    #----------------------------------------------------------------------
    if np.logical_or(c1<0,c1>n):
        sys.exit("INPUT_ERROR: c1 (min number of 1's in a column) should be in range between 0 and n!")
    #----------------------------------------------------------------------
    if c0>n-c1:
        sys.exit("INPUT_ERROR: condition c0>n-c1 is violated! Incompatible combination of parameters!")
    #----------------------------------------------------------------------
    #TODO: compatibility check between parameters r0,r1,c0,c1
    #----------------------------------------------------------------------
    if sum(rf)!=100:
        sys.exit("INPUT_ERROR: sizes of row categories (in %) (rf) do not sum up to 100!")
    elif np.count_nonzero(np.logical_or(rf<0,rf>100))>0:
            sys.exit("INPUT_ERROR: sizes of row categories (in %) (rf) should be within [0,100] range!")
    #----------------------------------------------------------------------
    if np.count_nonzero(np.logical_or(rp<0,rp>1))>0:
        sys.exit("INPUT_ERROR: probabilities of row categories (rp) should be within [0,1] range!")
    elif sum(rp)!=1:
        print("WARNING: probabilities of row categories (rp) do not sum up to 1! They will be normalized..")
        rp=rp/sum(rp)
    #----------------------------------------------------------------------
    if sum(cf)!=100:
        sys.exit("INPUT_ERROR: sizes of column categories (in %) (cf) do not sum up to 100!")
    elif np.count_nonzero(np.logical_or(cf<0,cf>100))>0:
            sys.exit("INPUT_ERROR: sizes of column categories (in %) (cf) should be within [0,100] range!")
    #----------------------------------------------------------------------
    if np.count_nonzero(np.logical_or(cp<0,cp>1))>0:
        sys.exit("INPUT_ERROR: probabilities of column categories (cp) should be within [0,1] range!")
    elif sum(cp)!=1:
        print("WARNING: probabilities of row categories (cp) do not sum up to 1! They will be normalized..")
        cp=cp/sum(cp)
    #----------------------------------------------------------------------
    if t<0:
        sys.exit("t corresponds to the number of trials to be performed to avoid isomorphic matrices (if an input file is provided) and must be >=0!")

def compute_info_matrix(m):
    """
    Compute the info about matrix.
    Format: in one row the following info is stored
        - number of rows, n
        - number of columns, k
        - number of zeros in a matrix
        - %% of zeros in a matrix
        - summary counts for rows: frequency of rows with sums 0,1,2,...,k
        - summary counts for columns: frequency of columns with sums 0,1,2,...,n
        - summary counts for columns/rows: frequency of columns that contain 1's comming from rows with sum=1
    """
    
    n=m.shape[0]
    k=m.shape[1]
    sum_0=n*k-sum(m.reshape(n*k))
    row_freq, col_freq, col_u_freq= freq_counts(m)
    
    
    info_matrix=str(n)+" "+str(k)+" "+str(int(sum_0))+" "+str(round(sum_0/(n*k)*100,2))+" "+"".join(np.array2string(row_freq, max_line_width=len(row_freq)*(len(str(max(row_freq)))+1)+2) + np.array2string(col_freq, max_line_width=len(col_freq)*(len(str(max(col_freq)))+1)+2)+np.array2string(col_u_freq, max_line_width=len(col_u_freq)*(len(str(max(col_u_freq)))+1)+2))
    
    #print(info_matrix)
    
    return info_matrix
    
    
def freq_counts(m):
    """
    Counts frequency of rows (columns) with sum equal to 0,...,k (n).
    Also counts frequency of columns with 1's from rows summing up to 1
    """
    n=m.shape[0]
    k=m.shape[1]
    row_freq=np.zeros(k+1).astype('int32')
    col_freq=np.zeros(n+1).astype('int32')
    col_u_info=np.zeros(k).astype('int32')
    
    for i in range(n):
        s=sum(m[i,:])
        row_freq[int(s)]+=1
        if s==1:
            j=np.where(m[i,:]==1)
            col_u_info[j]+=1
        
    for j in range(k):
        col_freq[int(sum(m[:,j]))]+=1
        
    u=row_freq[1]
    col_u_freq=np.zeros(u+1).astype('int32')
    c=0
    for j in range(k):
        col_u_freq[int(col_u_info[j])]+=1
        c+=col_u_info[j]
        if c==u:
            break
    
    #print("row_freq:",row_freq)
    #print("col_freq:",col_freq)
    
    return row_freq, col_freq, col_u_freq
    
def print_m_to_file(m,outfile):
    file=open(outfile+"_input","w")
    file.write(str(m.shape[0])+" "+str(m.shape[1])+'\n')
    for i in range(m.shape[0]):
        file.write("sp"+str(i+1)+" "+np.array2string(m[i,:], max_line_width=m.shape[1]*2+2).replace("[","").replace("]","")+'\n')
    file.close()
        
    
#=================================================================================
#=================================================================================
#                      MAIN FUNCTION TO GENERATE 0-1 MATRIX
#=================================================================================
#=================================================================================
def generate_0_1_matrix(n=10,k=10,m=50,u=0, up=np.array([0.33,0.33,0.33]), r0=1,r1=2, c0=1,c1=4,rf=np.array([60,10,30]), rp=np.array([0.1,0.6,0.3]),cf=np.array([60,10,30]),cp=np.array([0.1,0.6,0.3]),t=5,outfile="output_file",infile=None):
    """
    Generating a random 0-1 matrix.
    The rows and columns are split into categories with different probabilities of beeing sampled.
    The minimum number of 0 and 1 in each column/row is controlled by  parameters, which can be changed by the user.
    
    Parameters:
    -----------
    TODO
    """
    
    parameter_sanity_check(n,k,m,u,up,r0,r1,c0,c1,rf,rp,cf,cp,t,outfile,infile)
    
    file_log=outfile+".log"
    #------------------------------------------------------------
    # Set parameters:
    #------------------------------------------------------------
    # info_matrices:    Information about other available matrices (see function XXXX for the included characteristics and format). This information will be used for a stringent check for equivalent matrices with respect to column and row shuffles. In case information of the generated matrix is the same as for some other matrix, the script will attempt to perform another generation trial. The number of trials is controlled via parameter d["t"].
    info_matrices=[]
    if infile and path.exists(infile):
        with open(infile) as f:
            for line in f:
                #print(line)
                info_matrices.append(line)
            
        #print(info_matrices)
    #------------------------------------------------------------
    # Number of 0's to be introduced given the input percentage of missing data:
    zeros_num=round(n*k*m/100)
    # Note: if m=0 (m=100), the code will still allocated only necessary (allowed) number of 0's, given other constraints, like minimum number of 0/1 in col/row.
    #------------------------------------------------------------
    # Compute the number of unique taxa to be introduced:
    u_num=round(n*u/100)
    # check maximum allowed number of rows with sum equals 1
    # the condition will be hardly ever used, mainly for completeness
    u_allowed=n-c1
    if u_allowed<u_num:
        #file=open(file_log,"a")
        print("WARNING: the requested number of rows with sum equals 1 is too high (given the minimum number of 1's a column)! Setting to maximum allowed:",u_allowed)
        #file.write("WARNING: the requested number of rows with sum equals 1 is too high (given the minimum number of 1's a column)! Setting to maximum allowed:",u_allowed)
        #file.close()
    u_num=min(u_num,u_allowed)
    #------------------------------------------------------------
    # Minimum number of zeros in a column
    min_zeros_num=c0
    #------------------------------------------------------------
    # Taxa/rows to be split into categories
    rows_allocated=n-u_num
    #------------------------------------------------------------
    row_sz=cat_sizes(rows_allocated,rf)
    col_sz=cat_sizes(k,cf)
    #------------------------------------------------------------
    # Fill out probability vectors for rows and columns:
    row_probs_orgn=np.array([])
    for i in range(len(rp)):
        row_probs_orgn=np.append(row_probs_orgn,np.repeat(rp[i],row_sz[i]))
    row_probs_orgn=row_probs_orgn/sum(row_probs_orgn)
        
    col_probs_orgn=np.array([])
    for i in range(len(cp)):
        col_probs_orgn=np.append(col_probs_orgn,np.repeat(cp[i],col_sz[i]))
    col_probs_orgn=col_probs_orgn/sum(col_probs_orgn)
    
    col_probs_row_sum_1_orgn=np.array([])
    for i in range(len(up)):
        col_probs_row_sum_1_orgn=np.append(col_probs_row_sum_1_orgn,np.repeat(up[i],col_sz[i]))
    col_probs_row_sum_1_orgn=col_probs_row_sum_1_orgn/sum(col_probs_row_sum_1_orgn)

    #print("Row probs:",row_probs)
    #print("Col probs:",col_probs)
    #------------------------------------------------------------
    print("="*100)
    print("Generating 0-1 matrix for parameters | taxa","%s" % n,"| partitions",k,"| % of missing data",str(m)+"%")
    print("="*100)
    #------------------------------------------------------------
    trials=0
    try_gen_again=True
    #------------------------------------------------------------
    # GENERATING 0-1 MATRIX
    #------------------------------------------------------------
    while try_gen_again:
        #print("TRIAL#:",trials)
        #------------------------------------------------------------
        # Initialiaze matrix:
        m=np.ones((n,k)).astype('int32')
        warnings_cnt={"war_complete_rows": 0, "war_min_zeros": 0}
        used_zeros=0
        iso_found=False
        #------------------------------------------------------------
        # set probability vectors
        row_probs=np.array(row_probs_orgn)
        col_probs=np.array(col_probs_orgn)
        col_probs_row_sum_1=np.array(col_probs_row_sum_1_orgn)
        #------------------------------------------------------------
        # Fill out rows with sum(row)=1:
        if u_num>0:
            used_zeros=u_num*(k-1)
            for i in range(-u_num,0,1):
                m[i,:]=np.zeros(k)
                m[i,np.random.choice(k, 1,p=col_probs_row_sum_1)]=1
            row_probs=np.append(row_probs,np.zeros(u_num))
                
        #------------------------------------------------------------
        # Control minimum number of 0's in a row:
        if r0 == 0:
            m[0,:]=np.zeros(k)
            min_zeros_num+=1
        else:
            for i in range(n):
                while k-np.count_nonzero(m[i,:])<r0 and row_probs[i]>0:
                    if np.count_nonzero(col_probs)>0:
                        j=int(np.random.choice(k, 1, p=col_probs/sum(col_probs)))
                        m[i,j]=0
                        used_zeros+=1
                        #check_allowed_vec(col_probs,m[:,j],j,c1)
                        check_allowed_pair_rec(col_probs,row_probs,m,i,j,r1,c1)
                        
                    else:
                        print(col_probs)
                        warnings_cnt["war_complete_rows"]+=1
                        print("WARNING: cannot assure min number of 0's in a row, since there are no allowed columns to be modified by introdusing new 0's")
        #------------------------------------------------------------
        #print("="*100)
        #print("Control complete columns (not allowed, since in such a case there won't be terraces)")
        #print("="*100)
        if min_zeros_num > 0:
            # INFO: One could set the min_zeros_num to 1 by default, otherwise, allocate more zeros. However, when you need to allocate only one zero per column, you are less likely to get stuck, because there are no more allowed taxa, since they were used up on other columns. I think, this would only occur, when the min_zero_num is really high, though.
            for j in range(k):
                if sum(m[:,j])==n:
                    if np.count_nonzero(row_probs)>0:
                    
                        i=np.random.choice(len(row_probs),1,p=row_probs/sum(row_probs))
                        m[i,j]=0
                        used_zeros+=1

                        check_allowed_pair_rec(col_probs,row_probs,m,i,j,r1,c1)
                    else:
                        warnings_cnt["war_min_zeros"]+=1
                        print("WARNING: cannot assure that all columns have at least one zero.")

            if min_zeros_num>1:
                for j in range(k):
                    while n-np.count_nonzero(m[:,j])<min_zeros_num and np.count_nonzero(row_probs)>0 and col_probs[j]>0:
                        i=sample_index(row_probs,m[:,j])
                        m[i,j]=0
                        used_zeros+=1
                        check_allowed_pair_rec(col_probs,row_probs,m,i,j,r1,c1)
                    if np.count_nonzero(row_probs)==0:
                            warnings_cnt["war_min_zeros"]+=1
        #------------------------------------------------------------
        #print("="*100)
        #print("If used_zeros are < than requested, continue allocating 0 across the matrix")
        #print("="*100)
        while used_zeros < zeros_num and np.count_nonzero(row_probs)!=0 and np.count_nonzero(col_probs)!=0:
            #print("="*100)
            #print("MATRIX")
            #print(m)
            #print("row_probs:",np.array2string(row_probs, max_line_width=10000))
            #print("col_probs:",np.array2string(col_probs,max_line_width=10000))
            index_pair = sample_indices(col_probs,row_probs,m)
            #print("Printing sampled indices: ",index_pair)
            i=index_pair[0]
            j=index_pair[1]
            m[i,j]=0
            used_zeros+=1
            check_allowed_pair_rec(col_probs,row_probs,m,i,j,r1,c1)
            #print("="*100)
            #check_allowed_thorough(col_probs,row_probs,m,r1,c1)
        
        if r0 == 0:
            m[0,:]=np.ones(k)
            
        #------------------------------------------------------------
        info_matrix=compute_info_matrix(m)
        #------------------------------------------------------------
        # Check for equivalence against other matrices:
        if info_matrices and path.exists(infile):
            #info_matrix=info_matrices[0] # used for testing
            iso_found=False
            for i in range(len(info_matrices)):
                if info_matrices[i].replace(" ","") == info_matrix.replace(" ",""):
                    iso_found=True
                    print("INFO: generated matrix did not pass isomorphism check. Generate new sample matrix.")
                    break
        
        #------------------------------------------------------------
        trials+=1
        try_gen_again=False
        if iso_found and trials<t:
            try_gen_again=True
    #------------------------------------------------------------
    # FINISHED MATRIX GENERATION
    #------------------------------------------------------------
    if iso_found and trials==t:
        print("WARNING: Within",trials," trials I could not generate a matrix, which passed basic isomorphism check, given info about already existing matrices (contained in file",infile,"). That is, there is another existing matrix, which might be identical with respect to row/column shuffles.")
    else:
        # - print out matrix info, maybe plot matrix, and print the matrix itself with appropriate format
        print("INFO: Matrix generation is completed!")
        #print(m)
        #print(info_matrix)
        if infile:
            file=open(infile,"a")
            file.write(info_matrix+'\n')
            file.close()

        file=open(outfile+".log","a")
        file.write("Matrix INFO:\n")
        file.write("="*50+"\n")
        file.write("n k #0 %0 row_freq col_freq col_row_sum_1_freq\n")
        file.write(info_matrix+'\n')
        file.close()
            
        print_m_to_file(m,outfile)
        
#=================================================================================
#=================================================================================
#=================================================================================
#=================================================================================
        
#help(generate_0_1_matrix)

#=================================================================================
if __name__ == "__main__":
    parse_parameters()
    #generate_0_1_matrix()
    
    
    
    


