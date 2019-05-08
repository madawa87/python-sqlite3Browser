# -*- coding: utf-8 -*-
"""
@author: Jayalath A M Madawa Abeywardhana
"""

import os
import sys
import re
import json
import string

class config():

    def __init__(self):
        self.runParams = {}
        cur_dir = os.getcwd()
