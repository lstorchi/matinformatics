
export BASEVAL=150
export NUMPROCS=32
export START=0
export MAXNUM=40000

for i in $(seq 1 $NUMPROCS)
do
  export BASE=$BASEVAL
  export END=$(($START + $BASE))
  if [ $END -ge $MAXNUM ]; then
    python3 generate2Dfeats.py -S -f feature_rmse.csv -n 40 -k newadata.pkl -N 1 -r "$START:$MAXNUM" -F $MAXNUM 1> out_$i 2> err_$i &
    echo "Process " $i " will start from " $START " to " $MAXNUM " of " $MAXNUM
    echo ""
    exit
  fi
  python3 generate2Dfeats.py -S -f feature_rmse.csv -n 40 -k newadata.pkl -N 1 -r "$START:$END" -F $MAXNUM 1> out_$i 2> err_$i &
  echo "Process " $i " will start from " $START " to " $END " of " $MAXNUM
  echo ""
  export START=$(($START + $BASE))
  export BASE=$(($i * $BASE))
done
