import pandas as pd

from pretreatment.data_precondition import data_file_path, data_loading


def get_table_header():
    datas = data_loading()
    return datas.columns.to_list()


def selected_column_info(datas, column_name):
    return datas[column_name]


if __name__ == "__main__":
    get_table_header()
    print(selected_column_info(data_loading(), 'dum'))
