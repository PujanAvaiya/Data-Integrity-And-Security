import os
from datetime import datetime
path = 'C:/Users/pujan/PycharmProjects/untitled'
for root, dirs, filenames in os.walk(path):
 for filename in filenames:
      filename = os.path.join(root, filename)
      lastmodified = os.stat(filename).st_mtime
      print(filename)
      print(datetime.fromtimestamp(lastmodified))
