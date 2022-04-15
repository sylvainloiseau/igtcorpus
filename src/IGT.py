import xml.etree.ElementTree as ET

class IGT():

  """
  an IGT (interlinearized glossed text) represented as four-level
  lists of dictionaries (of text, paragraph, sentence, word, morph). At each
  level, the field (other than the sublevel "paragraphs", "sentences",
  "words", "morphemes"), are optional.

  text = {
   fieldn : valuen
   paragraphs : [
     {
       fieldn : valuen
       sentences : [
         {
           fieldn : valuen
           words : [
             {
               fieldn : valuen
               morphemes = [
                 {
                   fieldn : valuen
                   fieldx : valuex
                 }
               ]
             }
           ]
         }
       ]
     }
   ]
  }
  """

  ORDERED_LEVEL = [["text"], ["paragraphs","paragraph"], ["sentences","sentence"], ["words","word"], ["morphemes","morph"]]

  def __init__(self, text):
    self.text = text
    self.available_properties = None

  # def get_available_properties(self):
  #   if self.available_properties is None:
  #     self.available_properties = dict()
  #     self.available_properties["text"] = []
  #     self.available_properties["paragraphs"] = []
  #     self.available_properties["sentences"] = []
  #     self.available_properties["words"] = []
  #     self.available_properties["morphemes"] = []
  #     gather_properties_on_level(0)
  #   return(self.available_properties)

  # def gather_properties_on_level(level):
  #   pass

   
  def to_emeld(self, outfile, fields={'text':[], 'paragraph':[], 'sentence':[], 'word':[], 'morph':[]}):
    """
    Hierarchy in EMELD XML:
    "/document/interlinear-text/paragraphs/paragraph/phrases/phrase/words/word/morphemes/morph"
    actual content is in item element (with @type attr) under paragraph, phrase, word, morph.

    :param self

    :param outfile: path ane name of the XML document to be created

    :param fields: for each level (text, paragraph, sentence, word, morph), a list of the keys in the dict representing the unit of that level that will be turned into a <item> element in EMELD.

    """
    root = ET.Element('document')
    text_node = ET.SubElement(root, 'interlinear-text')
    self._populate_with_item(self.text, text_node, fields['text'])
    paragraphs_node = ET.SubElement(text_node, 'paragraphs')
    self._iterate_on_level(paragraphs_node, self.text["paragraphs"], 1, fields)
    # for p in self.text["paragraphs"]:
    #   paragraph_node = ET.SubElement(paragraphs_node, 'paragraph')
    #   self._populate_with_item(p, paragraph_node, paragraph_item_fields)
    #   sentences_node = ET.SubElement(paragraph_node, 'phrases')
    #   for s in p["sentences"]:
    #       sentence_node = ET.SubElement(sentences_node, 'phrase')
    #       self._populate_with_item(s, sentence_node, sentence_item_fields)
    #       words_node = ET.SubElement(sentence_node, 'words')
    #       for word in s["words"]:
    #         word_node = ET.SubElement(words_node, 'word')
    #         self._populate_with_item(word, word_node, word_item_fields)
    #         morphemes_node = ET.SubElement(word_node, 'morphemes')
    #         for m in word["morphemes"]:
    #           morph_node = ET.SubElement(morphemes_node, 'morph')
    #           self._populate_with_item(m, morph_node, morpheme_item_fields)
    tree = ET.ElementTree(root)
    with open(outfile, "wb") as f:
      tree.write(f, encoding="UTF-8", xml_declaration=True)

  def _iterate_on_level(self, parent_node, level, level_index, fields):
      """
      Iterate on all units of a given level (paragraphs, sentences, words, morphemes)
      """
      for unit in level:
          unit_name =IGT.ORDERED_LEVEL[level_index][1]
          unit_node = ET.SubElement(parent_node, unit_name)
          self._populate_with_item(unit, unit_node, fields[unit_name])
          if (level_index+1) < len(IGT.ORDERED_LEVEL):
            sub_level_node = ET.SubElement(unit_node, IGT.ORDERED_LEVEL[level_index + 1][0])
            self._iterate_on_level(sub_level_node, unit[IGT.ORDERED_LEVEL[level_index+1][0]], level_index + 1, fields)

  def _populate_with_item(self, obj, node, fields):
      for field in fields:
          item_node = ET.SubElement(node, "item")
          item_node.set("type", field)
          item_node.text = str(obj[field])
