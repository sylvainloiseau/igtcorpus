from igtcorpus.corpusobj import Corpus, Text, Paragraph
from igtcorpus.conll import Conll
from igtcorpus.emeld import Emeld
import pytest


class TestConll():

    def test_write(x): 
        file_in = "tests/data/EmeldByFlex.xml"
        c = Emeld.read(file_in)
        Conll.write(c,
                outdir="tests/data",
                text_name_field="title-abbreviation",
                sentence_id_field="segnum",
                sentence_text_field=None,
                sentence_ft_field="gls.en",
                sentence_extra_field=[],
                morph_txt_field="txt.tww",
                morph_lemma_field="cf.tww",
                morph_pos_field="msa.en",
                morph_extra_field=[("Gloss", "gls.en")])
