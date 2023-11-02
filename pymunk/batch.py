"""The batch module contain functions to efficiently get batched space data. 

.. note:: 
    This module is highly experimental and will likely change in future Pymunk 
    verisons including major, minor and patch verisons! 


First create space and two bodies.

>>> import pymunk, pymunk.batch
>>> s = pymunk.Space()
>>> b1 = pymunk.Body(1, 1)
>>> b1.position = 1,2
>>> s.add(b1, pymunk.Circle(b1, 4))
>>> b2 = pymunk.Body(1,1)
>>> b2.position = 3,4
>>> s.add(b2, pymunk.Circle(b2, 4))

To get data out first create a Buffer holder object, which is used to reuse
the underlying arrays between calls. Then call the batch method. Note that 
the fields on the body to extract need to be specified explicitly.

>>> data = pymunk.batch.Buffer()
>>> pymunk.batch.get_space_bodies(
...     s,
...     pymunk.batch.BodyFields.BODY_ID | pymunk.batch.BodyFields.POSITION,
...     data,
... )

The data is available in the Buffer object as cffi buffers. One that 
contains any int data, and one that contains floating point data. You can 
either use it directly like here, but also pass it in to 3rd parties that 
implements the buffer protocol like numpy arrays.

>>> list(memoryview(data.int_buf()).cast("P")) == [b1.id, b2.id]
True
>>> list(memoryview(data.float_buf()).cast("d"))
[1.0, 2.0, 3.0, 4.0]

Its also possible to get the arbiters with collision data. Note that we need
to call step to run the simulation, and clear the data data buffers first so 
they can be reused:

>>> s.step(1)
>>> data.clear()
>>> pymunk.batch.get_space_arbiters(
...     s,
...     pymunk.batch.ArbiterFields.BODY_A_ID | pymunk.batch.ArbiterFields.BODY_B_ID,
...     data,
... )
>>> list(memoryview(data.int_buf()).cast("P")) == [b2.id, b1.id]
True
>>> list(memoryview(data.float_buf()).cast("d"))
[]

"""
__docformat__ = "reStructuredText"

__all__ = [
    "BodyFields",
    "ArbiterFields",
    "Buffer",
    "get_space_bodies",
    "get_space_arbiters",
]

from enum import Flag

from ._chipmunk_cffi import ffi, lib
from .space import Space


class BodyFields(Flag):
    """Flag fields to specify body properties to get."""

    BODY_ID = lib.BODY_ID
    """:py:attr:`pymunk.Body.id`. Value stored in int_buf."""
    POSITION = lib.POSITION
    """:py:attr:`pymunk.Body.position`. X and Y stored in float_buf."""
    ANGLE = lib.ANGLE
    """:py:attr:`pymunk.Body.angle`. Value stored in float_buf."""
    VELOCITY = lib.VELOCITY
    """:py:attr:`pymunk.Body.velocity`. X and Y stored in float_buf."""
    ANGULAR_VELOCITY = lib.ANGULAR_VELOCITY
    """:py:attr:`pymunk.Body.angular_velocity`. X and Y stored in float_buf"""

    ALL = 0xFFFF
    """All the fields"""


class ArbiterFields(Flag):
    """Flag fields to specify arbiter properties to get."""

    BODY_A_ID = lib.BODY_A_ID
    """:py:attr:`pymunk.Body.id` of body A. Value stored in int_buf."""
    BODY_B_ID = lib.BODY_B_ID
    """:py:attr:`pymunk.Body.id` of body B. Value stored in int_buf."""
    TOTAL_IMPULSE = lib.TOTAL_IMPULSE
    """:py:attr:`pymunk.Arbiter.total_impulse`. X and Y stored in float_buf."""
    TOTAL_KE = lib.TOTAL_KE
    """:py:attr:`pymunk.Arbiter.total_ke`. Value stored in float_buf."""
    IS_FIRST_CONTACT = lib.IS_FIRST_CONTACT
    """:py:attr:`pymunk.Arbiter.is_first_contact`. Value (0 or 1) stored in int_buf."""
    NORMAL = lib.NORMAL
    """:py:attr:`pymunk.Arbiter.normal`. X and Y stored in float_buf."""

    CONTACT_COUNT = lib.CONTACT_COUNT
    """Number of contacts (1 or 2)`. Value stored in int_buf."""

    POINT_A_1 = lib.POINT_A_1
    """:py:attr:`pymunk.ContactPoint.point_a` of contact 1. X and Y stored in float_buf."""
    POINT_B_1 = lib.POINT_B_1
    """:py:attr:`pymunk.ContactPoint.point_b` of contact 1. X and Y stored in float_buf."""
    DISTANCE_1 = lib.DISTANCE_1
    """:py:attr:`pymunk.ContactPoint.distance` of contact 1. Value stored in float_buf."""

    POINT_A_2 = lib.POINT_A_2
    """:py:attr:`pymunk.ContactPoint.point_a` of contact 2. X and Y stored in float_buf."""
    POINT_B_2 = lib.POINT_B_2
    """:py:attr:`pymunk.ContactPoint.point_b` of contact 2. X and Y stored in float_buf."""
    DISTANCE_2 = lib.DISTANCE_2
    """:py:attr:`pymunk.ContactPoint.distance` of contact 2. Value stored in float_buf."""
    ALL = 0xFFFF
    """All the fields"""


class Buffer(object):
    _int_arr: ffi.CData = None
    _float_arr: ffi.CData = None

    def __init__(self) -> None:
        """Create a empty BatchData object."""
        self._float_arr = lib.pmFloatArrayNew(0)
        self._int_arr = lib.pmIntArrayNew(0)

    def clear(self) -> None:
        """Mark the internal arrays empty (for reuse).

        It is more efficient to reuse the BatchedData object and its internal
        arrays by calling clear, than to create a new object each step.
        """
        self._float_arr.num = 0
        self._int_arr.num = 0

    def float_buf(self) -> ffi.buffer:
        """Return a CFFI buffer object of the floating point data in the
        internal array.

        """
        return ffi.buffer(
            self._float_arr.arr, ffi.sizeof("cpFloat") * self._float_arr.num
        )

    def int_buf(self) -> ffi.buffer:
        """Return a CFFI buffer object of the integer data in the internal
        array.

        """
        return ffi.buffer(
            self._int_arr.arr, ffi.sizeof("uintptr_t") * self._int_arr.num
        )


def get_space_bodies(space: Space, fields: BodyFields, buffers: Buffer) -> None:
    """Get data for all bodies in the space.

    Filter out the fields you are interested in with the fields property.

    The data is returned in the batched_data buffers.
    """
    _data = ffi.new("pmBatchedData *")
    _data.fields = fields.value
    _data.floatArray = buffers._float_arr
    _data.intArray = buffers._int_arr

    lib.cpSpaceEachBody(
        space._space,
        ffi.addressof(lib, "pmSpaceBodyIteratorFuncBatched"),
        _data,
    )


def get_space_arbiters(space: Space, fields: ArbiterFields, buffers: Buffer) -> None:
    """Get data for all active arbiters in the space.

    Filter out the fields you are interested in with the fields property.

    The data is returned in the batched_data buffers.
    """
    _data = ffi.new("pmBatchedData *")
    _data.fields = fields.value
    _data.floatArray = buffers._float_arr
    _data.intArray = buffers._int_arr

    lib.cpSpaceEachCachedArbiter(
        space._space,
        ffi.addressof(lib, "pmSpaceArbiterIteratorFuncBatched"),
        _data,
    )
