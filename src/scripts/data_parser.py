import sys
import glob
import pandas as pd

args = sys.argv
conf_type = args[1]
job_num = args[2]

source = '../../data/Guacolda/out/*_{0}_*.out'.format(job_num)
file_list = glob.glob(source)


aux = file_list[0].rsplit('_', maxsplit=2)[0].rsplit('/', maxsplit=1)[1]
print(aux)
title = '{0}.csv'.format(aux)
print(title)
df_list = [pd.read_table(file) for file in file_list]
df = pd.concat(df_list)

dout = '../../data/{0}/{1}'.format(conf_type, title)
print(dout)
df.to_csv(dout, encoding='utf-8', index=False)


