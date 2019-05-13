__docformat__ = "reStructuredText"

from .vec2d import Vec2d

from . import _chipmunk_cffi
cp = _chipmunk_cffi.lib
ffi = _chipmunk_cffi.ffi   

from .contact_point_set import ContactPointSet

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
        self._space = space        
        
    def _get_contact_point_set(self):
        _set = cp.cpArbiterGetContactPointSet(self._arbiter)
        return ContactPointSet._from_cp(_set)
        
    def _set_contact_point_set(self, point_set):
        # This has to be done by fetching a new Chipmunk point set, update it 
        # according to whats passed in and the pass that back to chipmunk due
        # to the fact that ContactPointSet doesnt contain a reference to the 
        # corresponding c struct. 
        
        _set = cp.cpArbiterGetContactPointSet(self._arbiter)
        _set.normal = tuple(point_set.normal)
        
        if len(point_set.points) == _set.count:
            for i in range(_set.count):
                _set.points[i].pointA = tuple(point_set.points[0].point_a)
                _set.points[i].pointB = tuple(point_set.points[0].point_b)
                _set.points[i].distance = point_set.points[0].distance
        else:
            msg = 'Expected {} points, got {} points in point_set'.format(
                _set.count,  len(point_set.points))
            raise Exception(msg)
            
        cp.cpArbiterSetContactPointSet(self._arbiter, ffi.addressof(_set))
                
    contact_point_set = property(_get_contact_point_set, _set_contact_point_set,
        doc="""Contact point sets make getting contact information from the 
        Arbiter simpler.
        
        Return `ContactPointSet`""")

    def _get_shapes(self):
        shapeA_p = ffi.new("cpShape *[1]")
        shapeB_p = ffi.new("cpShape *[1]")

        cp.cpArbiterGetShapes(self._arbiter, shapeA_p, shapeB_p)

        a, b = self._space._get_shape(shapeA_p[0]), self._space._get_shape(shapeB_p[0])
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
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        elasticity of the two shapes together.
        """)

    def _get_friction(self):
        return cp.cpArbiterGetFriction(self._arbiter)
    def _set_friction(self, friction):
        cp.cpArbiterSetFriction(self._arbiter, friction)
    friction = property(_get_friction, _set_friction, 
        doc="""The calculated friction for this collision pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. The default calculation multiplies the 
        friction of the two shapes together.
        """)

    def _get_surface_velocity(self):
        return Vec2d._fromcffi(cp.cpArbiterGetSurfaceVelocity(self._arbiter))
    def _set_surface_velocity(self, velocity):
        cp.cpArbiterSetSurfaceVelocity(self._arbiter, velocity)
    surface_velocity = property(_get_surface_velocity, _set_surface_velocity,
        doc="""The calculated surface velocity for this collision pair. 
        
        Setting the value in a pre_solve() callback will override the value 
        calculated by the space. the default calculation subtracts the 
        surface velocity of the second shape from the first and then projects 
        that onto the tangent of the collision. This is so that only 
        friction is affected by default calculation. Using a custom 
        calculation, you can make something that responds like a pinball 
        bumper, or where the surface velocity is dependent on the location 
        of the contact point.
        """)

    def _get_total_impulse(self):
        return Vec2d._fromcffi(cp.cpArbiterTotalImpulse(self._arbiter))
    total_impulse = property(_get_total_impulse,
        doc="""Returns the impulse that was applied this step to resolve the
        collision.

        This property should only be called from a post-solve or each_arbiter
        callback.
        """)

    def _get_total_ke(self):
        return cp.cpArbiterTotalKE(self._arbiter)
    total_ke = property(_get_total_ke,
        doc="""The amount of energy lost in a collision including static, but
        not dynamic friction.

        This property should only be called from a post-solve or each_arbiter callback.
        """)

    def _get_is_first_contact(self):
        return bool(cp.cpArbiterIsFirstContact(self._arbiter))
    is_first_contact = property(_get_is_first_contact,
        doc="""Returns true if this is the first step the two shapes started 
        touching. 
        
        This can be useful for sound effects for instance. If its the first 
        frame for a certain collision, check the energy of the collision in a 
        post_step() callback and use that to determine the volume of a sound 
        effect to play.
        """)

    def _get_is_removal(self):
        return bool(cp.cpArbiterIsRemoval(self._arbiter))
    is_removal = property(_get_is_removal, 
        doc="""Returns True during a separate() callback if the callback was 
        invoked due to an object removal.
        """)

    def _get_normal(self):
        return Vec2d._fromcffi(cp.cpArbiterGetNormal(self._arbiter))
    normal = property(_get_normal,
        doc="""Returns the normal of the collision.
        """)
