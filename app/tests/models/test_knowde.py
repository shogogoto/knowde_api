import pytest

from domain.core.description import Description
from domain.core.defenition import Defenition
from domain.core import Knowde, KnowdeLink, KnowdeGraph


def test_create_with_sorce_link():
    k1 = Knowde(id="k1", name="name1")
    k2 = Knowde(id="k2", name="name2", sources=[k1])
    assert k2.links == set([KnowdeLink(k1.id, k2.id)])
    k3 = Knowde(id="k3", name="name3", sources=[k1, k2])
    assert k3.links == set([
        KnowdeLink(k1.id, k3.id),
        KnowdeLink(k2.id, k3.id)
    ])

def test_duplicate_link():
    k1 = Knowde(id="k1", name="name1")
    k2 = Knowde(id="k2", name="name2", sources=[k1])
    k2.linkFrom(k1)
    assert k2.links == set([KnowdeLink(k1.id, k2.id)])


def test_raise_link_src_eq_dest():
    with pytest.raises(ValueError):
        KnowdeLink(1, 1)


def test_graph():
    print("####################### test_graph")
    k1 = Knowde(id="k1", name="name1")
    k2 = Knowde(id="k2", name="name2", sources=[k1])
    k3 = Knowde(id="k3", name="name3", sources=[k1, k2])
    g = KnowdeGraph([k1, k2, k3])
    # Knowde(id="k1", **{"name": "xxx"})
    # print(g.nodes)
    # print(g.links)
    # g.nodes == [k1, k2, k3]
    # g.edges == [("k1", "k2"), ("k1", "k3"), ("k2", "k3")]
# def test_resolve_desctiption():
#     id = "ID"
#     desc = Description("xxx[[{}]]xxx", id)
#     dfn = Defenition(**{id: "NAME"})
#
#     d = {
#         "description": "xxx[[ID]]xxx",
#         "defenition": {
#             "ID": "NAME"
#         }
#     }
#     # print(desc.value)
