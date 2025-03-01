def appendFile(path, content):
    file = open(path, 'a') 
    file.write(content) 
    file.close()