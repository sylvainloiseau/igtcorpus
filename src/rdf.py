from rdflib import Graph, URIRef, RDF, Literal
from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit, SUBLEVEL4LEVEL, LEVELS
from typing import Union, Any, List, Tuple, Dict
#from ligt import LigtNS
import os

class IGTRDF():
  
  @classmethod
  def read(cls) -> Corpus:
    pass

  igt2ligt = dict(zip(LEVELS, [Corpus, Text, Paragraph, Sentence, Word, Morph]))

  @classmethod
  def _populate_with_level(graph, unitType:type, unit:LingUnit, parent_unit_uri:URIRef, previous_unit_uri:URIRef):
    graph.add((parent_unit_uri, RDF.type, IGTRDF.igt2ligt[unitType]))
    for p in unit.get_properties:
      graph.add((parent_unit_uri, Literal(p), Literal(unit.get_properties[p])))
    sublevel = SUBLEVEL4LEVEL[unitType]
    subunits = unit.get(sublevel)

    # link the parent to the first sub_unit
    firstunit = subunits[0]
    firstunit_id = p.get_properties("id") if sublevel == Text else str(i)
    firstunit_uri = URIRef(parent_unit_uri.__str__ + str(sublevel) + id)
    # TODO lien (hasWord, hasUtterance...) parent_unit_uri -> firstunit

    for i, u in enumerate(subunits):
      pass
      # faire le "next" link 
      # graph.add((rootURI, Literal(p), Literal(igt.get_properties[p]))
      # TODO :
      #IGTRDF._populate_with_level(graph, sublevels, u, u_uri, None)

  @classmethod
  def write(cls, igt: Corpus, outfile: str, rootURI: str="https://corpus.emeld/") -> None:
    root = URIRef(rootURI)
    graph = Graph(identifier=root)
    #graph.namespace_manager.bind('ligt', LigtNS, override=False)
    IGTRDF._populate_with_level(graph, Corpus, igt, root, None)

    
    texts = igt.get(Text)
    for ti, text in enumerate(texts):
      pass
      

        #           event = URIRef(self.corpus_uri_prefix + "/Event/" + quote_plus(event_directory))
        #         self.g.add((event, RDF.type, RICO.Event))
        #         self.g.add((event, FieldDataNS.ID, Literal(event_directory)))

        # instance = URIRef(str(record) + "/" + quote_plus(file))
        # self.g.add((record, RICO.hasInstance, instance))
        # self.g.add((instance, RDF.type, RICO.Instance))
        # self.g.add((instance, FieldDataNS.URL, Literal(os.path.join(path, file))))
        # self.g.add((instance, FieldDataNS.FileName, Literal(file)))

        #   target_output = os.path.join(tmp_path,'dictionary2tripleAttr.ttl')
        #   g.serialize(destination = target_output)
