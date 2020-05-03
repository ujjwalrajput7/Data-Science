import pandas as pd
import numpy as np

from copy import deepcopy

def merge_annual_datas(org_datas,show_process_information=True):
    '''
    Merge all of the annual datas which certains all the columns I am interested in.

    Parameters
    ----------------------
    org_datas:dict
    dict for annual_datas

    Returns
    ------------------------
    pd.DataFrame:
    a df after merged
    '''

    # dict for processed data
    datas = {}

    # deepcopy
    for year in org_datas:
        datas[year] = deepcopy(org_datas[year])

    def select_column(datas,year,select_column_indexes,select_column_names,show_df=True):
        '''
        select columns I am interested in

        Parameters:
        ----------------------
        datas: dict of pd.DataFrame
        dict for annual_datas
        year:int
        year
        select_column_indexes: list of str
        the indexes of selected columns
        select_column_names: list of str
        the names of selected columns
        show_df: bool
        whether to show df which only contains the columns I am interested in

        Returns:
        ----------------------
        pd.DataFrame:
        df containning the columns I am interested in

        '''

        select_column_index = select_column_indexes
        datas[year] = datas[year].iloc[:,select_column_index]
        datas[year].columns = select_column_names
  
        if show_process_information:
            print("*" * 20 + str(year) + "*" * 20 )
            print('select %s from data in %d year' %(','.join(select_column_names),year))
            print("-"* 40)
            print('indexes of above columns is %s' %str(select_column_indexes))
        if show_df:
            if show_process_information:
                print("-"* 40)
                print('show df after selected columns:')
                print("-"* 40)
                print(datas[year].head(2))

        return datas[year]


    # -----------------------2011--------------------
    # change_multiindex_to_simpleindex(datas[2011])
    datas[2011].loc[:,'languages'] = datas[2011]['Which languages are you proficient in?'].apply(lambda x:";".join([i  for i in list(x) if not pd.isna(i)]),axis=1)

    # select columns
    select_column_indexes = [0,2,3,4,5,6,65,45]
    select_column_names = ['country','age','IT_experience','industry','company_size','occupation','languages','salary']

    datas[2011] = select_column(datas,2011,select_column_indexes,select_column_names)

    # -----------------------2012--------------------
    # change_multiindex_to_simpleindex(datas[2012])
    datas[2012].loc[:,'languages'] = datas[2012]['Which languages are you proficient in?'].apply(lambda x:";".join([i  for i in list(x) if not pd.isna(i)]),axis=1)
        
    # select columns
    select_column_indexes = [0,2,3,4,5,6,75,39]
    select_column_names = ['country','age','IT_experience','industry','company_size','occupation','languages','salary']

    datas[2012] = select_column(datas,2012,select_column_indexes,select_column_names)

    # -----------------------2013--------------------
    # change_multiindex_to_simpleindex(datas[2013])
    datas[2013].loc[:,'languages'] = datas[2013]['Which of the following languages or technologies have you used significantly in the past year?'].apply(lambda x:";".join([i  for i in list(x) if not pd.isna(i)]),axis=1)
        
    # # select columns
    select_column_indexes = [0,2,3,4,5,6,128,100]
    select_column_names = ['country','age','IT_experience','industry','company_size','occupation','languages','salary']

    datas[2013] = select_column(datas,2013,select_column_indexes,select_column_names)

    # -----------------------2014--------------------
    # change_multiindex_to_simpleindex(datas[2014])
    datas[2014].loc[:,'languages'] = datas[2014]['Which of the following languages or technologies have you used significantly in the past year?'].apply(lambda x:";".join([i  for i in list(x) if not pd.isna(i)]),axis=1)
        
    # select columns
    select_column_indexes = [0,3,5,8,6,120,7]
    select_column_names = ['country','age','IT_experience','industry','occupation','languages','salary']

    datas[2014] = select_column(datas,2014,select_column_indexes,select_column_names)

    # -----------------------2015--------------------
    # merge all of the columns about languages
    datas[2015].loc[:,'languages'] = datas[2015].iloc[:,10:51].apply(lambda x:";".join([i  for i in list(x) if not pd.isna(i)]),axis=1)

    # select columns
    select_column_indexes = [0,1,4,108,5,222,106]
    select_column_names = ['country','age','IT_experience','industry','occupation','languages','salary']

    datas[2015] = select_column(datas,2015,select_column_indexes,select_column_names)

    # -----------------------2016--------------------
    # select columns
    select_column_indexes = [2,5,12,21,10,16,14]
    select_column_names = ['country','age','IT_experience','industry','occupation','languages','salary']

    datas[2016] = select_column(datas,2016,select_column_indexes,select_column_names)

    # -----------------------2017--------------------
    # merge all of the columns about occuptions
    datas[2017].loc[:,'occuption'] = datas[2017].iloc[:,15:18].apply(lambda x:";".join([i  for i in list(x) if not pd.isna(i)]),axis=1)
        
    # select columns
    select_column_indexes = [3,12,9,154,88,152]
    select_column_names = ['country','IT_experience','company_size','occupation','languages','salary']

    datas[2017] = select_column(datas,2017,select_column_indexes,select_column_names)

    # -----------------------2018--------------------
    # select columns
    select_column_indexes = [3,124,11,8,9,65,52]
    select_column_names = ['country','age','IT_experience','company_size','occupation','languages','salary']

    datas[2018] = select_column(datas,2018,select_column_indexes,select_column_names)

    # add column 'year'
    for year in range(2011,2019):
        datas[year]['year'] = year
    if show_process_information:
        print("*"*40)
        print('add column "year" for every annual data')

    # merge
    all_years_data = datas[2011]
    for year in range(2012,2019):
        all_years_data = all_years_data.append(datas[year])

    # reset_index
    all_years_data = all_years_data.reset_index()

    if show_process_information:
        print("*"*40)
        print('successed to merge all of the annual datas')
        print('merged data has %d rows and %d columns' %(all_years_data.shape[0],all_years_data.shape[1]))
        print("*"*40)

    return all_years_data