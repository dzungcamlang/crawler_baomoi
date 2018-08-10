import os

DIR = 'data/'
fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print(fileCount)