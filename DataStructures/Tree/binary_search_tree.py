from DataStructures.Tree import bst_node as bst
from DataStructures.List import single_linked_list as sl

def default_compare(key, element):
   if key == bst.get_key(element):
      return 0
   elif key > bst.get_key(element):
      return 1
   return -1

def new_map():
    return {"root":None}

def insert_node(root, key, value):
    if root is None:
        return bst.new_node(key, value)

    cmp = default_compare(key, root)
    if cmp == 0:
        root["value"] = value
    elif cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    else:
        root["right"] = insert_node(root["right"], key, value)

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root

def put(my_bst, key, value):
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def get_node(root, key):
    if root is None:
        return None

    cmp = default_compare(key, root) 
    if cmp == 0:        
        return root
    elif cmp < 0:         
        return get_node(root["left"], key)
    else:                 
        return get_node(root["right"], key)
    
def get(my_bst, key):
    node = get_node(my_bst["root"], key)
    if node is None:
        return None
    return bst.get_value(node)

def size_tree(root):
    if root is None:
        return 0
    return root["size"]

def size(my_bst):
    return size_tree(my_bst["root"])

def contains(my_bst,key):
    node= get(my_bst,key)
    if node is not None:
        return True
    else:
        return False
    
def is_empty(my_bst):
    return my_bst["root"] is None
    
def key_set_tree(root):
    keys = sl.new_list()
    if root is None:
        return keys

    left_keys = key_set_tree(root["left"])
    current = left_keys["first"]
    while current is not None:
        sl.add_last(keys, current["info"])
        current = current["next"]

    sl.add_last(keys, bst.get_key(root))

    right_keys = key_set_tree(root["right"])
    current = right_keys["first"]
    while current is not None:
        sl.add_last(keys, current["info"])
        current = current["next"]

    return keys

def key_set(my_bst):
    return key_set_tree(my_bst["root"])

def value_set_tree(root):
    
    values = sl.new_list()
    
    if root is None:
        return values

    left_values = value_set_tree(root["left"])
    current = left_values["first"]
    
    while current is not None:
        sl.add_last(values, current["info"])
        current = current["next"]

    sl.add_last(values, bst.get_value(root))

    right_values = value_set_tree(root["right"])
    current = right_values["first"]
    
    while current is not None:
        sl.add_last(values, current["info"])
        current = current["next"]

    return values

def value_set(my_bst):
    return value_set_tree(my_bst["root"])
    
def get_min_node(root):
    
    if root is None:
        return None
    
    if root["left"] is None:
        return bst.get_key(root)
    
    return get_min_node(root["left"])

def get_min(my_bst):
    return get_min_node(my_bst["root"])

def get_max_node(root):
    
    if root is None:
        return None
    
    if root["right"] is None:
        return bst.get_key(root)
    
    return get_max_node(root["right"])

def get_max(my_bst):
    return get_max_node(my_bst["root"])

def delete_min_tree(root):
    
    if root is None:
        return None
    
    if root["left"] is None:
        return root["right"]

    root["left"] = delete_min_tree(root["left"])

    left_size = 0
    right_size = 0

    if root["left"] is not None:
        left_size = root["left"]["size"]
        
    if root["right"] is not None:
        right_size = root["right"]["size"]

    root["size"] = 1 + left_size + right_size
    
    return root

def delete_min(my_bst):
    
    my_bst["root"] = delete_min_tree(my_bst["root"])
    
    return my_bst

def delete_max_tree(root):
    
    if root is None:
        return None
    
    if root["right"] is None:
        return root["left"]

    root["right"] = delete_max_tree(root["right"])

    left_size = 0
    right_size = 0

    if root["left"] is not None:
        left_size = root["left"]["size"]
        
    if root["right"] is not None:
        right_size = root["right"]["size"]

    root["size"] = 1 + left_size + right_size
    
    return root

def delete_max(my_bst):
    
    my_bst["root"] = delete_max_tree(my_bst["root"])
    
    return my_bst
    
def height(my_bst):
    
    return height_tree(my_bst["root"])

def height_tree(root):
    
    if root is None:
        return 0
    
    left_h = height_tree(root["left"])
    right_h = height_tree(root["right"])
    return 1 + max(left_h, right_h)

def keys(my_bst, key_initial, key_final):
    
    if key_initial is not None and key_final is not None and key_initial > key_final:
        key_initial, key_final = key_final, key_initial
        
    result = sl.new_list()
    
    return keys_range(my_bst["root"], key_initial, key_final, result)


def keys_range(root, key_initial, key_final, list_key):
    
    if root is None:
        return list_key

    k = bst.get_key(root)

    if key_initial is None or k > key_initial:
        keys_range(root["left"], key_initial, key_final, list_key)

    if (key_initial is None or k >= key_initial) and (key_final is None or k <= key_final):
        sl.add_last(list_key, k)

    if key_final is None or k < key_final:
        keys_range(root["right"], key_initial, key_final, list_key)

    return list_key

def values(my_bst, key_initial, key_final):
    
    if key_initial is not None and key_final is not None and key_initial > key_final:
        
        key_initial, key_final = key_final, key_initial
        
    result = sl.new_list()
    
    return values_range(my_bst["root"], key_initial, key_final, result)


def values_range(root, key_initial, key_final, list_values):
    
    if root is None:
        return list_values

    k = bst.get_key(root)

    if key_initial is None or k > key_initial:
        values_range(root["left"], key_initial, key_final, list_values)

    if (key_initial is None or k >= key_initial) and (key_final is None or k <= key_final):
        sl.add_last(list_values, bst.get_value(root))

    if key_final is None or k < key_final:
        values_range(root["right"], key_initial, key_final, list_values)

    return list_values