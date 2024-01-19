from typing import Type

from esa.app.helpers.exceptions.exceptions import DefinitionException


class ConfigurableSingleton(object):
    """
    child must be singleton to work
    """

    _replaced_class_type = None

    @classmethod
    def configure(cls, replaced_class_type: Type) -> None:
        cls._replaced_class_type = replaced_class_type


class Singleton(type):
    _instances: dict[type, type] = {}

    def __call__(cls, *args, **kwargs) -> type:
        if cls not in cls._instances:
            instantiated_object = super(Singleton, cls).__call__(*args, **kwargs)
            if isinstance(instantiated_object, ConfigurableSingleton):
                if instantiated_object._replaced_class_type is not None:
                    instantiated_object = super(Singleton, instantiated_object._replaced_class_type).__call__(
                        *args, **kwargs
                    )
                else:
                    raise DefinitionException(f"Forgot to call .configure for child of {cls.__name__}.")
            cls._instances[cls] = instantiated_object
        return cls._instances[cls]