__docformat__ = "reStructuredText"


from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from .space import Space
    from .body import Body

from ._chipmunk_cffi import ffi, lib
from .contact_point_set import ContactPointSet
from .shapes import Shape
from .vec2d import Vec2d


class Arbiter(object):
    """The Arbiter object encapsulates a pair of colliding shapes and all of
        the data about their collision.

        They are created when a collision starts, and persist until those
        shapes are no longer colliding.

    .. Warning::
        Because arbiters are handled by the space you should never
        hold onto a reference to an arbiter as you don't know when it will be
        destroyed! Use them within the callback where they are given to you
        and then forget about them or copy out the information you need from
        them.
    """

    def __init__(self, _arbiter: ffi.CData, space: "Space") -> None:
        """Initialize an Arbiter object from the Chipmunk equivalent struct
        and the Space.

        .. note::
            You should never need to create an instance of this class directly.
        """

        self._arbiter = _arbiter
        self._space = space

    @property
    def process_collision(self) -> bool:
        """Decides if the collision should be processed or rejected.

        Set this during a `begin()` or `pre_solve()` callback to override
        the default (`True`) value.

        Set this to `true` to process the collision normally or
        `false` to cause Pymunk to ignore the collision entirely. Note that
        while `post_solve` might be skipped if this is `false`, `separate`
        will always be called when the shapes stop overlapping.

        .. note::
            No collision will be processed for a sensor Shape, or a Shape
            attached to a STATIC or KINEMATIC Body.

        """
        return lib.cpArbiterGetProcessCollision(self._arbiter)

    @process_collision.setter
    def process_collision(self, v: bool) -> None:
        lib.cpArbiterSetProcessCollision(self._arbiter, v)

    @property
    def contact_point_set(self) -> ContactPointSet:
        """Contact point sets make getting contact information from the
        Arbiter simpler.

        Return `ContactPointSet`"""
        _set = lib.cpArbiterGetContactPointSet(self._arbiter)
        return ContactPointSet._from_cp(_set)

    @contact_point_set.setter
    def contact_point_set(self, point_set: ContactPointSet) -> None:
        # This has to be done by fetching a new Chipmunk point set, update it
        # according to whats passed in and the pass that back to chipmunk due
        # to the fact that ContactPointSet doesnt contain a reference to the
        # corresponding c struct.
        _set = lib.cpArbiterGetContactPointSet(self._arbiter)
        _set.normal = point_set.normal

        if len(point_set.points) == _set.count:
            for i in range(_set.count):
                _set.points[i].pointA = point_set.points[0].point_a
                _set.points[i].pointB = point_set.points[0].point_b
                _set.points[i].distance = point_set.points[0].distance
        else:
            msg = "Expected {} points, got {} points in point_set".format(
                _set.count, len(point_set.points)
            )
            raise Exception(msg)

        lib.cpArbiterSetContactPointSet(self._arbiter, ffi.addressof(_set))

    @property
    def bodies(self) -> tuple["Body", "Body"]:
        """The the bodies in the order their corresponding shapes were defined
        in the collision handler associated with this arbiter.

        This is a shorthand to get the bodes::

            arb.bodies == arb.shapes[0].body, arb.shapes[1].body .
        """
        a, b = self.shapes
        assert (
            a.body != None
        ), "Shape should have a body. Could be a bug in Pymunk, please report"
        assert (
            b.body != None
        ), "Shape should have a body. Could be a bug in Pymunk, please report"
        return a.body, b.body

    @property
    def shapes(self) -> tuple["Shape", "Shape"]:
        """Get the shapes in the order that they were defined in the
        collision handler associated with this arbiter
        """
        shapeA_p = ffi.new("cpShape *[1]")
        shapeB_p = ffi.new("cpShape *[1]")

        lib.cpArbiterGetShapes(self._arbiter, shapeA_p, shapeB_p)

        a, b = Shape._from_cp_shape(shapeA_p[0]), Shape._from_cp_shape(shapeB_p[0])
        assert a is not None
        assert b is not None
        return a, b

    @property
    def restitution(self) -> float:
        """The calculated restitution (elasticity) for this collision
        pair.

        Setting the value in a pre_solve() callback will override the value
        calculated by the space. The default calculation multiplies the
        elasticity of the two shapes together.
        """
        return lib.cpArbiterGetRestitution(self._arbiter)

    @restitution.setter
    def restitution(self, restitution: float) -> None:
        lib.cpArbiterSetRestitution(self._arbiter, restitution)

    @property
    def friction(self) -> float:
        """The calculated friction for this collision pair.

        Setting the value in a pre_solve() callback will override the value
        calculated by the space. The default calculation multiplies the
        friction of the two shapes together.
        """
        return lib.cpArbiterGetFriction(self._arbiter)

    @friction.setter
    def friction(self, friction: float) -> None:
        lib.cpArbiterSetFriction(self._arbiter, friction)

    @property
    def surface_velocity(self) -> Vec2d:
        """The calculated surface velocity for this collision pair.

        Setting the value in a pre_solve() callback will override the value
        calculated by the space. the default calculation subtracts the
        surface velocity of the second shape from the first and then projects
        that onto the tangent of the collision. This is so that only
        friction is affected by default calculation. Using a custom
        calculation, you can make something that responds like a pinball
        bumper, or where the surface velocity is dependent on the location
        of the contact point.
        """
        v = lib.cpArbiterGetSurfaceVelocity(self._arbiter)
        return Vec2d(v.x, v.y)

    @surface_velocity.setter
    def surface_velocity(self, velocity: tuple[float, float]) -> None:
        lib.cpArbiterSetSurfaceVelocity(self._arbiter, velocity)

    @property
    def total_impulse(self) -> Vec2d:
        """Returns the impulse that was applied this step to resolve the
        collision.

        This property should only be called from a post-solve or each_arbiter
        callback.
        """
        v = lib.cpArbiterTotalImpulse(self._arbiter)
        return Vec2d(v.x, v.y)

    @property
    def total_ke(self) -> float:
        """The amount of energy lost in a collision including static, but
        not dynamic friction.

        This property should only be called from a post-solve or each_arbiter callback.
        """
        return lib.cpArbiterTotalKE(self._arbiter)

    @property
    def is_first_contact(self) -> bool:
        """Returns true if this is the first step the two shapes started
        touching.

        This can be useful for sound effects for instance. If its the first
        frame for a certain collision, check the energy of the collision in a
        post_step() callback and use that to determine the volume of a sound
        effect to play.
        """
        return bool(lib.cpArbiterIsFirstContact(self._arbiter))

    @property
    def is_removal(self) -> bool:
        """Returns True during a separate() callback if the callback was
        invoked due to an object removal.
        """
        return bool(lib.cpArbiterIsRemoval(self._arbiter))

    @property
    def normal(self) -> Vec2d:
        """Returns the normal of the collision."""
        v = lib.cpArbiterGetNormal(self._arbiter)
        return Vec2d(v.x, v.y)


def _contacts_to_dicts(
    _contacts: Sequence[ffi.CData], count: int
) -> list[dict[str, Any]]:
    res = []
    for i in range(count):
        res.append(_contact_to_dict(_contacts[i]))
    return res


def _contact_to_dict(_contact: ffi.CData) -> dict[str, Any]:
    d = {}
    d["r1"] = _contact.r1.x, _contact.r1.y
    d["r2"] = _contact.r2.x, _contact.r2.y
    d["nMass"] = _contact.nMass
    d["tMass"] = _contact.tMass
    d["bounce"] = _contact.bounce
    d["jnAcc"] = _contact.jnAcc
    d["jtAcc"] = _contact.jtAcc
    d["jBias"] = _contact.jBias
    d["bias"] = _contact.bias
    d["hash"] = _contact.hash
    return d


def _contacts_from_dicts(ds: Sequence[dict[str, Any]]) -> ffi.CData:
    _contacts = lib.cpContactArrAlloc(len(ds))
    for i in range(len(ds)):
        _contact = _contacts[i]
        d = ds[i]
        _contact.r1.x = d["r1"][0]
        _contact.r1.y = d["r1"][1]
        _contact.r2.x = d["r2"][0]
        _contact.r2.y = d["r2"][1]
        _contact.nMass = d["nMass"]
        _contact.tMass = d["tMass"]
        _contact.bounce = d["bounce"]
        _contact.jnAcc = d["jnAcc"]
        _contact.jtAcc = d["jtAcc"]
        _contact.jBias = d["jBias"]
        _contact.bias = d["bias"]
        _contact.hash = d["hash"]
    return _contacts


def _arbiter_from_dict(d: dict[str, Any], space: "Space") -> ffi.CData:
    _arb = lib.cpArbiterNew(
        d["a"]._shape, d["b"]._shape
    )  # this will also set the bodies

    _arb.e = d["e"]
    _arb.u = d["u"]
    _arb.surface_vr = d["surface_vr"]

    _arb.count = d["count"]
    _arb.contacts = _contacts_from_dicts(d["contacts"])

    _arb.n = d["n"]

    _arb.swapped = d["swapped"]
    _arb.stamp = d["stamp"]
    _arb.state = d["state"]
    return _arb


def _arbiter_to_dict(_arbiter: ffi.CData, space: "Space") -> dict[str, Any]:
    d = {}
    d["e"] = _arbiter.e
    d["u"] = _arbiter.u
    d["surface_vr"] = (_arbiter.surface_vr.x, _arbiter.surface_vr.y)

    cp_bodies = {}
    cp_shapes = {}

    for body in space.bodies:
        cp_bodies[body._body] = body
    for shape in space.shapes:
        cp_shapes[shape._shape] = shape

    # cpDataPointer data;

    d["a"] = cp_shapes[_arbiter.a]
    d["b"] = cp_shapes[_arbiter.b]

    # these are not needed, since they can be fetched from the shapes
    # d['body_a'] = cp_bodies[_arbiter.body_a]
    # d['body_b'] = cp_bodies[_arbiter.body_b]

    # struct cpArbiterThread thread_a, thread_b;

    d["count"] = _arbiter.count
    d["contacts"] = _contacts_to_dicts(_arbiter.contacts, _arbiter.count)
    d["n"] = _arbiter.n.x, _arbiter.n.y

    # // Regular, wildcard A and wildcard B collision handlers.
    # cpCollisionHandler *handler, *handlerA, *handlerB;

    d["swapped"] = _arbiter.swapped
    d["stamp"] = _arbiter.stamp
    d["state"] = _arbiter.state
    return d
