import json
from igttools.igt import Corpus, Morph, LingUnit, NonTerminalLingUnit, Properties
from igttools.emeld import Emeld
from io import StringIO
from typing import List, Dict

class ToJson():

    @staticmethod
    def _walk_corpus(unit: LingUnit, level:int):
        res = {}
        if unit.properties is not None:
            res["item"] = {}
            for k,v in unit.properties.items():
              res["item"][k] = v or ""
        if isinstance(unit, NonTerminalLingUnit) and unit.units is not None:
            sub_level = Emeld.ORDERED_LEVEL[level][1]
            res[sub_level] = [ToJson._walk_corpus(u, level+1) for u in unit.units]
        return res

    @classmethod
    def read(cls, inputfile: str) -> Corpus:
      with open(inputfile, "r") as f:
        d = json.load(f)
      return ToJson._dicttoLingUnit(d, -1)

    @staticmethod
    def _dicttoLingUnit(level: Dict, level_index: int) -> Corpus:
      properties: Properties = {}
      sub_unit: List[LingUnit] = []
      if 'item' in level:
          items = level['item']
          for k,v in items.items():
            properties[ k ] = v or ""
      if (level_index + 1) < len(Emeld.ORDERED_LEVEL):
          sub_level_name = Emeld.ORDERED_LEVEL[level_index + 1][1] 
          if sub_level_name in level and level[sub_level_name] is not None:
            sublevels_in = level[sub_level_name]
            sublevels_out = [ ToJson._dicttoLingUnit(sublevel, level_index + 1) for sublevel in sublevels_in]
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
    def write(cls, corpus:Corpus, outfile: str):
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
                    }
                    'paragraph: [
                        {
                            'item': {}
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
        """
        res = ToJson._walk_corpus(corpus, 0)
        out_file = open(outfile, "w")
        json.dump(res, out_file, indent=4)
        out_file.close()
        #with open(outfile, "wb") as f:
        #  json.dump(res, f, indent=4)

