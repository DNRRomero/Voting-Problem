import glob
import os
import pandas as pd

import argparse

parser = argparse.ArgumentParser(description='Converts .out files into .csv data files in their respective folders')
parser.add_argument('conf_type', help='Type of configuration object simulated (i.e. Ring or Torus)')
parser.add_argument('job_num', help='Slurm job id')
parser.add_argument("-s", "--serial", help="add column with sample number per file", action="store_true")
parser.add_argument("-l", "--label", help="add additional label before job number")

args = parser.parse_args()

out_src = '../../data/Guacolda/out/*_{0}_*.out'.format(args.job_num)
err_src = '../../data/Guacolda/err/*_{0}_*.err'.format(args.job_num)
out_list = glob.glob(out_src)
err_list = glob.glob(err_src)

print('There are {0} files to be merged'.format(len(out_list)))
aux = out_list[0].rsplit('_', maxsplit=2)[0].rsplit('/', maxsplit=1)[1]

title = '{0}.csv'.format(aux)
try:
    a = out_list[0]
    if args.serial:
        df_list = []
        for i, file in enumerate(out_list):
            njob = file.rsplit('_', maxsplit=1)[1].rsplit('.', maxsplit=1)[0]
            serial = args.job_num + njob
            table = pd.read_table(file, sep=',')
            nrows = len(table.index)
            table['sample'] = nrows * [serial]
            df_list.append(table)
    else:
        df_list = [pd.read_table(file, sep=',') for file in out_list]

    df = pd.concat(df_list)

    dout = '../../data/{0}/{1}'.format(args.conf_type, title)
    print(dout)
    df.to_csv(dout, encoding='utf-8', index=False)

    for file in out_list:
        os.remove(file)
    for file in err_list:
        os.remove(file)
except IndexError:
    print('There are no files to be merged, parsing failed.mill')
