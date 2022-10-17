class O2d:
    @staticmethod
    def obj_to_dic(obj: object) -> object:
        """
        将传入的data对象转成字典
        """
        result = {}
        for temp in obj.__dict__:
            if temp.startswith('_') or temp == 'metadata':
                continue
            result[temp] = getattr(obj, temp)
        return result

    @staticmethod
    def obj_to_list(list_obj):
        """
        将传入的data对象转成List,list中的元素是字典
        """
        result = []
        for obj in list_obj:
            result.append(O2d.obj_to_dic(obj))

        return result
