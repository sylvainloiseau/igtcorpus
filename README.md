Utility for IGT (interlinear glossed texts).

# Installation

```
pip install git+https://github.com/sylvainloiseau/igtcorpus.git#egg=igtcorpus
```

# Usage

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

