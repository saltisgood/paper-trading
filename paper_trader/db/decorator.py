def primary_key(*key_names):
    def impl(clazz):
        clazz._primary_key = [k for k in key_names]
        return clazz
    return impl

def _get_primary_keys(clazz):
    assert hasattr(clazz, '_primary_key')
    return clazz._primary_key
