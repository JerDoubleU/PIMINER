# Named Entity Recognition Training
This directory contains [`piiminer_model_train.py`](piiminer_model_train.py), a script to update spaCy's named entity recognition model. Currently, this project ix under development. All files are zipped due to their size. In order to run with the updated model it is necessary to unzip the trained model, and rewrite `piminer.py` to include:

```python
nlp = spacy.blank('en').from_disk('/path/to/model')
```

This has not been tested, and is not included in the current version of `piminer.py`. Ideally, this logic can be controlled with an optional CLI flag. 
