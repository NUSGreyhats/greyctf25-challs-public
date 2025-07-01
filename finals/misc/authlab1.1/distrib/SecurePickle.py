import pickle, io

class SecurePickle(pickle.Unpickler):
    def find_class(self, module, name):
        if module != 'builtins' or '.' in name:
            raise KeyError('The pickle is spoilt :(')
        return pickle.Unpickler.find_class(self, module, name)
    # TODO:
    #   build a secure unpicker
    #   currently only accept builtins, so EasyCreds feature doesn't work

def loads(s):
    for word in ('os', 'sys', 'system', 'sh', 'cat', 'import', 'open', 'file', 'globals', 'Creds'):
        if word.encode() in s:
            raise KeyError(f'The pickle is spoilt :(')
    return SecurePickle(io.BytesIO(s)).load()

dumps = pickle.dumps