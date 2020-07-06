# Reference
Format should be double hash ## for general subject
and triple ### for the more specific reference
for the clustering text analysis (see README_clustered.md).
All other hashes >3 will be wrapped into the double hash.
Single hash not considered.

Considering that, this document needs updated.

## OS set up
Linux Debian Stretch. Also includes Debian on Windows Subsystem for Linux (WSL).
And some Google Cloud Platform.

### Add user
With sudo privileges.
```
sudo adduser john
sudo usermod -aG sudo john
su - john
```

### Change password
From root. Leave off user to change own password.
```
passwd <user>
```

### Update and upgrade
```
sudo apt-get update
sudo apt-get upgrade
```

### General programs, packages
Add vim #add
```
apt-get install wget
apt-get install zip
apt-get install git
apt-get install default-jdk
````
For example, Spark requires Java JDK, but check version.

### Python 3 and pip3 for installing Python libraries
```
sudo apt install python3 python3-pip
```

Trying to update to Python 3.7? caused issues I didn't want to address.

### Python libraries
Make this requirements.txt file:
```
PyYAML # import yaml
pandas
seaborn
openpyxl # pandas uses for xlsx writing
requests
python-docx # Working with MS Word docs. Check lxml >= 2.3.2
#requests_oauthlib
#paho? for mqtt server
scikit-learn
```
Add scapy!

And run:
```
pip3 install -r requirements
```

## System and admin reference

### System tasks update
```
top
```
But installing htop will show cores' activity and memory and swap
with color-coded bars.
```
sudo apt install htop
```

### Uninstall package
```
sudo apt-get purge <package>
sudo apt-get autoremove
```

### Get manual for a package
man <package>

### Mount a shares drive
Worked in WSL to a Microsoft share, but share drive must be mapped first, by simply clicking it in File Explorer.
```
sudo mkdir /mnt/z
sudo mount -t drvfs 'H:' /mnt/h
```

On WSL, have issue with using git on mounted drive.
Try exiting and logging back into session, if not reboot.
But comment says "Note that this is available after [WSL] build 17063."
```
sudo mount -t drvfs H: /mnt/h -o metadata
```
See https://stackoverflow.com/questions/52846489/cant-clone-repository-from-mounted-drive.

Also:
```
umount /mnt/h
```
### Check storage and disks
```
sudo df -h
sudo lsblk
```

### Resizing the file system (Google Cloud)
GCP instance's disk page -> Edit -> input new size -> Save

Check disks with:
```
sudo df -h
sudo lsblk
```

Make sure growpart from cloud-guest-utils is installed:
```
sudo apt-get install cloud-guest-utils
```

Resize with device ID and partition number.
```
sudo growpart /dev/sda 1
```

Extend the file system in order to use the additional space.
```
sudo resize2fs /dev/sda1
```

### CPU usage
```
sudo apt-get install sysstat
```

### System info
```
top
cat /proc/cpuinfo
cat /proc/meminfo
free -m
```

### Browse through large directory
```
ls -l |less
```
Search with forward slash ```/term```.

### Removing a directory
-r for recursive. If it has a git, it will confirm a bunch of deletes, so use the force option:
```
rm -rf <dir>
```

### Cron jobs
Schedule jobs. Edit crontab with:
```
crontab -e
crontab -e -u tom
```

Add jobs to crontab. Use full paths in crontab and in the program running.
```
* * * * * /user/bin/python3 /path/to/prog.py
* * * * * /user/bin/python3 /home/jop/prog.py
* * * * * /bin/sh /path/to/prog.sh
```
See [https://crontab.guru/](https://crontab.guru/).

```
sudo service cron status
sudo service cron start
sudo service cron restart
sudo service cron stop
```

Also see, but not tested yet:
```
You see, the problem is that if you close your WSL window, it’s like shutting down linux. So, no cron jobs.

So here we have a bit of a hack. Edit /root/.bashrc, and add the same line at the very end:

service cron start

Now, every time you fire up Ubuntu on Bash on Windows on Puter on Earth, the cron service will be automatically started.

As long as you leave the bash window open, your cron job(s) will run nicely.
```
Source: https://scottiestech.info/2018/08/07/run-cron-jobs-in-windows-subsystem-for-linux/

## Common git commands
```
clone <project url>
```

## Networking reference

### Packages
```
apt-get install netcat
apt-get install tcpdump
apt-get install tcpreplay
apt-get install tshark
apt-get install nmap
```

### Web server
```
sudo apt install apache2
```
Runs upon install.
```
sudo systemctl stop apache2
sudo systemctl start apache2
sudo systemctl restart apache2
```
```
sudo systemctl reload apache2
```
without dropping connections.

### Get IP, check interfaces
```
ip addr
ip link
ip link show
```

### See ports, protocols, and connected foreign IPs
```
netstat -ant
netstat -pnltu
```
Also see ```ss```, like ```ss -s```.

### Send data via host ports
Terminal 1 listening on port.
```
netcat -l -p 4444
```
Terminal 2 listening to host on port.
```
netcat localhost 4444
```

### Serve files with minimal setup
But also search kbase for "apache2" for that web server.
Make directory. Make index.html in directory.
Make sure the firewall is letting TCP ingress on port 8000.
In directory, run:
```
python3 -m http.server
```
Navigate to or wget <ip address>:8000.

### Sniff traffic
```
sudo tcpdump -i eth0 -nn -v port 8000
```
-n will not resolve hostnames.
-nn will not resolve hostnames or ports.
-v for verbose (can increase like -vvvv).

### TCP flags
```
['NS', 'CWR', 'ECE', 'URG', 'ACK', 'PSH', 'RST', 'SYN', 'FIN',]
[ 256,   128,    64,    32,    16,     8,     4,     2,     1,]
```
Decode by taking the hex dump value, like 0x12,
which is 18 in base 10.
Start from the left, add get the largest flag,
here ACK with value 16. Then SYN with value 2.

## Big data
### Spark
Requires Java JDK. Check version.
```
pip3 install pyspark
pip3 install findspark
```
findspark locates Spark in order to set up paths, for example:
```
/home/oberljn/.local/lib/python3.5/site-packages/pyspark/bin
/usr/lib/jvm/java-8-openjdk-amd64/jre
```

##### pyspark.ml

## Snippets
### Dummy stream /CPU usage stream
Of JSON with ID and timestamp.
Can pipe to netcat
and consume on that port with
streaming analytics like Spark:
```
datastream = ssc.socketTextStream('localhost', 6969)
```

get_cpu.py:
```
'''
For simulating streaming data for testing with Spark Streaming
First list on port like:
netcat -l -p 6969

Then run this file
'''
import os
import time
import json

index = 0
name = 'sys_cpu_pct'
value_cmd = "mpstat |grep all |awk '{print $6}'"
timestamp_cmd = 'date'

print_cmd = """printf '''{}\n'''"""

while True:
    _id = hex(index)[1:]
    index += 1
    timestamp = os.popen(timestamp_cmd).read()[:-1]
    value = os.popen(value_cmd).read()[:-1]

    d = {
        '_id': _id,
        'name': name,
        'value': value,
        'timestamp': timestamp,
    }
    d = json.dumps(d)
    os.system(print_cmd.format(d))

    time.sleep(1)
```
This one requires sysstat Linux package to run mpstat.

## Data processing
### Get non-null percent (completeness) of a feature
Useful for testing merges and joins in how completeness percentages drop
based on join keys.
```
def bread(df):
    x = round( df.notna().sum() / df.shape[0], 2 )
    x = x.sort_values(ascending=False)
    return x
```

# Windows
## Set javac compiler's path
Check version and edit first.
```
java -version
set path=C:\Program Files\Java\jdk1.8.0_251\bin;
```


# Chrome

## Close tab
```
ctrl + w
```

## Switch to tab 1
```
ctrl + 1
```


# Tableau
## Change data source in Tableau workbook and maintain formatting
Has differing results.

1. Create new workbook and connect to new data source. Save.
2. Open the file in text editor and copy the 'datasources' element.
3. Open the other, working workbook in text editor and replace the
datasources element in whole.

May need to replace the name attribute throughout. Do a find and replace all.
For example:
```
name='federated.0ajwapi0dqud9s18mdhfj18wgzln'
```

## Tableau search box filter
1. Create a parameter name 'Search Box' with a string value of nothing
or some default search term.
2. Create a calculated field named 'Search' with the below code
and pull it into filters, filter for True.
3. Show that string parameter on the dashboard with the sheet container's
dropdown menu -> Parameter.

```
contains(
   lower([Col to Search]),
   lower(trim([Search Box]))
)
or
contains(
   lower([Col 2 to Search]),
   lower(trim([Search Box]))
)
```

Can also take the search parameter and first split N terms by space.
```
split([Search Box], ' ', 1)
...
split([Search Box], ' ', 2)
```
For each term, can have above ```contains``` formulas,
joined by AND (or OR).

### Generate search filter formula in Python
```
note = '''// Searches N user terms (separated by space) in columns specified
// The logic is OR between columns and AND between terms
//
// John Oberlin
//
'''

# Number of terms to parse
t = 5

# Search box parameter name
s = 'Search Box'

# Columns to search
columns = ['ColA', 'ColB', 'ColC']

contains_p = '''
  CONTAINS(
    TRIM(LOWER([{}])),
    TRIM(LOWER(SPLIT([{}], ' ', {})))
  )'''

terms = list()

for i in range(t):
    contains_l =  list()
    for c in columns:
        contains_l.append(contains_p.format(c, s, i+1))

    term = ' OR'.join(contains_l)
    term = '(' + term + '\n)'
    terms.append(term)

full = ' AND\n'.join(terms)
full = note + full

with open('TableauSearchFilter.txt', 'w') as f:
    f.write(full)
```

## Circle info character in Tableau
Can use ⓘ in Tableau to replace the "Abc" text.

1. Create calculated field named 'Info' with formula simply: ```'ⓘ'```.
2. Add Info dimension to Rows.
3. Control+click and drag the Rows Info pill to Text Marks Card.
4. Right click the Rows Info pill and deselect 'Show Header'.
5. Click Tooltip Marks Card and delete the line 'Info:	<Info>'.

## Tableau XML notes looking toward programmatically editing a .twb file
It seems like the defaults, like the Tableau font,
is not contained in the XML. Once the default is changed,
it shows in XML. Thus, programmatically, will have to add
the appropriate elements.

### Worksheet by name
```
<worksheet name='Sheet 1'>
```

### Sheet > Format Shading > Row Banding > Pane color
```
<format attr='band-color' scope='rows' value='#db2ee1' />
```

### Text (card?) formatting
```
<style-rule element='worksheet'>
  <format attr='font-size' value='12' />
  <format attr='color' value='#333333' />
  <format attr='font-family' value='Source Sans Pro' />
</style-rule>
```

### Text (card?) alignment formatting
```
<style-rule element='cell'>
  <format attr='height' field='[federated.1poh0581eyi1l21b79cfa0mzl32s].[none:procedure:nk]' value='33' />
  <format attr='height' field='[federated.1poh0581eyi1l21b79cfa0mzl32s].[none:Calculation_620370901568208896:nk]' value='66' />
  <format attr='text-align' value='center' />
</style-rule>
```

### Text card formatting color
```
<customized-label>
  <formatted-text>
    <run fontcolor='#4b9839'>&lt;</run>
    <run fontcolor='#4b9839'>[federated.1poh0581eyi1l21b79cfa0mzl32s].[none:Calculation_620370901568208896:nk]</run>
    <run fontcolor='#4b9839'>&gt;</run>
  </formatted-text>
</customized-label>
```
