#!/bin/bash
# at 18:00 01/14/22
# nohup ./run.sh &
# lunch it at 02:00/06:00 etc

nohup python3 MainStochRSI.py config/config_BNBUSDT.json > output_BNB.txt 2>&1 &

sleep 5

nohup python3 MainStochRSI.py config/config_TRBUSDT.json > output_TRB.txt 2>&1 &

