import os, os.path
print(len([name for name in os.listdir('.') if os.path.isfile(name)]))