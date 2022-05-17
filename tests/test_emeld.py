from igtcorpus.igt import Corpus, Text, Paragraph
from igtcorpus.emeld import Emeld
import pytest
import lxml.etree as ET


class TestEmeld():

  def test_parse1(foo):
    doc_string = """<root><document>
    <interlinear-text>
    <item type="source">x</item>
    </interlinear-text>
    </document>
    </root>
    """
    doc = ET.fromstring(doc_string)
    res = Emeld._parse_emeld(doc, -1)
    assert Corpus({}, [Text({'source': 'x'}, [])]) == res

  def test_parse2(foo):
    doc_string = """<root><document>
    <interlinear-text>
    <item type="source">x</item>
    <paragraphs>
    <paragraph>
    <item type="x">z</item>
    </paragraph>
    <paragraph>
    <item type="x">y</item>
    </paragraph>
    </paragraphs>
    </interlinear-text>
    </document>
    </root>
    """
    doc = ET.fromstring(doc_string)
    res = Emeld._parse_emeld(doc, -1)
    assert Corpus({}, [Text({'source': 'x'}, [Paragraph({'x':'z'}, []), Paragraph({'x':'y'}, [])])]) == res

  def test_parse(foo):
    doc_string = """<root><document>
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
</root>
    """
    doc = ET.fromstring(doc_string)
    res = Emeld._parse_emeld(doc, -1)

  def test_parse_with_lang(foo):
    doc_string = """<root><document>
    <interlinear-text>
    <item type="source">x</item>
    <paragraphs>
    <paragraph>
    <item type="x" lang="tpi">z</item>
    </paragraph>
    <paragraph>
    <item type="x" lang="en">y</item>
    </paragraph>
    </paragraphs>
    </interlinear-text>
    </document>
    </root>
    """
    doc = ET.fromstring(doc_string)
    res = Emeld._parse_emeld(doc, -1)
    assert Corpus({}, [Text({'source': 'x'}, [Paragraph({'x.tpi':'z'}, []), Paragraph({'x.en':'y'}, [])])]) == res

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
  
  def test_readWriteEmeldWLang(foo):
    file_in = "tests/data/tiny.emeld.lang.xml"
    file_out = "tests/data/tiny.emeld.lang.xml.out"
    igt:Corpus = Emeld.read(file_in)
    Emeld.write(igt, file_out)
    igt_2: Corpus = Emeld.read(file_out)
    assert igt == igt_2
