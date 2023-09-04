from typing import Callable, Optional

import pymunk


class OverrideableConstraint(pymunk.Constraint):
    _pre_step_func: Callable[[pymunk.Constraint, float], None]
    _apply_cached_impulse_func: Callable[[pymunk.Constraint, float], None]
    _apply_impulse_func: Callable[[pymunk.Constraint, float], None]
    _get_impulse_func: Callable[[pymunk.Constraint], float]

    def __init__(self, a: pymunk.Body, b: pymunk.Body) -> None:
        _constraint = pymunk.ffi.new("cpConstraint *")
        klass = pymunk.ffi.new("cpConstraintClass *")
        klass.preStep = pymunk.cp.ext_cpConstraintPreStepImpl
        klass.applyCachedImpulse = pymunk.cp.ext_cpConstraintApplyCachedImpulseImpl
        klass.applyImpulse = pymunk.cp.ext_cpConstraintApplyImpulseImpl
        klass.getImpulse = pymunk.cp.ext_cpConstraintGetImpulseImpl
        pymunk.cp.cpConstraintInit(_constraint, klass, a._body, b._body)

        self._init(a, b, _constraint)

    def pre_step(self, dt):
        print(f"pre_step {c} {dt}")

    def apply_cached_impulse(self, dt):
        print(f"apply_cached_impulse {c} {dt}")

    def apply_impulse(self, dt):
        print(f"apply_impulse {c} {dt}")

    def get_impulse(self):
        print(f"get_impulse {c}")
        return 0


a, b = pymunk.Body(1, 2), pymunk.Body(1, 2)
c = OverrideableConstraint(a, b)

space = pymunk.Space()

space.add(a, b, c)

space.step(1)
space.step(0.1)
