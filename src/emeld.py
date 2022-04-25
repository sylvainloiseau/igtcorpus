#from lxml import etree as ET
import xml.etree.ElementTree as ET
from pathlib import Path
import xmltodict
from igttools.igt import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import Union, Any, List, Tuple, Dict
from collections import OrderedDict

class Emeld():
    
  ORDERED_LEVEL = [
          ("document", "interlinear-text", Text),
          ("paragraphs","paragraph", Paragraph),
          ("phrases","phrase", Sentence),
          ("words","word", Word),
          ("morphemes","morph", Morph)]

  """
  read IGT from document in Emeld-xml or write IGT into Emeld-XML

  Cathy Bow, Baden Hughes, Steven Bird, "Towards a general model of interlinear text"
  """

  @classmethod
  def read(cls, filename: str) -> Corpus:
    """
    Read an emeld document and turn it into an IGT object
    :param str filename: the XML Emeld document
    :rtype: Corpus
    """
    p = Path(filename)
    document = Path(filename).read_text()
    d = xmltodict.parse(document)

#    text = _walk_tree(text,
#            level_index=0,
#            item_fun=lambda x : [ x ] if isinstance(x, OrderedDict) else x,
#            sub_level_fun=lambda x : [ x ] if isinstance(x, OrderedDict) else x
#    )
#    #text = Emeld._regularize_xmltodict(, level_index=0)
#    text = _walk_tree(text,
#            level_index=0,
#            item_fun=lambda x : { (i['@type']: i['#text'] if '#text' in i else "" ) for i in x}
#            sub_level_fun=lambda x : [x] if isinstance(x, OrderedDict) else x
#    )

    texts = Emeld._regularize_xmltodict(d, level_index=-1)
    corpus = Emeld._turn_xmltodict_to_igt(texts, level_index=-1)
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
    # , fields={'text':[], 'paragraph':[], 'phrase':[], 'word':[], 'morph':[]}
    # :param dict fields: for each level (text, paragraph, phrase, word, morph), a list of the keys in the dict representing the unit of that level that will be turned into a <item> element in EMELD.
    root = ET.Element('document')
    Emeld._iterate_on_level_and_create_DOM(root, igt.get_units(), 0)
    tree = ET.ElementTree(root)
    #et.write(outputfile, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    with open(outfile, "wb") as f:
      tree.write(f, encoding="UTF-8", xml_declaration=True)

#  @staticmethod
#  def _walk_tree(level, level_index, item_fun = lambda x: x, sub_level_fun: lambda x: x):
#      """
#      Recursively walk the three and apply function
#      """
#      unit = {}
#      if 'item' in level:
#          unit['item'] = item_fun(level['item'])
#      sub_level_list_name = Emeld.ORDERED_LEVEL[level_index + 1][0] 
#      sub_level_name = Emeld.ORDERED_LEVEL[level_index + 1][1] 
#      if (level_index + 1) < len(Emeld.ORDERED_LEVEL) and sub_level_list_name in level:
#          if level[sub_level_list_name] is not None:
#            unit[sub_level_list_name] = sub_level_fun(level[sub_level_list_name])
#      return unit

  @staticmethod
  def _regularize_xmltodict(level, level_index):
      unit = {}
      """
      structure created by xmltodict contains either OrderedDict or List for a given key "x", depending on
      whether there is one child element "x" or several child element "x". This
      function turn all values associated to a key as list, be it a length-1 or
      not.
      """
      if 'item' in level:
          if isinstance(level['item'], OrderedDict):
            unit["item"] = [ level['item'] ]
          else:
            unit["item"] = level['item']
      if (level_index + 1) < len(Emeld.ORDERED_LEVEL) and Emeld.ORDERED_LEVEL[level_index + 1][0] in level:
          sub_level_list_name = Emeld.ORDERED_LEVEL[level_index + 1][0] 
          sub_level_name = Emeld.ORDERED_LEVEL[level_index + 1][1] 
          if level[sub_level_list_name] is not None  and sub_level_name in level[sub_level_list_name]:
            if isinstance(level[sub_level_list_name][sub_level_name], OrderedDict):
                level[sub_level_list_name][sub_level_name] = [ level[sub_level_list_name][sub_level_name] ]
            sublevels_in = level[sub_level_list_name][sub_level_name]
            unit[sub_level_list_name] = {}
            unit[sub_level_list_name][sub_level_name] = [ Emeld._regularize_xmltodict(sublevel, level_index + 1) for sublevel in sublevels_in]
      return unit

  @staticmethod
  def _turn_xmltodict_to_igt(level: OrderedDict, level_index: int) -> LingUnit:
      properties: Dict[str, str] = {}
      sub_unit: List[LingUnit] = []
      if 'item' in level:
          items = level['item']
          for item in items:
            properties[ item['@type'] ] = item['#text'] if '#text' in item else ""
      if (level_index + 1) < len(Emeld.ORDERED_LEVEL) and Emeld.ORDERED_LEVEL[level_index + 1][0] in level:
          sub_level_list_name = Emeld.ORDERED_LEVEL[level_index + 1][0] 
          sub_level_name =      Emeld.ORDERED_LEVEL[level_index + 1][1] 
          if level[sub_level_list_name] is not None  and sub_level_name in level[sub_level_list_name]:
            sublevels_in = level[sub_level_list_name][sub_level_name]
            sublevels_out = [ Emeld._turn_xmltodict_to_igt(sublevel, level_index + 1) for sublevel in sublevels_in]
            sub_unit = sublevels_out
      res:LingUnit
      if level_index == -1:
          res = Corpus(properties, sub_unit)
      elif level_index == 4:
          res = Morph(properties)
      else:
          res = Emeld.ORDERED_LEVEL[level_index][2](properties, sub_unit)
      return res

  @staticmethod
  def _iterate_on_level_and_create_DOM(parent_node: ET.Element, level: List[LingUnit], level_index: int) -> None:
      """
      Iterate on all units of a given level (paragraphs, phrases, words, morphemes)
      """
      for unit in level:
          unit_name = Emeld.ORDERED_LEVEL[level_index][1]
          unit_node = ET.SubElement(parent_node, unit_name)
          properties = unit.get_properties()
          if properties is not None:
              Emeld._populate_with_item(properties, unit_node)
          if (level_index+1) < len(Emeld.ORDERED_LEVEL):
            sub_units = unit.get_units()
            if sub_units is not None:
                sub_level_node = ET.SubElement(unit_node, Emeld.ORDERED_LEVEL[level_index + 1][0])
                Emeld._iterate_on_level_and_create_DOM(sub_level_node, sub_units, level_index + 1)

  @staticmethod
  def _populate_with_item(obj, node):
      for k, v in obj.items():
          item_node = ET.SubElement(node, "item")
          item_node.set("type", str(k))
          item_node.text = str(v)

