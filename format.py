import re
with open('train_data.txt') as file, open('train_data1.txt' ,'w+') as file1:
    line = file.readline()
    for i in range(1,len(line)):
        file1.write(line[i])
        if line[i] == ']' and line[i-1] == ']':
            file1.write('\n')
    
