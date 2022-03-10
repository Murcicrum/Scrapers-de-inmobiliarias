#!/usr/bin/python3

import time
import os, sys
import pandas as pd


def concat_df(dir_raw:str, n_last:int):

    files = os.listdir(dir_raw)
    files.sort()

    df_full = pd.DataFrame()         #Acá voy concatenando los csv

    for file in files[-n_last:]:
        if not file.endswith('.csv'): continue
        print('Unificando... ', file)
        
        #los nombres son como: YYYY-MM-DD_webpage_type.csv
        fe_scrap, web_orig, tipo_inm = file[:-4].split('_')
        
        df_aux = pd.read_csv( dir_raw + file )
        shape_ori = df_aux.shape
        df_aux.drop_duplicates( inplace=True )
        
        df_aux['web_orig'] = web_orig
        df_aux['tipo_imm'] = tipo_inm
        shape_fin = df_aux.shape

        print(f'\tShape original: {shape_ori}\t Shape final: {shape_fin}' )

        df_full = pd.concat([df_full,df_aux],
                             sort=True, ignore_index=True)
                             
    print('Shape total: ', df_full.shape)
    return df_full
    


if __name__ == '__main__':
    DIR_RAW = sys.argv[1]
    DIR_OUT = sys.argv[2]

    N_LAST = 6

    TODAY = time.strftime( "%Y-%m-%d", time.localtime() )
    FILEPATH = DIR_OUT + TODAY + '_unified.csv'

    df = concat_df(DIR_RAW, N_LAST)
    
    print('Guardo csv unificado como: ',FILEPATH)
    df.to_csv( FILEPATH ,index=False)
    
