from igtcorpus.corpusobj import Corpus, Text, Paragraph
from igtcorpus.conll import Conll
from igtcorpus.emeld import Emeld
import pytest


class TestConll():

    def test_write(x): 
        file_in = "tests/data/EmeldByFlex.xml"
        file_out = "tests/data/EmeldByFlex.conll"
        c = Emeld.read(file_in)
        Conll.write(c,
                outdir="tests/data",
                text_name_field="title-abbreviation",
                sentence_id_field="segnum",
                sentence_text_field=None,
                sentence_ft_field="gls.tpi",
                sentence_extra_field=[],
                morph_txt_field="txt.tww",
                morph_lemma_field="cf.tww",
                morph_pos_field="msa.en",
                morph_extra_field=["gls.en"])
