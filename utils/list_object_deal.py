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
