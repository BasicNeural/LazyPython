_print = print


class Effect(object):
    def __init__(self, f, a, w):
        self.f = f
        self.a = a
        self.w = w

    def excute(self):
        return self.f(*self.a, **self.w)

    def map(self, f):
        e = Effect(self.f, self.a, self.w)
        return ChainEffect([e, f])


class ChainEffect(object):
    def __init__(self, effect_list):
        self.effects = effect_list

    def map(self, f):
        self.effects.append(f)
        return self

    def excute(self):
        value = self.effects[0].excute()
        for effect in self.effects[1:]:
            value = effect(value).excute()
        return value


def lazy(function):
    def f(*arg, **kwargs):
        return Effect(function, arg, kwargs)
    return f


@lazy
def print(*arg, **kwargs):
    _print(*arg, **kwargs)
