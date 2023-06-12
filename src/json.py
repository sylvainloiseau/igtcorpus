import json
from igtcorpus.corpusobj import Corpus, Morph, LingUnit, NonTerminalLingUnit, Properties
from igtcorpus.emeld import Emeld
from io import StringIO
from typing import List, Dict, Sequence, Union, MutableMapping, Optional

class EmeldJson():
    """
    Reading/Writing IGT in JSON with a data model following emeld
    """

    ITEM = "item"
    EMPTY = ""

    @staticmethod
    def _walk_corpus(unit: LingUnit, level:int):
        res  = {} #: MutableMapping[str, Union[MutableMapping[str, str], Sequence[LingUnit]]]
        res[EmeldJson.ITEM] = {}
        for k,v in unit.properties.items():
            res[EmeldJson.ITEM][k] = v or EmeldJson.EMPTY
        if isinstance(unit, NonTerminalLingUnit) and unit.sub_units is not None:
            sub_level = Emeld.ORDERED_LEVEL[level][1]
            res[sub_level] = [EmeldJson ._walk_corpus(u, level+1) for u in unit.sub_units]
        return res

    @classmethod
    def read(cls, inputfile: str) -> Corpus:
      with open(inputfile, "r") as f:
        d = json.load(f)
      return EmeldJson._dicttoLingUnit(d, -1)

    @staticmethod
    def _dicttoLingUnit(level: Dict, level_index: int) -> Corpus:
      properties: Properties = {}
      sub_unit: List[LingUnit] = []
      if EmeldJson.ITEM in level:
          items = level[EmeldJson.ITEM]
          for k,v in items.items():
            properties[ k ] = v or EmeldJson.EMPTY
      if (level_index + 1) < len(Emeld.ORDERED_LEVEL):
          sub_level_name = Emeld.ORDERED_LEVEL[level_index + 1][1] 
          if sub_level_name in level and level[sub_level_name] is not None:
            sublevels_in = level[sub_level_name]
            sublevels_out = [ EmeldJson._dicttoLingUnit(sublevel, level_index + 1) for sublevel in sublevels_in]
            sub_unit = sublevels_out
      res:LingUnit
      if level_index == -1:
          res = Corpus(properties, sub_unit)
      elif level_index == 4:
          res = Morph(properties)
      else:
          res = Emeld.ORDERED_LEVEL[level_index][2](properties, sub_unit)
      return res

    @classmethod
    def write(cls, corpus:Corpus, outfile: str, indent: Optional[int] = 4):
        """
        turn the corpus into a dictionary and serialise it as json.
        
        In the JSON structure, each unit is a dict in a list.

        Each unit as a key 'item' a (dictionary of properties) 
        and a key 'paragraph', 'phrase', 'word' or 'morph' containing the sub-elements.

        {
            "interlinear-text": [
                {
                    'item': {
                        'id': 'text1'
                    },
                    'paragraph: [
                        {
                            'item': {},
                            'phrase': [
                                # etc.
                            ]
                        }
                    ]
                }
            ]
        }

        :param str outfile: the file in which to write json struct.
        :return: None
        :indent: indent in the json file
        """
        res = EmeldJson._walk_corpus(corpus, 0)
        out_file = open(outfile, "w")
        json.dump(res, out_file, indent=indent)
        out_file.close()
        #with open(outfile, "wb") as f:
        #  json.dump(res, f, indent=4)

