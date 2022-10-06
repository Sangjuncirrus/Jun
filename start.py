import os
import sys
import time
import json
import getpass
import pyvisa as visa
from numpy import arange
from time import sleep
from Pkg.vender.power_load_py3_1 import maynuo_9811_python3
from Pkg.vender.power_load_py3_1 import keysight_EL34143A
from Pkg.vender.power_analyzer1 import keysight_N6705B
from Pkg.vender.daq1 import keysight_DAQ970A
from Pkg.Labcode import find_equipment_ip
from Pkg.ReportXlsx import ReportXlsx
from Pkg.vender.Scope import Scope
from Pkg.Labcode import Labcode




sys.path.append("./Chip/")
from lion_8411.lion_8411 import lion_8411
from lion_8210.lion_8210 import lion_8210
from lion_8410.lion_8410 import lion_8410
from lion_8000.lion_8000 import lion_8000

#-----------------------------------------------------
# Select test ic and setup path str
#-----------------------------------------------------
chipName = input().upper()
userName = getpass.getuser()
userPath = './User/<userName>/'.replace('<userName>', userName )
eqPath = './User/'
eq_json_path = os.path.join( eqPath, 'equipment.json' )

#-----------------------------------------------------
# Query equipment ip addresses by json file.
#-----------------------------------------------------
with open(eq_json_path, 'r') as input_file:
        eq_data_all = json.load(input_file)
        eq_data = eq_data_all[ userName ]
        daq_mac         = eq_data       [ 'daq' ]   [ 'mac'  ]
        ag_mac          = eq_data       [ 'ag' ]    [ 'mac'  ]
        scope_mac       = eq_data       [ 'osc' ]   [ 'mac'  ]
        scope_type      = eq_data       [ 'osc' ]   [ 'type' ]
        scope_model     = eq_data       [ 'osc' ]   [ 'model' ]
        if  eq_data       [ 'load' ]   [ 'mac'  ][-1] == 'x':
                load_mac = ''
        else:
                load_mac    = eq_data       [ 'load' ]   [ 'mac'  ]
        eq_ip = find_equipment_ip(ag_mac=ag_mac, daq_mac=daq_mac, scope_mac=scope_mac, load_mac=load_mac)
        ag_addr     = eq_ip[ 'ag' ]
        daq_addr    = eq_ip[ 'daq' ]
        scope_addr  = eq_ip[ 'scope' ]
        load_addr   = eq_ip[ 'load']
print( 100*'*')

#-----------------------------------------------------
# Create equipment instances
#-----------------------------------------------------
rm = visa.ResourceManager()
ag = keysight_N6705B( ag_addr )
daq = keysight_DAQ970A( daq_addr )
scope = Scope(  instrName='Scope', connectType=scope_type, connectIP=scope_addr, equipmentID=scope_model, ag=ag, rm=rm)
osc=scope;sc=scope
ld = keysight_EL34143A( load_addr )
print( 100*'*')

#-----------------------------------------------------
# Create test ic instances
#-----------------------------------------------------
if chipName == 'LN8411':
        chip1 = lion_8411(log_to_console=False, is_master=True,i2c_group=0, debug=False)
        chip2 = lion_8411(log_to_console=False, is_master=False,i2c_group=1, debug=False)
elif chipName == 'LN8210':
        chip1 = lion_8210(log_to_console=False, is_master=True,i2c_group=3, debug=False)
        chip2 = lion_8210(log_to_console=False, is_master=False,i2c_group=4, debug=False)   
elif chipName == 'LN8410':
        chip1 = lion_8410(log_to_console=False, is_master=True,i2c_group=0)
        chip2 = lion_8410(log_to_console=False, is_master=False,i2c_group=1)

elif chipName == 'LN8000':
        chip1 = lion_8000(log_to_console=False, debug=False)
else:
        print('invalid chipName=%s'%(chipName))

#-----------------------------------------------------
# Create additional objects
#-----------------------------------------------------
xl = ReportXlsx( scope=scope )

END = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BLUE = "\033[34m"
BRIGHTBLUE = "\033[94m"
PURPLE = "\033[35m"
WHITE = "\033[37m"
BRIGHTYELLOW = "\033[93m"
BRIGHTPURPLE = "\033[95m"
BRIGHTCYAN = "\033[96m"
BRIGHTWHITE = "\033[97m"
BRIGHTBLACK = "\033[0m"
BGBLACK = "\033[40m"
BGRED = "\033[41m"
BGBRED = "\033[101m"
BGGREEN = "\033[42m"
BGYELLOW = "\033[43m"
BGBYELLOW = "\033[103m"
BGBLUE = "\033[44m"
BGBBLUE = "\033[104m"
BGPURPLE = "\033[45m"
BGCYAN = "\033[46m"