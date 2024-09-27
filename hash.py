import hashlib, pickle

# BUF_SIZE is totally arbitrary, change for your app!

def serialize_object(obj):
    return pickle.dumps(obj)

def sha1_hash(s_obj):
    sha1 = hashlib.sha1()

    sha1.update(s_obj)
    return sha1.hexdigest()