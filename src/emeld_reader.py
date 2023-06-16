from dataclasses import dataclass, field
from typing import Union, Any, List, Tuple, Dict, Set
from io import StringIO
import pkgutil
import xml
import pandas as pd
from enum import Enum
from xml.sax.handler import ContentHandler
from igtcorpus.emeld import Emeld

"""Set of classes for reading EMELD document with the XML SAX API."""

class EmeldUnit(Enum):
    morph = 1
    word = 2
    phrase = 3
    paragraph = 4
    text = 5
    def __init__(self, value):
        if len(self.__class__):
            # make links
            all = list(self.__class__)
            first, previous = all[0], all[-1]
            previous.next = self
            self.previous = previous
            self.next = first

NumberOccInt = int

AttrType=str
AttrLang=str

FieldCoordinate=Tuple[AttrType, AttrLang]

@dataclass
class LevelSpec():
    occ: int = 0
    fields: Dict[FieldCoordinate, NumberOccInt] = field(default_factory=dict)
    def add_occ(self, FieldCoordinate):
        if FieldCoordinate in self.fields:
            self.fields[FieldCoordinate] += 1
        else:
            self.fields[FieldCoordinate] = 1


EmeldSpecDict = Dict[EmeldUnit, LevelSpec]

class EmeldReader():
  """ Encapsulate the access to XML SAX Reader."""
  
  def __init__(self, filename:str):
      self.filename = filename
      self.spec = None
      
  def _get_emeld_spec(self) -> EmeldSpecDict:
    """
    Get info about the structure of an Emeld document:
    for each unit (morph, word, ...) the number of occurrences and the information ("gls", "ft", etc.) available about it.
    :param str filename: the XML Emeld document
    :rtype: a dictionary of specification by level
    """
    handler = EmeldSpecContentHandler()
    xml.sax.parse(self.filename, handler)
    self.spec = handler.get_emeld_spec()
    return self.spec

  def get_corpus(self) -> Dict[EmeldUnit, pd.DataFrame]:
    if self.spec is None:
          self._get_emeld_spec()
    
    handler = EmeldPopulateContentHandler(self.spec)
    xml.sax.parse(self.filename, handler)
    return handler.get_tables()

class EmeldSpecContentHandler(ContentHandler):
    
    """
    This class should not be used directly. See :class:`EmeldReader`.

    A SAX ContentHandler that count the number of occurrences
    for each level and each field in each level.
    """

    def startDocument(self) -> None:
        self.emeldSpecDict: EmeldSpecDict = {u: LevelSpec() for u in list(EmeldUnit)}

        self.name_to_type: Dict[str, EmeldUnit] = {u.name: u for u in list(EmeldUnit)}
        # special case of XML element local name that can't be used as python name
        self.name_to_type["interlinear-text"] = EmeldUnit.text

        self.current_level : EmeldUnit = EmeldUnit.text

    def startElement(self, name, attrs) -> None:
        if name in self.name_to_type:
            level = self.name_to_type[name]
            self.emeldSpecDict[level].occ += 1
            self.current_level = level

        if name == Emeld.ITEM_ELEMENT:
            type = attrs.get(Emeld.TYPE_ATTR)
            lang = attrs.get(Emeld.LANG_ATTR)
            self.emeldSpecDict[self.current_level].add_occ((type, lang))

    def endElement(self, name) -> None:
        if name in self.name_to_type:
            self.current_level = self.name_to_type[name].next

    def get_emeld_spec(self) -> EmeldSpecDict:
        return self.emeldSpecDict

class EmeldPopulateContentHandler(ContentHandler):

    PARENT_COLUMN = ".parent"
    EMPTY_STR = ""

    def __init__(self, spec: EmeldSpecDict):
        self.spec: EmeldSpecDict = spec
        self.counter: Dict[EmeldUnit, int] = {u: -1 for u in list(EmeldUnit)}

        for u in list(EmeldUnit):
            self.spec[u].add_occ((self.PARENT_COLUMN, self.EMPTY_STR))

        self.tables: Dict[EmeldUnit, pd.DataFrame] = {
            u: pd.DataFrame(
                columns=pd.MultiIndex.from_tuples(
                    list(self.spec[u].fields.keys()),
                    names=[Emeld.TYPE_ATTR, Emeld.LANG_ATTR]
                ),
                index=range(self.spec[u].occ),
                dtype=str
            )
            for u in list(EmeldUnit)
        }
        self.current_type = self.EMPTY_STR
        self.current_lang = self.EMPTY_STR

    def startDocument(self) -> None:
        self.unitname_to_unitobj: Dict[str, EmeldUnit] = {u.name: u for u in list(EmeldUnit)}
        # special case of XML element local name that can't be used as python name
        self.unitname_to_unitobj["interlinear-text"] = EmeldUnit.text

        self.current_level : EmeldUnit = EmeldUnit.text
        self.waiting_text = False

    def startElement(self, name, attrs) -> None:
        if name in self.unitname_to_unitobj:
            u = self.unitname_to_unitobj[name]
            self.counter[u] += 1
            self.current_level = u

            # On the new unit (but top-level unit text)
            # add a pointer to the id of the parent unit
            # (the word a morph belong to, etc)
            if name != EmeldUnit.text.name:
                self.tables[self.current_level][self.PARENT_COLUMN, ""][self.counter[self.current_level]] = self.counter[self.current_level.next]

        if name == Emeld.ITEM_ELEMENT:
            self.current_type = attrs.get(Emeld.TYPE_ATTR)
            self.current_lang = attrs.get(Emeld.LANG_ATTR)
            self.waiting_text = True

    def characters(self, content) -> None:
        if self.waiting_text:
            self.tables[self.current_level][self.current_type, self.current_lang][self.counter[self.current_level]] = content
            self.waiting_text = False

    def endElement(self, name) -> None:
        if name in self.unitname_to_unitobj:
            self.current_level = self.unitname_to_unitobj[name].next

    def get_tables(self) -> Dict[EmeldUnit, pd.DataFrame]:
        return self.tables

