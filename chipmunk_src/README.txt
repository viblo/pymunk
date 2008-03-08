Chipmunk 4.0.2

  Compiling:

      $ gcc -O3 -std=gnu99 -ffast-math -c *.c
    or
      $ gcc -O3 -std=gnu99 -ffast-math -fPIC -c *.c

   Linking:

      $ gcc -shared -o chipmunk.so *.o


  OS X: There is an included XCode project file for building the
  static library and demo application. Alteratively you could use the
  CMake files. 

  To build run 'cmake .' then 'make'. This should build a dynamic 
  library, a static library, and the demo application.
  
  http://files.slembcke.net/chipmunk/release/ChipmunkLatest.tgz
