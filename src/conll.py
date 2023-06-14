from pathlib import Path
from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import List, Tuple
import os.path 
import logging

class Conll():

  EMPTY_FIELD = "_"
  LOGGER = logging.getLogger(__name__)

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
      :param str morph_extra_field: other properties of morph units to be recopied in the extra (MISC) column for each morph. Each element of the list is a tuple (conll name / property).
      """

      if not os.path.isdir(outdir):
          raise Exception(f"Not a directory: {outdir}")

      for ti, text in enumerate(corpus.get(Text)):
          text_properties = text.get_properties()
          textname = Conll._get_prop_or_default(text_properties, text_name_field, str(ti))
          filename = outdir + "/" + textname + ".conll"
          f = open(filename, 'w')
          for pi, paragraph in enumerate(text.get(Paragraph)):
              for si, sentence in enumerate(paragraph.get(Sentence)):
                  sentence_properties = sentence.get_properties()
                  morphs_by_words: List[List[Morph]] = [w.get(Morph) for w in sentence.get(Word)]
                  morphs: List[Morph] = [m for ms in morphs_by_words for m in ms]

                  s_id = Conll._get_prop_or_default(
                      sentence_properties,
                      sentence_id_field,
                      "/".join([str(pi), str(si)])
                  )

                  s_text = Conll._get_prop_or_default(sentence_properties, sentence_text_field, "")
                  forms = Conll._get_forms(morphs, morph_txt_field)
                  s_text = s_text or " ".join(txt for txt in forms)
                  s_text_en = Conll._get_prop_or_default(sentence_properties, sentence_ft_field, Conll.EMPTY_FIELD)

                  Conll._write_sentence_field(f, "sent_id", s_id)
                  Conll._write_sentence_field(f, "text", s_text)
                  Conll._write_sentence_field(f, "text_en", s_text_en)
                  Conll._write_sentence_field(f, "doc_id", textname)

                  for sfield in sentence_extra_field:
                      sv = Conll._get_prop_or_default(sentence_properties, sfield, "_")
                      Conll._write_sentence_field(f, sfield, sv)

                  for im, m in enumerate(morphs):
                      props = m.get_properties()
                      txt = forms[im]
                      lemma = Conll._get_prop_or_empty(props, morph_lemma_field)
                      pos = Conll._get_prop_or_empty(props, morph_pos_field)
                      extra = Conll._get_extra(props, morph_extra_field)
                      token_columns = [str(im + 1),
                                    txt,
                                    lemma,
                                    pos,
                                    Conll.EMPTY_FIELD,
                                    Conll.EMPTY_FIELD,
                                    Conll.EMPTY_FIELD,
                                    Conll.EMPTY_FIELD,
                                    Conll.EMPTY_FIELD,
                                    extra
                      ]
                      Conll._write_token(f, token_columns)
                  Conll._write_sentence_sep(f)
          f.close()

  @staticmethod
  def _get_forms(morphs: List[Morph], morph_txt_field) -> List[str]:
    #s_text = s_text or " ".join(m.get_properties()[morph_txt_field] for m in morphs)  
    txts = [""] * len(morphs)
    for mi, m in enumerate(morphs):
        p = m.get_properties()
        ks = p.keys()
        if morph_txt_field in ks:
            txt = p[morph_txt_field]
        else:
            Conll.LOGGER.warning(f"No attribute {morph_txt_field} for morph {m}.")
            if "txt" in ks:
                txt = p["txt"]
                Conll.LOGGER.warning("Defaulting to 'txt'")
            else:
                tk = [si for si in p.keys() if si.startswith('txt')]
                if len(tk) > 0:
                    txt = p[tk[0]]
                    Conll.LOGGER.warning(f"Defaulting to '{tk[0]}'")
                else:
                    Conll.LOGGER.warning("No text found")
                    txt = Conll.EMPTY_FIELD
        txts[mi] = txt
    return txts

  @staticmethod
  def _get_prop_or_default(props:Properties, key:str, default="") -> str:
      if key is not None and key in props and props[key] is not None:
          return props[key]
      else:
          return default

  @staticmethod
  def _get_prop_or_empty(props:Properties, key:str):
      return Conll._get_prop_or_default(props, key, Conll.EMPTY_FIELD)

  @staticmethod
  def _get_extra(prop:Properties, extra_field: List[Tuple[str, str]]):
      if len(extra_field) == 0:
          return Conll.EMPTY_FIELD
      tuples = list(filter(lambda x : x[1] in prop, extra_field))
      if len(tuples) == 0:
          return Conll.EMPTY_FIELD
      ps = {tuple[0]: prop[tuple[1]] for tuple in tuples}
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

