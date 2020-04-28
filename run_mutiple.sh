if [ $# -ne 5 ]
then
  echo "No arguments supplied"
  echo "usage: " $0 " basevalue startprocnum endprocnum startidx maxidx"
  exit
fi

export BASEVAL=$1
export STARTPROC=$2
export NUMPROCS=$3
export START=$4
export MAXNUM=$5

for i in $(seq $STARTPROC $NUMPROCS)
do
  export BASE=$BASEVAL
  export END=$(($START + $BASE))
  if [ $END -ge $MAXNUM ]; then
    python3 generate2Dfeats.py -S -f feature_rmse.csv -n 20 -k newadata.pkl -N 1 -r "$START:$MAXNUM" -F $MAXNUM 1> out_$i 2> err_$i &
    echo "Process " $i " will start from " $START " to " $MAXNUM " of " $MAXNUM
    echo ""
    exit
  fi
  python3 generate2Dfeats.py -S -f feature_rmse.csv -n 20 -k newadata.pkl -N 1 -r "$START:$END" -F $MAXNUM 1> out_$i 2> err_$i &
  echo "Process " $i " will start from " $START " to " $END " of " $MAXNUM
  echo ""
  export START=$(($START + $BASE))
  export BASE=$(($i * $BASE))
done
