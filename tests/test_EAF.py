from igttools.Elan2IGT import EAF2IGT
from igttools.IGT import IGT
import pprint as pp
import pytest

class TestEAF():

  def test_eaf_file(foo):
    obj = EAF2IGT("tests/data/BEJ_MV_CONV_01_RICH.EAF")
    #pp.pprint(obj.paragraphs)
    igt = obj.get_igt()
    igt.to_emeld("tests/data/test.emeld", ["source"], ["speaker"], ["ft", "participant", "id"], [], ["txt", "gls", "id"])
  
