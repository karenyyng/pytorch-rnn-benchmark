#!/bin/sh

t=$1
lscpu
which python
conda list
export KMP_AFFINITY=compact,1,0,granularity=fine

if [ $t == 'bdw' ]; then
  export OMP_NUM_THREADS=44
  python LSTM.py $2 $3
fi
if [ $t == 'knl' ]; then
  export OMP_NUM_THREADS=68
  python LSTM.py $2 $3
fi
if [ $t == 'knm' ]; then
  export OMP_NUM_THREADS=72
  python LSTM.py $2 $3
fi
if [ $t == 'skx' ]; then
  export OMP_NUM_THREADS=56
  python LSTM.py $2 $3
fi
if [ $t == 'gpu' ]; then
  python LSTM.py $2 cuda $3
fi
if [ $t == 'bdw-profile' ]; then
  export OMP_NUM_THREADS=44
  python -m cProfile -o bdw_$(date '+%Y-%m-%d_%H%M%S').cprof LSTM.py $2 cuda $3
fi
if [ $t == 'knl-profile' ]; then
  export OMP_NUM_THREADS=68
  python -m cProfile -o knl_$(date '+%Y-%m-%d_%H%M%S').cprof LSTM.py $2 cuda $3
fi
if [ $t == 'knl-vtune-profile' ]; then
  export OMP_NUM_THREADS=68
  ARK=knl
  amplxe-cl -collect hotspot -r r@@@{at}_${ARK} -- python LSTM.py $2 cuda $3
fi
if [ $t == 'hsw-vtune-profile' ]; then
  export OMP_NUM_THREADS=16
  ARK=hsw
  amplxe-cl -collect hotspot -r r@@@{at}_${ARK} -- python LSTM.py $2 cuda $3
fi
