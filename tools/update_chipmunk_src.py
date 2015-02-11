
import sys, os.path
import subprocess
import shutil

pymunk_src_path = os.path.join("..", "chipmunk_src")

shutil.rmtree(os.path.join(pymunk_src_path, "src"), True)
shutil.rmtree(os.path.join(pymunk_src_path, "include"), True)

if len(sys.argv) > 1:
    chipmunk_git_path = sys.argv[1]
else:
    chipmunk_git_path = raw_input("Enter path to chipmunk source")

shutil.copytree(os.path.join(chipmunk_git_path,"src"), os.path.join(pymunk_src_path,"src"))    
shutil.copytree(os.path.join(chipmunk_git_path,"include"), os.path.join(pymunk_src_path,"include"))    

subprocess.call("git rev-parse HEAD", shell=True)

print("Remember to update git version string of chipmunk!")
