from typing import Dict, List, Union, TypeVar, Generic, Type, Tuple, Sequence
from typing_extensions import TypeAlias
import enum
from attr import define, field
from abc import ABC

Properties=Dict[str,str]
# Morph=Dict[str,str]
# Word=Tuple[Properties, List[Morph]]
# Sentence=Tuple[Properties, List[Word]]
# Paragraph=Tuple[Properties, List[Sentence]]
# Text=Tuple[Properties, List[Paragraph]]
# Corpus=Tuple[Properties, List[Text]]

@define
class LingUnit(ABC):

    fields: Properties
    
    @classmethod
    def make(cls, field):
        return cls(field, sub_unit)

@define
class NonTerminalLingUnit(LingUnit):

    units: Sequence[object]
    
    @classmethod
    def make(cls, field, sub_unit):
        return cls(field, sub_unit)

@define
class Morph(LingUnit):
    units: Sequence[LingUnit]

@define
class Word(NonTerminalLingUnit):
    units: Sequence[Morph]

@define
class Sentence(NonTerminalLingUnit):
    units: Sequence[Word]

@define
class Paragraph(NonTerminalLingUnit):
    units: Sequence[Sentence]

@define
class Text(NonTerminalLingUnit):
    units: Sequence[Paragraph]

@define
class Corpus(NonTerminalLingUnit):
    units: Sequence[Text]

class CorpusManager():
    pass

U  = TypeVar('U',         Word, Sentence, Paragraph, Text, Corpus)
SU = TypeVar('SU', Morph, Word, Sentence, Paragraph, Text)

SUB_LEVEL_TYPE: Dict[Type, Type] = {
        Morph: type(None),
        Word: Morph,
        Sentence: Word,
        Paragraph: Sentence,
        Text: Paragraph,
        Corpus: Text
}

@define(frozen=True)
class UnitFactory(Generic[U, SU]):

    #instance: U
    unit_type: Type[U]
    corpus_manager: CorpusManager
    Sub: Type[SU] = field(init=False)#, default=SUB_LEVEL_TYPE[self.unit_type])

    def __attrs_post_init__(self):
        #self.Sub = SUB_LEVEL_TYPE[self.unit_type]
        # For frozen class...
        object.__setattr__(self, "Sub", SUB_LEVEL_TYPE[self.unit_type])# self.x + 1)

    def createUnit(self, fields: Properties, sub_units: Sequence[SU]) -> U:
        #self.corpus.check_fields(level, fields)
        #return self.instance(fields, units)
        #return self.instance.make(fields, units)
        return self.unit_type(fields, sub_units)

if __name__ == '__main__':
    cm: CorpusManager = CorpusManager()
    tf:UnitFactory = UnitFactory(Text, cm)
    t = tf.createUnit({'One':'Two'}, [])
    print(t)
    sf:UnitFactory = UnitFactory(Sentence, cm)
    s = sf.createUnit({'One':'Three'}, [])
    print(s)

