import hashlib, pickle

def serialize_object(obj):
    return pickle.dumps(obj)

def deserialize_object(obj):
    return pickle.loads(obj)

def sha1_hash(string):
    """ Returns hash value of string input """
    sha1 = hashlib.sha1()

    sha1.update(string)
    return sha1.hexdigest()