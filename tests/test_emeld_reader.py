from igtcorpus.emeld_reader import EmeldReader, EmeldPopulateContentHandler, EmeldSpecContentHandler, EmeldUnit
import xml

class TestEmeldSpecContentHandler():

  def testTiny(self):
    filename = "tests/data/tiny.emeld.xml"
    handler = EmeldSpecContentHandler()
    xml.sax.parse(filename, handler)
    spec = handler.get_emeld_spec()
    assert spec[EmeldUnit.text][0] == 1
    assert spec[EmeldUnit.morph][0] == 5
    assert len(spec[EmeldUnit.phrase][1]) == 3 # there is 3 distinct field on phrase

class TestEmeldPopulateContentHandler():

  def testTiny(self):
    filename = "tests/data/tiny.emeld.xml"
    handler = EmeldSpecContentHandler()
    xml.sax.parse(filename, handler)
    spec = handler.get_emeld_spec()

    contentHandler = EmeldPopulateContentHandler(spec)
    xml.sax.parse(filename, contentHandler)
    tables = contentHandler.get_tables()
    assert tables[EmeldUnit.text].shape[0] == 1
    assert tables[EmeldUnit.phrase].shape[0] == 2
    assert tables[EmeldUnit.phrase].shape[1] == 4
    assert tables[EmeldUnit.word].shape[0] == 3
    assert tables[EmeldUnit.word].shape[1] == 1
    assert tables[EmeldUnit.morph].shape[0] == 5
    assert tables[EmeldUnit.morph].shape[1] == 4
                    
class TestEmeldReader():

  def test_get_count_and_fields(foo):
    filename = "tests/data/tiny.emeld.xml"
    r = EmeldReader(filename)
    spec = r._get_emeld_spec()
    #print(spec)

  def test_get_corpus(foo):
    filename = "tests/data/tiny.emeld.xml"
    r = EmeldReader(filename)
    c = r.get_corpus()
  
  def testEmeldPopulateContentHandler(foo):
    filename = "tests/data/test.emeld.xml"
    r = EmeldReader(filename)
    spec = r._get_emeld_spec()
    handler = EmeldPopulateContentHandler(spec)
    xml.sax.parse(filename, handler)
    res = handler.get_tables()
    for k in res.keys():
      pass
      # print("================")
      # print(k)
      # print(res[k])
