from pathlib import Path
from igtcorpus.corpusobj import Corpus, Text, Paragraph, Sentence, Word, Morph, Properties, LingUnit
from typing import List, Tuple
import os.path 
import logging
import pandas as pd

# TODO too much copied from Conll; refactor needed

class PlainText():

  EMPTY_FIELD = "_"
  LOGGER = logging.getLogger(__name__)

  @classmethod
  def write(cls,
            corpus: Corpus,
            outdir:str=None,
            text_name_field=None,
            text_id_field=None,
            sentence_id_field=None,
            sentence_text_field=None,
            sentence_ft_field="gls",
            sentence_extra_field:List[str]=[],
            morph_txt_field="txt",
            morph_lemma_field="lemma",
            homonym_field="cf",
            morph_pos_field="pos",
            morph_extra_field:List[Tuple[str, str]]=[]) -> None:
      """
      Write a corpus as plain text file(s)

      :param Corpus corpus: the corpus to be treated
      :param str outdir: name of the file
      :param str text_name_field: property holding the name of text unit.  Is used as file name and as first part of sentence ids. If None or not existing, the indice of the text is used.
      :param str sentence_id_field: property holding the id of sentence unit. Suffixed to the text name. If None or not existing, the indice of the sentence is used.
      :param str sentence_text_field: the property holding the text of sentence unit. If None or non existing, the concatenation of the text of each morph unit is used.
      :param str sentence_ft_field: the property holding the free translation of sentence unit. If None or non existing, "_" is used.
      :param str sentence_extra_field: other properties of sentence unit to be recopied in sentence headers of plain text document.
      :param str morph_txt_field: property holding the text of token unit.
      :param str morph_lemma_field: property holding the lemma of token unit. If None or non existing, "_" is used
      :param str morph_pos_field: property holding the pos of token unit. If None or non existing, "_" is used
      :param str morph_extra_field: other properties of morph units to be recopied in the extra (MISC) column for each morph. Each element of the list is a tuple (name / property).
      """

      if not os.path.isdir(outdir):
          raise Exception(f"Not a directory: {outdir}")

      for ti, text in enumerate(corpus.get(Text)):
          text_properties = text.get_properties()
          textid = PlainText._get_prop_or_default(text_properties, text_id_field, str(ti))
          texttitle = PlainText._get_prop_or_default(text_properties, text_name_field, "")
          filename = outdir + "/" + textid + ".txt"
          f = open(filename, 'w')
          s_n = 0
          for pi, paragraph in enumerate(text.get(Paragraph)):
              for si, sentence in enumerate(paragraph.get(Sentence)):
                  s_n += 1
                  sentence_properties = sentence.get_properties()
                  morphs_by_words: List[List[Morph]] = [w.get(Morph) for w in sentence.get(Word)]
                  morphs: List[Morph] = [m for ms in morphs_by_words for m in ms]

                  origin_s_id = PlainText._get_prop_or_default(
                      sentence_properties,
                      sentence_id_field,
                      "/".join([str(pi + 1), str(si + 1)]) #sentence number is 1-based
                  )

                  s_text = PlainText._get_prop_or_default(sentence_properties, sentence_text_field, "")
                  morph_txt = PlainText._get_forms(morphs, morph_txt_field)
                  s_text = s_text or " ".join(txt for txt in morph_txt)
                  s_text_en = PlainText._get_prop_or_default(sentence_properties, sentence_ft_field, PlainText.EMPTY_FIELD)

                  PlainText._write_sentence_field(f, "sent_id", textid + "__" + str(s_n))
                  PlainText._write_sentence_field(f, "doc_id", textid)
                  PlainText._write_sentence_field(f, "doc_title", texttitle)
                  PlainText._write_sentence_field(f, "origin_s_id", origin_s_id)
                  for sfield in sentence_extra_field:
                      sv = PlainText._get_prop_or_default(sentence_properties, sfield, "_")
                      PlainText._write_sentence_field(f, sfield, sv)

                  #df = pd.DataFrame(index=range(5),columns=range(len(morphs)))
                  # pd.DataFrame(np.empty((3, 4), dtype = np.str))

                 # word_txt: List[str] = [PlainText._get_prop_or_default(w.get_properties(), "txt") for w in sentence.get(Word)]
                 # morphs:List[str] = [ "".join(PlainText._get_prop_or_default(m.get_properties(), morph_txt_field) for m in w.get(Morph)) for w in sentence.get(Word) ]
                 # lemma:List[str] = [[PlainText._get_prop_or_default(m.get_properties(), morph_lemma_field) for m in w.get(Morph)] for w in sentence.get(Word)]
                 # homonym_index:List[str] = [PlainText._get_prop_or_default(m.get_properties(), homonym_field, "") for m in w.get(Morph)]
                 #   l = [l if hi =="" else l + "_" + hi for l, hi in zip(lemma, homonym_index)]
                 #   l = "".join(l)
 
                  f.write("-W: " + " ".join(word_txt) + "\n")
                  f.write("-M: ")
                  for w in sentence.get(Word):
                    morphs:str = "".join(PlainText._get_prop_or_default(m.get_properties(), morph_txt_field) for m in w.get(Morph))
                    f.write(f"{morphs} ")
                  f.write("\n")

                  f.write("-L: ")
                  for w in sentence.get(Word):
                    lemma = [PlainText._get_prop_or_default(m.get_properties(), morph_lemma_field) for m in w.get(Morph)]
                    homonym_index = [PlainText._get_prop_or_default(m.get_properties(), homonym_field, "") for m in w.get(Morph)]
                    l = [l if hi =="" else l + "_" + hi for l, hi in zip(lemma, homonym_index)]
                    l = "".join(l)
                    f.write(f"{l} ")
                  f.write("\n")

                  f.write("P: ")
                  for w in sentence.get(Word):
                    pos = "-".join(PlainText._get_prop_or_default(m.get_properties(), morph_pos_field) for m in w.get(Morph))
                    f.write(f"{pos} ")
                  f.write("\n")

                  f.write("G: ")
                  for w in sentence.get(Word):
                    gls = "-".join(PlainText._get_prop_or_default(m.get_properties(), "gls") for m in w.get(Morph))
                    f.write(f"{gls} ")
                  f.write("\n")

                  PlainText._write_line(f, "-T", s_text_en)
                  f.write("\n")
                  
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
            PlainText.LOGGER.warning(f"No attribute {morph_txt_field} for morph {m}.")
            if "txt" in ks:
                txt = p["txt"]
                PlainText.LOGGER.warning("Defaulting to 'txt'")
            else:
                tk = [si for si in p.keys() if si.startswith('txt')]
                if len(tk) > 0:
                    txt = p[tk[0]]
                    PlainText.LOGGER.warning(f"Defaulting to '{tk[0]}'")
                else:
                    PlainText.LOGGER.warning("No text found")
                    txt = PlainText.EMPTY_FIELD
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
      return PlainText._get_prop_or_default(props, key, PlainText.EMPTY_FIELD)

  @staticmethod
  def _get_extra(prop:Properties, extra_field: List[Tuple[str, str]]):
      if len(extra_field) == 0:
          return PlainText.EMPTY_FIELD
      tuples = list(filter(lambda x : x[1] in prop, extra_field))
      if len(tuples) == 0:
          return PlainText.EMPTY_FIELD
      ps = {tuple[0]: prop[tuple[1]] for tuple in tuples}
      return '|'.join(key + "=" + value for key, value in ps.items())

  @staticmethod
  def _write_sentence_field(fhandler, field, value):
     fhandler.write(f"# {field} = {value}\n")

  @staticmethod
  def _write_line(fhandler, field, value):
     fhandler.write(f"{field}: {value}\n")

  @staticmethod
  def _write_token(fhandler, cols):
     fhandler.write("\t".join(cols))
     fhandler.write("\n")

  @staticmethod
  def _write_sentence_sep(fhandler):
     fhandler.write("\n")

