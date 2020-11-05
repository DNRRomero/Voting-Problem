import sys
import glob
import pandas as pd
from pathlib import Path


args = sys.argv
conf_type = args[1]
job_num = args[2]

source = '../../data/Guacolda/out/*_{0}_*.out'.format(job_num)
file_list = glob.glob(source)

aux = file_list[0].rsplit('_', maxsplit=2)
title = '{0}.csv'.format(aux[0])
df_list = [pd.read_table(file) for file in file_list]
df = pd.concat(df_list)


dout = '../../data/{0}'.format(conf_type)
data_out = Path(dout)
df.to_csv(data_out / title, encoding='utf-8', index=False)


