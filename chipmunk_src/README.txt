Chipmunk 6.2.0rev3bdf1b7b3c
                 
see http://chipmunk-physics.net/

  Compiling:

      $ gcc -O3 -std=gnu99 -ffast-math -DCHIPMUNK_FFI -c *.c constraints/*.c 
    or (you might need -fPIC as well, at least on 64bit)
      $ gcc -O3 -std=gnu99 -ffast-math -fPIC -DCHIPMUNK_FFI -c *.c constraints/*.c

   Linking:
    on Linux
      $ gcc -shared -o libchipmunk.so *.o
    (you might need -fPIC as well, at least on 64bit)
      $ gcc -shared -o -fPIC libchipmunk.so *.o
    or if you are on OSX
      $ gcc -dynamiclib -o libchipmunk.dylib *.o
    or if you are on Windows
      $ gcc -shared -o chipmunk.dll *.o


