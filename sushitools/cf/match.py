from typing import List, Any, Tuple, Callable, NoReturn


class Matchable(object):
    @classmethod
    def get_values(cls) -> List[Any]:
        raise NotImplementedError

    @classmethod
    def get_n_values(cls) -> int:
        raise NotImplementedError

    def match(self, *cases: Tuple[Tuple[Any, Callable]]) -> NoReturn:
        for case in cases:
            if not (isinstance(case, tuple) or isinstance(case, list)):
                raise ValueError("case must be a tuple of value and callback")

            if not len(case) == 2:
                raise ValueError("case must only have a value and a callable.")

            comp, call = case
            call_n_args = call.__code__.co_argcount

            if self.__eq__(comp):
                if call_n_args > 0:
                    call_template = "res = call({args})"

                    str_args = []
                    for arg in self.get_values():
                        str_args.append(str(arg))

                    arg_difference = call_n_args - self.get_n_values()
                    if arg_difference < 0:  # remove remaining values from argset
                        str_args = str_args[:arg_difference]
                    elif arg_difference > 0:  # add missing values to argset
                        for i in range(arg_difference):
                            str_args.append("None")

                    f_call = call_template.format(args=",".join(str_args))

                    namespace = dict(__name__="match")
                    namespace["call"] = call
                    exec(f_call)
                else:
                    call()
