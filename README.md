# TRExFitter config translation
![](https://github.com/alexander-held/TRExFitter-config-translation/workflows/CI/badge.svg)

- [Overview](#overview)
- [Example](#example)
- [YAML config look](#yaml-config-look)
  - [General settings](#general-settings)
  - [Multiple types of similar objects](#multiple-types-of-similar-objects)
  - [Multiple parameters per setting](#multiple-parameters-per-setting)

## Overview
Parse [`TRExFitter`](https://gitlab.cern.ch/TRExStats/TRExFitter) config files and translate them into dictionaries that can be written to file in YAML or JSON format.

This project is a work in progress and the translation is likely to not work yet for all ways of writing a config that are accepted by `TRExFitter`.

## Example
The example `translate.py` uses the example config file from [alexander-held/template_fit_workflows](https://github.com/alexander-held/template_fit_workflows).

## YAML config look
This contains a few examples of how to write certain things in YAML.

### General settings
A list of general configuration settings may be specified like this:
```YAML
General:
  Lumi: 139.0
  Label: "My fit"
```
which is equivalent to:
```YAML
General: {Lumi: 139.0, Label: "My fit"}
```
The settings can be seen as a dictionary, the names of the settings are the keys.
The first form is very similar to the current `TRExFitter` config syntax.

### Multiple types of similar objects
While usually only one set of general settings would be expected, there are things for which multiple objects of the same kind are expected.
This includes samples, channels and systematic uncertainties.
Such cases can be specified as a list of dictionaries, with one dictionary per sample / channel / systematic uncertainty.
Consider a case with two channels, they can be written as:
```YAML
Channels:
  - Name: "Signal region"
    Variable: "jet_pt"
    Bins: [0, 25, 50, 75, 100, 150, 200]

  - Name: "Control region"
    Variable: "el_pt"
    Bins:
      - 0
      - 50
      - 200
```
The two ways of specifying the list of bins are equivalent.
Lists can either be written in the familiar form `[a,b,c]` or, as indicated for the second example, with each element starting with a dash `-`.
`Channels` here is the key of a dictionary, and the associated value is a list of channels.
The elements in this list, namely the individual channels, are themselves dictionaries.

Samples and systematic uncertainties can be specified in a similar way, as lists of dictionaries.
Here is an example specifiying two samples:
```YAML
Samples:
  - Name: "ttH"
    Type: "Signal"
    Path: "samples/ttH.root"
    Color: "#FFAA55"

  - Name: "ttbar"
    Type: "Background"
    Path: "samples/background.root"
    Color: "#F55EE33"
```
Written in JSON, this looks like:
```YAML
{
  "Samples": [
    {
      "Color": "#FFAA55",
      "Path": "samples/ttH.root",
      "Type": "Signal",
      "Name": "ttH"
    },
    {
      "Color": "#F55EE33",
      "Path": "samples/background.root",
      "Type": "Background",
      "Name": "ttbar"
    }
  ]
}
```

### Multiple parameters per setting
There might be settings that need more than one value to be specified.
An example in `TRExFitter` are automatic binning algorithms, where the type of algorithm needs to be specified alongside some parameters.
The `TRExFitter` syntax for this looks like the following: `Binning: "AutoBin","TransfoD",4,4` and would be written in one line.
Such an option could be written again as a dictionary, where each part of the setting is the value associated to a key describing the setting:
```YAML
Channels:
  - Name: "Signal region"
    Variable: "jet_pt"
    AutoBin:
      Type: "TransfoD"
      Parameter_1: 4
      Parameter_2: 4
```
This can be written equivalently as:
```YAML
Channels:
  - Name: "Signal region"
    Variable: "jet_pt"
    AutoBin: {Type: "TransfoD", Parameter_1: 4, Parameter_2: 4}
```
In these cases where a single parameter is insufficient as a value associated to a key, the value is instead a dictionary of all relevant settings.