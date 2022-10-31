import math

from . import _chipmunk_cffi

cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi

from .contact_point_set import ContactPointSet
from .query_info import PointQueryInfo, SegmentQueryInfo, ShapeQueryInfo
from .vec2d import Vec2d

# Space query callbacks


@ffi.def_extern()
def ext_cpSpacePointQueryFunc(_shape, point, distance, gradient, data):  # type: ignore
    self, query_hits = ffi.from_handle(data)
    shape = self._get_shape(_shape)
    p = PointQueryInfo(
        shape, Vec2d(point.x, point.y), distance, Vec2d(gradient.x, gradient.y)
    )
    query_hits.append(p)


@ffi.def_extern()
def ext_cpSpaceSegmentQueryFunc(_shape, point, normal, alpha, data):  # type: ignore
    self, query_hits = ffi.from_handle(data)
    shape = self._get_shape(_shape)
    p = SegmentQueryInfo(
        shape, Vec2d(point.x, point.y), Vec2d(normal.x, normal.y), alpha
    )
    query_hits.append(p)


@ffi.def_extern()
def ext_cpSpaceBBQueryFunc(_shape, data):  # type: ignore
    self, query_hits = ffi.from_handle(data)
    shape = self._get_shape(_shape)
    assert shape is not None
    query_hits.append(shape)


@ffi.def_extern()
def ext_cpSpaceShapeQueryFunc(_shape, _points, data):  # type: ignore
    self, query_hits = ffi.from_handle(data)
    found_shape = self._get_shape(_shape)
    point_set = ContactPointSet._from_cp(_points)
    info = ShapeQueryInfo(found_shape, point_set)
    query_hits.append(info)


# debug draw callbacks


@ffi.def_extern()
def ext_cpSpaceDebugDrawCircleImpl(pos, angle, radius, outline_color, fill_color, data):  # type: ignore
    options, _ = ffi.from_handle(data)
    options.draw_circle(
        Vec2d(pos.x, pos.y),
        angle,
        radius,
        options._c(outline_color),
        options._c(fill_color),
    )


@ffi.def_extern()
def ext_cpSpaceDebugDrawSegmentImpl(a, b, color, data):  # type: ignore
    # sometimes a and/or b can be nan. For example if both endpoints
    # of a spring is at the same position. In those cases skip calling
    # the drawing method.
    if math.isnan(a.x) or math.isnan(a.y) or math.isnan(b.x) or math.isnan(b.y):
        return
    options, _ = ffi.from_handle(data)
    options.draw_segment(
        Vec2d(a.x, a.y),
        Vec2d(b.x, b.y),
        options._c(color),
    )


@ffi.def_extern()
def ext_cpSpaceDebugDrawFatSegmentImpl(a, b, radius, outline_color, fill_color, data):  # type: ignore
    options, _ = ffi.from_handle(data)
    options.draw_fat_segment(
        Vec2d(a.x, a.y),
        Vec2d(b.x, b.y),
        radius,
        options._c(outline_color),
        options._c(fill_color),
    )


@ffi.def_extern()
def ext_cpSpaceDebugDrawPolygonImpl(count, verts, radius, outline_color, fill_color, data):  # type: ignore
    options, _ = ffi.from_handle(data)
    vs = []
    for i in range(count):
        vs.append(Vec2d(verts[i].x, verts[i].y))
    options.draw_polygon(vs, radius, options._c(outline_color), options._c(fill_color))


@ffi.def_extern()
def ext_cpSpaceDebugDrawDotImpl(size, pos, color, data):  # type: ignore
    options, _ = ffi.from_handle(data)
    options.draw_dot(size, Vec2d(pos.x, pos.y), options._c(color))


@ffi.def_extern()
def ext_cpSpaceDebugDrawColorForShapeImpl(_shape, data):  # type: ignore
    options, space = ffi.from_handle(data)
    shape = space._get_shape(_shape)
    return options.color_for_shape(shape)
