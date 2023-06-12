from pathlib import Path
from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import List, Tuple
import os.path 


class Conll():

  EMPTY_FIELD = "_"

  @classmethod
  def write(cls,
            corpus: Corpus,
            outdir:str=None,
            text_name_field=None,
            sentence_id_field=None,
            sentence_text_field=None,
            sentence_ft_field="gls",
            sentence_extra_field:List[str]=[],
            morph_txt_field="txt",
            morph_lemma_field="lemma",
            morph_pos_field="pos",
            morph_extra_field:List[Tuple[str, str]]=[]) -> None:
      """
      Write a corpus as Conll-U document(s)

      :param Corpus corpus: the corpus to be treated
      :param str outdir: name of the file
      :param str text_name_field: property holding the name of text unit.  Is used as file name and as first part of sentence ids. If None or not existing, the indice of the text is used.
      :param str sentence_id_field: property holding the id of sentence unit. Suffixed to the text name. If None or not existing, the indice of the sentence is used.
      :param str sentence_text_field: the property holding the text of sentence unit. If None or non existing, the concatenation of the text of each morph unit is used.
      :param str sentence_ft_field: the property holding the free translation of sentence unit. If None or non existing, "_" is used.
      :param str sentence_extra_field: other properties of sentence unit to be recopied in sentence headers of Conll document.
      :param str morph_txt_field: property holding the text of token unit.
      :param str morph_lemma_field: property holding the lemma of token unit. If None or non existing, "_" is used
      :param str morph_pos_field: property holding the pos of token unit. If None or non existing, "_" is used
      :param str morph_extra_field: other properties of morph units to be recopied in the extra column for each morph.
      """

      if not os.path.isdir(outdir):
          raise Exception(f"Not a directory: {outdir}")

      for i, text in enumerate(corpus.get(Text)):
          textname = Conll._get_value_or_default(text, text_name_field, str(i))
          filename = outdir + "/" + textname + ".conll"
          f = open(filename, 'w')
          for j, paragraph in enumerate(text.get(Paragraph)):
              for k, sentence in enumerate(paragraph.get(Sentence)):
                  morphs_by_words: List[List[Morph]] = [w.get(Morph) for w in sentence.get(Word)]
                  morphs: List[Morph] = [m for ms in morphs_by_words for m in ms]

                  s_id = Conll._get_value_or_default( sentence,
                          sentence_id_field,
                          ".".join([textname, str(j), str(k)]))

                  s_text = Conll._get_value_or_default(sentence, sentence_text_field, "")
                  s_text = s_text or " ".join(m.get_properties()[morph_txt_field] for m in morphs)  

                  s_text_en = Conll._get_value_or_default(sentence, sentence_ft_field, "_")

                  Conll._write_sentence_field(f, "sent_id", s_id)
                  Conll._write_sentence_field(f, "text", s_text)
                  Conll._write_sentence_field(f, "text_en", s_text_en)

                  for sfield in sentence_extra_field:
                      sv = Conll._get_value_or_default(sentence, sfield, "_")
                      Conll._write_sentence_field(f, sfield, sv)

                  for l, m in enumerate(morphs):
                      props = m.get_properties()

                      txt = Conll._get_field(props, morph_txt_field)
                      lemma = Conll._get_field(props, morph_lemma_field)
                      pos = Conll._get_field(props, morph_pos_field)
                      extra = Conll._get_extra(props, morph_extra_field)
                      token_cols = [str(l + 1), txt, lemma, pos,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              Conll.EMPTY_FIELD,
                              extra]
                      Conll._write_token(f, token_cols)
                  Conll._write_sentence_sep(f)
          f.close()

  @staticmethod
  def _get_value_or_default(unit, mykey, default="") -> str:
      props = unit.get_properties()
      if mykey is not None and mykey in props:
          res = props[mykey] or default
      else:
          res = default
      return res

  @staticmethod
  def _get_field(properties:Properties, field):
      if field in properties and properties[field] is not None:
          return properties[field]
      else:
          return Conll.EMPTY_FIELD

  @staticmethod
  def _get_extra(prop:Properties, extra_field: List[str]):
      if len(extra_field) == 0:
          return Conll.EMPTY_FIELD
      fs = list(filter(lambda x : x[0] in prop, extra_field))
      if len(fs) == 0:
          return Conll.EMPTY_FIELD
      ps = {tup[1]: prop[tup[0]] for tup in fs}
      return '|'.join(key + "=" + value for key, value in ps.items())

  @staticmethod
  def _write_sentence_field(fhandler, field, value):
     fhandler.write(f"# {field} = {value}\n")

  @staticmethod
  def _write_token(fhandler, cols):
     fhandler.write("\t".join(cols))
     fhandler.write("\n")

  @staticmethod
  def _write_sentence_sep(fhandler):
     fhandler.write("\n")

