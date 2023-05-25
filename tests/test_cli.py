from igtcorpus.igt import Corpus, Text, Paragraph
from igtcorpus.emeld import Emeld
from igtcorpus.cli import igtc
import pytest
import lxml.etree as ET
import sys
import logging

LOGGER = logging.getLogger(__name__)

def test_emeld2json(capsys, caplog, tmp_path):
    output_filename = f"{tmp_path}/test"
    out = _run_cli(["igtc", "-i", "tests/data/test.emeld.xml", "-o", output_filename, "-f", "emeld", "-t", "json"], capsys, caplog, tmp_path)
    LOGGER.info(out)
    LOGGER.info("Output file: {output_filename}")

def _run_cli(args, capsys, caplog, tmp_path):
    try:
        sys.argv = args
        igtc()
    except SystemExit:
        captured = capsys.readouterr()
        print(captured.err)
        assert False
    captured = capsys.readouterr()
    return captured.out

