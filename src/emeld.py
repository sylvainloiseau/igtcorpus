import xml.etree.ElementTree as ET
from pathlib import Path
import xmltodict
from igttools.igt import IGT
from typing import Union, List, Tuple, Dict, Any
from collections import OrderedDict
import pprint as pp

class Emeld():

  """
  read IGT from document in Emeld-xml or write IGT into Emeld-XML

  Cathy Bow, Baden Hughes, Steven Bird, "Towards a general model of interlinear text"
  """

  @classmethod
  def read(cls, filename: str) -> IGT:
    """
    Read an emeld document and turn it into an IGT object
    :param str filename: the XML Emeld document
    :rtype: IGT
    """
    p = Path(filename)
    document = Path(filename).read_text()
    d = xmltodict.parse(document)
    text = Emeld._turn_xmltodict_to_igt(d["document"]["interlinear-text"], level_index=0)
    return IGT(text)
    
  @classmethod
  def write(cls, igt: IGT, outfile: str, fields={'text':[], 'paragraph':[], 'sentence':[], 'word':[], 'morph':[]}) -> None:
    # : Dict[str, List[str]
    # 
    # igt.get_properties_by_level()
    """
    Hierarchy in EMELD XML:
    "/document/interlinear-text/paragraphs/paragraph/phrases/phrase/words/word/morphemes/morph"
    actual content is in item element (with @type attr) under paragraph, phrase, word, morph.

    :param IGT igt:
    :param str outfile: path ane name of the XML document to be created
    :param dict fields: for each level (text, paragraph, sentence, word, morph), a list of the keys in the dict representing the unit of that level that will be turned into a <item> element in EMELD.
    :rtype: None

    """
    root = ET.Element('document')
    text_node = ET.SubElement(root, 'interlinear-text')
    Emeld._populate_with_item(igt.text, text_node, fields['text'])
    paragraphs_node = ET.SubElement(text_node, 'paragraphs')
    pp.pprint(igt.text)
    Emeld._iterate_on_level_and_create_DOM(paragraphs_node, igt.text["paragraphs"], 1, fields)
    tree = ET.ElementTree(root)
    with open(outfile, "wb") as f:
      tree.write(f, encoding="UTF-8", xml_declaration=True)

  @staticmethod
  def _turn_xmltodict_to_igt(level, level_index):
      res = {}
      if 'item' in level:
          items = []
          if isinstance(level['item'], OrderedDict):
            items = [ level['item'] ]
          else:
            items = level['item']
          for item in items:
            res[item['@type']] = item['#text'] if '#text' in item else ""
      if (level_index + 1) < len(IGT.ORDERED_LEVEL) and IGT.ORDERED_LEVEL[level_index + 1][0] in level:
          # Or create key if do not exist?
          sub_level_list_name = IGT.ORDERED_LEVEL[level_index + 1][0] 
          sub_level_name = IGT.ORDERED_LEVEL[level_index + 1][1] 
          if level[sub_level_list_name] is not None  and sub_level_name in level[sub_level_list_name]:
            sublevels_in = []
            sublevels_out = []
            if isinstance(level[sub_level_list_name][sub_level_name], OrderedDict):
                sublevels_in = [ level[sub_level_list_name][sub_level_name] ]
            else:
                sublevels_in = level[sub_level_list_name][sub_level_name]
            #for sublevel in sublevels_in:
            sublevels_out = [ Emeld._turn_xmltodict_to_igt(sublevel, level_index + 1) for sublevel in sublevels_in]
            res[sub_level_list_name] = sublevels_out
      return res

  @staticmethod
  def _iterate_on_level_and_create_DOM(parent_node, level: List[Dict[str, Any]], level_index: int, fields) -> None:
      """
      Iterate on all units of a given level (paragraphs, sentences, words, morphemes)
      """
      for unit in level:
          unit_name =IGT.ORDERED_LEVEL[level_index][1]
          unit_node = ET.SubElement(parent_node, unit_name)
          Emeld._populate_with_item(unit, unit_node, fields[unit_name])
          if (level_index+1) < len(IGT.ORDERED_LEVEL) and IGT.ORDERED_LEVEL[level_index+1][0] in unit:
            # Or should the key always be present ?
            sub_level_node = ET.SubElement(unit_node, IGT.ORDERED_LEVEL[level_index + 1][0])
            Emeld._iterate_on_level_and_create_DOM(sub_level_node, unit[IGT.ORDERED_LEVEL[level_index+1][0]], level_index + 1, fields)

  @staticmethod
  def _populate_with_item(obj, node, fields):
      for field in fields:
          item_node = ET.SubElement(node, "item")
          item_node.set("type", field)
          item_node.text = str(obj[field])

