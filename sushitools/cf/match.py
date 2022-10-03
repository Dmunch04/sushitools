from typing import List, Any, Tuple, Callable, NoReturn, Union


def create_value_cb(value: Any) -> Callable:
    return lambda: value


def perform_call(cb: Callable, args: List[Any], n_values: int) -> Union[Any, None]:
    call_n_args = cb.__code__.co_argcount
    
    if call_n_args > 0:
        call_template = "res = call({args})"

        str_args = []
        for arg in args:
            if isinstance(arg, str):
                arg = "'%s'" % arg
            
            str_args.append(str(arg))

        arg_difference = call_n_args - n_values
        if arg_difference < 0: # remove remaining values from argset
            str_args = str_args[:arg_difference]
        elif arg_difference > 0: # add missing values to argset
            for i in range(arg_difference):
                str_args.append("None")

        f_call = call_template.format(args=",".join(str_args))

        namespace = dict(__name__="match")
        namespace["call"] = cb
        exec(f_call, namespace)
        return namespace["res"]
    else:
        return cb()


class Matchable(object):
    """base class for all objects than can be matched
    """

    @classmethod
    def get_values(cls) -> List[Any]:
        """get all the values that can be matched

        Returns:
            List[Any]: a list of all the possible values to be matched against
        """
        raise NotImplementedError

    @classmethod
    def get_n_values(cls) -> int:
        """the amount of values that can be matched

        Returns:
            int: the amount of values
        """

        raise NotImplementedError

    def match(self, *cases: Tuple[Any, Union[Callable, Any]], default: Union[Callable, Any, None] = None) -> Union[NoReturn, Any]:
        """matches self against all cases until a success is found

        Args:
            *cases (Tuple[Any, Union[Callable, Any]]): all the match cases
            default (Union[Callable, Any, None], optional): the default branch to goto if no other case is matched. defaults to None.

        Raises:
            ValueError: if case is not a tuple consisting of a match value and callback

        Returns:
            Union[NoReturn, Any]: either nothing (if matched branch is a callback) or any value
        """

        for case in cases:
            if not (isinstance(case, tuple) or isinstance(case, list)):
                raise ValueError("case must be a tuple of value and callback or return value")

            if not len(case) == 2:
                raise ValueError("case must only have a value and a callable or return value.")

            comp, call = case
            call = call if callable(call) else create_value_cb(call)

            if self.__eq__(comp):
                return perform_call(call, self.get_values(), self.get_n_values())

        if default:
            call = default if callable(default) else create_value_cb(default)
            return perform_call(call, self.get_values(), self.get_n_values())
