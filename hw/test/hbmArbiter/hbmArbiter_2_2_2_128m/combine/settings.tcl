# U50
set XPART xcu50-fsvh2104-2L-e
# U200
# set XPART xcu200-fsgd2104-2-e
# U250
# set XPART xcu250-figd2104-2L-e
# U280
# set XPART xcu280-fsvh2892-2L-e

set CLKP 330MHz

# do .xo kernel export only:
set EXPORT_XO_ONLY 0 #must be 0 in this folder

#COSIM waveform enable:
set WAVE_DEBUG 0
#COSIM waveform dump ALL (1=ALL, 0=PORT):
set TRACE_LEVEL_ALL 0

set CSIM 1
set CSYNTH 0 #must be 0 in this folder
set COSIM 0 #must be 0 in this folder
set VIVADO_SYN 0 #must be 0 in this folder
set VIVADO_IMPL 0 #must be 0 in this folder
set QOR_CHECK 0 #must be 0 in this folder

