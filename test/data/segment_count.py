import sys
import os

from utils import file_helper_functions as fhf

def test():
    test = {}
    test['hello'] = "bla"
    x = fhf.dict_to_array(test)
    print(x)


if __name__ == "__main__":
    test()
