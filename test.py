#!/usr/bin/python3

import sys
import os
import json
import random
import time

start = time.time()

#print(f"Arguments of the script : {sys.argv[1:]=}")

data = {}
data['version'] = sys.argv[4]
data['accuracy'] = random.random() * 100

#Reference: http://www.easypythondocs.com/random.html

end = time.time()
data['test_time'] = end - start

#json_data = json.dumps(data)
json.dump(data, sys.stdout, indent=4)
