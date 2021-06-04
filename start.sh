start_pwd=$(cd "$(dirname "$0")";pwd)
cert="/threatpy/cert360threaten.py"
ali="/threatpy/alithreaten.py"
das="/threatpy/dasthreaten.py"
tx="/threatpy/txthreaten.py"
path_cert=$start_pwd$cert
path_ali=$start_pwd$ali
path_das=$start_pwd$das
path_tx=$start_pwd$tx
python3 $path_cert
python3 $path_ali
python3 $path_das
python3 $path_tx
 
