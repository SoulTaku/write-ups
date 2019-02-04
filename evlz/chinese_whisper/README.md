```
BOSS: It better be secure!!!

Ciphertext https://storage.cloud.google.com/evlzctf2019/Ciphertext.txt

readme https://storage.cloud.google.com/evlzctf2019/Readme.txt

xuts https://storage.cloud.google.com/evlzctf2019/xuts.txt
```

Reading through the provided files we see that the key for each message is the key for the last message with the last byte changed and shifted. We are also provided with the key for the 40000 message. With some python magic we can write a simple solver for this that generates a previous key based on the given one until the plaintext is readable and do this for all the messages.
After a bit of playing with the ciphertext we observe that it is encrypted using mode ECB so now the only thing left is to write the script which can be found [here](https://github.com/SoulTaku/write-ups/evlz/chinese_whisper/chinese_whisper.py)
