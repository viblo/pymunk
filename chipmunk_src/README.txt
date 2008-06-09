Chipmunk rev 223
see http://wiki.slembcke.net/main/published/Chipmunk

  Compiling:

      $ gcc -O3 -std=gnu99 -ffast-math -c *.c
    or
      $ gcc -O3 -std=gnu99 -ffast-math -fPIC -c *.c

   Linking:
    on Linux
      $ gcc -shared -o chipmunk.so *.o
    or if you are on OSX
      $ gcc -dynamiclib -o libchipmunk.dylib *.o
      


