
import os

src = """C:\code\gh\pymunk\chipmunk_src\src\*.c"""
include = """C:\code\gh\pymunk\chipmunk_src\include"""

options = [
    "/LD",
    "/TP",
    "/DWIN32" "/D_LIB",
    "/D_CRT_SECURE_NO_WARNINGS",
    "/DCHIPMUNK_VERSION_MAJOR=7",
    "/DCHIPMUNK_VERSION_MINOR=0",
    "/DCHIPMUNK_VERSION_PATCH=0",
    f"/I {include}",
]


cl = """C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\cl.exe"""
cl = "cl.exe"
s = f"{cl} " + " ".join(options) + " " + src

os.system(s)

#os.system("gcc -mrtd -O3 -shared -fno-omit-frame-pointer -std=gnu99 -fPIC -ffast-math -m32 -c ex.c")
#os.system("gcc -O1 -std=gnu99 -fPIC -ffast-math -c ex.c")
#os.system("gcc -dynamiclib ex.o -o libex.dylib")
#os.system("gcc -shared -mrtd ex.o -o ex.dll")
