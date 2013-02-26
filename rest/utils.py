# -*- coding: utf-8 -*-
import inspect

def get_argument_names_for_a_function(f):
    '''This method returns all arguments of a function taking into
    account that the function might be wrapped into decorators.

    I'm not 100% sure that using func_closure is portable across different
    python implementations, but it works with standard CPython 2.7. 
    '''
    # 1. unwind decorators
    current_layer = f.im_func
    while current_layer.func_closure:
        current_layer = current_layer.func_closure[0].cell_contents

    # 2. get arg names
    return inspect.getargspec(current_layer).args
