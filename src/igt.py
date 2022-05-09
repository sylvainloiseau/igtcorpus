from typing import Dict, Sequence, List, Type
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

    def get(self, level: Type[LingUnit]):
        if not level == SUBLEVEL4LEVEL[type(self)]:
            raise Exception(f"{str(self.__class__)} does not contain {str(level)}")
        return self.get_sub_units()

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

LEVELS :List[Type[LingUnit]] = [ Corpus, Text, Paragraph, Sentence, Word, Morph ]
SUBLEVEL4LEVEL = dict(zip([None] + LEVELS, LEVELS + [None]))
