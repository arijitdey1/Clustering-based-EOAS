import numpy as np
import pandas as pd
import random
import math,time
from __future__ import division
from matplotlib import pyplot
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import csv


data = pd.read_csv('/content/drive/MyDrive/feature_extraced_savee_dataset.csv')
label = pd.read_csv('/content/drive/MyDrive/class.csv')
data = np.asarray(data)
label = label['class']
label = np.asarray(label)
(a,b)=np.shape(data)
print(a,b)
dimension = np.shape(data)[1] #particle dimension

# trainX=data
# trainy=label
cross=5
test_size=(1/cross)
trainX, testX, trainy, testy = train_test_split(data, label,stratify=label ,test_size=test_size)

clf=KNeighborsClassifier(n_neighbors=5)
# clf=MLPClassifier(alpha=0.001, max_iter=1000) #hidden_layer_sizes=(1000,500,100)
clf.fit(trainX,trainy)
val=clf.score(testX,testy)
print("acc: ",val)

alpha=50 
beta=0.2 #we can vary alph and beta 
omega=0.9 #used in case of multi-objective, else =1
limit=30 #total no of iterations T
atomno=20 #population size
dim=np.shape(df)[1]-1 #dimension of atom position d

def sigmoid(gamma):     # convert to probability
  if gamma<0:
    return 1-1/(1+math.exp(gamma))
  else:
    return 1/(1+math.exp(-gamma))

def Vfunction(gamma):
  #return abs(np.tanh(gamma))
  #another V-shaped function
  val=(math.pi/2)*gamma
  val=np.arctan(val)
  val=(2/math.pi)*val
  return abs(val)

#fitenss
def fitness(atom):
  cols=np.flatnonzero(atom)
  val=1
  if np.shape(cols)[0]==0:
    return val
  else:
    clf=KNeighborsClassifier(n_neighbors=5)
    #cross=4
    #test_size=(1/cross)
  # X_train, X_test, y_train, y_test = train_test_split(trainX, trainy,  stratify=trainy,test_size=test_size)
    train_data=trainX[:,cols]
    test_data=testX[:,cols]
    #clf=MLPClassifier(alpha=0.01, max_iter=1000) #hidden_layer_sizes=(1000,500,100)
    clf.fit(train_data,trainy)
    val=1-clf.score(test_data,testy)

    #in case of multi objective  []
    set_cnt=sum(atom)
    set_cnt=set_cnt/np.shape(atom)[0]
    val=omega*val+(1-omega)*set_cnt
    return val

def allfit(population):
  x=np.shape(population)[0]
  acc=np.zeros(x)
  for i in range(x):
    acc[i]=fitness(population[i])     
  return acc

#initialize atoms randomly, within a range
def initialize2(atomno,dim):
  population=np.zeros((atomno,dim))
  minn=math.floor(0.1*dim)
  maxx=math.floor(0.8*dim)
  
  for i in range(atomno):
    random.seed(i**3+i**2+101*i+5+int(time.time()))
    no=random.randint(minn,maxx)
    pos=random.sample(range(0,dim-1),no)
    for j in pos:
      population[i][j]=1
    
    # print(population[i])  
    
  return population

def initialize1(atomno,dim):
  population=np.zeros((atomno,dim))
  for i in range(atomno):
    for j in range(dim):
      random.seed(i*j+i+j+100*i+int(time.time()))
      r=random.random()
      if r>0.6:
        population[i][j]=1
      #print(population[i][j],end=' ')
    #print()
  return population

#initialize velocity
def init_vel(atomno,dim):
  velo=np.zeros((atomno,dim))
  for i in range(atomno):
    for j in range(dim):
      random.seed(i*j+i+j+100*i+int(time.time()))
      r=random.random()   #(0,1)
      velo[i][j]=r
      #print(velo[i][j],end=' ')
    #print()
  return velo

#number of neighbors
def kneighbor(curr): #curr: current iteration no
  x=math.sqrt(curr/limit)
  x=x*(atomno-2)
  x=atomno-x
  x=math.floor(x)
  return x

#since the def of fit_best and fit_worst is different from the paper, we may need to interchange their values
def calc_mass(inx,acc):
  x=np.shape(population)[0]
  maxx=0
  minn=1
  arr_M=np.zeros(x)
  for i in range(x):
    arr_M[i]=acc[i]
    if i==inx:
      fit_i=arr_M[inx]
    tmp1=arr_M[i]
    if tmp1>maxx:
      maxx=tmp1
    if tmp1<minn:
      minn=tmp1
  
  best=minn
  worst=maxx
  tmp=(fit_i- best)/(worst-best)
  M_i=math.exp(-tmp)
  for i in range(x):
    temp=(arr_M[i]-best)/(worst-best)
    arr_M[i]=math.exp(-temp)
  
  
  mass=M_i/sum(arr_M)
  #print(M_i,sum(arr_M))
  return mass

def geometric(i,best,curr,total):
  #we may need to interchage x_best and x_i
  x_i=population[i]
  x_b=population[best]
  arr=np.subtract(x_b,x_i)
  
  temp=(-20*curr)/total
  temp=math.exp(temp)
  temp=temp*beta
  
  result=[x*temp for x in arr]
  result=np.array(result)
  return result

def getKbest(acc,K):
  temp=acc.argsort()
  Kbest=temp[:K]
  return Kbest

def getsigma(kbest,K,i):
  s=np.zeros(np.shape(population)[1])
  for j in kbest:
    tmp=population[j]
    tmp=np.array(tmp)
    s=s+tmp
  x_o=s/K
  x_i=population[i]
  dimn=np.shape(population)[1]
  
  ans=0
  for i in range(dimn):
    tmp=x_o[i]-x_i[i]
    tmp=tmp**2
    ans=ans+tmp
  
  return math.sqrt(ans)

def get_hij(i,j,sig,curr):
  hmin=1.1 + 0.1*(math.sin((curr/limit)*(math.pi/2)))
  hmax=2
  
  if sig==0:
    return hmax
  
  xi=population[i]
  xj=population[j]
  
  dimn=np.shape(population)[1]
  rij=0
  for k in range(dimn):
    tmp=xi[k]-xj[k]
    tmp=tmp**2
    rij+=tmp
  rij=math.sqrt(rij)
  hij=rij/sig
  
  if hij>hmax:
    return hmax
  if hij<hmin:
    return hmin
  return hij

def norm2(a,b,n):
  x1=population[a]
  x2=population[b]
  if all(x1==x2):
    #print(a,b)
    return 0.1
  ans=0
  for i in range(n):
    tmp=(x1[i]-x2[i])**2
    ans+=tmp
  return math.sqrt(ans)

def LJpotential(inx,curr,kbest,K): #inx denotes the atom no, curr: loop no
  sig=getsigma(kbest,K,inx)
  
  dimn=np.shape(population)[1]
  arr=np.zeros(dimn)
  for j in kbest:
    if i==j:
      continue
    
    hij=get_hij(inx,j,sig,curr)
    tmp1=hij**13
    tmp2=hij**7
    tmp=2*tmp1-tmp2
    
    xi=population[inx]
    xj=population[j]
    tmp1=norm2(inx,j,np.shape(population)[1])
    gamma=tmp/tmp1
    
    for l in range(dimn):
      random.seed(i+j+l+int(time.time()))
      arr[l]=arr[l]+gamma*(xj[l]-xi[l])*random.random()
      
  const=(-20*curr)/limit
  const=math.exp(const)
  const=(1-(curr-1)/limit)*alpha*const
  
  for l in range(dimn):
    arr[l]*=const
    
  return arr

def onecount(atom):
  cnt=0
  for i in atom:
    if i==1.0:
      cnt+=1
  return cnt

def perturb(atom):
  percent=0.3
  numFeatures=np.shape(population)[1]
  numChange=int(numFeatures*percent)
  pos=np.random.randint(0,numFeatures-1,numChange)
  atom[pos]=1-atom[pos]
  return atom

def SA():
  #dispPop()
  [numAtoms,numFeatures]=np.shape(population)
  T0=numFeatures
  #print('T0: ',T0)
  for atomNo in range(numAtoms):
    T=2*numFeatures
    curAtom=population[atomNo].copy()  
    curAcc=fit_val[atomNo].copy()  
    #print('Atom:',atomNo, 'curAcc:',curAcc, 'curFeat:', onecount(curAtom), 'fitness_check:', fitness(curAtom))
    bestAtom=curAtom.copy()
    bestAcc=curAcc.copy()
    while T>T0:
      #print('T: ',T)
      newAtom=perturb(curAtom)
      newAcc=fitness(newAtom)/1      
      if newAcc<bestAcc:
        curAtom=newAtom.copy()
        curAcc=newAcc.copy()
        bestAtom=curAtom.copy()
        bestAcc=curAcc.copy()
      elif newAcc==bestAcc:
        if onecount(newAtom)<onecount(bestAtom):
          curAtom=newAtom.copy()
          curAcc=newAcc.copy()
          bestAtom=curAtom.copy()
          bestAcc=curAcc.copy()
      else:            
        prob=np.exp((bestAcc-curAcc)/T)
        if(random.random()<=prob):
          curAtom=newAtom.copy()
          curAcc=newAcc.copy()
      T=int(T*0.93)
    #print('bestAcc: ',bestAcc)
    #print('Atom:',atomNo, 'newAcc:',bestAcc, 'newFeat:', onecount(bestAtom), 'fitness_check: ', fitness(bestAtom))
    population[atomNo]=bestAtom.copy() 
    fit_val[atomNo]=bestAcc.copy()

def dispPop():
  numPop=np.shape(population)[0]
  for i in range(numPop):
    print('fitness: ',fit_val[i], 'num: ', onecount(population[i]), 'fitness_check:', fitness(population[i]))
  print(' ')

def findBest(pop,fit_pop):
  numPop=np.shape(pop)[0]
  bestAtom=pop[0]
  bestFit=fit_pop[0]
  bestIdx=0
  for i in range(1,numPop):
    if fit_pop[i]<bestFit:
      bestAtom=pop[i]
      bestFit=fit_pop[i]
      bestIdx=i
    elif fit_pop[i]==bestFit:
      if onecount(pop[i]<onecount(bestAtom)):
        bestAtom=pop[i]
        bestFit=fit_pop[i]
        bestIdx=i
  #print('bestFit: ', bestFit, 'bestIdx: ', bestIdx)
  return bestIdx

population=initialize2(atomno,dim)
fit_val=np.zeros(atomno)
velocity=init_vel(atomno,dim)

start_time = datetime.now()

x_axis=[]
y_axis=[]
curr=1 
fit_val=allfit(population)  
best_idx_i=findBest(population,fit_val)
#print('best index: ',best_idx_i)
best_atom=population[best_idx_i].copy()
best_fit_val=fit_val[best_idx_i].copy()

for curr in range(1,limit+1):  
  print(curr)
  x_axis.append(curr)

  for i in range(atomno):    
    atom_i=population[i].copy()
    fit_i=fit_val[i]        
    best=-1
    mass=calc_mass(i,fit_val)
    K=kneighbor(curr)
    best=np.argmin(fit_val)
    G=geometric(i,best,curr,limit)
    Kbest=getKbest(fit_val,K)
    LJ=LJpotential(i,curr,Kbest,K)
    force=G+LJ
    accl=force/mass
    dimn=np.shape(population)[1]
    
    for l in range(dimn):
      random.seed(i*l+i*299+l**3)
      velocity[i][l]=velocity[i][l]*random.random()+accl[l]
      tmp=population[i][l]+velocity[i][l]      
      tmp=sigmoid(tmp)      
      if tmp>0.5:
        atom_i[l]=1
      else:
        atom_i[l]=0
    
    fit_new=fitness(atom_i)
    if fit_new<fit_i:
      population[i]=atom_i.copy()
      fit_val[i]=fit_new.copy()
    elif fit_new==fit_i:
      if onecount(atom_i)<onecount(population[i]):        
        population[i]=atom_i.copy()
        fit_val[i]=fit_new.copy()   
  SA()
  #dispPop()
  best_idx_i=findBest(population,fit_val)

  if(fit_val[best_idx_i]<best_fit_val):
    best_atom=population[best_idx_i].copy()
    best_fit_val=fit_val[best_idx_i].copy()  
  y_axis.append(best_fit_val)
  print("best_till_now: ",best_fit_val,'count: ',onecount(best_atom))

time_required = datetime.now() - start_time
print("best fitness : ",best_fit_val,"time :",time_required)

pyplot.plot(x_axis,y_axis)
pyplot.xlim(0,curr+1)
pyplot.ylim(0.15,0.30)
pyplot.show()

print(onecount(best_atom))
print(fitness(best_atom))
print(best_atom)
print(best_fit_val)

#test accuray
cols=np.flatnonzero(best_atom)
test_data=testX[:,cols]
train_data=trainX[:,cols]
#print(np.shape(train_data),np.shape(test_data))

clf=KNeighborsClassifier(n_neighbors=5)
#clf=MLPClassifier( alpha=0.001, max_iter=2000) #hidden_layer_sizes=(1000,500,100 ),
clf.fit(train_data,trainy)
val=clf.score(test_data, testy )
print(val,np.shape(cols)[0])
