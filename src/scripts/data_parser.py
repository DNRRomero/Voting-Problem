import sys
import glob
import pandas as pd

args = sys.argv
job_num = (args[1])

title = '*_{0}_*.out'.format(job_num)
file_list = glob.glob(title)
aux = file_list[0].rsplit('_', maxsplit=2)
title = '{0}.csv'.format(aux[0])
df_list = [pd.read_table(file) for file in file_list]
df = pd.concat(df_list)

df.to_csv(title)


