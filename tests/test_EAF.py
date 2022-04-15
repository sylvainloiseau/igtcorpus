from igttools.Elan2IGT import EAF2IGT
from igttools.IGT import IGT
from igttools.emeld import Emeld
import pprint as pp
import pytest

class TestEAF():

  def test_eaf_file(foo):
    obj = EAF2IGT("tests/data/BEJ_MV_CONV_01_RICH.EAF")
    #pp.pprint(obj.paragraphs)
    igt = obj.get_igt()
    Emeld.write(igt, "tests/data/BEJ_MV_CONV_01_RICH.emeld.xml", {'text':["source"], 'paragraph':["speaker"], 'sentence':["ft", "participant", "id"], 'word':[], 'morph':["txt", "gls", "id"]})
  
  def test_readEmeld(foo):
    igt:IGT = Emeld.read("tests/data/test.emeld.xml")
  
  def test_readWriteEmeld(foo):
    igt:IGT = Emeld.read("tests/data/tiny.emeld.xml")
    Emeld.write(igt, "tiny.emed.xml.out")
  
