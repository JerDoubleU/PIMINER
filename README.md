# Detecting PII in Documents
This repository contains tools for discovering PII as a final project for CIS 545. The goal is to detect information that may be sensitive in a document in order to prevent accidental disclosure. We do not recommend the use of these tools outside of academic settings as they have not been fully validated.

## Dependencies
The full toolset relies heavily on a number of dependencies. NOTE: This list is frequently changing. Currently, there is no tooling to manage dependencies, so please check to make sure you have everything installed:

```python
import argparse
import os
import pandas as pd
import math
import textract
import re
import spacy
import time
from spacy.symbols import nsubj, VERB
from sklearn import covariance, cluster
from sklearn.cluster import AffinityPropagation
import numpy as np
import sklearn.metrics as met
import matplotlib.pyplot as plt
from itertools import cycle
```

## `piminer.py`
[`piminer.py`](PIMINER.py) is a CLI script. The script is invoked in the following way from a shell window:

```
./piminer.py --input_file [your file] --regex_input [regex patterns]
```

Note: the output of `piminer.py` is save to the directory that `piminer.py` is run from. The output is not intended to be human friendly, but is human readable.

## `patterns.txt`
The purpose of [`patterns.txt`](patterns.txt) is to allow for further customization of the regular expression matching. This may be important in domains with very specifically formatted PII. The format of `patterns.txt` is all follows:

```
[ENTITY TYPE]; [REGULAR EXPRESSION]
```

For example:

```
DATE; ([a-zA-Z]+) (\d+)
```

Note: any file in this format can be supplied via argument `--regex_input [regex patterns]`. Regular expressions depend on `python re` and must be compatible with `python 3.6` or later.

## `mineRelations.py`
[`mineRelations.py`](mineRelations.py) is currently under development. This script will be used to run analysis on the output of `piminer.py` in order to identify clusters and highly similar information. Current invocation:

```
./mineRelations --input_file [piminer output file]
```

## Disclaimer
This repository is intended only as a way for me to organize my thoughts and my work.

Please review the [University of Michigan Dearborn Academic Code of Conduct](http://catalog.umd.umich.edu/graduate/academic-policies/academic-code-of-conduct/).
