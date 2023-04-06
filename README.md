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
