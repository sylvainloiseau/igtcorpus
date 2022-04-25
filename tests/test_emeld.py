from igttools.igt import Corpus
from igttools.emeld import Emeld
import pprint as pp
import pytest
from collections import OrderedDict
import xmltodict


class TestEmeld():

  def test_regularize(foo):
    doc = """<?xml version="1.0" encoding="UTF-8"?>
<document>
  <interlinear-text>
    <item type="source">tests/data/BEJ_MV_CONV_01_RICH.EAF</item>
    <paragraphs>
      <paragraph>
        <item type="speaker">SP1</item>
        <phrases>
          <phrase>
            <item type="ft">In the old days</item>
            <item type="participant">SP1</item>
            <item type="id">a4933</item>
            <words>
              <word>
                <morphemes>
                  <morph>
                    <item type="txt">suːr</item>
                    <item type="gls">before</item>
                    <item type="id">a15527</item>
                  </morph>
                  <morph>
                    <item type="txt">suːr</item>
                    <item type="gls">before</item>
                    <item type="id">a15527</item>
                  </morph>
                </morphemes>
              </word>
            </words>
          </phrase>
        </phrases>
      </paragraph>
    </paragraphs>
  </interlinear-text>
</document>
    """
    d = xmltodict.parse(doc)
    text = Emeld._regularize_xmltodict(d, level_index=-1)
    assert isinstance(text["document"]["interlinear-text"], list)
    assert len(text["document"]["interlinear-text"]) == 1
    assert isinstance(text["document"]["interlinear-text"][0]["paragraphs"]["paragraph"], list)
    assert len(text["document"]["interlinear-text"][0]["paragraphs"]["paragraph"][0]["phrases"]["phrase"][0]["words"]["word"][0]["morphemes"]["morph"]) == 2

  def test_convert(foo):
    doc = """<?xml version="1.0" encoding="UTF-8"?>
<document>
  <interlinear-text>
    <item type="source">tests/data/BEJ_MV_CONV_01_RICH.EAF</item>
    <paragraphs>
      <paragraph>
        <item type="speaker">SP1</item>
        <phrases>
          <phrase>
            <item type="ft">In the old days</item>
            <item type="participant">SP1</item>
            <item type="id">a4933</item>
            <words>
              <word>
                <morphemes>
                  <morph>
                    <item type="txt">suːr</item>
                    <item type="gls">before</item>
                    <item type="id">a15527</item>
                  </morph>
                </morphemes>
              </word>
            </words>
          </phrase>
        </phrases>
      </paragraph>
    </paragraphs>
  </interlinear-text>
</document>
    """
    d = xmltodict.parse(doc)
    corpus = Emeld._regularize_xmltodict(d, level_index=-1)
    corpus = Emeld._turn_xmltodict_to_igt(corpus, level_index=-1)
    assert isinstance(corpus, Corpus)

  def test_readEmeld_not_valid(foo):
      with pytest.raises(Exception):
          c:Corpus = Emeld.read("tests/data/test.not_valid.emeld.xml")

  def test_readEmeld(foo):
    c:Corpus = Emeld.read("tests/data/test.emeld.xml")
  
  def test_readWriteEmeld(foo):
    file_in = "tests/data/tiny.emeld.xml"
    file_out = "tests/data/tiny.emeld.xml.out"
    igt:Corpus = Emeld.read(file_in)
    Emeld.write(igt, file_out)
    igt_2: Corpus = Emeld.read(file_out)
    assert igt == igt_2
  
