import sys
import glob
import pandas as pd

args = sys.argv
job_num = (args[1])
job_id = (args[2])

title = '*_{0}_*.txt'.format(job_num)
file_list = glob.glob(title)
df_list = [pd.read_table(file) for file in file_list]
df = pd.concat(df_list)