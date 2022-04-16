Utility for IGT (interlinear glossed texts).

# Installation

pip install git+https://github.com/sylvainloiseau/igt-tools.git

# Usage

```
from igttools.elan import ElanCorpoAfr
from igttools.igt import IGT
from igttools.emeld import Emeld

# Read EAF file
obj = ElanCorpoAfr("tests/data/BEJ_MV_CONV_01_RICH.EAF")
igt = obj.get_igt()

# Read emeld document
igt = Emeld.read("tests/data/test.emeld.xml")

# Write as emeld
Emeld.write(igt, "emeld.xml")
```

