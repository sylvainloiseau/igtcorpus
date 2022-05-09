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

LEVELS :List[Type[LingUnit]] = [ Corpus, Text, Paragraph, Sentence, Word, Morph ]
LEVEL_INDEX : Dict[Type[LingUnit], int]  = dict([(l, i) for i, l in enumerate(LEVELS)])

UnitCountType    = Dict[Type[LingUnit], int]
AccumulatorType  = Dict[Type[LingUnit], Sequence[LingUnit]] 
PropertyListType = Dict[Type[LingUnit], Dict[str, int]] 

class CorpusFactory():
  """
  Create piece by piece.
  """

  def __init__(self):
      self.unit_factory = UnitFactory()
      self.nb_unit         : UnitCountType    = dict([(l, 0) for l in LEVELS])
      self.accumulator     : AccumulatorType  = dict([(l, []) for l in LEVELS])
      self.properties_list : PropertyListType = dict([(l, {}) for l in LEVELS])

      self.currently_in : Type[NonTerminalLingUnit] = None
      self.current_unit_property : Dict[Type[NonTerminalLingUnit], Properties] = {}

  def createMorph(self, properties: Properties) -> None:
      if self.currently_in != Word:
          raise Exception(f"Can't create Morph while in { str(self.currently_in) }")
      self.accumulator[Morph].append(
              self.unit_factory.createMorph(properties)
              )
      self._check_properties(Morph, properties)
      self._increment(Morph)

  def start_unit(self, level: Type[NonTerminalLingUnit], properties: Properties = {}) -> None:
      if level == Corpus:
          if self.currently_in is not None:
              raise Exception(f"Can't create { str(level) } when other unit is already open")
      elif level == Text:
          if self.currently_in != Corpus:
              raise Exception(f"Can't create { str(level) } in { str(self.currently_in) }")
      elif level == Paragraph:
          if self.currently_in != Text:
              raise Exception(f"Can't create { str(level) } in { str(self.currently_in) }")
      elif level == Sentence:
          if self.currently_in != Paragraph:
              raise Exception(f"Can't create { str(level) } in { str(self.currently_in) }")
      elif level == Word:
          if self.currently_in != Sentence:
              raise Exception(f"Can't create { str(level) } in { str(self.currently_in) }")
      else:
          raise Exception(f"Unknwon unit type: { str(level) }")

      self.currently_in = level
      self.current_unit_property[level] = properties

  def end_unit(self, level:Type[NonTerminalLingUnit]=Word) -> None:
      if level != self.currently_in:
        raise Exception(f"Trying to close { level } while in { self.currently_in }")
      li = LEVEL_INDEX[level] 
      sublevel = LEVELS[li + 1]
      self.accumulator[level].append(
        self.unit_factory.createNonTerminalUnit(
          level,
          self.current_unit_property[level],
          self.accumulator[ sublevel ]
        )
      )
      self.accumulator[ sublevel ] = []
      self._increment(level)
      self._check_properties(level, self.current_unit_property[level])

      if level == Corpus:
          self.currently_in = None
      else:
          self.currently_in = LEVELS[li - 1]
          self.current_unit_property[level] = {}

  def get_corpus(self, corpus_properties: Properties = {}) -> Corpus:
      if len(self.accumulator[Corpus]) < 1:
          raise Exception("No corpus created")
      if self.currently_in != None:
          raise Exception("Can't build the corpus while some unit are still open")
      return self.accumulator[Corpus][0]

  def get_occ_nbr_for_level(self, level:Type[LingUnit]) -> int:
      return self.nb_unit[level]

  def get_properties_for_level(self, level:Type[LingUnit]) -> Dict[str, int]:
      return self.properties_list[level]

  def _increment(self, level: Type[LingUnit]) -> None:
      self.nb_unit[level] += 1

  def _check_properties(self, level, properties) -> None:
      for k in properties.keys():
          if k in self.properties_list[ level ]:
              self.properties_list[ level ][k] += 1
          else:
              self.properties_list[ level ][k] = 0


