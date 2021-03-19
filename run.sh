#!/bin/bash

export METHOD = 1

if [ "$#" -ne 6 ];
then
  echo "illegal number of parameters"
  echo "usage: $0 DATAFILE ATOMICFEATURES LABEL DATASHEETNAME ATOMICSHEETNAME METHOD"
  exit
fi

export DATAFILE=$1
export ATOMICFEATURES=$2
export LABEL=$3
export DATASHEETNAME=$4
export ATOMICSHEETNAME=$5
export METHOD=$6

python3 generatefeats_pelect.py  -f $DATAFILE -b $ATOMICFEATURES -j -m $METHOD -l $LABEL \
  --sheetnames "$DATASHEETNAME,$ATOMICSHEETNAME"
python3 ffilter.py -f newadata.pkl -n 50 -i "$DATAFILE,$LABEL,$DATASHEETNAME"
python3 checksingleformula.py -n 1000 -f newadata.pkl  -i "$DATAFILE,$LABEL,$DATASHEETNAME"
python3 ./extractNformulas.py -f feature_rmse.csv
