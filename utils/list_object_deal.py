import pandas as pd

from model import BigData


def get_list_attr_by_attrname(data, attr):
    list = []
    for obj in data:
        list.append(obj.__getattribute__(attr))
    return list


def get_list_attr_by_attrnames(data, attr):
    list = []
    for obj in data:
        temp = BigData()
        for v in attr:
            temp.__setattr__(v, obj.__getattribute__(v))
        list.append(temp)
    return list


def get_list_selected_attr_by_attrname(data, attrname) -> list:
    list = []
    for obj in data:
        list.append(obj.__getattribute__(attrname))
    return list


def get_key_val_by_query_datas(datas):
    key = []
    value = []
    for i in datas:
        key.append(i[0])
        value.append(i[1])
    return key, value


def all_data_convert_dataFrame(datas):
    testxx = {
        "城市可支配收入": get_list_selected_attr_by_attrname(datas, "city_able_income"),
        "城市可支配收入与收入比": get_list_selected_attr_by_attrname(datas, "city_able_income_ratio"),
        "城市总收入": get_list_selected_attr_by_attrname(datas, "city_income"),
        "城市收入与城市人口比 ": get_list_selected_attr_by_attrname(datas, "city_income_population_ratio"),
        "城市人口": get_list_selected_attr_by_attrname(datas, "city_population"),
        "城市人口与总人口比": get_list_selected_attr_by_attrname(datas, "city_population_ratio"),
        "城镇化": get_list_selected_attr_by_attrname(datas, "city_ratio"),
        "总收入": get_list_selected_attr_by_attrname(datas, "income"),
        "总人口": get_list_selected_attr_by_attrname(datas, "population"),
        "泰尔指数": get_list_selected_attr_by_attrname(datas, "theil_index"),
        "乡村可支配收入": get_list_selected_attr_by_attrname(datas, "village_able_income"),
        "乡村可支配收入与收入比": get_list_selected_attr_by_attrname(datas, "village_able_income_ratio"),
        "乡村收入": get_list_selected_attr_by_attrname(datas, "village_income"),
        "乡村收入与人口比 ": get_list_selected_attr_by_attrname(datas, "village_income_population_ratio"),
        "乡村人口": get_list_selected_attr_by_attrname(datas, "village_population"),
        "乡村人口与总人口比": get_list_selected_attr_by_attrname(datas, "village_population_ratio")
    }
    df = pd.DataFrame(testxx)
    return df
