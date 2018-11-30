# Detecting PII in Documents
This repository contains tools for discovering PII as a final project for CIS 545. The goal is to detect information that may be sensitive in a document in order to prevent accidental disclosure. We do not recommend the use of these tools outside of academic settings as they have not been fully validated.

## Dependencies
The full toolset relies heavily on a number of dependencies. NOTE: This list is frequently changing. Currently, there is no tooling to manage dependencies, so please check to make sure you have everything installed:

```python
import argparse
import os
import pandas as pd
import numpy as np
import math
import textract
import re
import spacy
import time
from tqdm import tqdm
from sklearn import covariance, cluster
import sklearn.metrics as met
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from itertools import cycle
```

## `piminer.py`
[`piminer.py`](PIMINER.py) is a CLI script used to identify potentially identifiable data points and to construct a dataset from these points. [`piminer.py`](PIMINER.py) uses regular expression pattern matching and [spaCy's](https://spacy.io/) off-the-shelf Named Entity Recognition functionality. [`piminer.py`](PIMINER.py) has the following arguments:

1. `--src`: A text file to extract PII elements from.
1. `--r`: A text file containing regular expressions and labels. See and example here: [`patterns.txt`](patterns.txt).
1. `--model`: An optional argument for declaring a custom NER model. Default to `en_core_web_md`.

### Sample Invocation
The script is invoked in the following way from a shell window:

```
./piminer.py --input_file [your file] --regex_input [regex patterns] --model [model]
```

Note: the output of `piminer.py` is saved to the directory that `piminer.py` is run from. The output is not intended to be human friendly, but is human readable.


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

## `affinity_clustering.py`
[`affinity_clustering.py`](affinity_clustering.py) will be used to run analysis on the output of `piminer.py` in order to identify clusters and highly similar information. Brief description of each argument below:

1. `--src` the source file to generate clusters from. Expects data in the output format of `piminer.py`.
1. `--pref` a parameter from which to base exemplar identification. "High values of the preferences will cause affinity propagation to find many exemplars (clusters), while low values will lead to a small number of exemplars (clusters). A good initial choice for the preference is the minimum similarity or the median similarity."

```
[1]“FAQ for Affinity Propagation.” [Online]. Available: https://www.psi.toronto.edu/affinitypropagation/faq.html. [Accessed: 08-Nov-2018].
```

1. `--plot` a binary argument used to determine if a visualization of the clusters is generated.
1. `--damp` an optional flag to control the damping parameter of the affinity model. See:

```
[1]“FAQ for Affinity Propagation.” [Online]. Available: https://www.psi.toronto.edu/affinitypropagation/faq.html. [Accessed: 08-Nov-2018].
```

1. `--dest` the destination filepath.

### Sample Invocation

```
./affinity_clustering --input_file [piminer output file]
```

### Citations

```
[1]D. Dueck, “AFFINITY PROPAGATION: CLUSTERING DATA BY PASSING MESSAGES,” p. 154.
[2]B. J. Frey and D. Dueck, “Clustering by Passing Messages Between Data Points,” Science, vol. 315, no. 5814, pp. 972–976, Feb. 2007.
[3]K. Wang, J. Zhang, D. Li, X. Zhang, and T. Guo, “Adaptive Affinity Propagation Clustering,” arXiv:0805.1096 [cs], May 2008.
```

## Disclaimer
This repository is intended only as a way for us to organize our thoughts and our work.

Please review the [University of Michigan Dearborn Academic Code of Conduct](http://catalog.umd.umich.edu/graduate/academic-policies/academic-code-of-conduct/).
