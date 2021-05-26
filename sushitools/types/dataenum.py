from typing import List, Tuple


# TODO: setattr doesnt work (it just recurses endlessly)
# TODO: make fields that doesnt take in any args a static field and not a function like that maybe. like a property
# TODO: im pretty sure the enum fields arent comparable yet. so 2 vars of the same enum field doesnt equal because theyre different objects

_enum_template = """\
class {name}:
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
        if not isinstance(other.__instance, self.__instance.__class__):
            return False

        return self.__instance.COMPARATOR == other.COMPARATOR

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__instance.__str__()

{cdefs}

{fdefs}
"""

_class_template = """\
    class __{name}_{fname}:
        __slots__ = ({fargsq})

        COMPARATOR = {id}

        def __init__(self, {fargs}):
{fassigns}

        def __str__(self):
            return "{name}.{fname}({fargs})"
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


def dataenum(name: str, fields: List[Tuple[str]]):
    enum_classes = []
    enum_fields = []

    i = 0
    for field in fields:
        assert len(field) >= 1

        fname = field[0]
        fargs = ", ".join(field[1:])

        fassigns = []
        for arg in field[1:]:
            fassigns.append(f"            self.{arg} = {arg}")
        fassigns = "\n".join(fassigns)

        enum_classes.append(
            _class_template.format(
                name=name,
                fname=fname,
                fargsq=", ".join([f'"{arg}"' for arg in field[1:]]),
                id=i,
                fargs=fargs,
                fassigns=fassigns,
                fsargs=", ".join([f"self.{arg}" for arg in field[1:]]),
            )
        )

        enum_fields.append(_field_template.format(name=name, fname=fname, fargs=fargs))

        i += 1

    cdefs = "\n".join(enum_classes)
    fdefs = "\n".join(enum_fields)

    enum_definition = _enum_template.format(name=name, cdefs=cdefs, fdefs=fdefs)

    namespace = dict(__name__="dataenum_%s" % name)
    exec(enum_definition, namespace)
    result = namespace[name]
    result._source = enum_definition

    return result
