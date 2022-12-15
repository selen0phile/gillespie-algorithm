import numpy as np
import matplotlib.pyplot as plt
import random


GAMMA = 1
BETA = 1.25

N = 1000
graph = [[] for i in range(N+1)]
beta = [0 for i in range(N+1)]
gamma = [0 for i in range(N+1)]
status = [0 for i in range(N+1)]

T = [0]
S = [N-1]
I = [1]
R = [0]

def infect(u):
  print('[!] Infecting', u)
  status[u] = 1
  gamma[u] = GAMMA
  beta[u] = 0
  for v in graph[u]:
    if status[v] == 0:
      beta[v] += BETA

def donothing():
  print("[i] Doing nothing ... zzZ")
  

def recover(u):
  print('[+] Recovering', u)
  status[u] = 2
  gamma[u] = 0
  beta[u] = 0
  for v in graph[u]:
    beta[v] -= BETA
  

def create_complete_graph():
  for i in range(1,N+1):
    graph[i] = []
  for i in range(1, N+1):
    for j in range(1, N+1):
      if i == j:
        continue
      graph[i].append(j)
  inf = 1
  for i in range(inf):
    u = random.randint(1, N)
    while status[u] == 1:
      u = random.randint(1, N)  
    infect(u)

def create_ring_graph():
  for i in range(1,N+1):
    graph[i] = []
  
  graph[1] = [2, N]
  graph[N] = [1, N-1]
  for i in range(2, N):
      graph[i].append(i+1)
      graph[i].append(i-1)

  inf = 150
  for i in range(inf):
    u = random.randint(1, N)
    while status[u] == 1:
      u = random.randint(1, N)  
    infect(u)
  
def simulate():
  s = 0
  r = [0]
  for i in range(1, N+1):
    if status[i] == 0:
      s += beta[i]
      r.append(r[-1]+beta[i])
    elif status[i] == 1:
      s += gamma[i]
      r.append(r[-1]+gamma[i])
    elif status[i] == 2:
      s += 0
      r.append(r[-1] + 0)
  if s == 0:
    return
  tau = np.random.exponential(scale=1/s)
  T.append(T[-1] + tau)
  print("[i] Time", T[-1])

  rand = random.uniform(0,1)
  val = rand * s
  for i in range(1, N+1):
    if val < r[i]:
      if status[i] == 0:
        infect(i)
        S.append(S[-1] - 1)
        I.append(I[-1] + 1)
        R.append(R[-1])
      elif status[i] == 1:
        recover(i)
        S.append(S[-1])
        I.append(I[-1] - 1)
        R.append(R[-1] + 1)
      else:
        S.append(S[-1])
        I.append(I[-1])
        R.append(R[-1])
      break

create_ring_graph()
for i in range(1000):
  simulate()

print(T)
print(S)
print(I)
print(R)

for i in range(len(S)):
  S[i] = S[i] / N
  I[i] = I[i] / N
  R[i] = R[i] / N
  
plt.plot(T, S, color='yellow')
plt.plot(T, I, color='red')
plt.plot(T, R, color='lightgreen')
plt.show()
