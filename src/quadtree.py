# -*- coding: utf-8 -*-

# Copyright 2016 - 2018: Stefano Mazzucco <stefano AT curso DOT re>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

from itertools import chain

try:
    from functools import reduce
except ImportError:  # pragma: no cover
    pass

__version__ = '1.0.0'
__all__ = ['QuadTree']


class QuadTree(object):
    def __init__(self, bbox, max_items=10, max_depth=10):
        """Initialize a quadtree.

        :param bbox: bounding box, 4-iterable containing the bottom-left and
                     top right coordinates (easting, northing).
                     E.g. [0, 0, 10, 10]
        :param max_items: the maximum number of items that can be
                          held in the bounding box before the
                          quadtree splits it into four smaller ones
                          (children quadtrees)
        :param max_depth: the maximum depth of the quadtree. Once this
                          value is reached, the instance will split no
                          more and all elements will be stored in the
                          lowest level quadrant

        """
        _validate_bbox(bbox)
        self.max_items = max_items
        self.max_depth = int(max_depth) if max_depth >= 0 else 0
        self.bbox = bbox
        self.contents = []
        self.children = ()

    def insert(self, element):
        """Insert an element in the quadtree. If the
        element's coordinates are not within the quadtree's
        bounding box, the insertion will fail.

        Note that an element with coordinates x, y is
        considered to be inside the bounding box if
        x0 <= x < x1 and y0 <= y < y1.

        :param element: 3-iterable, the first item
                        is the element's "value"
                        while the second and third
                        are the easting and northing
                        respectively.

        :returns: True or False depending on whether
                  the insertion succeeded.

        """
        if not _inside(element, self.bbox):
            return False
        if self.children:
            for child in self.children:
                result = child.insert(element)
                if result:
                    self.contents = []
                    return result
        self.contents.append(element)
        if len(self.contents) > self.max_items and self.max_depth > 0:
            self._split()
        return True

    def _split(self):
        x0, y0, x1, y1 = self.bbox
        xm = (x1 - x0) / 2
        ym = (y1 - y0) / 2

        sw = x0, y0, x0 + xm, y0 + ym
        se = x0 + xm, y0, x1, y0 + ym
        ne = x0 + xm, y0 + ym, x1, y1
        nw = x0, y0 + ym, x0 + xm, y1
        self.children = (QuadTree(sw, self.max_items, self.max_depth - 1),
                         QuadTree(se, self.max_items, self.max_depth - 1),
                         QuadTree(ne, self.max_items, self.max_depth - 1),
                         QuadTree(nw, self.max_items, self.max_depth - 1))

        while self.contents:
            element = self.contents.pop()
            for child in self.children:
                if child.insert(element):
                    break

    def intersect(self, bbox):
        """Return a list of elements of the quadtree
        that intersect the given bounding box.

        :param bbox: 4-iterable containing the bottom-left and
                     top right coordinates (easting, northing).
                     E.g. [0, 0, 10, 10]

        :returns: a set of intersecting elements (may be empty)

        """
        if not self._intersects_bbox(bbox):
            return set()
        if self.children:
            return reduce(
                lambda x, y: x.union(y),
                (c.intersect(bbox) for c in self.children),
                set())
        return set(element for element in self.contents
                   if _inside(element, bbox))

    def _intersects_bbox(self, bbox):
        x0, y0, x1, y1 = self.bbox
        xi0, yi0, xi1, yi1 = bbox

        vertical_intersect = not (yi0 >= y1 or yi1 < y0)
        horizontal_intersect = not (xi0 >= x1 or xi1 < x0)

        return vertical_intersect and horizontal_intersect

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self.bbox,
            self.max_items,
            self.max_depth)

    def __contains__(self, element):
        return (element in self.contents or
                any(element in qt for qt in self.children))

    def __iter__(self):
        if self.contents:
            return (element for element in self.contents)
        else:
            return chain.from_iterable(self.children)

    def __len__(self):
        if self.contents:
            return len(self.contents)
        else:
            return sum(len(child) for child in self.children)

    def __getitem__(self, key):
        """Will return the first element containing whose
        value equals key.
        """
        if self.children:
            item = None
            for child in self.children:
                try:
                    item = child[key]
                    break
                except KeyError:
                    continue
            if item is None:
                raise KeyError(key)
            return item
        items = [el for el in self.contents if el[0] == key]
        if not items:
            raise KeyError(key)
        return items[0]


def _inside(element, bbox):
    """Test whether an element is inside a bounding box.

    :param element: 3-iterable, the first item
                    is the element's "value"
                    while the second and third
                    are the easting and northing
                    respectively.

    :param bbox: 4-iterable containing the bottom-left and
                 top right coordinates (easting, northing).
                 E.g. [0, 0, 10, 10]

    """
    x0, y0, x1, y1 = bbox
    _, x, y = element
    return x0 <= x < x1 and y0 <= y < y1


def _validate_bbox(bbox):
    x0, y0, x1, y1 = bbox
    x_ok = x0 < x1
    y_ok = y0 < y1
    if not x_ok and not y_ok:
        raise ValueError(
            'Invalid bounding box: {}'.format(bbox))
