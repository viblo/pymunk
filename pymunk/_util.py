class _DeadRef:
    """An empty reference that does not depend on garbage collection.

    Use a callable object so it also works as a class attribute without
    becoming a bound method.
    """

    def __call__(self) -> None:
        return None


_dead_ref = _DeadRef()
