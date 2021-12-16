import sys, dis, marshal, py_compile, os
from io import StringIO

def main():
    '''usage: bc_printer.py -py src.py
This program generate bytecode from file.py, .pyc, or string 
compile
    -py file.py compile file into bytecode and store it as file.pyc
    -s "src" compile src into bytecode and store it as out.pyc
print
    -py src.py produce human-readable bytecode from python file
    -pyc src.pyc produce human-readable bytecode from compiled .pyc file
    -s "src" produce human-readable bytecode from normal string
compare -format src [-format src]+
    produce bytecode comparison for giving sources 
    (supported formats -py, -pyc, -s)''' 
    return

def get_bytecode(arg):
    return dis.Bytecode(arg)
    
def expand_bytecode(bytecode):
    result = []
    for instruction in bytecode:
        if str(type(instruction.argval)) == "<class 'code'>":
            result += expand_bytecode(get_bytecode(instruction.argval))
        else:
            result.append(instruction)
    return result

def print_bc():
    c = 1
    for i in sys.argv[3:]:
        source = None
        if sys.argv[2] == "-py":
            try:
                with open(i,"r") as f:
                    source = f.read()
            except Exception as e:
                print(f'skipping : {i}')
            
        elif sys.argv[2] == "-pyc":
            try:
                #header = 12
                #if sys.version_info >= (3.7):
                header = 16      
                with open(i,"rb") as target:
                    target.seek(header)
                    source = marshal.load(target)
            except Exception as e:
                print(f'skipping : {i}')            
            
        elif sys.argv[2] == "-s":
            source = i
        
        else:
            print("[ERROR]: flag must be '-py'/'-pyc'/'-s'")
            c = 0
        
        if c == 1:    
            bc = get_bytecode(source)
            instructions = expand_bytecode(bc)
            for instruction in instructions :
                print(f'{instruction.opname}\t{instruction.argrepr}')
            print('\n')
         
def compile():
    for i in sys.argv[3:]:
        source = None
        if sys.argv[2] == "-py":
            try:
                py_compile.compile(i, cfile=i+"c")
            except Exception as e:
                print(e, '\nERROR')
            
        elif sys.argv[2] == "-s":
            try:
                with open('out.py','w') as temp:
                    temp.write(i)
                    temp.seek(0)
                    py_compile.compile('out.py',cfile="out.pyc")
                os.remove('out.py')                    
            except Exception as e:
                print(e, '\nERROR')      

def compare():    
    c = 1
    index = 0
    result = {}
    size = int((len(sys.argv)-2)/2)
    for i in sys.argv[3::2]:
        source = None
        if sys.argv[2] == "-py":
            try:
                with open(i,"r") as f:
                    source = f.read()
            except Exception as e:
                print(f'skipping : {i}')
            
        elif sys.argv[2] == "-pyc":
            try:
                #header = 12
                #if sys.version_info >= (3.7):
                header = 16      
                with open(i,"rb") as target:
                    target.seek(header)
                    source = marshal.load(target)
            except Exception as e:
                print(f'skipping : {i}')            
            
        elif sys.argv[2] == "-s":
            source = i
        
        else:
            print("[ERROR]: flag must be '-py'/'-pyc'/'-s'")
            c = 0
                
        if c == 1:               
            bc = get_bytecode(source)
            instructions = expand_bytecode(bc)

            for instruction in instructions:
                if instruction.opname in result:
                    result[instruction.opname][index]+=1
                else:
                    result[instruction.opname]=[0]*size
                    result[instruction.opname][index]=1
                 
            index+=1

    result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1],reverse=True)} #sorting to find peak 
    I = "INSTRUCTION"
    s1 = "print(f'{I:<13}|"
    for j in range(3,len(sys.argv),2):
        s1 += '{sys.argv['+str(j)+'][0:13]:<13}|'
    s1 = s1[:-1]
    s1 += "')"
    #s1 = "print(f'{I:<13}|{sys.argv[3][0:13]:<13}|{sys.argv[5][0:13]:<13}|{sys.argv[7][0:13]:<13}')"   
    eval(s1)
    for item in result:
        s2 = "print(f'{item[0:13]:<13}|"
        for n in range(size):
            s2 += '{result[item]['+str(n)+']:<13}|'
        s2 = s2[:-1]
        s2 += "')"
        eval(s2)   
    
    #with open('result.txt','w') as r:
        #eval(s1) #for output in cmd
        
        #old_stdout = sys.stdout #for output in result.txt
        #sys.stdout = mystdout = StringIO()
        #eval(s1)
        #sys.stdout = old_stdout
        #message = mystdout.getvalue()    
        #r.write(message)
        
        #for item in result:
            #s2 = "print(f'{item[0:13]:<13}|"
            #for n in range(size):
                #s2 += '{result[item]['+str(n)+']:<13}|'
            #s2 = s2[:-1]
            #s2 += "')"
            #eval(s2) #for output in cmd
     
            #old_stdout = sys.stdout #for output in result.txt
            #sys.stdout = mystdout = StringIO()
            #eval(s2)
            #sys.stdout = old_stdout
            #message = mystdout.getvalue()    
            #r.write(message)
           
    
    #python3 bc.py compare -py src1.py -py src2.py -py src3.py > o.txt write 
    #python3 bc.py compare -py src1.py -py src2.py -py src3.py >> o.txt append        

if __name__ == '__main__':
    
    if len(sys.argv) == 1 and sys.argv[0] == 'bc.py': #sys.argv list of all commands passed 
        print(main.__doc__)        
    
    elif len(sys.argv) > 1 and len(sys.argv) < 4:
        if (sys.argv[1] != 'print' and sys.argv[1] != 'compile' and sys.argv[1] != 'compare'):
            print("[ERROR]: Put more args and check task name; print, compile, or compare")
        elif (sys.argv[1] == 'print' and sys.argv[1] == 'compile' and sys.argv[1] == 'compare' or len(sys.argv) == 3):
            print("[ERROR]: Put more args")
    
    elif len(sys.argv) > 3 :
        if sys.argv[1] == "print":
            print_bc()
        elif sys.argv[1] == "compile":
            compile()
        elif sys.argv[1] == "compare":
            compare()
        else:
            print("No action!!")
      
    else:
        print("[ERROR]: Please check your input")       
    
    
 
        
