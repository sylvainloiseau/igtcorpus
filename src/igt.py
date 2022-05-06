from typing import Dict, Sequence
from dataclasses import dataclass

Properties=Dict[str,str]

@dataclass
class LingUnit():

    properties: Properties
    
    def get_properties(self) -> Properties:
        return self.properties

@dataclass
class NonTerminalLingUnit(LingUnit):

    sub_units: Sequence[LingUnit]
    
    def get_sub_units(self) -> Sequence[LingUnit]:
        return self.sub_units

@dataclass
class Morph(LingUnit): pass

@dataclass
class Word(NonTerminalLingUnit): pass

@dataclass
class Sentence(NonTerminalLingUnit): pass

@dataclass
class Paragraph(NonTerminalLingUnit): pass

@dataclass
class Text(NonTerminalLingUnit): pass

@dataclass
class Corpus(NonTerminalLingUnit): pass

