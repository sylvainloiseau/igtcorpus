from typing import Dict, List, Union, TypeVar, Generic, Type, Tuple, Sequence
import enum
from attr import define, field
from abc import ABC
import enum

Properties=Dict[str,str]

@define(frozen=True)
class LingUnit(ABC):

    properties: Properties
    
    def get_properties(self) -> Properties:
        return self.properties

@define(frozen=True)
class NonTerminalLingUnit(LingUnit):

    units: Sequence[LingUnit]
    
    def get_units(self) -> Sequence[LingUnit]:
        return self.units

@define(frozen=True)
class Morph(LingUnit):
    pass

@define(frozen=True)
class Word(NonTerminalLingUnit):
    units: Sequence[Morph]

@define(frozen=True)
class Sentence(NonTerminalLingUnit):
    units: Sequence[Word]

@define(frozen=True)
class Paragraph(NonTerminalLingUnit):
    units: Sequence[Sentence]

@define(frozen=True)
class Text(NonTerminalLingUnit):
    units: Sequence[Paragraph]

@define(frozen=True)
class Corpus(NonTerminalLingUnit):
    units: Sequence[Text]

@define(frozen=True)
class UnitFactory():

    def createMorph(self, properties: Properties) -> Morph:
        return Morph(properties)

    def createWord(self, properties: Properties, morphs: Sequence[Morph]) -> Word:
        return Word(properties, morphs)

    def createSentence(self, properties: Properties, words: Sequence[Word]) -> Sentence:
        return Sentence(properties, words)

    def createParagraph(self, properties: Properties, sentences: Sequence[Sentence]) -> Paragraph:
        return Paragraph(properties, sentences)

    def createText(self, properties: Properties, paragraphs: Sequence[Paragraph]) -> Text:
        return Text(properties, paragraphs)

