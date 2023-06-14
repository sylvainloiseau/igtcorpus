from igtcorpus.corpusobj import Corpus, Text, Paragraph
from igtcorpus.emeld import Emeld
from igtcorpus import cli
import pytest
import lxml.etree as ET
import sys
import logging

LOGGER = logging.getLogger(__name__)

def test_emeld_summary(capsys, caplog, tmp_path):
    output_filename = f"{tmp_path}/test"
    out = _run_emeld(["emeld", "summary", "tests/data/test.emeld.xml"], capsys, caplog, tmp_path)
    LOGGER.info(out)

def test_emeld2json(capsys, caplog, tmp_path):
    output_filename = f"{tmp_path}/test"
    out = _run_igtc(["igtc", "-i", "tests/data/test.emeld.xml", "-o", output_filename, "-f", "emeld", "-t", "json", "-l", "", "-m", ""], capsys, caplog, tmp_path)
    LOGGER.info(out)
    LOGGER.info("Output file: {output_filename}")

# def test_emeld2conll_tww(capsys, caplog, tmp_path):
#     output_filename = ""
#     out = _run_igtc(["igtc", "-i", "/home/sylvain/Corpus/Tuwari/EmeldLift/INTERLINEAR20230613.xml", "-o", "/home/sylvain/Corpus/Tuwari/Conversion/conllu/conll/", "-f", "emeld", "-t", "conll", "-l", "tww", "-m", "en"], capsys, caplog, tmp_path)
#     LOGGER.info(out)
#     LOGGER.info("Output file: {output_filename}")

def _run_emeld(args, capsys, caplog, tmp_path):
    _run_cli("emeld", args, capsys, caplog, tmp_path)

def _run_igtc(args, capsys, caplog, tmp_path):
    _run_cli("igtc", args, capsys, caplog, tmp_path)

def _run_cli(cmd_name, args, capsys, caplog, tmp_path):
    try:
        sys.argv = args
        cmd = getattr(cli, cmd_name)
        cmd()
    except SystemExit:
        captured = capsys.readouterr()
        print(captured.err)
        assert False
    captured = capsys.readouterr()
    return captured.out

