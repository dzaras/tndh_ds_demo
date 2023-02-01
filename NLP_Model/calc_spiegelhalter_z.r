## Calculation of Spiegelhalter z test for model calibration

library(rms)
library(readr)

setwd("~/TDH_DS_demo")

set.seed(0)

preds <- read_csv('svm_model_preds_freq.csv')

df <- val.prob(p=preds$PREDICTION,
               y=preds$OUTCOME,
               pl=FALSE)

df2 <- t(as.data.frame(df))
df2