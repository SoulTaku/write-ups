
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## Online encryption (100): Forensics

### Proof of flag
>* ECSC{dd545fbf12fd608daa8c201f50f95c8520bec9f744a3573b1dc0bc53ce019726}

### Summary
>* Analyze pcap > find http traffic to encrypt the flag > decode base64 > decrypt rot13

### Proof of solving

After looking through the capture, we see that the user makes some requests to a website to encrypt something using AES CBC. So we are unable to decrypt the data without the key. But wait... we captured the request so we have both the key and the plaintext. Silly user... 

**_Fires up scapy_**

```python
>>> from base64 import b64decode as d
>>> packets = rdpcap('online.pcapng')
>>> plaintext = ''
>>> for p in packets:
...:    if p.haslayer(TCP):
...:        if p.dport == 80:
...:            if p.haslayer(Raw):
...:                if 'here' in p.load:
...:                    plaintext += p.load.split('plainText=')[1].split('&')[0].replace('%3D', '=')
...:                    
>>> d(plaintext)
'RPFP{qq545sos12sq608qnn8p201s50s95p8520orp9s744n3573o1qp0op53pr019726}'
```

Hmm, that looks like ROT13, so let's try that online. Oh, it was ROT13 indeed. :)
