
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## global-cell (300): Networking

### Proof of flag
>* ECSC{50fb4a9bee63b51141c2b32e42251d1f88104731d1a7b73ff9750626227d7f5a}

### Summary
>* Analyze pcap > find GSM info > find location > sha256(area_code)

### Proof of solving

After opening the pcap in wireshark I see some MySQL packets and some really interesting GSM packets. After losing a some time looking over the GSM packets and trying to find something useful I finally decide to look over the MySQL packets too.
Analyzing the queries, near the end of the pcap I found:
```MySQL
INSERT INTO `pta_report_items` (`task_id`, `user_id`, `vuln_id`, `raw_output`, `created_at`, `updated_at`)
VALUES (1129, 1, 419, '## Interconnection
Peer SCTP Host: 127.0.0.1
Peer SCTP Port: 2905
SCTP Mode: CLIENT
PTA M3UA PC: 8888
Peer M3UA PC: 8889
M3UA Routing Context: 0
Network Indicator: 0
PTA SCCP GT: 123456789012542
Perimeter: international:SIGTRAN
ID: 37
Name: SIGTRAN MODULES TEST

==== Global Cell ID ====
MSISDN used by PTA: 333456789011111
Global Cell ID discovered:
Mobile Country Code (MCC) : 208 (33)
Mobile Network Code (MNC) : 20 (Bouygues Telecom)
Location Area Code  (LAC) : 22510
Cell ID                   : 1106
Cell ID BSC               : 0
Cell ID BTS               : 69
Cell ID Sector            : 2
HLR answering: 333456789011111 (France, Olo Zone 3)', '2018-10-11 15:54:50', '2018-10-11 15:54:50')
```
And i remembered from my previous hours of googling that I can track the phone using the MCC, MNC, LAC and CID numbers. Copied those into an [online](http://www.cell2gps.com/) service that I've found, copied the coordinates into google maps and found out the city as Lanton. Googled the area code and found two possible values (33138/33229). Tested them both and the second one worked.
