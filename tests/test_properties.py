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
