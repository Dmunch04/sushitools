import inspect


class Label:
    def __init__(self, filename: str, parent: str, name: str, lineno: int):
        self.filename = filename
        self.parent = parent
        self.name = name
        self.lineno = lineno

        self.key = f"{self.filename}:{self.parent}:{self.name}"


class LabelStore:
    def __init__(self):
        self.store = {}

    def empty(self, filename: str) -> bool:
        return not filename in self.store.keys()

    def add_file(self, filename: str):
        self.store[filename] = []

    def has_key(self, filename: str, key: str) -> bool:
        return sum([1 if label.key == key else 0 for label in self.store[filename]]) > 0

    def insert(self, filename: str, parent: str, name: str, lineno: int):
        if self.empty(filename):
            self.add_file(filename)

        self.store[filename].append(Label(filename, parent, name, lineno))

    def get(self, filename: str, key: str) -> int:
        for label in self.store[filename]:
            if label.key == key:
                return label.lineno


__LABEL_STORE = LabelStore()
__LABEL_MAP = {}


class LabelHandler:
    __store: dict[str, Label] = {}

    @staticmethod
    def file_exists(filename: str) -> bool:
        return filename in LabelHandler.__store.keys()

    @staticmethod
    def add_file(filename: str):
        LabelHandler.__store[filename] = [Label(filename, "", "FILE_BEGIN", 1)]

    @staticmethod
    def file_has_label(filename: str, key: str):
        return sum([1 if label.key == key else 0 for label in LabelHandler.__store[filename]]) > 0

    @staticmethod
    def insert(filename: str, parent: str, name: str, lineno: int):
        if not LabelHandler.file_exists(filename):
            LabelHandler.add_file(filename)

        LabelHandler.__store[filename].append(Label(filename, parent, name, lineno))

    @staticmethod
    def get(filename: str, key: str) -> int:
        for label in LabelHandler.__store[filename]:
            if label.key == key:
                return label.lineno


def __process_labels(frame):
    print(frame)
    back = frame.f_back
    f = inspect.getouterframes(back, 2)
    # func name: f[0].function
    # TODO: find parent (class in this case)
    #print(dir(f[0].frame))
    #print(dir(f[0]))
    print(f[0].frame.f_back.f_code)


def label(name: str):
    curframe = inspect.currentframe()
    """
    if __LABEL_STORE.empty("a"):
        __process_labels(curframe)
        __LABEL_STORE.add_file("a")
    else:
        #assert __LABEL_STORE.has_key()
        ...
    """

    callframe = inspect.getouterframes(curframe, 2)
    key = f"{callframe[0].filename}:{callframe[1][3]}:{name}"

    if key in __LABEL_MAP.keys():
        raise Exception("cannot override label (key %s)" % key)

    __LABEL_MAP[key] = int(callframe[1].lineno)


def goto(label: str):
    global line

    curframe = inspect.currentframe()
    callframe = inspect.getouterframes(curframe, 2)
    key = f"{callframe[0].filename}:{callframe[1][3]}:{label}"

    if not key in __LABEL_MAP.keys():
        raise Exception("cannot find label %s (key %s)" % (label, key))

    line = __LABEL_MAP[key]