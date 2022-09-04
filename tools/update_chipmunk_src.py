import subprocess

subprocess.call("git submodule update --remote ../Chipmunk2D", shell=True)
subprocess.call("git submodule status ../Chipmunk2D", shell=True)

print(
    """
Remember to update git version string of chipmunk! At least these files:
    pymunk/_version.py
    README.rst
    """
)
