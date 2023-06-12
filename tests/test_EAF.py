from igtcorpus.elan import ElanCorpoAfr
from igtcorpus.corpusobj import Corpus
from igtcorpus.emeld import Emeld
import pytest

class TestEAF():

  def test_eaf_file(foo):
    corpus = ElanCorpoAfr.read("tests/data/BEJ_MV_CONV_01_RICH.EAF")
    Emeld.write(corpus, "tests/data/BEJ_MV_CONV_01_RICH.EAF.out")

