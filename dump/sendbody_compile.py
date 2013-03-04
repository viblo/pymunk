
import os

#os.system("gcc -mrtd -O3 -shared -fno-omit-frame-pointer -std=gnu99 -fPIC -ffast-math  -c ex.c")
os.system("gcc -mrtd -shared -fno-omit-frame-pointer -std=gnu99 -fPIC -ffast-math -I../chipmunk_src/include/chipmunk -c sendbody.c -o sendbody.o")
#os.system("gcc -dynamiclib ex.o -o libex.dylib")
os.system("gcc -shared -mrtd -s sendbody.o -o sendbody.dll")
