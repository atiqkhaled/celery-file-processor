import os.path
import shutil
from app_config import LOCAL_DESTINATION_DIR        
        
class LocalStorageHandler():
    def upload(self, file):
        des = LOCAL_DESTINATION_DIR
        if not os.path.isdir(des):
           os.mkdir(des)
        shutil.move(file, des)
        ## If file exists, delete it ##
        if os.path.isfile(file):
          os.remove(file)
        print('upload done')  
        
    def download(self,file):
        return 'read file from local storage' 