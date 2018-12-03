# Output Data
Naming schema is as follows:

```
[script]_[NER_model]_[dataset]_[log]
```

1. `[script]` can be `pm` for 'piminer' or `af` for 'affinity propagation'.
1. `[NER_model]` can be `std` for standard (that is, default spaCy model: `en_core_web_md`) or `cus` for the custom NER model in `NER_model/`.
1. `[dataset]` is the filename from `input_data/` that was run.
1. If `[log]` then the file is a run_log with information about the execution of the `[dataset]`.

For example:

```
pm_cus_original_doctored_data.csv
```

1. `pm` = `piminer.py`
1. `cus` = custom NER model from `NER_model/`
1. `original_doctored_data` = `input_data/original_doctored_data.docx`
1. This is not a run_log. 
