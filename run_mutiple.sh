
export BASE=4000
export MAX=16
export START=0

for i in $(seq 1 $MAX)
do
  export END=$(($START + $BASE))
  python3 generate2Dfeats.py -f feature_rmse.csv -n 40 -k newadata.pkl -N 1 -r "$START:$END" 1> out_$i 2> err_$i &
  export START=$(($START + $BASE))
done
