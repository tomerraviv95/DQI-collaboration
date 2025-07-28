def scalprod(b,c):
   wt = 0
   for j in range(127):
       if b[j] == 1:
           if c[j] == 1:
               wt = wt + 1
   skal = mod(wt, 2)
   return skal

def hamwt(c):
   wt = 0
   for j in range(127):
       if c[j] == 1:
           wt = wt + 1
   return wt

clear_vars
import numpy
n = 127
d = 21
dim = 64
Ball = matrix(GF(2), 201930, 127)
# load min_wt_dual, num_cw_dual, dual_poly_matrix
Ball = load('dualdecvec.sobj')

erwt = 11
onestep = 5
simzahl = 3
anzsim = 0
wer = 0
ker = 0

for sim in range(simzahl):
   fstellen = random_vector(erwt, 127)
   err = vector(GF(2), 127)
   for j in range(erwt):
       pos = fstellen[j]
       err[pos] = 1
   print(fstellen)
#    print(err)
   if hamwt(err) == erwt:
       anzsim = anzsim + 1
       rx = copy(err)
       for ij in range(onestep):
           Phi = vector(ZZ, 127)
           for j in range(201930):
               b = copy(Ball[j])
               if scalprod(b, rx) == 0:
                   for i in range(127):
                       if b[i] == 1:
                           Phi[i] = Phi[i] + 1
#        print(Phi)
           min = 220000
           for j in range(127):
               if Phi[j] < min:
                   min = Phi[j]
                   minpos = j

           print(ij, ' Onestep Min at pos', minpos)
           rx[minpos] = 0

       Phi = vector(ZZ, 127)
       for j in range(201930):
           b = copy(Ball[j])
           if scalprod(b, rx) == 0:
               for i in range(127):
                   if b[i] == 1:
                       Phi[i] = Phi[i] + 1

       for i in range(6):
           min = 220000
           for j in range(127):
               if Phi[j] < min:
                   min = Phi[j]
                   minpos = j

           print(i, 'Min at pos', minpos)
           rx[minpos] = 0
           Phi[minpos] = 220000


       if rx == 0:
           ker = ker + 1
           print(sim, 'correct decoded')
       else:
           print(sim, 'wrong decoded')
           print(fstellen)
           wer = wer + 1


print('Number simulations', simzahl, 'where', anzsim, 'with', erwt, 'errors')
print('wrong decoded', wer, 'correct decoded', ker)
