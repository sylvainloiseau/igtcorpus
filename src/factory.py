from typing import Dict, List, Type, Sequence, cast
from igtcorpus.igt import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit, NonTerminalLingUnit

class UnitFactory():
  """
  Utility for creating unit
  """

  def createMorph(self, properties: Properties) -> Morph:
      return Morph(properties)

  def createNonTerminalUnit(self, level: Type[NonTerminalLingUnit], properties: Properties, sub_units: Sequence[LingUnit]) -> NonTerminalLingUnit:
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

LEVELS :List[Type[LingUnit]] = [ Text, Paragraph, Sentence, Word, Morph ]
LEVEL_INDEX : Dict[Type[LingUnit], int]  = dict([(l, i) for i, l in enumerate(LEVELS)])

UnitCountType    = Dict[Type[LingUnit], int]
AccumulatorType  = Dict[Type[LingUnit], Sequence[LingUnit]] 
PropertyListType = Dict[Type[LingUnit], Dict[str, int]] 

class CorpusFactory():
  """
  Create a corpus.

  f = CorpusFactory()
  f.createMorph({'tx': 'a', 'gl': '1SG'})
  f.end_unit(Word)
  f.createMorph({'tx': 'mami', 'gl': 'pig'})
  f.createMorph({'tx': '-mo', 'gl': '-CL'})
  f.end_unit(Word)
  f.createMorph({'tx': 'iefi', 'gl': 'shoot'})
  f.createMorph({'tx': '-mwii', 'gl': '-1SG.M'})
  f.end_unit(Word)
  f.end_unit(Sentence)
  f.end_unit(Paragraph)
  f.end_unit(Text)

  c: Corpus = f.get_corpus()
  """

  def __init__(self):
      self.unit_factory = UnitFactory()
      self.nb_unit         : UnitCountType    = dict([(l, 0) for l in LEVELS])
      self.accumulator     : AccumulatorType  = dict([(l, []) for l in LEVELS])
      self.properties_list : PropertyListType = dict([(l, {}) for l in LEVELS])

  def createMorph(self, properties: Properties) -> None:
      self.accumulator[Morph].append(
              self.unit_factory.createMorph(properties)
              )
      self._check_properties(Morph, properties)
      self._increment(Morph)

  def end_unit(self, level: Type[NonTerminalLingUnit], properties: Properties = {}) -> None:
      li = LEVEL_INDEX[level] 
      sublevel = LEVELS[li + 1]
      self.accumulator[level].append(
        self.unit_factory.createNonTerminalUnit(
          level,
          properties,
          self.accumulator[ sublevel ]
        )
      )
      self.accumulator[ sublevel ] = []
      self._increment(level)
      self._check_properties(level, properties)

  def get_corpus(self, properties: Properties = {}) -> Corpus:
      return Corpus(properties, self.accumulator[Text])

  def _increment(self, level: Type[LingUnit]) -> None:
      self.nb_unit[level] += 1

  def _check_properties(self, level, properties) -> None:
      for k in properties.keys():
          if k in self.properties_list[ level ]:
              self.properties_list[ level ][k] += 1
          else:
              self.properties_list[ level ][k] = 0


