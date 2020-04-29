for name in out_*
do 
  echo $name 
  grep "estimated tot." $name | tail -n 1 
  grep "Min LR value" $name
done
