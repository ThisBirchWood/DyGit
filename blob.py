import hash

class Blob:
    def __init__(self, data):
        self.data = data
        self.hash = hash.sha1_hash(self.data)
        self.size = len(self.data)