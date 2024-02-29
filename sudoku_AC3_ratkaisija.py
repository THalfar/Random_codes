import numpy as np
import time
import random
import itertools
# from numba import jit

# @jit
def sudoku_solver_ac3(taulu):
    
    askelia = 0
    
    n = int(np.sqrt(taulu.shape[0]))
    
    
    
    vaaka_askeleet = np.array(range(0,n**2,n))
    pysty_askeleet = np.array(range(0,n**2,n))  
    
    # Täytetään kaikki ruudut joilla voi olla vain yksi arvo ja täytetään ne 
    for i in range(0,2):
        
        for pysty in range(0, taulu.shape[1]):
            
            numerot = np.array(range(1,n**2+1))
                                             
            for vaaka in range(0, taulu.shape[0]):
                                                            
                if taulu[pysty, vaaka] == 0:
                    
                    valmiit = np.append(taulu[pysty, :],taulu[:, vaaka])
                    
                    vaaka_indeksi = np.argwhere(vaaka_askeleet <= vaaka)
                    vaaka_indeksi = int(vaaka_indeksi[-1])
                    vaaka_indeksi = vaaka_askeleet[vaaka_indeksi]
                                                
                    pysty_indeksi = np.argwhere(pysty_askeleet <= pysty)
                    pysty_indeksi = int(pysty_indeksi[-1])
                    pysty_indeksi = pysty_askeleet[pysty_indeksi]
                    
                    solu = taulu[pysty_indeksi:pysty_indeksi+n, vaaka_indeksi:vaaka_indeksi+n] 
                    solu = solu.flatten()
                    
                    valmiit = np.append(valmiit, solu)
                                                            
                    valmiit = np.delete(valmiit, np.argwhere(valmiit==0))        
                    vaakanumerot = np.setdiff1d(numerot, valmiit)  
                    
                    if len(vaakanumerot)==1:
                         
                        taulu[pysty, vaaka] = random.choice(vaakanumerot)   
                        break
                    
    permutaatiot = []
    paikat = []
    numerot = np.array(range(1,n**2+1))
    indeksit = []
    
    # Luodaan kaikki mahdolliset permutaatiot jotka ovat riville mahdollisia rajoituksena
    for i in range(0, taulu.shape[0]):
        
        puuttuvat = np.setdiff1d(numerot, taulu[i,:])
        
        if len(puuttuvat)>0:
            
            permutaatio = list(itertools.permutations(puuttuvat))            
            random.shuffle(permutaatio) #arvonta
            permutaatiot.append(permutaatio)
            paikat.append(i)
            indeksit.append(0)
        
    pysty = 0
    paikka = 0
    kopio = np.copy(taulu)     
       
    while pysty < len(permutaatiot):
      
        if np.count_nonzero(np.isin(taulu,0)) == 0:    
            print("Askelia otettiin yhteensä:", askelia)
            return [taulu, True]
            
        else:
                                             
            paikka = indeksit[pysty]     
             
            while paikka < len(permutaatiot[pysty]):
                
                indeksi = 0
                                                                        
                for vaaka in range(0, taulu.shape[1]):
                    
                    if taulu[paikat[pysty],vaaka] == 0:
                        
                        askelia += 1
                        
                        if askelia%1e5 == 0:
                            print("Askelia otettu:", askelia)
                        
                        valmiit = np.append(taulu[paikat[pysty], :], taulu[:, vaaka])
                        
                        vaaka_indeksi = np.argwhere(vaaka_askeleet <= vaaka)
                        vaaka_indeksi = int(vaaka_indeksi[-1])
                        vaaka_indeksi = vaaka_askeleet[vaaka_indeksi]
                                                    
                        pysty_indeksi = np.argwhere(pysty_askeleet <= paikat[pysty])
                        pysty_indeksi = int(pysty_indeksi[-1])
                        pysty_indeksi = pysty_askeleet[pysty_indeksi]
                    
                        solu = taulu[pysty_indeksi:pysty_indeksi+n, vaaka_indeksi:vaaka_indeksi+n] 
                        solu = solu.flatten()
                    
                        valmiit = np.append(valmiit, solu)
                        valmiit = np.delete(valmiit, np.argwhere(valmiit==0))    
                        
                        syotettava = permutaatiot[pysty][paikka][indeksi]
                        
                        if np.count_nonzero(np.isin(valmiit, syotettava)) == 0:
                            
                            taulu[paikat[pysty], vaaka] = syotettava
                            indeksi +=1
                            
                            if indeksi == len(permutaatiot[pysty][0]):
                                
                                if np.count_nonzero(np.isin(taulu,0)) == 0:     
                                    print("Askelia otettiin yhteensä:", askelia)
                                    return [taulu, True]
                                
                                indeksit[pysty] = paikka
                                paikka = 2**42 # Suuri numero >> 9! jolla looppi rikotaan. Väsyneenä tehty typeryys.                           
                                pysty += 1     
                                break
                                                                                        
                        else:
                            
                            if paikka<len(permutaatiot[pysty])-1:
                                             
                                paikka += 1
                                taulu[paikat[pysty], :] = kopio[paikat[pysty], :]                        
                                break
                            
                            else:
                            
                                taulu[paikat[pysty], :] = kopio[paikat[pysty], :]
                                taulu[paikat[pysty]-1, :] = kopio[paikat[pysty]-1, :]
                                indeksit[pysty] = 0    
                                indeksit[pysty-1] = indeksit[pysty-1] +1                                                                                            
                                paikka = 2**42
                                pysty -= 1
                                break

# Testataan AC3 ratkaisijaa vaikeaan tapaukseen 
# https://www.ibm.com/developerworks/community/blogs/jfp/entry/solving_the_hardest_sudoku?lang=en

tosi_vaikee_sudoku = np.array([[8,0,0,0,0,0,0,0,0],
                              [0,0,3,6,0,0,0,0,0],
                              [0,7,0,0,9,0,2,0,0],
                              [0,5,0,0,0,7,0,0,0],
                              [0,0,0,0,4,5,7,0,0],
                              [0,0,0,1,0,0,0,3,0],
                              [0,0,1,0,0,0,0,6,8],
                              [0,0,8,5,0,0,0,1,0],
                              [0,9,0,0,0,0,4,0,0]
                              ])

print(tosi_vaikee_sudoku)
print("****************************")
t = time.time()      
tosi_vaikee_sudoku_ratkaisu = sudoku_solver_ac3(tosi_vaikee_sudoku)    
print(tosi_vaikee_sudoku_ratkaisu[0])
kului = (time.time() - t)         
print("Aikaa meni sudokun ratkaisuu: {0:.1f}s".format(kului))




    
    
    
    




    
    