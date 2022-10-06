from typing import Callable, NoReturn, Any


def create_value_cb(value: any) -> Callable:
    """creates a lambda function that returns the given value

    Args:
        value (any): the value to wrap in a lambda function

    Returns:
        Callable: the created lambda
    """

    return lambda: value


def perform_call(cb: Callable, args: list[any], n_values: int) -> Any | None:
    """performs a call to the given function with the given arguments.
    before this is does various checks such as making sure there are never too few nor too many arguments passed

    Args:
        cb (Callable): the function to call
        args (list[any]): the arguments to be passed to the function
        n_values (int): the amount of arguments

    Returns:
        any | None: the result of the function call if any, else `None`
    """

    call_n_args = cb.__code__.co_argcount

    if call_n_args > 0:
        call_template = "res = call({args})"

        str_args = []
        for arg in args:
            if isinstance(arg, str):
                arg = "'%s'" % arg

            str_args.append(str(arg))

        arg_difference = call_n_args - n_values
        if arg_difference < 0:  # remove remaining values from argset
            str_args = str_args[:arg_difference]
        elif arg_difference > 0:  # add missing values to argset
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
    """base class for all objects than can be matched"""

    @classmethod
    def get_values(cls) -> list[any]:
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

    def match(
        self, *cases: tuple[any, Any | Callable], default: Any | Callable | None = None
    ) -> NoReturn | None:
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
                raise ValueError(
                    "case must be a tuple of value and callback or return value"
                )

            if not len(case) == 2:
                raise ValueError(
                    "case must only have a value and a callable or return value."
                )

            comp, call = case
            call = call if callable(call) else create_value_cb(call)

            if self.__eq__(comp):
                return perform_call(call, self.get_values(), self.get_n_values())

        if default:
            call = default if callable(default) else create_value_cb(default)
            return perform_call(call, self.get_values(), self.get_n_values())
