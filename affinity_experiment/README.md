# Experiment
This experiment runs `affinity_clustering.py` on `output_data/pm_std_updated_doctored_data.csv` at various different values for preference. The results are stored to show 'tighter' clusters at lower (more negative) values for `--pref`.

## Example trial
```
./affinity_clustering.py --src output_data/pm_std_updated_doctored_data.csv --pref -100000 --plot
```
