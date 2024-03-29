if [ $# -ne 5 ]
then
  echo "No arguments supplied"
  echo "usage: " $0 " basevalue startprocnum numofprocs startidx maxidx"
  exit
fi

export PROGNAME=generate3Dfeats.py

export UPDATEVAL=0

export BASEVAL=$1
export STARTPROC=$2
export NUMPROCS=$(($2 + $3))
export START=$4
export MAXNUM=$5

export BASE=$BASEVAL

for i in $(seq $STARTPROC $NUMPROCS)
do
  export END=$(($START + $BASE))
  if [ $END -ge $MAXNUM ]; then
    python3 $PROGNAME -S -f feature_mse.csv -n 20 -k newadata.pkl -r "$START:$MAXNUM" -F $MAXNUM 1> out_$i 2> err_$i &
    echo "Process " $i " will start from " $START " to " $MAXNUM " of " $MAXNUM
    echo ""
    echo "Next start from " $MAXNUM " and procs " $(( $i + 1))
    exit
  fi
  python3 $PROGNAME -S -f feature_mse.csv -n 20 -k newadata.pkl -r "$START:$END" -F $MAXNUM 1> out_$i 2> err_$i &
  echo "Process " $i " will start from " $START " to " $END " of " $MAXNUM
  echo ""
  export START=$(($START + $BASE))
  if [ $UPDATEVAL -eq 1 ]
  then 
    export BASE=$(($i * $BASE))
  fi
done

echo "Next start from " $END " and procs " $(( $i + 1))

echo $0 $1 $(( $i + 1)) $3 $END $MAXNUM
 
