"""Tests for to_quads() and the Graph/ConjunctiveGraph/Dataset add_many() methods."""

from __future__ import annotations

from rdflib import ConjunctiveGraph, Dataset, Graph, URIRef
from rdflib.graph import to_quads

S = URIRef("urn:s")
P = URIRef("urn:p")
O = URIRef("urn:o")


class TestToQuads:
    def test_triple_uses_default_context(self) -> None:
        ctx = Graph(identifier=URIRef("urn:ctx"))
        result = list(to_quads([(S, P, O)], ctx))
        assert result == [(S, P, O, ctx)]

    def test_quad_is_yielded_unchanged(self) -> None:
        ctx = Graph(identifier=URIRef("urn:ctx"))
        other = Graph(identifier=URIRef("urn:other"))
        result = list(to_quads([(S, P, O, other)], ctx))
        assert result == [(S, P, O, other)]

    def test_mixed_triples_and_quads(self) -> None:
        ctx = Graph(identifier=URIRef("urn:ctx"))
        other = Graph(identifier=URIRef("urn:other"))
        items = [(S, P, O), (S, P, O, other)]
        result = list(to_quads(items, ctx))
        assert result == [(S, P, O, ctx), (S, P, O, other)]

    def test_empty_input(self) -> None:
        ctx = Graph(identifier=URIRef("urn:ctx"))
        assert list(to_quads([], ctx)) == []

    def test_multiple_triples_all_get_default_context(self) -> None:
        ctx = Graph(identifier=URIRef("urn:ctx"))
        s2, p2, o2 = URIRef("urn:s2"), URIRef("urn:p2"), URIRef("urn:o2")
        result = list(to_quads([(S, P, O), (s2, p2, o2)], ctx))
        assert result == [(S, P, O, ctx), (s2, p2, o2, ctx)]

    def test_result_is_lazy_generator(self) -> None:
        """to_quads should return a generator, not a list."""
        ctx = Graph(identifier=URIRef("urn:ctx"))
        import types

        result = to_quads([(S, P, O)], ctx)
        assert isinstance(result, types.GeneratorType)


class TestGraphAddMany:
    def test_triple_uses_self_as_context(self) -> None:
        g = Graph(identifier=URIRef("urn:g"))
        g.add_many([(S, P, O)])
        assert (S, P, O) in g

    def test_quad_with_matching_context_is_added(self) -> None:
        g = Graph(identifier=URIRef("urn:g"))
        g.add_many([(S, P, O, g)])
        assert (S, P, O) in g

    def test_quad_with_non_matching_context_is_skipped(self) -> None:
        g = Graph(identifier=URIRef("urn:g"))
        other = Graph(identifier=URIRef("urn:other"))
        g.add_many([(S, P, O, other)])
        assert (S, P, O) not in g

    def test_mixed_triple_and_matching_quad(self) -> None:
        g = Graph(identifier=URIRef("urn:g"))
        s2, p2, o2 = URIRef("urn:s2"), URIRef("urn:p2"), URIRef("urn:o2")
        g.add_many([(S, P, O), (s2, p2, o2, g)])
        assert (S, P, O) in g
        assert (s2, p2, o2) in g

    def test_returns_self(self) -> None:
        g = Graph()
        assert g.add_many([(S, P, O)]) is g

    def test_empty_input(self) -> None:
        g = Graph()
        g.add_many([])
        assert len(g) == 0


class TestConjunctiveGraphAddMany:
    def test_triple_goes_to_default_context(self) -> None:
        cg = ConjunctiveGraph()
        cg.add_many([(S, P, O)])
        assert (S, P, O) in cg.default_context

    def test_quad_goes_to_named_context(self) -> None:
        cg = ConjunctiveGraph()
        ctx = cg.get_context(URIRef("urn:ctx"))
        cg.add_many([(S, P, O, ctx)])
        assert (S, P, O) in ctx
        assert (S, P, O) not in cg.default_context

    def test_mixed_triple_and_quad(self) -> None:
        cg = ConjunctiveGraph()
        ctx = cg.get_context(URIRef("urn:ctx"))
        s2, p2, o2 = URIRef("urn:s2"), URIRef("urn:p2"), URIRef("urn:o2")
        cg.add_many([(S, P, O), (s2, p2, o2, ctx)])
        assert (S, P, O) in cg.default_context
        assert (s2, p2, o2) in ctx

    def test_returns_self(self) -> None:
        cg = ConjunctiveGraph()
        assert cg.add_many([(S, P, O)]) is cg

    def test_empty_input(self) -> None:
        cg = ConjunctiveGraph()
        cg.add_many([])
        assert len(cg) == 0


class TestDatasetAddMany:
    def test_triple_goes_to_default_context(self) -> None:
        ds = Dataset()
        ds.add_many([(S, P, O)])
        assert (S, P, O) in ds.default_context

    def test_quad_goes_to_named_context(self) -> None:
        ds = Dataset()
        ctx = ds.graph(URIRef("urn:ctx"))
        ds.add_many([(S, P, O, ctx)])
        assert (S, P, O) in ctx
        assert (S, P, O) not in ds.default_context

    def test_returns_self(self) -> None:
        ds = Dataset()
        assert ds.add_many([(S, P, O)]) is ds
