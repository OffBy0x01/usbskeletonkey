#pull target IP from module configuration

#pull in dependies rcpclient, net, nmblookup, smbclient

#or run skeleton key verison of them

#rpcclient
#   standard enum4linux runs: enum4linux [ip address]

#   nmblookup -A [ip address]
#       do?

#   rpcclient -U "" [ip address] -c "lsaquery" 2>&1
#       -U is the username
#       -c is to execute a command
#       command is lsaquery
#       THINK: 2>&1 is to do with the RID cycling

#   smbclient //[ip address]/ipc$ -U"" -c "help" 2>&1
#       do?