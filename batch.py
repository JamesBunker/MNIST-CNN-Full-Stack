# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _batch
else:
    import _batch

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class MiniBatches(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    inputs = property(_batch.MiniBatches_inputs_get, _batch.MiniBatches_inputs_set)
    targets = property(_batch.MiniBatches_targets_get, _batch.MiniBatches_targets_set)
    patterns = property(_batch.MiniBatches_patterns_get, _batch.MiniBatches_patterns_set)
    batchsize = property(_batch.MiniBatches_batchsize_get, _batch.MiniBatches_batchsize_set)
    scaledown = property(_batch.MiniBatches_scaledown_get, _batch.MiniBatches_scaledown_set)
    batches = property(_batch.MiniBatches_batches_get, _batch.MiniBatches_batches_set)
    nextbatch = property(_batch.MiniBatches_nextbatch_get, _batch.MiniBatches_nextbatch_set)
    order = property(_batch.MiniBatches_order_get, _batch.MiniBatches_order_set)

    def __init__(self, input, output, batch_size, scaledown):
        _batch.MiniBatches_swiginit(self, _batch.new_MiniBatches(input, output, batch_size, scaledown))

    def restart(self):
        return _batch.MiniBatches_restart(self)

    def next(self):
        return _batch.MiniBatches_next(self)

    def __iter__(self):
        return _batch.MiniBatches___iter__(self)

    def __next__(self):
        return _batch.MiniBatches___next__(self)
    __swig_destroy__ = _batch.delete_MiniBatches

# Register MiniBatches in _batch:
_batch.MiniBatches_swigregister(MiniBatches)
class MiniBatch(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    inputs = property(_batch.MiniBatch_inputs_get, _batch.MiniBatch_inputs_set)
    targets = property(_batch.MiniBatch_targets_get, _batch.MiniBatch_targets_set)
    __swig_destroy__ = _batch.delete_MiniBatch

    def __init__(self):
        _batch.MiniBatch_swiginit(self, _batch.new_MiniBatch())

# Register MiniBatch in _batch:
_batch.MiniBatch_swigregister(MiniBatch)

def newminibatches(inputs, targets, batchsize, scaledown):
    return _batch.newminibatches(inputs, targets, batchsize, scaledown)

def randrange(min, max):
    return _batch.randrange(min, max)

def shuffle(minibatches_ptr):
    return _batch.shuffle(minibatches_ptr)

def restartminibatches(mbs):
    return _batch.restartminibatches(mbs)

def newminibatch(mbs, batchsize):
    return _batch.newminibatch(mbs, batchsize)

def nextminibatch(minibatches_ptr):
    return _batch.nextminibatch(minibatches_ptr)

def freeminibatches(minibatches_ptr):
    return _batch.freeminibatches(minibatches_ptr)

def freeminibatch(mb):
    return _batch.freeminibatch(mb)

