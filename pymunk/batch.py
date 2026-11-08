"""The batch module contain functions to efficiently get and set space data in
   a batch instead of one by one.

.. note::
    This module is highly experimental and will likely change in future Pymunk
    verisons including major, minor and patch verisons!


To get data out
===============

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


Layouts and setting data
========================

Query the layout instead of hardcoding column indices. Offsets and strides
are in elements, separately for each buffer:

>>> flags = BodyFields.POSITION | BodyFields.ANGLE
>>> layout = get_body_layout(flags)
>>> layout[BodyFields.ANGLE].offset, layout[BodyFields.POSITION].offset
(0, 1)
>>> layout.float_stride, layout.int_stride
(3, 0)
>>> layout[BodyFields.POSITION].size
2

A float record is now [angle, x, y], not [x, y, angle]. Only selections
containing both ANGLE and POSITION change relative ordering; flag values are
unchanged. This is a breaking format change to the experimental batch API.
Saved raw buffers and hardcoded column indices using the old layout must be
migrated; do not share raw buffers between different Pymunk versions.

For example, build records using the queried offsets:

>>> import array
>>> records = array.array("d", [0.0] * (2 * layout.float_stride))
>>> for row, (angle, x, y) in enumerate(((0.5, 5, 6), (1.0, 7, 8))):
...     base = row * layout.float_stride
...     records[base + layout[BodyFields.ANGLE].offset] = angle
...     p = base + layout[BodyFields.POSITION].offset
...     records[p:p + 2] = array.array("d", [x, y])
>>> updates = Buffer()
>>> updates.set_float_buf(records)
>>> set_space_bodies(s, flags, updates)
>>> b1.angle, tuple(b1.position), b2.angle, tuple(b2.position)
(0.5, (5.0, 6.0), 1.0, (7.0, 8.0))

The example uses doubles, as in the standard Pymunk build. Layout item sizes
are available for consumers of other buffer formats. Record indices follow
native iteration order, not IDs; adding/removing bodies can change that order.
See also the NumPy example in planet.py.


"""

__docformat__ = "reStructuredText"

__all__ = [
    "ArbiterFields",
    "BodyFields",
    "Buffer",
    "FieldLayout",
    "Layout",
    "get_body_layout",
    "get_arbiter_layout",
    "set_space_bodies",
    "get_space_arbiters",
    "get_space_bodies",
]

from dataclasses import dataclass
from enum import Flag
from functools import lru_cache
from typing import Any, Literal, Union

from ._chipmunk_cffi import ffi, lib
from .space import Space


class BodyFields(Flag):
    """Flag fields to specify body properties to get."""

    BODY_ID = lib.BODY_ID
    """:py:attr:`pymunk.Body.id`. Value stored in int_buf."""
    ANGLE = lib.ANGLE
    """:py:attr:`pymunk.Body.angle`. Value stored in float_buf."""
    POSITION = lib.POSITION
    """:py:attr:`pymunk.Body.position`. X and Y stored in float_buf."""
    VELOCITY = lib.VELOCITY
    """:py:attr:`pymunk.Body.velocity`. X and Y stored in float_buf."""
    ANGULAR_VELOCITY = lib.ANGULAR_VELOCITY
    """:py:attr:`pymunk.Body.angular_velocity`. Value stored in float_buf"""
    FORCE = lib.FORCE
    """:py:attr:`pymunk.Body.force`. X and Y stored in float_buf."""
    TORQUE = lib.TORQUE
    """:py:attr:`pymunk.Body.torque`. Value stored in float_buf"""
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


@dataclass(frozen=True)
class FieldLayout:
    """Location of one selected field within a batch record.

    ``buffer`` is ``"float"`` or ``"int"``. ``offset`` and ``size`` are in
    scalar elements of that buffer, not bytes. Vector components are X, Y.
    """

    field: Union[BodyFields, ArbiterFields]
    buffer: Literal["float", "int"]
    offset: int
    size: int


@dataclass(frozen=True)
class Layout:
    """Immutable description of records in the two separate batch buffers.

    ``fields`` lists the selected fields in native packing order. Each buffer
    contains consecutive records, without padding. ``float_stride`` and
    ``int_stride`` are elements per record; multiply by the corresponding
    itemsize for bytes. Float elements have C type ``cpFloat``; integer
    elements have C type ``uintptr_t`` (including IDs and boolean values).

    A layout describes fields, not body/arbiter iteration order. Do not assume
    record indices remain stable after changes to the space. Layouts and raw
    buffers should not be assumed compatible across Pymunk versions.
    """

    fields: tuple[FieldLayout, ...]
    float_stride: int
    int_stride: int
    float_itemsize: int
    int_itemsize: int

    def __getitem__(self, field: Union[BodyFields, ArbiterFields]) -> FieldLayout:
        """Return the descriptor for one selected field, or raise KeyError."""
        for entry in self.fields:
            if entry.field == field:
                return entry
        raise KeyError(field)


# Explicit packing order, independent of numeric flag values. Keep these
# tables in sync with the native iterators in pymunk_cffi/extensions.c.
_BODY_LAYOUT = (
    (BodyFields.BODY_ID, "int", 1),
    (BodyFields.ANGLE, "float", 1),
    (BodyFields.POSITION, "float", 2),
    (BodyFields.VELOCITY, "float", 2),
    (BodyFields.ANGULAR_VELOCITY, "float", 1),
    (BodyFields.FORCE, "float", 2),
    (BodyFields.TORQUE, "float", 1),
)
_ARBITER_LAYOUT = (
    (ArbiterFields.BODY_A_ID, "int", 1),
    (ArbiterFields.BODY_B_ID, "int", 1),
    (ArbiterFields.TOTAL_IMPULSE, "float", 2),
    (ArbiterFields.TOTAL_KE, "float", 1),
    (ArbiterFields.IS_FIRST_CONTACT, "int", 1),
    (ArbiterFields.NORMAL, "float", 2),
    (ArbiterFields.CONTACT_COUNT, "int", 1),
    (ArbiterFields.POINT_A_1, "float", 2),
    (ArbiterFields.POINT_B_1, "float", 2),
    (ArbiterFields.DISTANCE_1, "float", 1),
    (ArbiterFields.POINT_A_2, "float", 2),
    (ArbiterFields.POINT_B_2, "float", 2),
    (ArbiterFields.DISTANCE_2, "float", 1),
)


def _make_layout(
    fields: Union[BodyFields, ArbiterFields],
    spec: tuple[tuple[Any, str, int], ...],
) -> Layout:
    offsets = {"float": 0, "int": 0}
    entries = []
    for field, buffer, size in spec:
        if field in fields:
            # The tables above contain only the two supported buffer names.
            kind: Literal["float", "int"] = "float" if buffer == "float" else "int"
            entries.append(FieldLayout(field, kind, offsets[kind], size))
            offsets[kind] += size
    return Layout(
        tuple(entries),
        offsets["float"],
        offsets["int"],
        ffi.sizeof("cpFloat"),
        ffi.sizeof("uintptr_t"),
    )


@lru_cache(maxsize=128)
def get_body_layout(fields: BodyFields) -> Layout:
    """Describe body records for exactly the selected flags.

    Packing order is BODY_ID (integer buffer), then ANGLE, POSITION, VELOCITY,
    ANGULAR_VELOCITY, FORCE, TORQUE (float buffer). Unselected fields take no
    space. Flag numeric values do not define packing order. ``ALL`` selects
    every supported field; ``BodyFields(0)`` gives zero strides. Reserved bits
    are ignored, matching the native batch functions.

    The setter uses the same float layout, but ignores BODY_ID and the entire
    integer buffer: it updates bodies in native iteration order, not by ID.
    Query once and reuse the result; batch get/set functions do not call this.
    """
    if not isinstance(fields, BodyFields):
        raise TypeError("fields must be BodyFields")
    return _make_layout(fields, _BODY_LAYOUT)


@lru_cache(maxsize=128)
def get_arbiter_layout(fields: ArbiterFields) -> Layout:
    """Describe arbiter records for exactly the selected flags.

    Fields follow the order listed in ArbiterFields, with separate offsets
    for the integer and float buffers. ``ALL`` selects every supported field;
    ``ArbiterFields(0)`` gives zero strides. Reserved bits are ignored, matching
    the native batch function. Missing contacts retain their selected slots,
    filled with zeros; consult CONTACT_COUNT to distinguish them.
    """
    if not isinstance(fields, ArbiterFields):
        raise TypeError("fields must be ArbiterFields")
    return _make_layout(fields, _ARBITER_LAYOUT)


class Buffer:
    _int_arr: ffi.CData = None
    _float_arr: ffi.CData = None

    def __init__(self) -> None:
        """Create a empty BatchData object."""
        self._float_arr = lib.pmFloatArrayNew(0)
        self._int_arr = lib.pmIntArrayNew(0)

        self._int_buf = None

        self._float_buf = None

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
        arr = self._float_buf
        if arr is None:
            arr = self._float_arr.arr
        return ffi.buffer(arr, ffi.sizeof("cpFloat") * self._float_arr.num)

    def set_float_buf(self, buffer: Any) -> None:
        """Set the floating point internal data to the supplied buffer.

        buffer should be an array of floats, implmenting the buffer/memoryview
        interface like a numpy array or array.array.

        The storage stays exported while this Buffer or a returned view uses it.
        Its elements can be changed, but it must not be resized. On CPython,
        resizing is blocked until those exports are released.

        (From Python 3.12 the buffer argument will be typed as
        collections.abc.Buffer)

        """
        arr = ffi.from_buffer("cpFloat[]", buffer)
        self._float_buf = arr
        self._float_arr.arr = arr
        self._float_arr.max = len(arr)
        self._float_arr.num = len(arr)

    def int_buf(self) -> ffi.buffer:
        """Return a CFFI buffer object of the integer data in the internal
        array.

        """
        arr = self._int_buf
        if arr is None:
            arr = self._int_arr.arr
        return ffi.buffer(arr, ffi.sizeof("uintptr_t") * self._int_arr.num)

    def set_int_buf(self, buffer: Any) -> None:
        """Set the integer internal data to the supplied buffer.

        buffer should be an array of ints, implmenting the buffer/memoryview
        interface like a numpy array or array.array.

        The storage stays exported while this Buffer or a returned view uses it.
        Its elements can be changed, but it must not be resized. On CPython,
        resizing is blocked until those exports are released.

        (From Python 3.12 the buffer argument will be typed as
        collections.abc.Buffer)
        """
        arr = ffi.from_buffer("uintptr_t[]", buffer)
        self._int_buf = arr
        self._int_arr.arr = arr
        self._int_arr.max = len(arr)
        self._int_arr.num = len(arr)


def get_space_bodies(space: Space, fields: BodyFields, buffers: Buffer) -> None:
    """Get data for all bodies in the space.

    Filter out the fields you are interested in with the fields property.

    The data is appended to the buffers. Call Buffer.clear() before reuse
    unless appending is intended. See :func:`get_body_layout` for packing order.
    """
    _data = ffi.new("pmBatchedData *")
    _data.fields = fields.value
    _data.floatArray = buffers._float_arr
    _data.intArray = buffers._int_arr

    lib.cpSpaceEachBody(
        space._space,
        ffi.addressof(lib, "pmSpaceBodyGetIteratorFuncBatched"),
        _data,
    )


def set_space_bodies(space: Space, fields: BodyFields, buffers: Buffer) -> None:
    """Set data for all bodies in the space.

    Filter out the fields you want to set with the fields property.

    The data to update is passed in the batched_data buffers.

    The float buffer follows :func:`get_body_layout`. BODY_ID and the integer
    buffer are ignored; records are applied in native body iteration order,
    not matched by ID.
    """
    _data = ffi.new("pmBatchedData *")
    _data.fields = fields.value
    _data.floatArray = buffers._float_arr
    _data.intArray = buffers._int_arr

    # To iterate from the beginning of the array, num should start at 0
    orig_float_num = buffers._float_arr.num
    buffers._float_arr.num = 0

    lib.cpSpaceEachBody(
        space._space,
        ffi.addressof(lib, "pmSpaceBodySetIteratorFuncBatched"),
        _data,
    )

    buffers._float_arr.num = orig_float_num


def get_space_arbiters(space: Space, fields: ArbiterFields, buffers: Buffer) -> None:
    """Get data for all active arbiters in the space.

    Filter out the fields you are interested in with the fields property.

    The data is appended to the buffers. Call Buffer.clear() before reuse
    unless appending is intended. See :func:`get_arbiter_layout` for packing order.
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
