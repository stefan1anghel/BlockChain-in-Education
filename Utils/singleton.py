
class Singleton:  # FOLOSIT CA DECORATOR
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """ Prima apelare a metodei creaza instanta, apoi de fiecare data cand metoda va fi apelata, se va returna
        instanta deja creata """

        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
