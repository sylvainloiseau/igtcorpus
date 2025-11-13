Utilities for converting interlinear glossed texts (IGT) corpora between the following formats:

- EMELD (Cathy Bow, Baden Hughes, Steven Bird, (2003) "Towards a general model of interlinear text", *Proceedings of Emeld workshop 2003*) [Online](https://www.researchgate.net/publication/244446092_Towards_a_general_model_of_interlinear_text). Used in particular by [SIL FLEX](https://software.sil.org/fieldworks/)
- CONLL
- ELAN [Elan website](https://archive.mpi.nl/tla/elan) [in a specific configuration -- can be adapted to others]
- JSON representation of Emeld


# Installation

```
pip install git+https://github.com/sylvainloiseau/igtcorpus.git#egg=igtcorpus
```

# Usage

Two commnand line utilities are installed.

## emeld: info about an Emeld document

Print a summary of the fields used in the document and their number of occurrences.

```console
$ emeld summary tests/data/EmeldByFlex.xml
Unit 'EmeldUnit.morph':
        503 occurrences
        fields:
                cf, tww (502 occurrences)
                gls, en (502 occurrences)
                glsAppend, en (4 occurrences)
                glsPrepend, en (4 occurrences)
                hn, tww (231 occurrences)
                msa, en (502 occurrences)
                txt, tww (503 occurrences)
                variantTypes, en (4 occurrences)
Unit 'EmeldUnit.word':
        366 occurrences
        fields:
                gls, en (220 occurrences)
                pos, en (262 occurrences)
                punct, tww (61 occurrences)
                txt, tww (273 occurrences)
Unit 'EmeldUnit.phrase':
        0 occurrences
        fields:
                gls, en (31 occurrences)
                gls, tpi (32 occurrences)
                gls, tww (1 occurrences)
                lit, en (32 occurrences)
                note, tww (10 occurrences)
                note, en (12 occurrences)
                segnum, en (32 occurrences)
Unit 'EmeldUnit.paragraph':
        6 occurrences
        fields:
Unit 'EmeldUnit.text':
        1 occurrences
        fields:
                title, en (1 occurrences)
                title-abbreviation, en (1 occurrences)
```

## igtc: conversion between format

Command line interface:

```console
$ igtc -i input.xml -o output.json -f emeld -t json -l tww -m en
```

See the doc:

```
$ igtc -h
usage: igtc [-h] [--verbose] --output OUTPUT --input INPUT --fromformat {json,emeld,elan} --toformat {json,emeld,conll} [--olanguage OLANGUAGE] [--mlanguage MLANGUAGE]

Utilities for converting between interlinear glossed texts formats.

options:
  -h, --help            show this help message and exit
  --verbose, -v         output detailled information
  --output OUTPUT, -o OUTPUT
                        output file
  --input INPUT, -i INPUT
                        input file
  --fromformat {json,emeld,elan}, -f {json,emeld,elan}
                        input file format
  --toformat {json,emeld,conll}, -t {json,emeld,conll}
                        output file format
  --olanguage OLANGUAGE, -l OLANGUAGE
                        Object language
  --mlanguage MLANGUAGE, -m MLANGUAGE
                        Meta language
```

# API

```
from igtcorpus.elan import ElanCorpoAfr
from igtcorpus.igt import Corpus
from igtcorpus.emeld import Emeld
from igtcorpus.json import EmeldJson

# Read...
# - EAF (elan) file
corpus = ElanCorpoAfr.read("tests/data/BEJ_MV_CONV_01_RICH.EAF")
# - Emeld document
corpus = Emeld.read("tests/data/test.emeld.xml")
# - json
corpus = EmeldJson.read("tests/data/tiny.json")

# ...Write...
# - as emeld
Emeld.write(corpus, "corpus.emeld")
# - as JSON
EmeldJson.write(corpus, "corpus.json")
```
