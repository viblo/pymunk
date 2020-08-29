from typing import NamedTuple


class ShapeFilter(NamedTuple):
    """
    Pymunk has two primary means of ignoring collisions: groups and
    category masks.

    Groups are used to ignore collisions between parts on a complex object. A
    ragdoll is a good example. When jointing an arm onto the torso, you'll
    want them to allow them to overlap. Groups allow you to do exactly that.
    Shapes that have the same group don't generate collisions. So by placing
    all of the shapes in a ragdoll in the same group, you'll prevent it from
    colliding against other parts of itself. Category masks allow you to mark
    which categories an object belongs to and which categories it collides
    with.

    For example, a game has four collision categories: player (0), enemy (1),
    player bullet (2), and enemy bullet (3). Neither players nor enemies
    should not collide with their own bullets, and bullets should not collide
    with other bullets. However, players collide with enemy bullets, and
    enemies collide with player bullets.

    ============= =============== ====================
    Object        Object Category Category Mask
    ============= =============== ====================
    Player        0b00001 (1)     0b11000 (4, 5)
    Enemy         0b00010 (2)     0b01110 (2, 3, 4)
    Player Bullet 0b00100 (3)     0b10001 (1, 5)
    Enemy Bullet  0b01000 (4)     0b10010 (2, 5)
    Walls         0b10000 (5)     0b01111 (1, 2, 3, 4)
    ============= =============== ====================

    Note that in the table the categories and masks are written as binary
    values to clearly show the logic. To save space only 5 digits are used. The
    default type of categories and mask in ShapeFilter is an unsigned int,
    with a resolution of 32 bits. That means that the you have 32 bits to use,
    in binary notation that is `0b00000000000000000000000000000000` to
    `0b11111111111111111111111111111111` which can be written in hex as
    `0x00000000` to `0xFFFFFFFF`.

    Everything in this example collides with walls. Additionally,
    the enemies collide with each other.

    By default, objects exist in every category and collide with every category.

    Objects can fall into multiple categories. For instance, you might have a
    category for a red team, and have a red player bullet. In the above
    example, each object only has one category.

    The default type of categories and mask in ShapeFilter is unsigned int
    which has a resolution of 32 bits on most systems.

    There is one last way of filtering collisions using collision handlers.
    See the section on callbacks for more information. Collision handlers can
    be more flexible, but can be slower. Fast collision filtering rejects
    collisions before running the expensive collision detection code, so
    using groups or category masks is preferred.

    Example of how category and mask can be used to filter out player from
    enemy object:

    >>> import pymunk
    >>> s = pymunk.Space()
    >>> player_b = pymunk.Body(1,1)
    >>> player_c = pymunk.Circle(player_b, 10)
    >>> s.add(player_b, player_c)
    >>> player_c.filter = pymunk.ShapeFilter(categories=0b1)
    >>> hit = s.point_query_nearest((0,0), 0, pymunk.ShapeFilter())
    >>> hit != None
    True
    >>> filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1)
    >>> hit = s.point_query_nearest((0,0), 0, filter)
    >>> hit == None
    True
    >>> enemy_b = pymunk.Body(1,1)
    >>> enemy_c = pymunk.Circle(enemy_b, 10)
    >>> s.add(enemy_b, enemy_c)
    >>> hit = s.point_query_nearest((0,0), 0, filter)
    >>> hit != None
    True

    """

    group: int = 0
    """Two objects with the same non-zero group value do not collide.
	
    This is generally used to group objects in a composite object together to disable self collisions.
    """

    categories: int = 0xFFFFFFFF
    """A bitmask of user definable categories that this object belongs to.
	
    The category/mask combinations of both objects in a collision must agree for a collision to occur.
    """

    mask: int = 0xFFFFFFFF
    """A bitmask of user definable category types that this object object collides with.
	
    The category/mask combinations of both objects in a collision must agree for a collision to occur.
	"""

    @staticmethod
    def ALL_MASKS() -> int:
        return 0xFFFFFFFF

    @staticmethod
    def ALL_CATEGORIES() -> int:
        return 0xFFFFFFFF
