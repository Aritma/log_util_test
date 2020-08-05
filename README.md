# log_util_test  
Log filter utility, created based on included `specification.txt` file.  
Read `specification.txt` for more info.  

####Deployment / Installation  
Simply just copy-paste util.py and use as a script. No additional actions are required.  

####How to use the script?  
The whole code is written as a standalone script and use default python 3.x modules.  
To use the script, simply execute it with file-path argument `./util.py <file-path>` or pass data in pipeline `cat <file-path> | ./util.py`  

Missing file-path behaviour:  
If there is no file-path provided, input is read from a standard input (STDIN).  

Missing option behaviour:  
If there are no filter options provided, input data is simply print to a standard output (STDOUT) without any modifications.  

> Created and tested with Python 3.7.4  