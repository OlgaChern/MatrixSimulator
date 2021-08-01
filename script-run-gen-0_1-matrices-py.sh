#!/bin/bash
#----------------------------------------------------------------------------
# Unix
#f_main=/project/olga-phylo/terraces/2021/02.Feb
f_main=/project/olga-phylo/terraces/2021/03.Mar_REF
f_script=/project/olga-phylo/terraces/scripts/scripts_gen_0_1_matrices
#----------------------------------------------------------------------------
# Mac
#f_main=/Users/Olga/Projects/Science/Projects/terraces/2021/03.Mar
#f_script=/Users/Olga/Projects/Science/Projects/terraces/scripts_gen_0_1_matrices
#----------------------------------------------------------------------------
f_work=$f_main/data/simulated
#script=$f_script/script-run-gen-0_1-matrices-for_one_param_comb-py.sh
script=$f_script/script-run-gen-0_1-matrices-types.sh
#----------------------------------------------------------------------------
taxa="20 50 100 300 700"			#"20 50 100 300 700 1000"
partitions="5 10 30 100"		#"5 10 30 100 200"
missing_data="10 30 50 70 90"		#"10 30 50 70 90"
#----------------------------------------------------------------------------
#taxa="20"
#partitions="5"
#missing_data="10"
#----------------------------------------------------------------------------
for n in ${taxa}
do
	for k in ${partitions}
	do
		for md in ${missing_data}
		do

			echo "Generating matrices for n$n k$k md${md}...."
			f_out=$f_work/datasets_${n}_taxa/part_${k}/missing_data_${md}
			mkdir -p $f_out
			file_out=$f_out/output_info-matrix_gen

			$script $n $k $md $f_work $f_script > $file_out
			#submit2sge -N m$n-$k-$md -q desktops "$script $n $k $md $f_work $f_script > $file_out"
		done
	done
done


