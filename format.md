```YAML
Fit:
  FitRegion: CRSR
  FitType: SPLUSB
  Name: SPLUSB_CRSR_Asimov
  POIAsimov: 1
  SetRandomInitialNPval: 0.1
  UseMinos: Signal_norm
Job:
  CmeLabel: X TeV
  CorrelationThreshold: 0.01
  DebugLevel: 3
  GetChi2: STAT
  HistoChecks: NOCRASH
  ImageFormat: pdf
  KeepPruning: 'TRUE'
  Label: Toy example
  Lumi: 1.0
  LumiLabel: X fb^{-1}
  MCstatThreshold: 0.01
  MCweight: weight
  Name: minimal_example
  NtupleName: nominal_Loose
  NtuplePaths: ntuples
  POI: Signal_norm
  PlotOptions: CHI2, YIELDS
  RankingMaxNP: 20
  RankingPlot: all
  ReadFrom: NTUP
  SplitHistoFiles: 'TRUE'
  SystControlPlots: 'TRUE'
  SystErrorBars: 'TRUE'
  SystLarge: 0.99
  SystPruningNorm: 0.005
  SystPruningShape: 0.005
  UseGammaPulls: 'TRUE'
NormFactor:
- Max: 2
  Min: 0
  Name: Signal_norm
  Nominal: 1
  Samples: Signal
  Title: Signal norm
Region:
- Label: Signal region
  Name: Signal_region
  Selection: (jet_pt>200 && jet_pt<800)
  Type: SIGNAL
  Variable: jet_pt,6,200,800
  VariableTitle: jet p_T [GeV]
Sample:
- Name: data
  NtupleFiles: data
  NtupleName: pseudodata
  Title: Pseudodata
  Type: DATA
- FillColor: 857
  LineColor: 857
  Name: Background
  NtupleFile: prediction
  NtupleName: background
  Title: Background
  Type: BACKGROUND
- FillColor: 418
  LineColor: 418
  Name: Signal
  NtupleFile: prediction
  NtupleName: signal
  Title: Signal
  Type: SIGNAL
Systematic:
- Name: Luminosity
  OverallDown: -0.02
  OverallUp: 0.02
  Samples: all
  Title: Luminosity
  Type: OVERALL
```
