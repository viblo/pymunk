=========
Threading
=========

Pymunk supports being imported and used on free-threaded CPython builds.

Individual Pymunk objects are not thread safe. Do not access the same
``Space``, ``Body``, ``Shape``, ``Constraint``, or callback data from multiple
threads at the same time unless you protect that access with your own locks.
This includes concurrent reads if another thread might mutate or destroy the
same object.

It is expected to be safe to use separate ``Space`` instances from separate
threads, as long as those spaces and the objects attached to them are not shared
between threads.
