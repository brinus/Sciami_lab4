#RUN_TEST
import numpy as np
import math
S = 1074/101 # Rescaling factor

def check(t1, t2):
    if np.abs(t2 - t1) > 1.0:
        return 1
    else: 
        return 0

def check_dif(t1: float, t2: float, d1:np.datetime64, d2:np.datetime64):
    DELTAp = d2 - d1 + np.timedelta64(500, 'ms')
    DELTAm = d2 - d1 - np.timedelta64(1000, 'ms')
    if DELTAm < np.timedelta64(int(abs(t1-t2)*1e9), 'ns') < DELTAp :
        return 0
    else:
        return 1

def val_cent(t):
	t1=t[1:]
	t2=t[:-1]
	t3=np.negative(t2)
	c = np.add(t2, np.divide(np.add(t1,np.negative(t2)),2))
	return c

########
def array_zero_one_from_fit(arr, soglia):
	for idx in arr:
		if (arr[idx]<soglia):
			arr[idx]=0
		else arr[idx]=1
	return arr

def array_zero_one(arr):
    arr1=arr[1:]
    arr2=arr[:-1]
    arr3 = np.add(arr2, np.negative(arr1))
    for idx in arr3:
        if (arr3[idx]<0):
            arr3[idx]=0
        else arr3[idx]=1
    return arr3

def expected_run(arr):
	x1=len(arr[arr==1])
	x0=len(arr[arr==0])
	exp = 1 + (2*x1*x0/(x1+x0))
	var = ( (exp-1) * (exp -2) ) / (x1+x0-1)
	return exp, var

def run_count(arr):
	arr1=arr[1:]
	arr2=arr[:-1]
	arr3 = np.abs(np.add(arr2, np.negative(arr1)))
	return np.sum(arr3)+1


if __name__ == '__main__':
    ch, time, date, _ = np.genfromtxt("events220309_1d.dat", unpack=True, dtype=(int, float, 'datetime64[ms]'))

    mask1 = ch==1 # R123
    mask2 = ch==2 # R456

    time1 = time[mask1]
    time2 = time[mask2]
    date1 = date[mask1]
    date2 = date[mask2]

    # corr1 = np.zeros(len(time1))
    # for idx in range(len(time1)-1):
    #     corr1[idx] = check(time1[idx], time1[idx+1])*(time1[idx] -time1[idx+1])
    # time1 = time1 + corr1.cumsum()
    corr1 = np.zeros(len(time1))

    for idx in range(len(time1)-1):
        is_dif = check_dif(time1[idx], time1[idx+1], date1[idx], date1[idx+1])
        corr1[idx+1] = is_dif*(time1[idx] + (date1[idx+1]-date1[idx])/np.timedelta64(1,'s') - time1[idx+1])

    time1 = time1 + corr1.cumsum()
    corr2 = np.zeros(len(time2))
    for idx in range(len(time2)-1):
        corr2[idx] = check(time2[idx], time2[idx+1])*(time2[idx] -time2[idx+1])
    time2 = time2 + corr2.cumsum()

##############
	#time 1 e time 2 sono gli array R123 e R456
	val1, edges1, _ = plt.hist(time1, histtype = 'step')
	val2, edges2, _ = plt.hist(time2, histtype = 'step')

	#creo array di zeri e uno: zero se il bin è più basso del precedente, uno se è più alto
	Val1 = array_zero_one(val1)
	Val2 = array_zero_one(val2)

	#array di zeri e uno a seconda se il bin è sopra o sotto la soglia q in uscita dal fit dell'istogramma con una funzione costante
	#Val1_from_fit = array_zero_one_from_fit(val1, q)
	#Val2_from_fit = array_zero_one_from_fit(val2, q)

	#conto il numero di run (quando il valore dell'array cambia valore +1)
	run1 = run_count(Val1)
	run2 = run_count(Val2)

	#calcolo dei run aspettati con varianza
	exp1, var1 = expected_run(Val1)
	exp2, var2 = expected_run(Val2)

	print(f'Numer of runs for the first telescope are {run1}, when the expected number is {exp1} with variance {var1}\n So the test statistic is $Z_{TS,1}$={(run1-exp1)/math.sqrt(var1)} ')
	print(f'Numer of runs for the second telescope are {run2}, when the expected number is {exp2} with variance {var2}\n So the test statistic is $Z_{TS,2}$={(run2-exp2)/math.sqrt(var2)} ')