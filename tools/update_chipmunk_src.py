
import sys, os
import shutil

pymunk_src_path = "../chipmunk_src"

if len(sys.argv) > 1:
    chipmunk_svn_path = sys.argv[1]
else:
    chipmunk_svn_path = raw_input('Enter path to chipmunk source')

def copyfiles(basepath, subpath=""):
    path = os.path.join(basepath, subpath)
    for fn in os.listdir(path):
        fpath = os.path.join(path, fn)
        if os.path.isfile(fpath) and fn[-2:] in (".c", ".h"):
            dst = os.path.join(pymunk_src_path, subpath)
            shutil.copy(fpath, dst)
            
        elif os.path.isdir(fpath) and fn[0] != ".":
            copyfiles(basepath, os.path.join(subpath, fn))
        
            

copyfiles(os.path.join(chipmunk_svn_path, "src"))
copyfiles(chipmunk_svn_path, "include")

for (dirpath, x, fns) in os.walk(pymunk_src_path):
    for fn in fns:
        fpath = os.path.join(dirpath, fn)
        if os.path.isfile(fpath) and fn[-2:] == ".o":
            os.remove(fpath)
    
print "Remember to update svn version string of chipmunk!"
