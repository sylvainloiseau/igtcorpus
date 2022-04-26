Utility for IGT (interlinear glossed texts).

# Installation

```
pip install git+https://github.com/sylvainloiseau/igt-tools.git#egg=igttools
```

# Usage

```
from igttools.elan import ElanCorpoAfr
from igttools.igt import Corpus
from igttools.emeld import Emeld
from igttools.json import ToJson

# Read...
# - EAF (elan) file
eaf = ElanCorpoAfr("tests/data/BEJ_MV_CONV_01_RICH.EAF")
corpus = eaf.get_igt()
# - Emeld document
corpus = Emeld.read("tests/data/test.emeld.xml")
# - json
corpus = ToJson.read("tests/data/tiny.json")

# ...Write...
# - as emeld
Emeld.write(corpus, "corpus.emeld")
# - as JSON
ToJson.write(corpus, "corpus.json")
```

