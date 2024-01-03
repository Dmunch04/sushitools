class staticproperty(staticmethod):
    """defines a static property of a class"""

    def __get__(self, *_):
        return self.__func__()