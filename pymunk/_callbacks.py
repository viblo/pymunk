import logging
import math
import warnings

from ._chipmunk_cffi import ffi, lib
from .arbiter import Arbiter
from .contact_point_set import ContactPointSet
from .query_info import PointQueryInfo, SegmentQueryInfo, ShapeQueryInfo
from .vec2d import Vec2d

_logger = logging.getLogger(__name__)

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


# space iterator funcs


@ffi.def_extern()
def ext_cpSpaceShapeIteratorFunc(cp_shape, data):  # type: ignore
    cp_shapes = ffi.from_handle(data)
    cp_shapes.append(cp_shape)


@ffi.def_extern()
def ext_cpSpaceConstraintIteratorFunc(cp_constraint, data):  # type: ignore
    cp_constraints = ffi.from_handle(data)
    cp_constraints.append(cp_constraint)


@ffi.def_extern()
def ext_cpSpaceBodyIteratorFunc(cp_body, data):  # type:ignore
    cp_bodys = ffi.from_handle(data)
    cp_bodys.append(cp_body)


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


# autogeometry.py


@ffi.def_extern()
def ext_cpMarchSegmentFunc(v0: ffi.CData, v1: ffi.CData, data: ffi.CData) -> None:
    pl_set = ffi.from_handle(data)
    pl_set.collect_segment((v0.x, v0.y), (v1.x, v1.y))


@ffi.def_extern()
def ext_cpMarchSampleFunc(point: ffi.CData, data: ffi.CData) -> float:
    # print("SAMPLE", point.x, point.y)
    sample_func = ffi.from_handle(data)
    return sample_func((point.x, point.y))


# collision_handler.py


@ffi.def_extern()
def ext_cpCollisionBeginFunc(
    _arb: ffi.CData, _space: ffi.CData, data: ffi.CData
) -> bool:
    handler = ffi.from_handle(data)
    x = handler._begin(Arbiter(_arb, handler._space), handler._space, handler.data)
    if isinstance(x, bool):
        return x

    func_name = handler._begin.__code__.co_name
    filename = handler._begin.__code__.co_filename
    lineno = handler._begin.__code__.co_firstlineno

    warnings.warn_explicit(
        "Function '" + func_name + "' should return a bool to"
        " indicate if the collision should be processed or not when"
        " used as 'begin' or 'pre_solve' collision callback.",
        UserWarning,
        filename,
        lineno,
        handler._begin.__module__,
    )
    return True


@ffi.def_extern()
def ext_cpCollisionPreSolveFunc(
    _arb: ffi.CData, _space: ffi.CData, data: ffi.CData
) -> bool:
    handler = ffi.from_handle(data)
    x = handler._pre_solve(Arbiter(_arb, handler._space), handler._space, handler.data)
    if isinstance(x, bool):
        return x

    func_name = handler._pre_solve.__code__.co_name
    filename = handler._pre_solve.__code__.co_filename
    lineno = handler._pre_solve.__code__.co_firstlineno

    warnings.warn_explicit(
        "Function '" + func_name + "' should return a bool to"
        " indicate if the collision should be processed or not when"
        " used as 'begin' or 'pre_solve' collision callback.",
        UserWarning,
        filename,
        lineno,
        handler._pre_solve.__module__,
    )
    return True


@ffi.def_extern()
def ext_cpCollisionPostSolveFunc(
    _arb: ffi.CData, _space: ffi.CData, data: ffi.CData
) -> None:
    handler = ffi.from_handle(data)
    handler._post_solve(Arbiter(_arb, handler._space), handler._space, handler.data)


@ffi.def_extern()
def ext_cpCollisionSeparateFunc(
    _arb: ffi.CData, _space: ffi.CData, data: ffi.CData
) -> None:
    handler = ffi.from_handle(data)
    try:
        # this try is needed since a separate callback will be called
        # if a colliding object is removed, regardless if its in a
        # step or not.
        handler._space._locked = True
        handler._separate(Arbiter(_arb, handler._space), handler._space, handler.data)
    finally:
        handler._space._locked = False


# body.py
@ffi.def_extern()
def ext_cpBodyPositionFunc(_body: ffi.CData, dt: float) -> None:
    body = ffi.from_handle(lib.cpBodyGetUserData(_body))
    body._position_func(body, dt)


@ffi.def_extern()
def ext_cpBodyVelocityFunc(
    _body: ffi.CData, gravity: ffi.CData, damping: float, dt: float
) -> None:
    body = ffi.from_handle(lib.cpBodyGetUserData(_body))
    body._velocity_func(body, Vec2d(gravity.x, gravity.y), damping, dt)


@ffi.def_extern()
def ext_cpBodyArbiterIteratorFunc(
    _body: ffi.CData, _arbiter: ffi.CData, data: ffi.CData
) -> None:
    body, func, args, kwargs = ffi.from_handle(data)
    assert body._space is not None
    arbiter = Arbiter(_arbiter, body._space)
    func(arbiter, *args, **kwargs)


@ffi.def_extern()
def ext_cpBodyConstraintIteratorFunc(
    cp_body: ffi.CData, cp_constraint: ffi.CData, _: ffi.CData
) -> None:
    _logger.debug("bodyfree remove constraint %s %s", cp_body, cp_constraint)
    cp_space = lib.cpConstraintGetSpace(cp_constraint)
    if cp_space != ffi.NULL:
        lib.cpSpaceRemoveConstraint(cp_space, cp_constraint)


@ffi.def_extern()
def ext_cpBodyShapeIteratorFunc(
    cp_body: ffi.CData, cp_shape: ffi.CData, _: ffi.CData
) -> None:
    _logger.debug("bodyfree remove shape %s %s", cp_body, cp_shape)
    cp_space = lib.cpShapeGetSpace(cp_shape)
    if cp_space != ffi.NULL:
        lib.cpSpaceRemoveShape(cp_space, cp_shape)
    lib.cpShapeSetBody(cp_shape, ffi.NULL)


# constraint.py


@ffi.def_extern()
def ext_cpConstraintPreSolveFunc(cp_constraint: ffi.CData, cp_space: ffi.CData) -> None:
    constraint = ffi.from_handle(lib.cpConstraintGetUserData(cp_constraint))
    assert constraint.a.space is not None
    constraint._pre_solve_func(constraint, constraint.a.space)


@ffi.def_extern()
def ext_cpConstraintPostSolveFunc(
    cp_constraint: ffi.CData, cp_space: ffi.CData
) -> None:
    constraint = ffi.from_handle(lib.cpConstraintGetUserData(cp_constraint))
    assert constraint.a.space is not None
    constraint._post_solve_func(constraint, constraint.a.space)
