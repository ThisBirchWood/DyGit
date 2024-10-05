import hashlib, pickle

def serialize_object(obj):
    return pickle.dumps(obj)

def deserialize_object(obj):
    return pickle.loads(obj)

def sha1_hash(s_obj):
    sha1 = hashlib.sha1()

    sha1.update(s_obj)
    return sha1.hexdigest()