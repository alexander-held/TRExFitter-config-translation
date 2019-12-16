# TRExFitter config translation

Parses [`TRExFitter`](https://gitlab.cern.ch/TRExStats/TRExFitter) config files and translates them into dictionaries that can be written to file in YAML or JSON format.

This project is a work in progress and the translation is likely to not work yet for all ways of writing a config that are accepted by `TRExFitter`.

## Example

The example `translate.py` uses the example config file from [alexander-held/template_fit_workflows](https://github.com/alexander-held/template_fit_workflows).