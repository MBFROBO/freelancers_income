class Processing:
    def __init__(self, data):
        self.data = data

    def process(self):
        # Placeholder for processing logic
        # This method should be overridden in subclasses
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_data(self):
        return self.data