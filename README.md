# Frequency Encode
This library allows you to encode *arbitrary* data to any frequency distribution.

The goal of this library is to be able to change the fingerprint of your data to a more suitable distribution. 


## Is this encryption?  
No! This library does not come with any cryptographic guarantees and no protection of confidentiality or integrity!
Think of it as base64 encoding or hex encoding.

However, I believe this library works well together with encryption. 
Good encryption should produce random data, which can be easy to detect. 
Frequency encoding might help make it harder for an adversary to detect that your data is encrypted 

For example:

```
echo "secret" | gpg -c | base64 | python3 example.py encode --freqfile data/englishLetterFrequency.csv | \
python3 example.py decode --freqfile data/englishLetterFrequency.csv | base64 -d | gpg -d
```

After our frequency encoding the data would be:

```
who her to been best end like and he they in broken the equal ...
```


## Usage
### CLI
You can test example.py for CLI usage. E.g:

```
echo "test" | python3 example.py encode --freqfile data/englishWordFrequency.csv --seed 1337
```

Will result in:

```
what are no is taken and looked as mine his to dress little past of brought had
the with most going you country made others if caught which look his purpose
first by i the to what were the would you now has must to some by that rose
told heard his her do so whole new an near may to lives my my took the him here
by close knew this place too said with we i of the the and
```

While this text makes no sense, it is still identified as English by many online tools (Google Translate, Cortical, and translated LABS).


### Library
freqEncode.py have two simple functions that can be used, `encode` and `decode`. 

```
import freqEncode
print( freqEncode.encode("A", {'a': 0.5, 'b': 0.5}, 11) )
# a b a b b b a b b b a a a b b a b b b b a a b a a a a a a b b b b a

print( freqEncode.decode("a b a b b b a b b b a a a b b a b b b b a a b a a a a a a b b b b a", {'a': 0.5, 'b': 0.5}, 11) )
# A

```


## How does it work? 
The main idea is simple:

1. Generate two values from a given distribution
2. If the values are the same, ignore them and don't encode any information
3. Else, swap them to encode a 1 bit

The decoder generates the same values and checks which values are swapped. 


The key insight is that frequency is invariant under swapping. 
If we just care about letter frequency, for example, then the order 
of the letters does not matter.

How about bigrams, trigrams, and n-grams you might wonder. If we care about
those we can generate *words* from a distribution instead of *letters*. 

But some sequences of words are more common than others! Well, then we
generate *sentences*. Of course, this quickly becomes infeasible. 


## Feasibility 
The big downside to this method is the data overhead. 
For letters, each *bit* is encoded using two *letters*, that's a 16x increase in data! 
And this is the lower bound since data can only be encoded between different values.

## Future work
I think there is much to improve so feel free to make any pull requests! 

Some parts could definitely be more optimized. Making it more pythonic would be 
good too. And probably much more! :) 













