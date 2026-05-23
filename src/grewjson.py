import json
from igtcorpus.corpusobj import Corpus, Morph, LingUnit, NonTerminalLingUnit, Properties
from igtcorpus.emeld import Emeld
from io import StringIO
from typing import List, Dict, Sequence, Union, MutableMapping, Optional

class GrewJson():
    """
    Reading/Writing IGT in JSON in the Grew format
    See https://grew.fr/doc/json/
    """

    ITEM = "item"
    EMPTY = ""

    @staticmethod
    def _walk_corpus(unit: LingUnit, level:int, nodes:Dict[str, Dict[str, str]], edges:List[Dict[str, str]], node_id:int, ordering:List[str]):

        node_id += 1
        this_node_id = node_id

        this_node_key = str(this_node_id)

        nodes[this_node_key] = unit.get_properties()
        if level == 0 :
          nodes[this_node_key]["type"] = "corpus"
        elif level == 3 :
          nodes[this_node_key]["type"] = "sentence"
        else:
          nodes[this_node_key]["type"] = Emeld.ORDERED_LEVEL[level-1][1]

        child_id = node_id
        greater = node_id
        if isinstance(unit, NonTerminalLingUnit) and unit.sub_units is not None:
            sub_level = Emeld.ORDERED_LEVEL[level][1]
            if level == 2:
              sub_level = "sentence"
            for child in unit.sub_units:
              child_id, greater = GrewJson._walk_corpus(child, level+1, nodes, edges, greater, ordering) 
              edges.append({"src":this_node_key, "tar":str(child_id), "label":str(sub_level)})
        elif isinstance(unit, Morph):
            ordering.append(str(this_node_id))
        else:
            print("weird: " + nodes)

        return (this_node_id, greater)

    @classmethod
    def read(cls, inputfile: str) -> Corpus:
        raise Exception("Not implemented")
      # with open(inputfile, "r") as f:
      #   d = json.load(f)
      # return GrewJson._dicttoLingUnit(d, -1)

    @staticmethod
    def _dicttoLingUnit(level: Dict, level_index: int) -> Corpus:
      properties: Properties = {}
      sub_unit: List[LingUnit] = []
      if GrewJson.ITEM in level:
          items = level[GrewJson.ITEM]
          for k,v in items.items():
            properties[ k ] = v or GrewJson.EMPTY
      if (level_index + 1) < len(Emeld.ORDERED_LEVEL):
          sub_level_name = Emeld.ORDERED_LEVEL[level_index + 1][1] 
          if sub_level_name in level and level[sub_level_name] is not None:
            sublevels_in = level[sub_level_name]
            sublevels_out = [ GrewJson._dicttoLingUnit(sublevel, level_index + 1) for sublevel in sublevels_in]
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
        nodes:Dict[str, Dict[str, str]] = {}
        node_id: int = 0
        edges: List[Dict] = []
        ordering:List[str] = []
        GrewJson._walk_corpus(corpus, 0, nodes, edges, node_id, ordering)
        out_file = open(outfile, "w")
        graph = {
          "nodes": nodes,
          "edges": edges,
          "order": ordering
        }
        json.dump(graph, out_file, indent=indent)
        out_file.close()
        #with open(outfile, "wb") as f:
        #  json.dump(res, f, indent=4)

