__docformat__ = "reStructuredText"


from typing import TYPE_CHECKING, Tuple, Dict, List, Any, Iterable, Sequence

if TYPE_CHECKING:
    from .space import Space
    from .shapes import Shape

from ._chipmunk_cffi import ffi, lib
from .contact_point_set import ContactPointSet
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

    def _get_contact_point_set(self) -> ContactPointSet:
        _set = lib.cpArbiterGetContactPointSet(self._arbiter)
        return ContactPointSet._from_cp(_set)

    def _set_contact_point_set(self, point_set: ContactPointSet) -> None:
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

    contact_point_set = property(
        _get_contact_point_set,
        _set_contact_point_set,
        doc="""Contact point sets make getting contact information from the 
        Arbiter simpler.
        
        Return `ContactPointSet`""",
    )

    @property
    def shapes(self) -> Tuple["Shape", "Shape"]:
        """Get the shapes in the order that they were defined in the
        collision handler associated with this arbiter
        """
        shapeA_p = ffi.new("cpShape *[1]")
        shapeB_p = ffi.new("cpShape *[1]")

        lib.cpArbiterGetShapes(self._arbiter, shapeA_p, shapeB_p)

        a, b = self._space._get_shape(shapeA_p[0]), self._space._get_shape(shapeB_p[0])
        assert a is not None
        assert b is not None
        return a, b

    def _get_restitution(self) -> float:
        return lib.cpArbiterGetRestitution(self._arbiter)

    def _set_restitution(self, restitution: float) -> None:
        lib.cpArbiterSetRestitution(self._arbiter, restitution)

    restitution = property(
        _get_restitution,
        _set_restitution,
        doc="""The calculated restitution (elasticity) for this collision 
        pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        elasticity of the two shapes together.
        """,
    )

    def _get_friction(self) -> float:
        return lib.cpArbiterGetFriction(self._arbiter)

    def _set_friction(self, friction: float) -> None:
        lib.cpArbiterSetFriction(self._arbiter, friction)

    friction = property(
        _get_friction,
        _set_friction,
        doc="""The calculated friction for this collision pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        friction of the two shapes together.
        """,
    )

    def _get_surface_velocity(self) -> Vec2d:
        v = lib.cpArbiterGetSurfaceVelocity(self._arbiter)
        return Vec2d(v.x, v.y)

    def _set_surface_velocity(self, velocity: Vec2d) -> None:
        lib.cpArbiterSetSurfaceVelocity(self._arbiter, velocity)

    surface_velocity = property(
        _get_surface_velocity,
        _set_surface_velocity,
        doc="""The calculated surface velocity for this collision pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. the default calculation subtracts the 
        surface velocity of the second shape from the first and then projects 
        that onto the tangent of the collision. This is so that only 
        friction is affected by default calculation. Using a custom 
        calculation, you can make something that responds like a pinball 
        bumper, or where the surface velocity is dependent on the location 
        of the contact point.
        """,
    )

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
) -> List[Dict[str, Any]]:
    res = []
    for i in range(count):
        res.append(_contact_to_dict(_contacts[i]))
    return res


def _contact_to_dict(_contact: ffi.CData) -> Dict[str, Any]:
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


def _contacts_from_dicts(ds: Sequence[Dict[str, Any]]) -> List[ffi.CData]:
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


def _arbiter_from_dict(d: Dict[str, Any], space: "Space") -> ffi.CData:
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


def _arbiter_to_dict(_arbiter: ffi.CData, space: "Space") -> Dict[str, Any]:
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
