from typing import Dict, List

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

  def remove_empty_unit(self) -> None:
      """
      remove empty entry, for instance, a word, without any morph neither property of its own

         {
           fieldn : valuen
           words : [
             {
               morphemes = [
                 {
                 }
               ]
             }
           ]
         }
      """
      pass

  def get_properties_by_level(self) -> Dict[str, List[str]]:
    """
    extract for each level the list of the properties in the data.
    For instance below sentences have property "field_x", words have property
    "field_y" and morphemes have properties "field_v" and "field_w". Properties
    are not guarantee to be present on each actual unit.

       sentences : [
         {
           field_x : valuen
           words : [
             {
               field_y : valuen
               morphemes = [
                 {
                   field_v : valuen
                   field_w : valuex
                 }
               ]
             }
           ]
         }
       ]

       fields={'text':[], 'paragraph':[], 'sentence':[], 'word':[], 'morph':[]}
    """
    pass


