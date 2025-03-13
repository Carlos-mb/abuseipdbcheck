# abuseipdbcheck

In my role as a SOC Analyst, I frequently need to check a list of IP addresses to determine if they are malicious. I typically use abuseipdb.com, but manually checking each IP is a tedious and time-consuming task. Furthermore, I often found myself re-checking IPs that I had already investigated. To address this, I developed a Python script. Now, I can input a file containing IP addresses, and the script will create a database of IPs accessed from my network, sorted by potential risk. When I need to check new IPs, I simply add them to the file and run the script. It automatically removes duplicates, retrieves information for the newly added IPs, and re-sorts the entire list by risk.

Now, my ips.txt file contains all previously checked IPs, and I can easily add new IPs and quickly identify the risky ones.

The script automates the process of checking IP addresses against AbuseIPDB. It is designed to enhance a list of ips in the file "ips.txt" with information from AbuseIPDB, a database that tracks IP addresses associated with malicious activity. 

**Key Features:**

* Reads `ips.txt` line by line, skipping already processed entries. It expects one IP address per line.
* Queries AbuseIPDB for unique IPs, preventing duplicates.
* Efficiently resolves `abuseipdb.com` only once.
* Updates `ips.txt` with AbuseIPDB data, preserving existing information.
* Sorts `ips.txt` by abuse confidence score (highest at the bottom).
* Verbose output option (`-v`).

**Setup:**

1.  Obtain a free AbuseIPDB API key.
2.  Ensure Python 3 is installed.
3.  Edit the script to put yout API key. The free API allows 1000 request by day. 


**How it works**

**Reading and Filtering:** The script opens ips.txt and reads it line by line.
It checks each line to see if it already contains information from AbuseIPDB. If it does, it skips that line because it's already been processed.
It also makes sure that each line it processes contains only a single IP address. This prevents errors from lines with other data.

**AbuseIPDB Queries:** For each unique IP address that passes the filtering, the script queries the AbuseIPDB database.
Because I had problems with DNS resolution in my home lab, the script avoids redundant queries. Resolving the domain name only once.It resolves the abuseipdb.com domain name only once at the beginning, rather than every time it needs to make a query. 
It also prevents querying the same ip adress multiple times during the same execution of the script.

**Updating the File:** The script takes the information retrieved from AbuseIPDB (specifically, the "abuseConfidenceScore") and adds it to the corresponding line in ips.txt.

It does this in a way that preserves any existing data in the file. So, if you've run the script before, it won't overwrite your previous results.

You can add IPs and rerun the script knwing that it will process only the new IPs.

**Sorting:** After updating the file, the script sorts the lines in ips.txt based on the abuseConfidenceScore.

The sorting is done in ascending order, meaning IP addresses with the highest abuse confidence scores (the ones most likely to be malicious) will appear at the bottom of the file.

After the script completes, you can use "cat ips.txt" to view the results. The most dangerous IPs will be at the bottom of the list, while the least suspicious IPs will be at the top.

**Verbose Output:** The script has a "-v" parameter. When used, the script will output more information to the user during its execution. This is useful for debugging or monitoring the script's progress.
