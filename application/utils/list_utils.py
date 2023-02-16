import pprint
from typing import List


def key_by(items, key):
    key_dict = {}
    for item in items:
        key_dict[getattr(item, key)] = item
    return key_dict


def group_by(items, key):
    group_dict = {}
    for item in items:
        value = getattr(item, key)
        if not group_dict.get(value):
            group_dict[value] = []
        group_dict[value].append(item)
    return group_dict


def list_to_tree(source: List[dict]):
    """
    将元素中包含有父节点的列表构造转化成一颗带有子节点对象的树状列表结构

     source = [
        {"id": 1, "name": "A", "parent_id": None},
        {"id": 2, "name": "B", "parent_id": 1},
        {"id": 3, "name": "C", "parent_id": 2},
        {"id": 4, "name": "D", "parent_id": 3},
        {"id": 5, "name": "E", "parent_id": 2},
    ]
    转化为

    target=[{"id": 1,
             "name": "A",
             "children": [{"id": 2,
                           "name": "B",
                           "children": [{"id": 3,
                                         "name": "C",
                                         "children": [{"id": 4,
                                                       "name": "D",
                                                       "children": []}]},
                                        {"id": 5,
                                         "name": "E",
                                         "children": []}]}]}]

    """
    # 先把列表变成字典(key 是id，value 是列表元素
    source_dict = {item.get("id"): item for item in source}
    target = []
    for item in source:
        if not item.get("parent_id"):

            # 第0级别直接加到target
            target.append(item)
        else:
            # 如果当前元素是子节点，则找到父元素后，加入到父元素的children属性里面
            parent = source_dict.get(item.get("parent_id"))
            if parent:
                parent.setdefault("children", []).append(item)
            else:
                # 即使有parent_id,也有可能没有parent_id的权限，当前节点就当作父节点
                target.append(item)
    return target


def flatten(itr: List[list]):
    """
    打平列表
    [[1, 2, 3], [4, 5, 6], [7], [8, 9]]
    to
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    from functools import reduce
    import operator
    if itr:
        return reduce(operator.concat, itr)
    else:
        return itr


def all_children_codes(node: dict, authrys: List[str], check=True):
    """
    获取 node下指定节点authrys的所有的子节点

    node = {
                "code": '01',
                "children": [
                    {
                        "code": '11',
                        "children": [{
                            "code": '111',
                        }]},
                    {
                        "code": '22',
                        "children": [{
                            "code": '222',
                        }]
                    },
                ],
            }
    返回： ["01", "11", "21", '111', '222']
    :param node 当前节点
    :param authrys  需要获取的节点的code值
    :param check
    :return list
    """
    result: List[str] = []
    need_check = True
    if not check or (node.get("code") in authrys):
        result.append(node.get("code"))
        need_check = False
    if node.get("children"):
        children = map(lambda item: all_children_codes(item, authrys, need_check), node.get("children"))

        result.extend(flatten(children))

    return result
