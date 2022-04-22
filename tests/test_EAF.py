from igttools.elan import ElanCorpoAfr
from igttools.igt import Corpus
from igttools.emeld import Emeld
import pprint as pp
import pytest

class TestEAF():

  def test_eaf_file(foo):
    obj = ElanCorpoAfr("tests/data/BEJ_MV_CONV_01_RICH.EAF")
    igt = obj.get_igt()
    pp.pprint(igt)
    Emeld.write(igt, "tests/data/BEJ_MV_CONV_01_RICH.EAF.out")

