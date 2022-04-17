from igttools.elan import ElanCorpoAfr
from igttools.igt import IGT
import pprint as pp
import pytest

class TestEAF():

  def test_eaf_file(foo):
    obj = ElanCorpoAfr("tests/data/BEJ_MV_CONV_01_RICH.EAF")
    #pp.pprint(obj.paragraphs)
    igt = obj.get_igt()
