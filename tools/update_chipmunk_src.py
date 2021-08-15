import subprocess

subprocess.call(f"git submodule update --remote ../Chipmunk2D", shell=True)
subprocess.call(f"git submodule status ../Chipmunk2D", shell=True)

print(
    """
Remember to update git version string of chipmunk! At least these files:
    pymunk/_version.py
    README.rst
    """
)
