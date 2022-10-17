import pandas as pd

from pretreatment.data_precondition import data_file_path, data_loading


def get_table_header():
    datas = data_loading()
    return datas.columns.to_list()


def selected_column_info(column_name):
    return data_loading()[{'year','dum',column_name}]
