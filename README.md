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
The main function is a CLI tool [`piminer.py`](piminer.py). The function is called in the following way from a shell window:

    ./piminer --input_file [your file] --regex_input [regex patterns]

## Disclaimer
This repository is intended only as a way for me to organize my thoughts and my work.

Please review the [University of Michigan Dearborn Academic Code of Conduct](http://catalog.umd.umich.edu/graduate/academic-policies/academic-code-of-conduct/).
