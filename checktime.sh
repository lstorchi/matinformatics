for name in out_*
do 
  echo $name 
  grep "estimated tot." $name | tail -n 1 | awk '{print $9, $10}'
done
