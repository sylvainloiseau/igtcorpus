from dataclasses import dataclass
from typing import Dict, Sequence, Type, TypeVar, cast

Properties=Dict[str,str]

#@define(frozen=True)
@dataclass
class LingUnit(): #ABC

    properties: Properties

    #@property
    def get_properties(self) -> Properties:
        return self.properties

#@define(frozen=True)
@dataclass
class NonTerminalLingUnit(LingUnit):

    sub_units: Sequence[LingUnit]

    #@property
    #@abstractmethod
    def get_sub_units(self) -> Sequence[LingUnit]:
        return self.sub_units

#@define(frozen=True)
@dataclass
class Morph(LingUnit):
    pass

#@define(frozen=True)
@dataclass
class Word(NonTerminalLingUnit):
    pass
    #def __init__(cls, properties: Properties, sub_units: Sequence[Morph]):
    #    super().__init__(properties, sub_units)

    #sub_units: Sequence[Morph]


@dataclass
class UnitFactory():

  def createMorph(self, properties: Properties) -> Morph:
      return Morph(properties)

  def createNonTerminalUnit(self, level: Type[NonTerminalLingUnit], properties: Properties, sub_units: Sequence[LingUnit]) -> NonTerminalLingUnit:
      return level(properties, sub_units)

  def createWord(self, properties: Properties, morphs: Sequence[Morph]) -> NonTerminalLingUnit:
      w = self.createNonTerminalUnit(Word, properties, morphs)
      return cast(Word, w)


f = UnitFactory()
w = f.createWord({'foo': 'bar'}, [Morph({'x':'1'}), Morph({'y': '2'})])
print(type(w))
print(w.get_properties()['foo'])
print(w.get_sub_units())
