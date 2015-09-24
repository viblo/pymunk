__version__ = "$Id$"
__docformat__ = "reStructuredText"

import ctypes as ct
from . import _chipmunk as cp

class Arbiter(object):
    """Arbiters are collision pairs between shapes that are used with the
    collision callbacks.

    .. Warning::
        Because arbiters are handled by the space you should never
        hold onto a reference to an arbiter as you don't know when it will be
        destroyed! Use them within the callback where they are given to you
        and then forget about them or copy out the information you need from
        them.
    """
    def __init__(self, _arbiter, space):
        """Initialize an Arbiter object from the Chipmunk equivalent struct
        and the Space.

        .. note::
            You should never need to create an instance of this class directly.
        """

        self._arbiter = _arbiter
        self._arbitercontents = self._arbiter.contents
        self._space = space
        self._contacts = None # keep a lazy loaded cache of converted contacts

    def _get_contacts(self):
        point_set = cp.cpArbiterGetContactPointSet(self._arbiter)

        if self._contacts is None:
            self._contacts = []
            for i in range(point_set.count):
                self.contacts.append(Contact(point_set.points[i]))
        return self._contacts
    contacts = property(_get_contacts,
        doc="""Information on the contact points between the objects. Return [`Contact`]""")

    def _get_shapes(self):
        shapeA_p = ct.POINTER(cp.cpShape)()
        shapeB_p = ct.POINTER(cp.cpShape)()

        cp.cpArbiterGetShapes(self._arbiter, shapeA_p, shapeB_p)

        a, b = self._space._get_shape(shapeA_p), self._space._get_shape(shapeB_p)
        return a, b

    shapes = property(_get_shapes,
        doc="""Get the shapes in the order that they were defined in the
        collision handler associated with this arbiter""")

    def _get_elasticity(self):
        return self._arbiter.contents.e
    def _set_elasticity(self, elasticity):
        self._arbiter.contents.e = elasticity
    elasticity = property(_get_elasticity, _set_elasticity,
        doc="""Elasticity""")

    def _get_friction(self):
        return self._arbiter.contents.u
    def _set_friction(self, friction):
        self._arbiter.contents.u = friction
    friction = property(_get_friction, _set_friction, doc="""Friction""")

    def _get_surface_velocity(self):
        return self._arbiter.contents.surface_vr
    surface_velocity = property(_get_surface_velocity,
        doc="""Used for surface_v calculations, implementation may change""")

    def _get_total_impulse(self):
        return cp.cpArbiterTotalImpulse(self._arbiter)
    total_impulse = property(_get_total_impulse,
        doc="""Returns the impulse that was applied this step to resolve the
        collision.

        This property should only be called from a post-solve, post-step""")

    def _get_total_impulse_with_friction(self):
        return cp.cpArbiterTotalImpulseWithFriction(self._arbiter)
    total_impulse_with_friction = property(_get_total_impulse_with_friction,
        doc="""Returns the impulse with friction that was applied this step to
        resolve the collision.

        This property should only be called from a post-solve, post-step""")

    def _get_total_ke(self):
        return cp.cpArbiterTotalKE(self._arbiter)
    total_ke = property(_get_total_ke,
        doc="""The amount of energy lost in a collision including static, but
        not dynamic friction.

        This property should only be called from a post-solve, post-step""")

    def _get_stamp(self):
        return self._arbiter.contents.stamp
    stamp = property(_get_stamp,
        doc="""Time stamp of the arbiter. (from the space)""")

    def _get_is_first_contact(self):
        return bool(cpffi.cpArbiterIsFirstContact(self._arbiter))
    is_first_contact = property(_get_is_first_contact,
        doc="""Returns true if this is the first step that an arbiter existed.
        You can use this from preSolve and postSolve to know if a collision
        between two shapes is new without needing to flag a boolean in your
        begin callback.""")
