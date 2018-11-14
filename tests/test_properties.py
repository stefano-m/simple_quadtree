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

from hypothesis import given, strategies as st

from quadtree import QuadTree

X0 = -10
Y0 = -10
X1 = 10
Y1 = 10
BBOX = (X0, Y0, X1, Y1)


@given(
    st.tuples(st.text(),
              st.integers(X0, X1 - 1),
              st.integers(Y0, Y1 - 1)))
def test_insert_inside(element):
    qt = QuadTree(BBOX)
    assert qt.insert(element)


@given(
    st.tuples(st.text(),
              st.integers(None, X0 - 1),
              st.integers(None, Y0 - 1)))
def test_insert_outside1(element):
    qt = QuadTree(BBOX)
    assert not qt.insert(element)


@given(
    st.tuples(st.text(),
              st.integers(X1, None),
              st.integers(Y1, None)))
def test_insert_outside2(element):
    qt = QuadTree(BBOX)
    assert not qt.insert(element)
