# -*- coding: UTF-8 -*-

import os

def files_searching(ext, wdir=os.getcwd()):
    for i in os.listdir(wdir):
        if os.path.splitext(i)[1] == ext:
            yield (os.path.join(wdir,i))