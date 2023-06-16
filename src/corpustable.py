import pandas as pd
from lxml import etree
from igtcorpus.emeld_reader import EmeldUnit
from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import Dict

class CorpusTable():

    def __init__(self, tables: Dict[EmeldUnit, pd.DataFrame]):
        self.tables = tables
    
    def n(self, unit: EmeldUnit) -> int:
        return self.tables[unit].shape[0]