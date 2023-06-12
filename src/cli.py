import argparse
import sys
import os
from typing import List
import logging
from pathlib import Path
from igtcorpus.elan import ElanCorpoAfr
from igtcorpus.corpusobj import Corpus
from igtcorpus.emeld import Emeld
from igtcorpus.json import EmeldJson
from igtcorpus.conll import Conll

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.FileHandler(os.path.expanduser(Path("~/.igtc.log")), mode="w"))


def _igtc_callback(arg: argparse.Namespace) -> None:
    i = arg.input
    o = arg.output
    t = arg.toformat
    f = arg.fromformat
    corpus: Corpus
    if f == "emeld":
        corpus = Emeld.read(i)
    elif f == "elan":
        corpus = ElanCorpoAfr.read(i)
    elif f == "json":
        corpus = EmeldJson.read(i)
    else:
        raise _exit_with_error_msg(f"Unsupported input format: {f}")

    if t == "emeld":
        Emeld.write(corpus, o)
    elif t == "json":
        EmeldJson.write(corpus, o)
    elif t == "conll":
        morph_txt_field="txt"
        morph_lemma_field="cf"
        if arg.olanguage:
            morph_txt_field=morph_txt_field + "." + arg.olanguage
            morph_lemma_field=morph_lemma_field + "." + arg.olanguage

        sentence_ft_field="gls"
        morph_pos_field="msa"
        morph_extra_field_str = "gls"
        if arg.mlanguage:
            sentence_ft_field=sentence_ft_field + "." + arg.mlanguage
            morph_pos_field=morph_pos_field + "." + arg.mlanguage
            morph_extra_field_str = morph_extra_field_str + "." + arg.mlanguage

        Conll.write(corpus, o,
                morph_txt_field=morph_txt_field,
                sentence_ft_field=sentence_ft_field,
                morph_lemma_field=morph_lemma_field,
                #sentence_extra_field:List[str]=[],
                morph_pos_field=morph_pos_field,
                morph_extra_field = [(morph_extra_field_str, "Gloss")]
                )
    else:
        raise _exit_with_error_msg(f"Unsupported output format: {t}")


def _emeld_summary_callback(arg: argparse.Namespace) -> None:
    corpus = Emeld.read(arg.file)
    u = corpus.get_sub_units()
    print(f"{len(u)} {type(u)}")


def _exit_with_error_msg(msg: str) -> None:
    LOGGER.warning(msg)
    print(msg)
    sys.exit()



def igtc() -> None:
    # Main level
    parser = argparse.ArgumentParser(description='Utilities for converting between interlinear glossed texts formats.')
    parser.add_argument('--verbose', '-v', help='output detailled information', required=False, action='store_true')
    parser.add_argument('--output', '-o', help='output file', required=True)
    # parser.add_argument('--output', '-o', help='output file (or standard output if not specified)', nargs="?",
    #                     default=sys.stdout, type=argparse.FileType("w"))
    parser.add_argument('--input', '-i', help='input file', required=True)
    parser.add_argument('--fromformat', '-f', help='input file format', choices=["json", "emeld", "elan"], required=True, default="emeld")
    parser.add_argument('--toformat', '-t', help='output file format', choices=["json", "emeld", "conll"], required=True, default="conll")
    parser.add_argument('--olanguage', '-l', help='Object language', required=False, default="")
    parser.add_argument('--mlanguage', '-m', help='Meta language', required=False, default="")
    parser.set_defaults(func=_igtc_callback)

    if len(sys.argv) <= 1:
        sys.argv.append('-h')

    # TODO: ???
    if len(sys.argv) == 2 and sys.argv[1] == "convert":
        sys.argv.append('-h')

    argument = parser.parse_args()

    for arg in vars(argument):
        LOGGER.info(f"Argument: {arg}, / {getattr(argument, arg)}")

    p = Path(argument.input)
    # if not os.access(argument.input, os.R_OK):
    if not p.expanduser().exists():
        _exit_with_error_msg(f"{argument.input} is not readable")
    argument.func(argument)

def emeld() -> None:
    parser = argparse.ArgumentParser(description='Utilities for emeld documents (see also `igtc`).')
    parser.add_argument('--verbose', '-v', help='output detailled information', required=False, action='store_true')

    command_subparser = parser.add_subparsers(title="subcommand", description="one valid subcommand",
                                              help='subcommand: the main action to run. See `subcommand -h` for more '
                                                   'info', required=True)

    # summary subcommand
    summary = command_subparser.add_parser('summary', help='Print summary about the corpus')
    summary.set_defaults(func=_emeld_summary_callback)

    parser.add_argument('file', type=str, help='Emeld document filename')

    if len(sys.argv) <= 1:
        sys.argv.append('-h')

    argument = parser.parse_args()

    for arg in vars(argument):
        LOGGER.info(f"Argument: {arg}, / {getattr(argument, arg)}")

    p = Path(argument.file)
    if not p.expanduser().exists():
        _exit_with_error_msg(f"{argument.file} is not readable")

    argument.func(argument)
