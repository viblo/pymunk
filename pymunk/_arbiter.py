__version__ = "$Id$"
__docformat__ = "reStructuredText"

import ctypes as ct
from . import _chipmunk as cp
from ._contact import ContactPointSet


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

    def _get_contact_points(self):
        point_set = cp.cpArbiterGetContactPointSet(self._arbiter)

        if self._contacts is None:
            self._contacts = []
            for i in range(point_set.count):
                self._contacts.append(Contact(point_set.points[i]))
        return self._contacts
    contact_points = property(_get_contact_points,
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

    def _get_restitution(self):
        return cp.cpArbiterGetRestitution(self._arbiter)
    def _set_restitution(self, restitution):
        cp.cpArbiterSetRestitution(self._arbiter, restitution)
    restitution = property(_get_restitution, _set_restitution,
        doc="""The calculated restitution (elasticity) for this collision 
        pair. 
        
        Setting the value in a preSolve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        elasticity of the two shapes together.
        """)

    def _get_friction(self):
        return cp.cpArbiterGetFriction(self._arbiter)
    def _set_friction(self, friction):
        cp.cpArbiterSetFriction(self._arbiter, friction)
    friction = property(_get_friction, _set_friction, 
        doc="""The calculated friction for this collision pair. 
        
        Setting the value in a preSolve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        friction of the two shapes together.
        """)

    def _get_surface_velocity(self):
        return cp.cpArbiterGetSurfaceVelocity(self._arbiter)
    def _set_surface_velocity(self, velocity):
        cp.cpArbiterSetSurfaceVelocity(self._arbiter, velocity)
    surface_velocity = property(_get_surface_velocity, _set_surface_velocity,
        doc="""The calculated surface velocity for this collision pair. 
        
        Setting the value in a preSolve() callback will override the value 
        calculated by the space. the default calculation subtracts the 
        surface velocity of the second shape from the first and then projects 
        that onto the tangent of the collision. This is so that only 
        friction is affected by default calculation. Using a custom 
        calculation, you can make something that responds like a pinball 
        bumper, or where the surface velocity is dependent on the location 
        of the contact point.
        """)

    def _get_count(self):
        return cp.cpArbiterGetCount(self._arbiter)
    count = property(_get_count, 
        doc="""Get the number of contacts tracked by this arbiter
        """)
    
    def _get_normal(self):
        return cp.cpArbiterGetNormal(self._arbiter)
    normal = property(_get_normal, 
        doc="""Get the collision normal of the collision""")
    
    def get_point_a(self, i):
        """Get the collision point of the i:th contact."""
        return cp.cpArbiterGetPointA(self._arbiter, i)
    def get_point_b(self, i):
        """Get the collision point of the i:th contact."""
        return cp.cpArbiterGetPointB(self._arbiter, i)
        
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
