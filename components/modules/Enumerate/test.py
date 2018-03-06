raw_command = """user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[Benny Hill] rid:[0x3e8]
user:[R.Gudino] rid:[0x20da]
user:[E.Breck] rid:[0x20db]
user:[D.Lecroy] rid:[0x20dc]
user:[C.Armes] rid:[0x20dd]"""

users = []
rids = []
# Success
# raw_command = subprocess.run("enumdomusers").stdout.decode('utf-8')
#  iterate along string
index = 0
start = 0
counter = 0
for char in raw_command:
    if char == "\n":
        counter += 1
for times in range(0, counter+1):
    start = index
    start = raw_command.find('[', index)
    start += 1
    end = raw_command.find(']', start)
    users.append(raw_command[start:end])
    index = end

    start = raw_command.find('[', index)
    start += 1
    end = raw_command.find(']', start)
    rids.append(raw_command[start:end])
    index = end
    times += 1

    #current = TargetInfo
    #users = (ip, users)
    #rids = (ip, rids)
    #current.DOMAIN.append(users)
    #current.DOMAIN.append(rids)