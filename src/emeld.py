from lxml import etree as ET
from pathlib import Path
from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import Union, Any, List, Tuple, Dict
from io import StringIO
import pkgutil
import xml
import pandas as pd
#from igtcorpus.corpustable import CorpusTable # circular import with Emeld
import logging

class Emeld():
  
  LOGGER = logging.getLogger(__name__)

  ITEM_ELEMENT = "item"
  LANG_ATTR = "lang"
  TYPE_ATTR = "type"

  MULTI_KEY_SEP = "/"
  TYPE_LANG_SEPARATOR = "."
  EMPTY_STRING = ""
  
  ORDERED_LEVEL = [
          ("document", "interlinear-text", Text),
          ("paragraphs","paragraph", Paragraph),
          ("phrases","word", Sentence),
          ("words","word", Word),
          ("morphemes","morph", Morph)]

  """
  read IGT from document in Emeld-xml or write IGT into Emeld-XML

  Cathy Bow, Baden Hughes, Steven Bird, "Towards a general model of interlinear text"
  """

  def __init__(self, filename, validate=False):
      self.filename = filename
      self.doc = None
      if validate:
          self.validate()

  def _load_doc(self):
      self.doc = ET.parse(self.filename)

  def validate(self):
    #dtd_string = pkg_resources.read_text(schema, "emeld.dtd")
    if self.doc is None:
        self._load_doc()
    dtd_string = pkgutil.get_data(__name__, "schema/emeld.dtd").decode('UTF-8')
    dtd = ET.DTD(StringIO(dtd_string))
    try:
        dtd.assertValid(self.doc)
    except Exception as e:
        raise Exception("Emeld document is not valid.") from e
        # + dtd.error_log.filter_from_errors()[0])
      
  def create_corpus_obj(self) -> Corpus:
    newroot = ET.Element("root") # we need an extra level for ease of recursion
    newroot.append(self.doc.getroot())
    corpus = Emeld._parse_emeld(newroot, level_index=-1)
    return corpus

  # TODO remove
  @classmethod
  def read(cls, filename: str, validate=False) -> Corpus:
    """
    Read an emeld document and turn it into an IGT object
    :param str filename: the XML Emeld document
    :param bool validate: should the document be validated against an Emeld DTD
    :rtype: Corpus
    """

    doc = ET.parse(filename)
    if validate:
        #dtd_string = pkg_resources.read_text(schema, "emeld.dtd")
        dtd_string = pkgutil.get_data(__name__, "schema/emeld.dtd").decode('UTF-8')
        dtd = ET.DTD(StringIO(dtd_string))
        try:
            dtd.assertValid(doc)
        except Exception as e:
            raise Exception("Emeld document is not valid.") from e
            # + dtd.error_log.filter_from_errors()[0])

    newroot = ET.Element("root") # we need an extra level for ease of recursion
    newroot.append(doc.getroot())
    corpus = Emeld._parse_emeld(newroot, level_index=-1)
    return corpus

  @classmethod
  def write(cls, igt: Corpus, outfile: str) -> None:
    """
    Hierarchy in EMELD XML:
    "/document/interlinear-text/paragraphs/paragraph/phrases/phrase/words/word/morphemes/morph"
    actual content is in item element (with @type attr) under paragraph, phrase, word, morph.

    :param Corpus igt:
    :param str outfile: path ane name of the XML document to be created
    :rtype: None

    """
    root = ET.Element('document')
    Emeld._iterate_on_level_and_create_DOM(root, igt.sub_units, 0)
    tree = ET.ElementTree(root)
    tree.write(outfile, pretty_print=True, xml_declaration=True, encoding='UTF-8')

  @staticmethod
  def _parse_emeld(e, level_index: int):
      properties: Dict[str, str] = {}
      sub_unit: List[LingUnit] = []
      for i in e.iterchildren("item"):
          data = Emeld._get_item_data(i)
          if data[0] in properties:
              if data[1] != Emeld.EMPTY_STRING:
              #raise Exception(f"duplicate entry: {data[0]}")
              #print(f"duplicate entry: {data[0]}; in: {properties}")
                properties[data[0]] = properties[data[0]] + Emeld.MULTI_KEY_SEP + data[1]
          else:
              properties[data[0]] = data[1]
      if (level_index + 1) < len(Emeld.ORDERED_LEVEL):
        sub_level_list_name = Emeld.ORDERED_LEVEL[level_index + 1][0] 
        sub_level_name = Emeld.ORDERED_LEVEL[level_index + 1][1] 
        sub_level = e.find(sub_level_list_name)
        if sub_level is not None:
          sub_unit = [Emeld._parse_emeld(s, level_index + 1) for s in sub_level.iterchildren()]
      res:LingUnit
      if level_index == -1:
          res = Corpus(properties, sub_unit)
      elif level_index == 4:
          res = Morph(properties)
      else:
          res = Emeld.ORDERED_LEVEL[level_index][2](properties, sub_unit)
      return res

  @staticmethod
  def _get_item_data(i) -> Tuple[str, str]:
      type_attr = i.get("type")
      if type_attr is None or type_attr == "":
          raise Exception("type attribute cannot be null")
      lang_attr = i.get("lang")
      if lang_attr is not None and lang_attr != "":
          type_attr = type_attr + Emeld.TYPE_LANG_SEPARATOR + lang_attr
      res = (type_attr, i.text or "")
      return res

  @staticmethod
  def _iterate_on_level_and_create_DOM(parent_node: ET.Element, level: List[LingUnit], level_index: int) -> None:
      """
      Iterate on all units of a given level (paragraphs, phrases, words, morphemes)
      """
      for unit in level:
          unit_name = Emeld.ORDERED_LEVEL[level_index][1]
          unit_node = ET.SubElement(parent_node, unit_name)
          properties = unit.properties
          if properties is not None:
              Emeld._populate_with_item(properties, unit_node)
          if (level_index+1) < len(Emeld.ORDERED_LEVEL):
            sub_units = unit.sub_units
            if sub_units is not None:
                sub_level_node = ET.SubElement(unit_node, Emeld.ORDERED_LEVEL[level_index + 1][0])
                Emeld._iterate_on_level_and_create_DOM(sub_level_node, sub_units, level_index + 1)

  @staticmethod
  def _populate_with_item(obj, node):
      for k, v in obj.items():
          item_node = ET.SubElement(node, "item")

          l = str(k).rsplit(".", 1)
          #print(l)
          type_attr = l[0]
          item_node.set("type", type_attr)

          if (len(l) == 2):
              lang_attr = l[1]
              item_node.set("lang", lang_attr)

          item_node.text = str(v)

class EmeldToTableCorpusDom():

    """
    Produce a :class:`CorpusTable` through an in-memory method.
    Deprecated. Please use :class:`EmeldReader`
    """

    @staticmethod
    def from_emeld(filename: str):
        doc = ET.parse(filename)
        
        # newroot = etree.Element("root") # we need an extra level for ease of recursion
        # newroot.append(doc.getroot())

        tables = dict()

        path = ""
        for i, level in enumerate(Emeld.ORDERED_LEVEL):
            path = path + "/" + level[0] + "/" + level[1]
            unit = level[2]
            if unit != Morph:
                sub_unit = Emeld.ORDERED_LEVEL[i + 1]
                sub_unit_path = sub_unit[0] + "/" + sub_unit[1]
            else:
                sub_unit_path = None
            table = CorpusTable._create_table(level[2], path, doc, sub_unit_path)
            tables[unit] = table

        return CorpusTable(tables)

    @staticmethod
    def _create_table(level_name, path, doc, sub_unit_path):
        print(path)
        
        nodes = doc.xpath(path)

        n = len(nodes)
        print(n)
        print(nodes[0].tag)
        
        table = pd.DataFrame()
        table.index = range(1,n+1)
        table.columns = pd.MultiIndex.from_arrays([[], []], names=["field", "lang"])
        table["id", ""] = [node.get("id") for node in nodes]
        for i, node in enumerate(nodes):
            #print(node.tag)
            items = node.findall("item")
            #print(len(items))
            for j, item in enumerate(items):
                #print(etree.tostring(node))
                lang = item.get("lang")
                type = item.get("type")
                if lang is None:
                    lang = ""
                if not table.columns.isin([(type, lang)]).any():
                    table[type, lang] = [0] * table.shape[0]
                    
                table[type, lang][j] = item.text

        sub_unit_n = None
        if sub_unit_path is not None:
            sub_unit_n = [len(node.findall(sub_unit_path)) for node in nodes]

        return table
