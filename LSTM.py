import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import time

count = 20
OpenNMT = 0

if OpenNMT == 1:
  sizes = [[64,15,500,500],
         [64,20,500,500],
         [64,25,500,500],
         [64,30,500,500],
         [64,35,500,500],
         [64,40,500,500],
         [64,45,500,500],
         [64,50,500,500]
        ]
else:
  sizes = [[16,25,512,512],
         [32,25,512,512],
         [64,25,512,512],
         [128,25,512,512],
         [16,25,1024,1024],
         [32,25,1024,1024],
         [64,25,1024,1024],
         [128,25,1024,1024],
         [16,25,2048,2048],
         [32,25,2048,2048],
         [64,25,2048,2048],
         [128,25,2048,2048],
         [16,25,4096,4096],
         [32,25,4096,4096],
         [64,25,4096,4096],
         [128,25,4096,4096],
         [64,50,500,500]
        ]


print("size , duration, gflops, GFLOPS")
for idx in range(len(sizes)):
  size = sizes[idx]
  N = size[0]
  T = size[1]
  D = size[2]
  H = size[3]

  rnn = nn.LSTM(D,H,1)
  input = Variable(torch.randn(N, T, D))
  h0 = Variable(torch.randn(1, T, H))
  c0 = Variable(torch.randn(1, T, H))
  output, hn = rnn(input, (h0, c0))

  start = time.time()
  for j in range(count):
    output, hn = rnn(input, (h0, c0))
  dura = (time.time() - start)/count
  gflops = T*4*(N*H*D*2 + N*H*H*2)/1e9
  GFLOPS = gflops/dura
  print("%s, %.4f, %.4f, %.4f" %(size,dura,gflops,GFLOPS))

