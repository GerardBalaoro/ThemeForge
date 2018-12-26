import os

for root, dirs, files in os.walk('.'):
    for folder in dirs[1]:
        print(folder)