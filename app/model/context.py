class Context:
    """
    Context class to hold the current state of the application.
    This can be used to store user preferences, settings, or any other
    information that needs to be accessed globally within the application.
    """
    
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def clear(self):
        self.data.clear()