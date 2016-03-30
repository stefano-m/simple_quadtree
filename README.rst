.. image:: https://travis-ci.org/stefano-m/simple_quadtree.svg?branch=master
    :target: https://travis-ci.org/stefano-m/simple_quadtree

.. image:: https://codecov.io/github/stefano-m/simple_quadtree/coverage.svg?branch=master
    :target: https://codecov.io/github/stefano-m/simple_quadtree?branch=master

=================
 Simple QuadTree
=================
A simple QuadTree class implemented in pure Python.

At the moment, only point elements can be inserted.

A point element is a 3-iterable whose 1st item is the
element's value (anything really) while the second and third
are respectively the easting (x axis) and northing (y axis).

A bounding box is defined as a 4-iterable that contains the bottom-left
and top-right spatial coordinates. E.g. ``bounding_box = (0, 4, 10, 20)``.

See also https://en.wikipedia.org/wiki/Quadtree

Highlights
==========

The ``insert`` method will return ``True`` or ``False`` depending on whether the
insertion has been successful. E.g. inserting a point outside the QuadTree's
bounding box will fail.

The ``intersect`` method will return a set of all elements that intersect the
given bounding box.

QuadTree implements ``__getitem__`` so that elements can be easily retrieved.
Trying to get a missing element will raise a ``KeyError`` similarly to what happens
with dictionaries.

Also, ``__contains__`` is implemented to allow users to use the ``in`` keyword to
check whether an element has been inserted.

The ``children`` attribute of a QuadTree is a tuple that, when not empty,
represents the SW, SE, NE, NW quadrants respectively.


Example usage in Python 3
=========================

  >>> from quadtree import QuadTree
  >>> bbox = (-5, -5, 5, 5)
  >>> q = QuadTree(bbox)
  >>> print(q)
  QuadTree((-5, -5, 5, 5), 10, 10)
  >>> q.insert(('element 1', 0, 0))
  True
  >>> q['element 1']
  ('element 1', 0, 0)
  >>> ('element 1', 0, 0) in q
  True
  >>> q.insert(('element 2', -1, -1))
  True
  >>> q.insert(('element 3', 50, 50))
  False
  >>> sorted(q.intersect (bbox))
  [('element 1', 0, 0), ('element 2', -1, -1)]
  >>> sorted(q.intersect((-0.5, -0.5, 2, 2)))
  [('element 1', 0, 0)]

Missing features:
=================
* deletion
* dealing with shapes
* merging
* latitude/longitude
* persistence

Motivation
==========
Implementing a quadtree was a long-standing task of mine. There are a number
of other implementations on PyPI, some in pure Python, other that include binary
extensions. This implementation does not claim to be the fastest or the "bestest",
but I think it's good enough for experimenting and possibly to use in production
since it's very simple.

For example, the QuadTree could be used to build a spatial index to store
information about postcodes and their coordinates so that one could retrieve all
landmarks within a given distance to a postcode.


Other implementations on PyPI can be found with the search URL below:

https://pypi.python.org/pypi?%3Aaction=search&term=quadtree&submit=search
