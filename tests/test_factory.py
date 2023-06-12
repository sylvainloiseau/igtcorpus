from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph
from igtcorpus.corpusobj_factory import CorpusFactory
import pytest

class TestFactory:

    def test_raise_error_empty(x):
        f = CorpusFactory()
        with pytest.raises(Exception):
          c = f.get_corpus()

    def test_factory_one_text(x):
        f = CorpusFactory()
        f.start_unit(Corpus)
        f.start_unit(Text)
        f.end_unit(Text)
        f.end_unit(Corpus)
        c = f.get_corpus()
        assert Corpus({}, [Text({}, [])]) == c

    def test_get_corpus_raise_unfinished_unit(x):
        f = CorpusFactory()
        f.start_unit(Corpus)
        f.start_unit(Text)
        with pytest.raises(Exception):
          c = f.get_corpus()

    def test_open_unit_unkown_type_raise_error(x):
        f = CorpusFactory()
        f.start_unit(Corpus)
        with pytest.raises(Exception):
          f.start_unit(str)

    def test_closing_unmatching_unit(x):
        f = CorpusFactory()
        f.start_unit(Corpus)
        f.start_unit(Text)
        with pytest.raises(Exception):
          f.end_unit(Paragraph)

    @pytest.fixture
    def tiny_corpus_factory(x):
      f = CorpusFactory()
      f.start_unit(Corpus)
      f.start_unit(Text)
      f.start_unit(Paragraph)
      f.start_unit(Sentence)
      f.start_unit(Word)
      f.createMorph({'tx': 'a', 'gl': '1SG'})
      f.end_unit(Word)
      f.start_unit(Word)
      f.createMorph({'tx': 'mami', 'gl': 'pig'})
      f.createMorph({'tx': '-mo', 'gl': '-CL'})
      f.end_unit()
      f.start_unit(Word)
      f.createMorph({'tx': 'iefi', 'gl': 'shoot'})
      f.createMorph({'tx': '-mwii', 'gl': '-1SG.M'})
      f.end_unit(Word)
      f.end_unit(Sentence)
      f.end_unit(Paragraph)
      f.end_unit(Text)
      f.end_unit(Corpus)
      return f

    def test_tiny_corpus_factory(x, tiny_corpus_factory):
      pass

    def test_factory_morph_property(x, tiny_corpus_factory):
      c = tiny_corpus_factory.get_corpus()
      assert 1 == len(c.get_sub_units())
      assert Morph({'tx': 'a', 'gl': '1SG'}) == c.get_sub_units()[0].get_sub_units()[0].get_sub_units()[0].get_sub_units()[0].get_sub_units()[0]
      assert Morph({'tx': 'a', 'gl': '1SG'}) == c.get(Text)[0].get(Paragraph)[0].get(Sentence)[0].get(Word)[0].get(Morph)[0]

#  def test_occ_nbr_for_level(factory):
#
#    assert factory.get_occ_nbr_for_level(Morph) == 2
#    assert factory.get_occ_nbr_for_level(Word) == 1
#    assert factory.get_occ_nbr_for_level(Sentence) == 1
#    assert factory.get_occ_nbr_for_level(Paragraph) == 1
#    assert factory.get_occ_nbr_for_level(Text) == 1
#    
#    
#  def test_property_for_level(factory):
#    factory.createMorph({'tx': 'aio', 'gl': 'alas'})
#    factory.end_unit(Word, {'pos': 'INTER'})
#    factory.end_unit(Sentence, {'type': 'matrix'})
#    factory.end_unit(Paragraph, {'speaker': 'x'})
#    factory.end_unit(Text)
#
#    mp = factory.get_properties_for_level(Morph)
#    assert set(mp.keys()) == set('tx', 'gl')
#
#    wp = factory.get_properties_for_level(Word)
#    assert set(wp.keys()) == set('pos')
#
#    sp = factory.get_properties_for_level(Sentence)
#    assert set(sp.keys()) == set('type')
#    
#    pp = factory.get_properties_for_level(Paragraph)
#    assert set(pp.keys()) == set('speaker')
#
#    
