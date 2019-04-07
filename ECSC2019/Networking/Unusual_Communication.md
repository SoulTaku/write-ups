
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## Unusual Communication (200): Networking

### Proof of flag
>* ECSC{5d0d4436ad7e07d5375948ad13746fe2987aa7fd7126dfdd47acedf89905a0a4}

### Summary
>* analyze pcap > extract ICMP data > write image > decrypt CISCO 7 password

### Proof of solving

After analyzing the capture, we see some unusual ICMP data and we can conclude that the user us sending the image through an ICMP tunnel.
Fire up scapy and with a few line we can extract the data.
```python
>>> packets = rdpcap('captura.pcapng')
>>> data = ''
...:for p in packets:
...:    if p.haslayer(ICMP):
...:        if p[IP].src == '10.10.10.1':
...:            data += p.load
...:            
>>> open('password.png', 'wb').write(data)
```
![password.png](https://github.com/SoulTaku/write-ups/raw/master/ECSC2019/Networking/password.png)

The password is a type 7 CISCO password. Could've used OCR, but was afraid it wasn't going to be accurate so I copied it digit by digit. Decrypt it using this [tool](https://github.com/richardstrnad/cisco7decrypt.git) and you get the flag.
