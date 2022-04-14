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

  ORDERED_LEVEL = ["paragraphs", "sentences", "words", "morphemes"}

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

   
  def to_emeld(self, outfile, text_item_fields=[], paragraph_item_fields=[], sentence_item_fields=[], word_item_fields=[], morpheme_item_fields=[]):
    """
    Hierarchy in EMELD XML:
    "/document/interlinear-text/paragraphs/paragraph/phrases/phrase/words/word/morphemes/morph"
    actual content is in item element (with @type attr) under paragraph, phrase, word, morph.

    text_item_fields: list of keys in in the dict representing a text that will be turned into a item element.

    paragrph_item_fields: list of keys in in the dict representing a paragraph that will be turned into a item element.

    sentence_item_fields: list of keys in in the dict representing a sentencethat will be turned into a item element.

    word_item_fields: list of keys in in the dict representing a word that will be turned into a item element.

    morpheme_item_fields: list of keys in in the dict representing a morpheme that will be turned into a item element.

    """
    root = ET.Element('document')
    text_node = ET.SubElement(root, 'interlinear-text')
    self._populate_with_item(self.text, text_node, text_item_fields)
    paragraphs_node = ET.SubElement(text_node, 'paragraphs')
    for p in self.text["paragraphs"]:
      paragraph_node = ET.SubElement(paragraphs_node, 'paragraph')
      self._populate_with_item(p, paragraph_node, paragraph_item_fields)
      sentences_node = ET.SubElement(paragraph_node, 'phrases')
      for s in p["sentences"]:
          sentence_node = ET.SubElement(sentences_node, 'phrase')
          self._populate_with_item(s, sentence_node, sentence_item_fields)
          words_node = ET.SubElement(sentence_node, 'words')
          for word in s["words"]:
            word_node = ET.SubElement(words_node, 'word')
            self._populate_with_item(word, word_node, word_item_fields)
            morphemes_node = ET.SubElement(word_node, 'morphemes')
            for m in word["morphemes"]:
              morph_node = ET.SubElement(morphemes_node, 'morph')
              self._populate_with_item(m, morph_node, morpheme_item_fields)
    tree = ET.ElementTree(root)
    with open(outfile, "wb") as f:
      tree.write(f)

  def _populate_with_item(self, obj, node, fields):
      for field in fields:
          item_node = ET.SubElement(node, "item")
          item_node.set("type", field)
          item_node.text = str(obj[field])
