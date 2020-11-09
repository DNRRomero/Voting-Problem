import sys
import glob
import os
import pandas as pd

args = sys.argv
conf_type = args[1]
job_num = args[2]

source = '../../data/Guacolda/out/*_{0}_*.out'.format(job_num)
file_list = glob.glob(source)

print('There are {0} files to be merged'.format(len(file_list)))
aux = file_list[0].rsplit('_', maxsplit=2)[0].rsplit('/', maxsplit=1)[1]

title = '{0}.csv'.format(aux)

df_list = [pd.read_table(file, sep=',') for file in file_list]
df = pd.concat(df_list)

dout = '../../data/{0}/{1}'.format(conf_type, title)
print(dout)
df.to_csv(dout, encoding='utf-8', index=False)

for file in file_list:
    os.remove(file)


