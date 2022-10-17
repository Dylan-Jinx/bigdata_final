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