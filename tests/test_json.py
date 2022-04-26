from igttools.igt import Corpus
from igttools.emeld import Emeld
from igttools.json import ToJson
import pprint as pp
import pytest

class TestToJson():

  def test_walk_corpus(foo):
    c:Corpus = Emeld.read("tests/data/test.emeld.xml")
    j = ToJson.walk_corpus(c, 0)
    if c.units is not None:
        assert len(c.units) == len(j["interlinear-text"])

    # number of sentences of the first paragraph of the first text
    assert len(c.units[0].units[0].units) == len(j["interlinear-text"][0]["paragraph"][0]["phrase"])

  def test_write_json(foo):
    c:Corpus = Emeld.read("tests/data/test.emeld.xml")
    ToJson.to_json(c, "tests/data/test.emeld.json.out")
  