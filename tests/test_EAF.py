from igttools.elan import ElanCorpoAfr
from igttools.igt import Corpus
from igttools.emeld import Emeld
import pprint as pp
import pytest

class TestEAF():

  def test_eaf_file(foo):
    corpus = ElanCorpoAfr.read("tests/data/BEJ_MV_CONV_01_RICH.EAF")
    Emeld.write(corpus, "tests/data/BEJ_MV_CONV_01_RICH.EAF.out")

