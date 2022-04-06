import pytest
from domain.space import Space, SpaceRoot, SpaceChain, AlreadyMergedError
from anytree.node.exceptions import LoopError


def test_add_space():
    s1 = Space(id="s1", name="name1")
    s2 = Space(id="s2", name="name2", parent=s1)

    assert len(s1.children) == 1
    d = {
        "id": "s1",
        "name": "name1",
        "children": [
            {
                "id": "s2",
                "name": "name2",
                "children": []
            }
        ]
    }
    assert s1.json() == d

    s3 = Space(id="s3", name="name3", parent=s1)
    # s1.add(s3)

    assert len(s1.children) == 2
    d = {
        "id": "s1",
        "name": "name1",
        "children": [
            {
                "id": "s2",
                "name": "name2",
                "children": []
            },
            {
                "id": "s3",
                "name": "name3",
                "children": []
            }
        ]
    }
    assert s1.json() == d
    assert s2.parent == s1
    assert s3.parent == s1


def test_3depth():
    s1 = Space(id="s1", name="name1")
    s2 = Space(id="s2", name="name2", parent=s1)
    s3 = Space(id="s3", name="name3", parent=s2)
    d = {
        "id": "s1",
        "name": "name1",
        "children": [
            {
                "id": "s2",
                "name": "name2",
                "children": [
                    {
                        "id": "s3",
                        "name": "name3",
                        "children": []
                    }
                ]
            }
        ]
    }
    assert s1.json() == d
    assert s3.parent == s2
    assert s2.parent == s1

def test_error_parent_has_same_id():
    s1 = Space(id="s1", name="name1")
    with pytest.raises(LoopError):
        s2 = Space(id="s1", name="name1", parent=s1)


userId = "user"
#
# @pytest.fixture(scope="function")
# def fn():
#     root = SpaceRoot(userId=userId)
#     b    = SpaceBranch(root)
#     yield (root, deepcopy(root), b)
def test_raise_duplicate_id():
    r    = SpaceRoot(userId=userId)
    cmn  = Space("common", id="c1", parent=r)
    with pytest.raises(LoopError):
        Space("common", id="c1", parent=r)

def test_raise_root_set_parent():
    r = SpaceRoot(userId=userId)
    s = Space("s1", id="s1")
    with pytest.raises(ValueError):
        r.parent = s

def test_raise_chain():
    s1 = Space("s1", id="s1")
    s2 = Space("s2", id="s2", parent=s1)
    s3 = Space("s3", id="s3", parent=s1)
    with pytest.raises(ValueError):
        SpaceChain(s1)

    chain  = SpaceChain(Space("root", id="root"))
    with pytest.raises(ValueError):
        chain.extendTail(s1)

    with pytest.raises(ValueError):
        chain.extendHead(s1)

    common  = Space("root2", id="root")
    with pytest.raises(LoopError):
        chain.extendTail(common)

    with pytest.raises(LoopError):
        chain.extendHead(common)


def test_merge():
    chain = SpaceChain.create([
        Space("s1", id="s1"),
        Space("s2", id="s2"),
        Space("s3", id="s3")
    ])

    t1 = Space("s1", id="s1")
    t2 = Space("s2", id="s2", parent=t1)
    t4 = Space("s4", id="s4", parent=t1)

    u1 = Space("s1", id="s1")
    u2 = Space("s2", id="s2", parent=u1)
    u3 = Space("s3", id="s3", parent=u2)
    u4 = Space("s4", id="s4", parent=u1)

    chain.merge(t1)
    assert t1.json() == u1.json()
    with pytest.raises(AlreadyMergedError):
        chain.merge(t1)


def test_merge_extend_head_case():
    chain = SpaceChain.create([
        Space("s0", id="s0"),
        Space("s1", id="s1"),
        Space("s2", id="s2"),
        Space("s3", id="s3")
    ])

    t1 = Space("s1", id="s1")
    t2 = Space("s2", id="s2", parent=t1)
    t4 = Space("s4", id="s4", parent=t1)

    u0 = Space("s0", id="s0")
    u1 = Space("s1", id="s1", parent=u0)
    u2 = Space("s2", id="s2", parent=u1)
    u3 = Space("s3", id="s3", parent=u2)
    u4 = Space("s4", id="s4", parent=u1)

    chain.merge(t1)
    assert t1.root.json() == u0.json()


def test_merge3():
    chain = SpaceChain.create([
        Space("s0", id="s0"),
        Space("s1", id="s1"),
        Space("s2", id="s2"),
        Space("s3", id="s3"),
        Space("s4", id="s4"),
        Space("s5", id="s5"),
        Space("s6", id="s6")
    ])

    t1 = Space("s2", id="s2")
    Space("x", id="x", parent=t1)
    Space("y", id="y", parent=t1)

    u0 = Space("s0", id="s0")
    u1 = Space("s1", id="s1", parent=u0)
    u2 = Space("s2", id="s2", parent=u1)
    u3 = Space("s3", id="s3", parent=u2)
    u4 = Space("s4", id="s4", parent=u3)
    u5 = Space("s5", id="s5", parent=u4)
    u6 = Space("s6", id="s6", parent=u5)
    Space("x", id="x", parent=u2)
    Space("y", id="y", parent=u2)

    chain.merge(t1)
    assert t1.root.json() == u0.json()
