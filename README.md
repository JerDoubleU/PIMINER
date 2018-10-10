# PIMINER
A toolset for discovering PII as a final project for CIS 545. The goal is to detect information that may be sensitive in a document in order to prevent accidental disclosure. We do not recommend the use of these tools outside of academic settings as they have not been fully validated.

## `piminer.py`
A tool using [spacy.io](https://spacy.io/) to detect entities of certain types in context. Also contains regex pattern matching in order to identify low-hanging fruit.

## `text_cleaner.sh`
A shell script used to prepare data for ingestion into `piminer.py`.
