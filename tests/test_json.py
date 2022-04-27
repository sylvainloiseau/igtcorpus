from igttools.igt import Corpus, Text
from igttools.emeld import Emeld
from igttools.json import EmeldJson
import pprint as pp
import pytest

class TestToJson():

  def test_walk_corpus(foo):
    c:Corpus = Emeld.read("tests/data/test.emeld.xml")
    j = EmeldJson._walk_corpus(c, 0)
    if c.units is not None:
        assert len(c.units) == len(j["interlinear-text"])
    # number of sentences of the first paragraph of the first text
    assert len(c.units[0].units[0].units) == len(j["interlinear-text"][0]["paragraph"][0]["phrase"])

  def test_dicttoLingUnit(foo):
    d = {
       'item' : {},
      'interlinear-text': [
         {
            'item': {
              'id': 'foo'
            },
            'paragraph' : []
         },
         {
            'item': {
              'id': 'bar'
            },
            'paragraph' : []
         }
      ]
    }
    c: Corpus = EmeldJson._dicttoLingUnit(d, -1)
    assert c == Corpus({}, [Text({'id':'foo'}, []), Text({'id':'bar'}, [])])

  def test_write_json_tiny(foo):
    c:Corpus = Emeld.read("tests/data/tiny.emeld.xml")
    out = "tests/data/tiny.emeld.json.out"
    EmeldJson.write(c, out)
    newc: Corpus = EmeldJson.read(out)
    assert c == newc

  def test_write_json(foo):
    c:Corpus = Emeld.read("tests/data/test.emeld.xml")
    out = "tests/data/test.emeld.json.out"
    EmeldJson.write(c, out)
    newc: Corpus = EmeldJson.read(out)
    assert c == newc

    