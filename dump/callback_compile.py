import os

os.system("gcc -mrtd -O3 -shared -fno-omit-frame-pointer -std=gnu99 -fPIC -ffast-math -m32 -c callback.c")
#os.system("gcc -O1 -std=gnu99 -fPIC -ffast-math -c callback.c")
#os.system("gcc -dynamiclib ex.o -o libex.dylib")
os.system("gcc -shared -mrtd callback.o -o callback.dll")
