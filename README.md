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

# Read EAF file
obj = ElanCorpoAfr("tests/data/BEJ_MV_CONV_01_RICH.EAF")
corpus = obj.get_igt()

# Read emeld document
corpus = Emeld.read("tests/data/test.emeld.xml")

# Write as emeld
Emeld.write(corpus, "emeld.xml")
```

