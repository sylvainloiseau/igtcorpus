import json
from igttools import Corpus, LingUnit, NonTerminalLingUnit, Properties
from igttools.emeld import ORDERED_LEVEL

class ToJson():

    def walk_corpus(unit: LingUnit, level:int):
        res = {}
        if unit.properties is not None:
            res["item"] = {}
            for k,v in unit.properties.items():
              res["item"][k] = v
        if isinstance(unit, NonTerminalLingUnit) and unit.items is not None:
            sub_level = ORDERED_LEVEL[level][1]
            res[sub_level] = [ToJson.walk_corpus(u, level+1) for u in unit.items]
        return res

    @classmethod
    def to_json(corpus:Corpus, outfile: str):
        res = ToJson.walk_corpus(corpus, 0)
        with open(outfile, "wb") as f:
          json.dump(res, f, indent=4)

