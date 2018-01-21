class Singleton:
    """
   Singleton class decorator

   Awaiting description

   Based on Packt Python Design patterns video

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def __call__(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
