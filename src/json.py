import json
from igttools.igt import Corpus, LingUnit, NonTerminalLingUnit, Properties
from igttools.emeld import Emeld
from io import StringIO

class ToJson():

    def walk_corpus(unit: LingUnit, level:int):
        res = {}
        if unit.properties is not None:
            res["item"] = {}
            for k,v in unit.properties.items():
              res["item"][k] = v
        if isinstance(unit, NonTerminalLingUnit) and unit.units is not None:
            sub_level = Emeld.ORDERED_LEVEL[level][1]
            res[sub_level] = [ToJson.walk_corpus(u, level+1) for u in unit.units]
        return res

    @classmethod
    def to_json(cls, corpus:Corpus, outfile: str):
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
        res = ToJson.walk_corpus(corpus, 0)
        out_file = open(outfile, "w")
        json.dump(res, out_file, indent=4)
        out_file.close()
        #with open(outfile, "wb") as f:
        #  json.dump(res, f, indent=4)

