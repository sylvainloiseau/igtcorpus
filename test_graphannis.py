from graphannis.cs import CorpusStorageManager
from graphannis.util import node_name_from_match
from graphannis.graph import GraphUpdate

with CorpusStorageManager() as cs:
    print(cs.list())

    g = GraphUpdate()

    # First argument is the node name.
    g.add_node("tutorial/doc1#t1")
    # First argument is the node name,
    # then comes the annotation namespace, name and value.
    g.add_node_label("tutorial/doc1#t1", "annis", "tok", "That")

    g.add_node("tutorial/doc1#t2")
    g.add_node_label("tutorial/doc1#t2", "annis", "tok", "is")

    g.add_node("tutorial/doc1#t3")
    g.add_node_label("tutorial/doc1#t3", "annis", "tok", "a")

    g.add_node("tutorial/doc1#t4")
    g.add_node_label("tutorial/doc1#t4", "annis", "tok", "Category")

    g.add_node("tutorial/doc1#t5")
    g.add_node_label("tutorial/doc1#t5", "annis", "tok", "3")

    g.add_node("tutorial/doc1#t6")
    g.add_node_label("tutorial/doc1#t6", "annis", "tok", "storm")

    g.add_node("tutorial/doc1#t7")
    g.add_node_label("tutorial/doc1#t7", "annis", "tok", ".")

    # Add the ordering edges to specify token order.
    # The names of the source and target nodes are given as arguments,
    # followed by the component layer, type and name.
    g.add_edge("tutorial/doc1#t1", "tutorial/doc1#t2", "annis", "Ordering", "")
    g.add_edge("tutorial/doc1#t2", "tutorial/doc1#t3", "annis", "Ordering", "")
    g.add_edge("tutorial/doc1#t3", "tutorial/doc1#t4", "annis", "Ordering", "")
    g.add_edge("tutorial/doc1#t4", "tutorial/doc1#t5", "annis", "Ordering", "")
    g.add_edge("tutorial/doc1#t5", "tutorial/doc1#t6", "annis", "Ordering", "")
    g.add_edge("tutorial/doc1#t6", "tutorial/doc1#t7", "annis", "Ordering", "")

    cs.apply_update("tutorial", g)
    # this now includes the "tutorial"
    print(cs.list())

    number_of_matches = cs.count("tutorial", 'tok=/.*s.*/')
    print(number_of_matches)
    matches = cs.find("tutorial", 'tok=/.*s.*/', offset=0, limit=100)
    print(matches)

    matches = cs.find("tutorial", 'tok . tok', offset=0, limit=100)
    for m in matches:
        print(m)
        G = cs.subgraph("tutorial", node_name_from_match(m), ctx_left=2, ctx_right=2)
        print("Number of nodes in subgraph: " + str(len(G.nodes)))

    g = GraphUpdate()
    # create the corpus and document node
    g.add_node('tutorial', node_type='corpus')
    g.add_node('tutorial/doc1', node_type='corpus')
    g.add_edge('tutorial/doc1','tutorial', 'annis', 'PartOf', '')
    # add the corpus structure to the existing nodes
    g.add_edge('tutorial/doc1#t1','tutorial/doc1', 'annis', 'PartOf', '')
    g.add_edge('tutorial/doc1#t2','tutorial/doc1', 'annis', 'PartOf', '')
    g.add_edge('tutorial/doc1#t3','tutorial/doc1', 'annis', 'PartOf', '')
    g.add_edge('tutorial/doc1#t4','tutorial/doc1', 'annis', 'PartOf', '')
    g.add_edge('tutorial/doc1#t5','tutorial/doc1', 'annis', 'PartOf', '')
    g.add_edge('tutorial/doc1#t6','tutorial/doc1', 'annis', 'PartOf', '')
    g.add_edge('tutorial/doc1#t7','tutorial/doc1', 'annis', 'PartOf', '')
    # apply the changes
    cs.apply_update('tutorial', g)
    # get the whole document as graph
    G = cs.subcorpus_graph('tutorial', ['tutorial/doc1'])
    print(G.nodes)

