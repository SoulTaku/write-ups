
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## Alice (300): Crypto

### Proof of flag
>* ECSC{dc0eb76143e50fe3dbeb6383605de5ffa9fefe455caca597677eab7cbf0ad649}

### Summary
>* The second half of the flag is straightforward, but the first one requires a bit of thinking and answering "What would the attacker's best strategy be?"

### Proof of solving

Since the attacker only queries for indexes in the first half, all the characters in the second half are wrong, so for a position i, all the characters on that position are wrong, so by filtering them out from a list of all possible characters we get the right one for that position. Now for the first half i had to to think a bit, "What is the best strategy so you can get the whole hash in 16 queries?". The answer is that you query each position only once. so we know that for a position j there is a character that will appear only once. [Solver](https://github.com/SoulTaku/write-ups/blob/master/ECSC2019/Crypto/alice.py)
