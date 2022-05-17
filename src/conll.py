from pathlib import Path
from igtcorpus.igt import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import List


class Conll():

  EMPTY_FIELD = "_"

  @staticmethod
  def get_field(properties:Properties, field):
      if field in properties and properties[field] is not None:
          return properties[field]
      else:
          return Conll.EMPTY_FIELD

  @staticmethod
  def get_extra(prop:Properties, extra_field: List[str]):
      if len(extra_field) == 0:
          return Conll.EMPTY_FIELD
      fs = list(filter(lambda x : x in prop, extra_field))
      if len(fs) == 0:
          return Conll.EMPTY_FIELD
      ps = {key: prop[key] for key in fs}
      return '|'.join(key + "=" + value for key, value in ps.items())

  @classmethod
  def write(cls, igt: Corpus, outfile: str, sentence_id_field=None,
            sentence_text_field=None, sentence_ft_field="gls.tpi",
            txt_field="txt.tww", lemma_field="cf.tww",
            pos_field="msa.en", extra_field=["gls.en"]) -> None:
      f = open(outfile, 'w')
      for i, t in enumerate(igt.get(Text)):
          for j, p in enumerate(t.get(Paragraph)):
              for k, s in enumerate(p.get(Sentence)):
                  morphs_by_words: List[List[Morph]] = [w.get(Morph) for w in s.get(Word)]
                  morphs: List[Morph] = [m for ms in morphs_by_words for m in ms]

                  if sentence_id_field is None:
                      s_id = ".".join([str(j), str(k)])
                  if sentence_text_field is None:
                    text = " ".join(m.get_properties()[txt_field] for m in morphs)  

                  f.write("# sent_id = " + s_id + "\n")
                  f.write("# text = " + text + "\n")
                  f.write("# text_en = " + (s.get_properties()[sentence_ft_field] or "-") + "\n")
                  for l, m in enumerate(morphs):
                      props = m.get_properties()

                      txt = Conll.get_field(props, txt_field)
                      lemma = Conll.get_field(props, lemma_field)
                      pos = Conll.get_field(props, pos_field)
                      extra = Conll.get_extra(props, extra_field)
                      line = [str(l + 1), txt, lemma, pos,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              extra]
                      f.write("\t".join(line))
                      f.write("\n")
                  f.write("\n")
      f.close()


