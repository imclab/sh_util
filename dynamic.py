#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Real-world use case:
--------------------

class MyModel(
    MainModel,
    DynamicallyGenerateTransformedAttributes(str, '_str', 'id', 'user_id')
):
    def __init__(self, id, user_id):
        self.id = id
        self.user_id = user_id

u = MyModel(29, 30)
u.id = 29
u.id_str = '29'
u.user_id = 30
u.user_id_str = '30'

--------------------
The "<attr>_str" class properties are dynamically defined and attached with the
declaration of class `User`, so I don't have to put each of the _str functions
in manually.
"""

__author__ = 'Jay Taylor [@jtaylor]'


def DynamicallyGenerateTransformedAttributes(transformFn, suffix, *attributes):
    """
    Function which dynamically generates a class with "foo_<suffix>" properties
    which apply and return the transformed value of "foo" after passing it
    through the mapping function.

    @param transformFn Function which takes the value of a given instance
        attribute and returns the transformed value.

    @param suffix String to append to attribute name to form new attribute name,
        or a function which when provided with an attr name produces another
        string.

    @param *attributes Attribute names to dynamically generate field transforms
        for.

    This is intended to make it easy to have programmatically transformed
    attributes automatically generated for any class.


    Example usage/Unit-test:
    ========================

    # Utility function to obtain an objects string representation and type.
    >>> valueAndType = lambda x: '{0}/{1}'.format(x, type(x))

    # Test case where the ``suffix`` is a string ('_str'):
    >>> class TestStringSuffix(
    ...     DynamicallyGenerateTransformedAttributes(str, '_str', 'id', 'foo')
    ... ):
    ...     def __init__(self, id, foo):
    ...         self.id = id
    ...         self.foo = foo

    >>> t = TestStringSuffix(30, 'bar')

    >>> print 'id: {0}, id_str: {1}'.format(
    ...     valueAndType(t.id),
    ...     valueAndType(t.id_str)
    ... )
    id: 30/<type 'int'>, id_str: 30/<type 'str'>

    >>> print 'foo: {0}, foo_str: {1}'.format(
    ...     valueAndType(t.id),
    ...     valueAndType(t.id_str)
    ... )
    foo: bar/<type 'str'>, foo_str: bar/<type 'str'>

    # Test case where the ``suffix`` is a function:
    >>> suffixFn = lambda attr: attr[::-1] # Reverse the attribute name.

    >>> txFn = lambda x: str(x)[::-1] # Output is reversed string of input.

    >>> class TestFunctionSuffix(
    ...     DynamicallyGenerateTransformedAttributes(txFn, suffixFn, 'id', 'foo')
    ... ):
    ...     def __init__(self, id, foo):
    ...         self.id = id
    ...         self.foo = foo

    >>> t = TestFunctionSuffix(30, 'bar')

    >>> print 'id: {0}, di: {1}'.format(
    ...     valueAndType(t.id),
    ...     valueAndType(t.di)
    ... )
    id: 30/<type 'int'>, di: 03/<type 'str'>

    >>> print 'foo: {0}, oof: {1}'.format(
    ...     valueAndType(t.foo),
    ...     valueAndType(t.oof)
    ... )
    foo: bar/<type 'str'>, oof: rab/<type 'str'>
    """

    class GeneratedClass(object):
        """Class which will have properties dynamically set on it."""
        pass

    def generateTransformedProperty(attr):
        """
        Generate and return a property function to access the transformation of
        the named attribute.
        """
        @property
        def f(self):
            """Generated property function to alias attribute."""
            return transformFn(getattr(self, attr))
        return f

    # Generate and attach "suffix" property alias for each specified attribute.
    for a in attributes:
        setattr(
            GeneratedClass,
            '{0}{1}'.format(a, suffix) if isinstance(suffix, str) or \
                isinstance(suffix, unicode) else suffix(a),
            generateTransformedProperty(a)
        )

    return GeneratedClass


def WithStrAttrs(*attributes):
    """Convenience method."""
    return DynamicallyGenerateTransformedAttributes(str, '_str', *attributes)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

