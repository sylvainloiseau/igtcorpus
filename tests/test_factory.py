from igtcorpus.igt import Corpus, Text, Paragraph, Sentence, Word, Morph
from igtcorpus.factory import CorpusFactory
import pytest

class TestFactory():

  def test_factory(foo):
    f = CorpusFactory()
    f.createMorph({'tx': 'a', 'gl': '1SG'})
    f.end_unit(Word)
    f.createMorph({'tx': 'mami', 'gl': 'pig'})
    f.createMorph({'tx': '-mo', 'gl': '-CL'})
    f.end_unit(Word)
    f.createMorph({'tx': 'iefi', 'gl': 'shoot'})
    f.createMorph({'tx': '-mwii', 'gl': '-1SG.M'})
    f.end_unit(Word)
    f.end_unit(Sentence)
    f.end_unit(Paragraph)
    f.end_unit(Text)
    c: Corpus = f.get_corpus()

    assert 1 == len(c.get_sub_units())
    assert Morph({'tx': 'a', 'gl': '1SG'}) == c.get_sub_units()[0].get_sub_units()[0].get_sub_units()[0].get_sub_units()[0].get_sub_units()[0]

