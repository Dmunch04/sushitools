from typing import List, Any, Tuple, Callable, NoReturn


class Matchable(object):
    @classmethod
    def get_values(cls) -> List[Any]:
        raise NotImplementedError

    @staticmethod
    @classmethod
    def get_n_values() -> int:
        raise NotImplementedError

    def match(self, *cases: Tuple[Tuple[Any, Callable]]) -> NoReturn:
        for case in cases:
            if not (isinstance(case, tuple) or isinstance(case, list)):
                raise ValueError("cannot match against a singular value.")

            if not len(case) == 2:
                raise ValueError("case must only have a value and a callable.")

            comp, call = case
            call_n_args = call.__code__.co_argcount

            if issubclass(comp, Matchable):
                self_repr = str(self)
                comp_repr = None

                try:
                    tmp_str = "tmp = comp({args})".format(
                        args=", ".join(["None" for arg in range(comp.get_n_values())])
                    )

                    namespace = dict(__name__="tmp_t")
                    namespace["comp"] = comp
                    exec(tmp_str, namespace)
                    result = namespace["tmp"]

                    comp_repr = str(result)
                except:
                    pass

                if (
                    (self.get_n_values() == comp.get_n_values()) and
                    (self.__str__() == comp.__str__) or
                    (self_repr == comp_repr)
                ):
                    exec(
                        "call({args})".format(
                            args=", ".join([f"'{str(val)}'" for val in self.get_values()[:call_n_args]])
                        )
                    )

                    return
            elif hasattr(comp, "_matchable"):
                # TODO: ?
                matchable = comp._matchable

                return
            elif value == comp:
                if call_n_args > 0:
                    raise ValueError("cannot call callback when case is non-matchable.")

                case()

                return


def matchable(matchable: Matchable) -> Callable:
    def wrapper(callback: Callable):
        setattr(callback, "_matchable", matchable)
        return matchable
    return wrapper
