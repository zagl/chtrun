# -*- coding: utf-8 -*-

import os
from definitions import *
from Config import Config

def new():
    config = Config()
    
    if not os.path.exists(work_dir):
        template = get_template()
        work=template.cloneCase(work_dir)
        
    if not os.path.exists(geom_dir):
        os.makedirs(orig_dir)
