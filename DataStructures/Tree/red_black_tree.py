from DataStructures.Tree import rbt_node as rbt
from DataStructures.List import single_linked_list as sl


def default_compare(a, b):
    
    if a == b:
        return 0
    return -1 if a < b else 1

def size_tree(node_rbt):
    if node_rbt is None:
        return 0
    else:
        return node_rbt["size"]

def update_size(node_rbt):
    if node_rbt is not None:
        node_rbt["size"] = 1 + size_tree(node_rbt["left"]) + size_tree(node_rbt["right"])

def is_red(node_rbt):
    if node_rbt is None:
        return False
    else:
        if node_rbt["color"] == rbt.RED:
            return True
        else:
            return False

def flip_node_color(node_rbt):
    if node_rbt["color"] == rbt.RED:
        node_rbt["color"] = rbt.BLACK
    else:
        node_rbt["color"] = rbt.RED
    return node_rbt

def rotate_left(node_rbt):
    x = node_rbt["right"]
    node_rbt["right"] = x["left"]
    x["left"] = node_rbt
    x["color"] = node_rbt["color"]
    node_rbt["color"] = rbt.RED
    update_size(node_rbt)
    update_size(x)
    return x

def rotate_right(node_rbt):
    x = node_rbt["left"]
    node_rbt["left"] = x["right"]
    x["right"] = node_rbt
    x["color"] = node_rbt["color"]
    node_rbt["color"] = rbt.RED
    update_size(node_rbt)
    update_size(x)
    return x

def flip_colors(node_rbt):
    flip_node_color(node_rbt)
    flip_node_color(node_rbt["left"])
    flip_node_color(node_rbt["right"])
    return node_rbt
    
def insert_node(h, key, value):
    if h is None:
        return rbt.new_node(key, value, rbt.RED)

    cmp = default_compare(key, rbt.get_key(h))

    if cmp < 0:
        h["left"] = insert_node(h["left"], key, value)
    elif cmp > 0:
        h["right"] = insert_node(h["right"], key, value)
    else:
        h["value"] = value

    if is_red(h["right"]) and not is_red(h["left"]):
        h = rotate_left(h)
    if is_red(h["left"]) and is_red(h["left"]["left"]):
        h = rotate_right(h)
    if is_red(h["left"]) and is_red(h["right"]):
        flip_colors(h)

    update_size(h)
    
    return h

def put(my_rbt, key, value):
    
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    my_rbt["root"]["color"] = rbt.BLACK
    
    return my_rbt

def get_node(root, key):
    while root is not None:
        cmp = default_compare(key, rbt.get_key(root))
        if cmp < 0:
            root = root["left"]
        elif cmp > 0:
            root = root["right"]
        else:
            return rbt.get_value(root)
    return None

def get(my_rbt, key):
    return get_node(my_rbt["root"], key)

def contains(my_rbt, key):
    if get(my_rbt, key) is not None:
        return True
    return False

def size(my_rbt):
    if my_rbt["root"] is None:
        return 0
    else:
        return size_tree(my_rbt["root"])

def is_empty(my_rbt):
    if size_tree(my_rbt["root"]) == 0:
        return True
    else:
        return False
    
def key_set_tree(root):
    keys = sl.new_list()
    if root is None:
        return keys

    left_keys = key_set_tree(root["left"])
    current = left_keys["first"]
    while current is not None:
        sl.add_last(keys, current["info"])
        current = current["next"]

    sl.add_last(keys, rbt.get_key(root))

    right_keys = key_set_tree(root["right"])
    current = right_keys["first"]
    while current is not None:
        sl.add_last(keys, current["info"])
        current = current["next"]

    return keys

def key_set(my_rbt):
    return key_set_tree(my_rbt["root"])

def value_set_tree(root):
    values = sl.new_list()
    if root is None:
        return values

    left_values = value_set_tree(root["left"])
    current = left_values["first"]
    while current is not None:
        sl.add_last(values, current["info"])
        current = current["next"]

    sl.add_last(values, rbt.get_value(root))

    right_values = value_set_tree(root["right"])
    current = right_values["first"]
    while current is not None:
        sl.add_last(values, current["info"])
        current = current["next"]

    return values

def value_set(my_rbt):
    return value_set_tree(my_rbt["root"])

def get_min_node(root):
    if root is None:
        return None
    if root["left"] is None:
        return rbt.get_key(root)
    return get_min_node(root["left"])

def get_min(my_rbt):
    return get_min_node(my_rbt["root"])

def get_max_node(root):
    if root is None:
        return None
    if root["right"] is None:
        return rbt.get_key(root)
    return get_max_node(root["right"])

def get_max(my_rbt):
    return get_max_node(my_rbt["root"])

def height_tree(root):
    if root is None:
        return 0
    left_h = height_tree(root["left"])
    right_h = height_tree(root["right"])
    if left_h >= right_h:
        return 1 + left_h
    else:
        return 1 + right_h

def height(my_rbt):
    return height_tree(my_rbt["root"])

def keys_range(root, key_initial, key_final, list_key):
    if root is None:
        return list_key

    k = rbt.get_key(root)

    if key_initial is None or k > key_initial:
        keys_range(root["left"], key_initial, key_final, list_key)

    if (key_initial is None or k >= key_initial) and (key_final is None or k <= key_final):
        sl.add_last(list_key, k)

    if key_final is None or k < key_final:
        keys_range(root["right"], key_initial, key_final, list_key)

    return list_key

def keys(my_rbt, key_initial, key_final):
    if key_initial is not None and key_final is not None:
        if key_initial > key_final:
            key_initial, key_final = key_final, key_initial
    result = sl.new_list()
    return keys_range(my_rbt["root"], key_initial, key_final, result)

def values_range(root, key_initial, key_final, list_values):
    if root is None:
        return list_values

    k = rbt.get_key(root)

    if key_initial is None or k > key_initial:
        values_range(root["left"], key_initial, key_final, list_values)

    if (key_initial is None or k >= key_initial) and (key_final is None or k <= key_final):
        sl.add_last(list_values, rbt.get_value(root))

    if key_final is None or k < key_final:
        values_range(root["right"], key_initial, key_final, list_values)

    return list_values

def values(my_rbt, key_initial, key_final):
    if key_initial is not None and key_final is not None:
        if key_initial > key_final:
            key_initial, key_final = key_final, key_initial
    result = sl.new_list()
    return values_range(my_rbt["root"], key_initial, key_final, result)
    
    
    
    