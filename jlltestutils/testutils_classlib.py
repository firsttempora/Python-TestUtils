from __future__ import print_function, division, absolute_import


class KeywordCombinations(object):
    @property
    def may_replace(self):
        return self._may_replace

    @may_replace.setter
    def may_replace(self, value):
        if not isinstance(value, bool):
            raise TypeError('KeywordPermutations.may_replace must be a bool')
        else:
            self._may_replace = value

    def __init__(self, **keywords):
        self._keywords = dict()
        self._may_replace = True
        for key, value in keywords.items():
            self.add_keyword(key, *value)

    def add_keyword(self, keyword, *options):
        if keyword in self._keywords and not self.may_replace:
            raise KeyError('{} already defined'.format(keyword))
        else:
            self._keywords[keyword] = options

    def __iter__(self):
        keys = [k for k in self._keywords.keys()]
        dims = [len(self._keywords[k]) for k in keys]
        for i in range(_prod(dims)):
            chk = {k: self._keywords[k][ind] for k, ind in zip(keys, _ind2sub(i, dims))}
            yield chk


def _ind2sub(ind, dims):
    if ind >= _prod(dims):
        raise IndexError('Index {} exceeds max ({}) given the number of elements'.format(ind, _prod(dims)-1))
    sub = [0] * len(dims)
    sub[0] = ind % dims[0]
    for i in range(1, len(dims)):
        place = _prod(dims[:i])
        sub[i] = (ind // place) % dims[i]

    return sub


def _prod(iterable):
    p = iterable[0]
    for i in iterable[1:]:
        p *= i
    return p