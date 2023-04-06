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

    # def add_property(level: Type[LingUnit], name, func):
    #       # TODO check for type
    #       _rec_apply(level, name, funct, self)

    # def _rec_apply(level, name, func, unit):
    #     if type(unit) != level:
    #         for u in unit.get_sub_unit():
    #             _rec_apply(level, name, func, u)
    #     else:
    #         unit.properties[name] = func(unit)


LEVELS :List[Type[LingUnit]] = [ Corpus, Text, Paragraph, Sentence, Word, Morph ]
SUBLEVEL4LEVEL = dict(zip([None] + LEVELS, LEVELS + [None]))
