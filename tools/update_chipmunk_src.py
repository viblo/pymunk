
import sys, os.path
import subprocess
import shutil

pymunk_src_path = os.path.join("..", "chipmunk_src")

shutil.rmtree(os.path.join(pymunk_src_path, "src"), True)
shutil.rmtree(os.path.join(pymunk_src_path, "include"), True)

if len(sys.argv) > 1:
    chipmunk_git_path = sys.argv[1]
else:
    chipmunk_git_path = input("Enter path to chipmunk source")

shutil.copytree(os.path.join(chipmunk_git_path,"src"), os.path.join(pymunk_src_path,"src"))    
shutil.copytree(os.path.join(chipmunk_git_path,"include"), os.path.join(pymunk_src_path,"include"))    

print("Git hash")
subprocess.call(f"git -C {chipmunk_git_path} rev-parse HEAD", shell=True)
print("Changes not commited (if changes, do not trust git hash!):")
subprocess.call(f"git -C {chipmunk_git_path} status --porcelain", shell=True)

print("""
Remember to update git version string of chipmunk! At least these files:
    chipmunk_src/README.txt
    pymunk/__init__.py
    README.rst
    """)
    

