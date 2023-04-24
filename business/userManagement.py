import subprocess
import zipfile
import passlib.hash
import os
import datetime
class User :
    def userExist(self,name, password) -> bool :
        shadowUser = subprocess.run(['sudo cat /etc/shadow | cut -d: -f1 | grep ' + name], capture_output= True, text= True,shell=True)
        #print(type(result.stdout.strip()))
        shadowPwd= subprocess.run(['sudo cat /etc/shadow | grep ' + name + ' | cut -d: -f2'], capture_output=True, text=True,shell=True).stdout.strip()
        #print(shadowPwd)
        hashed = passlib.hash(password)
        #print(hashed)
        if name == shadowUser.stdout.strip() and passlib.hash.verify(shadowPwd, hashed):
            print("v")
            return True
        return False
    
    def files(self, name) -> int:
        nbfiles = 0
        for root, dirs, files in os.walk('/home/' + name):
            nbfiles += len(files)
        return nbfiles

    def dirs(self, name) -> int:
        nbdirs = 0
        for root, dirs, files in os.walk('/home/' + name):
            nbdirs += len(dirs)
        return nbdirs
    
    def size(self, name):
        return subprocess.check_output(["sudo", "du", "-sh", '/home/' + name]).decode("utf-8").split()[0] #User().files(name) + User().dirs(name)

    def ls(self, name):
        dirs = []
        for d in os.listdir('/home/' + name):
            path = os.path.join('/home', name, d)
            size = os.path.getsize(path)
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)) 
            dirs.append((d, size, mtime))
        return dirs
    
    def cat(self, name):
        return subprocess.run(['cat '+'/home/' + name], capture_output= True, text= True,shell=True)
    
    def search(self, path, key):  
        print(path)
        fichiers = []
        for fichier in os.listdir('/home/'+path):
            if key and key not in fichier:
                continue
            fichiers.append(os.path.join(path, fichier))
        return fichiers
    
    def zip(self, user):
        home_dir = os.path.expanduser('/home/' + user)
        zip_filename = f'{user}_home.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(home_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, home_dir))

if __name__ == '__main__':
    user = '/home/ubuntu/Downloads/'
    #User().userExist("dev", "123")
    print(User().files('dev'))
    print(User().dirs('dev'))
    print(User().size('ubuntu'))
    #print(User().ls('ubuntu'))
    #print(User().cat('/home/ubuntu/Downloads/main.py'))
    User().zip('dev')
    #print(User().search('/home/ubuntu/Downloads', 'main'))
    #subprocess.run(["cat ", '/home/ubuntu/Downloads/main.py'], capture_output= True, text= True,shell=True)

    
