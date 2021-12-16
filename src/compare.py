import sys
import timeit
import subprocess
from os.path import exists

def main():
    '''usage: compare.py [files]
This program compare the execution time of N py files starting with the fastest'''
    if len(sys.argv) ==1 and sys.argv[0] == 'compare.py': #sys.argv list of all commands passed 
        print(main.__doc__)
    
    elif len(sys.argv) ==2 and sys.argv[0] == 'compare.py':
        if not exists(sys.argv[1]):
            print(f'[ERROR]: Put more args and file {sys.argv[1]} does not exist')
        else:
            print("[ERROR]: Put more args")
    
    elif len(sys.argv) >2:
        c = 1
        result = dict()
        for i in sys.argv[1:]:
            if not exists(i):
                print(f'File {i} does not exist')
                c = 0
            else:
                #print(f'File {i} exists')
                timer = timeit.timeit(lambda : subprocess.run(["python3", i], stdout=subprocess.PIPE), number=1) #subprocess: run a py file inside another file #?
                result[i] = timer
                #print(result)  
        if c == 1:        
            print("PROGRAM | RANK | TIME ELAPSED")
            j = 0
            #print(sorted(result.items()))
            for tpl in reversed(sorted(result.items())):
                print(f'{tpl[0]}    {j+1}     {tpl[1]}s')
                j += 1      
    else:
        print("[ERROR]: Please check your input")
        
            
if __name__ == '__main__':
    main()
