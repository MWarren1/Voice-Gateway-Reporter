# Voice-Gateway-Reporter
###### Dependencies : Python 2.7
###### By Redemption.Man
Reports on a single Voice gateway from Cisco CDR records, Useful for reporting on h.323 gateways 
```
usage: gateway_reporter.py [-h] --input INPUT --gateway GATEWAY
                           [--channels CHANNELS]

Reports on the utilization of a sinlge gateway for every second for the length
of the cdr file

optional arguments:

  -h, --help           show this help message and exit
  
  --input INPUT        CDR file input(must be csv)
  
  --gateway GATEWAY    IP address of gateway
  
  --channels CHANNELS  The number of channels on the gateway(optional)
```
