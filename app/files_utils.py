import os   
import shutil

def appendFile(path, content):
    file = open(path, 'a') 
    file.write(content) 
    file.close()
    
def writeFile(path, content):
    file = open(path, 'w') 
    file.write(content) 
    file.close()
    
def removeFile(path):
    if os.path.exists(path):
        os.remove(path)
    
def concatFiles(path, concat_paths):
    print("AAAAAAAAAAAAA")
    print(path, concat_paths)
    with open(path, "wb") as outfile:
        for file in concat_paths:
            with open(file, "rb") as infile:
                shutil.copyfileobj(infile, outfile)