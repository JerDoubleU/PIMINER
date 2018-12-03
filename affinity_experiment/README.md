# Experiment
This experiment runs `affinity_clustering.py` on `output_data/pm_std_updated_doctored_data.csv` at various different values for preference. The results are stored to show 'tighter' clusters at lower (more negative) values for `--pref`.

_"preference: The preference of point i, called p(i) or s(i,i), is the a priori suitability of point i to serve as an exemplar. Preferences can be set to a global (shared) value, or customized for particular data points. High values of the preferences will cause affinity propagation to find many exemplars (clusters), while low values will lead to a small number of exemplars (clusters). A good initial choice for the preference is the minimum similarity or the median similarity."_

from:

```
[1]“FAQ for Affinity Propagation.” [Online]. Available: https://www.psi.toronto.edu/affinitypropagation/faq.html. [Accessed: 08-Nov-2018].
```

## Example trial
```
./affinity_clustering.py --src output_data/pm_std_updated_doctored_data.csv --pref -100000 --plot
```
