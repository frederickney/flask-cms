import re


def val(array, _v):
    return _v if _v in array else None


def subkey(_dict, key):
    if '.' in key:
        return subkey(_dict[key.split('.')[0]], key.removeprefix("{}.".format(key.split('.')[0])))
    if re.search('\[.*\]', key):
        return val(_dict[key.split('[')[0]], re.search('\[(.*)\]', key).groups()[0])


def extract_fields(_mapper):

    def decorated(func):

        def map(*args, **kwargs):
            _kwargs = {}
            for key, map in _mapper.items():
                if '.' not in key and not re.search('\[.*\]', key):
                    _kwargs[map[0]] = map[1](kwargs[key])
                else:
                    try:
                        _kwargs[map[0]] = map[1](
                            subkey(
                                kwargs[key.split('.')[0]],
                                key.removeprefix("{}.".format(key.split('.')[0]))
                            )
                        )
                    except KeyError:
                        try:
                            _kwargs[map[0]] = map[1](None)
                        except TypeError:
                            _kwargs[map[0]] = None
                        pass

            return func(**_kwargs)

        return map

    return decorated
