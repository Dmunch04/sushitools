from typing import List, Tuple


# TODO: setattr doesnt work (it just recurses endlessly) -> i forgot what this issue was about?


class staticproperty(staticmethod):
    def __get__(self, *_):
        return self.__func__()


_enum_template = """\
#from match import Matchable
from sushitools.cf.match import Matchable
class {name}(Matchable):
    'DataEnum {name}'
    __slots__ = ("__instance")
    def __init__(self):
        self.__instance = None
    def __getattr__(self, name):
        if self.__instance is None:
            raise AttributeError
        if not hasattr(self.__instance, name):
            raise AttributeError
        return getattr(self.__instance, name)
    def __eq__(self, other):
        if callable(other):
            return other.__name__ == type(self.__instance).__name__.split("_")[-1]
        elif isinstance(other, type(self)):
            return type(other.__instance).__name__.split("_")[-1] == type(self.__instance).__name__.split("_")[-1]
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return self.__instance.__str__()
    def get_values(self):
        return self.__instance.get_values()
    def get_n_values(self):
        return self.__instance.get_n_values()
{cdefs}
{fdefs}
"""

_class_template = """\
    class __{name}_{fname}(Matchable):
        __slots__ = ({fargsq})
        def __init__(self, {fargs}):
{fassigns}
        def __str__(self):
            return "{name}.{fname}({fargs})"
        def __eq__(self, other):
            raise Exception("idk")
        def get_values(self):
            return ({fsargs})
        def get_n_values(self):
            return {fsargs_len}
"""

_field_template = """\
    @staticmethod
    def {fname}({fargs}):
        tmp = {name}()
        tmp.__new_{fname}({fargs})
        return tmp
    def __new_{fname}(self, {fargs}):
        self.__instance = self.__{name}_{fname}({fargs})
"""

_property_field_template = """\
    @staticproperty
    def {fname}():
        tmp = {name}()
        tmp.__new_{fname}()
        return tmp
    def __new_{fname}(self):
        self.__instance = self.__{name}_{fname}()
"""


# explanation for why this is commented out:
# if you provide a list instead of vararg of tuple,
# then it wrapes the list in a tuple which fucks everything up.
# UPDATE: i changed it to other way around. lists are no longer supported (for now?)
def dataenum(name: str, *fields: List[Tuple[str]]):
#def dataenum(name: str, fields: List[Tuple[str]]):
    enum_classes = []
    enum_fields = []

    i = 0
    for field in fields:
        assert len(field) >= 1

        if len(field) > 1 and (isinstance(field, tuple) or isinstance(field, list)):
            fname = field[0]
            fargs = ", ".join(field[1:])
            args = field[1:]
        else:
            fname = field
            fargs = ""
            args = []

        fassigns = []
        for arg in args:
            fassigns.append(f"            self.{arg} = {arg}")
        fassigns = "\n".join(fassigns)

        if not fassigns:
            fassigns = "            pass"

        enum_classes.append(
            _class_template.format(
                name=name,
                fname=fname,
                fargsq=", ".join([f'"{arg}"' for arg in args]),
                fargs=fargs,
                fassigns=fassigns,
                fsargs=", ".join([f"self.{arg}" for arg in args])
                + ("," if len(args) == 1 else ""),
                fsargs_len=len([arg for arg in args]),
            )
        )

        if len(args) > 0:
            enum_fields.append(
                _field_template.format(name=name, fname=fname, fargs=fargs)
            )
        else:
            enum_fields.append(_property_field_template.format(name=name, fname=fname))

        i += 1

    cdefs = "\n".join(enum_classes)
    fdefs = "\n".join(enum_fields)

    enum_definition = _enum_template.format(name=name, cdefs=cdefs, fdefs=fdefs)

    namespace = dict(__name__="dataenum_%s" % name)
    namespace["staticproperty"] = staticproperty
    exec(enum_definition, namespace)
    result = namespace[name]
    result._source = enum_definition

    return result
