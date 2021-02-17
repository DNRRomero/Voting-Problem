import glob
import os
import pandas as pd

import argparse

parser = argparse.ArgumentParser(description='Converts .out files into .csv data files in their respective folders')
parser.add_argument('conf_type', help='Type of configuration object simulated (i.e. Ring or Torus)')
parser.add_argument('job_num', help='Slurm job id')
parser.add_argument("-s", "--serial", help="add column with sample number per file", action="store_true")
parser.add_argument("-m", "--maintain", help="convert non empty files up to now, do not remove after conversion",
                    action="store_true")
parser.add_argument("-l", "--label", help="add additional label before job number")

args = parser.parse_args()

out_src = f'../../data/Guacolda/out/*_{args.job_num}_*.out'
err_src = f'../../data/Guacolda/err/*_{args.job_num}_*.err'
out_list = glob.glob(out_src)
err_list = glob.glob(err_src)

try:
    lab = args.label if args.label else ''
    aux = out_list[0].rsplit('_', maxsplit=2)[0].rsplit('/', maxsplit=1)[1]
    title = f'{aux}__{lab}.csv'
    print(f'There are {len(out_list)} files to be merged')
    if args.serial:
        df_list = []
        for i, file in enumerate(out_list):
            if os.path.getsize(file) <= 0:
                continue
            njob = file.rsplit('_', maxsplit=1)[1].rsplit('.', maxsplit=1)[0]
            serial = args.job_num + njob
            table = pd.read_table(file, sep=',')
            nrows = len(table.index)
            table['sample'] = nrows * [serial]
            df_list.append(table)
    else:
        df_list = [pd.read_table(file, sep=',') for file in out_list if os.path.getsize(file)>0]

    df = pd.concat(df_list)

    dout = f'../../data/{args.conf_type}/{title}'
    print(dout)
    df.to_csv(dout, encoding='utf-8', index=False)
    if not args.maintain:
        for file in out_list:
            os.remove(file)
        for file in err_list:
            os.remove(file)
except IndexError:
    print('There are no files to be merged, parsing failed.mill')
