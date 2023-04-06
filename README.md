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

Command line interface:

```console
$ igtc -i input.xml -o output.json -f emeld -t json 
```

See the doc:

```
$ igtc -h
usage: igtc [-h] [--verbose] --output OUTPUT --input INPUT --fromformat {json,emeld,elan} --toformat {json,emeld,conll}

Utilities for converting between interlinear glossed texts formats.

optional arguments:
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
