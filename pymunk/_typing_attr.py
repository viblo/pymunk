from typing import Any


class TypingAttrMixing:
    """Type helper mixin to make mypy accept dynamic attribtutes.
    
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """Override default setattr to make sure type checking works."""
        super().__setattr__(name, value)

    def __getattr__(self, name: str) -> Any:
        """Override default getattr to make sure type checking works."""
        return self.__getattribute__(name)
