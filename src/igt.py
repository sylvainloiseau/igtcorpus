from typing import Dict, List, Union, Type, Tuple, Sequence, cast
from dataclasses import dataclass
import pprint as pp

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

    def __str__(self):
        return f'{type(self)}(properties={pp.pformat(self.properties)}, {pp.pformat(self.sub_units)})'
    
    def __repr__(self):
        return f'Class{type(self)}(properties={pp.pformat(self.properties)}, {pp.pformat(self.sub_units)})'

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

class UnitFactory():

  nb_unit: Dict[Type, int] = {
          Morph : 0,
          Word : 0,
          Sentence : 0,
          Paragraph : 0,
          Text : 0
  }

  def createMorph(self, properties: Properties) -> Morph:
      self.nb_unit[Morph] += 1
      return Morph(properties)

  def createNonTerminalUnit(self, level: Type[NonTerminalLingUnit], properties: Properties, sub_units: Sequence[LingUnit]) -> NonTerminalLingUnit:
      self.nb_unit[level] += 1
      return level(properties, sub_units)

  def createWord(self, properties: Properties, morphs: Sequence[Morph]) -> Word:
      res = self.createNonTerminalUnit(Word, properties, morphs)
      return cast(Word, res)

  def createSentence(self, properties: Properties, words: Sequence[Word]) -> Sentence:
      res = self.createNonTerminalUnit(Sentence, properties, words)
      return cast(Sentence, res)

  def createParagraph(self, properties: Properties, sentences: Sequence[Sentence]) -> Paragraph:
      res = self.createNonTerminalUnit(Paragraph, properties, sentences)
      return cast(Paragraph, res)

  def createText(self, properties: Properties, paragraphs: Sequence[Paragraph]) -> Text:
      res = self.createNonTerminalUnit(Text, properties, paragraphs)
      return cast(Text, res)

  def get_corpus(self, properties: Properties, texts: Sequence[Text]) -> Corpus:
      return Corpus(properties, texts)

#  @unique
#  class LLevel(IntEnum):
#      Morph = 1
#      Word = 2
#      Sentence = 3
#      Paragraph = 4
#      Text = 5
#      Corpus = 6
#  
#  LU = TypeVar('LU', bound=LingUnit)
#  LSU = TypeVar('LSU', bound=LingUnit)
#  
#  ## start 0 : with generic
#  
#  class LUnitFactoryWithGeneric(Generic[LU, LSU]):
#  
#      def createUnit(self, properties:Properties, sublevel: Sequence[LSU]) -> LU:
#          return LU(properties, sublevel)
#  
#  ## end 0 : with generic
#  
#  ## start 1 : with type
#  
#  class LUnitFactoryWithTypeVar():
#      level_type: Type[LU]
#      sublevel_type: Type[LTU]
#  
#      def __init__(self, level_type: Type[LU], sublevel_type: Type[LSU]):
#          self.level_type = level_type
#          self.sublevel_type = sublevel_type
#  
#      def createUnit(self, properties:Properties, sublevel: Sequence[LSU]) -> LU:
#          return self.level_type(properties, sublevel)
#  
#  ## end 1 : with type
#  
#  ## start 2 : with enum
#  
#  class LUnitFactoryWithEnum():
#      level_type: LLevel
#      sublevel_type: LLevel
#  
#      def __init__(self, level_type: LLevel, sublevel_type: LLevel):
#          self.level_type = level_type
#          self.sublevel_type = sublevel_type
#          if sublevel_type >= level_type:
#              raise Exception("sublevel type cannot be super higher than level type")
#  
#      def createUnit(self, properties:Properties, sublevel: Sequence[LUnit]) -> LUnit:
#          assert all([x.level_type == self.sublevel_type for x in sublevel])
#          return LUnit(level_type, properties, sublevel)
#  
#  class LUnit():
#      level_type: LLevel
#      properties: Properties
#      sublevel: Sequence[LUnit]
#  
#  ## end 2

