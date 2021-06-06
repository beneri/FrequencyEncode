import random

# Helper functions

def normalizeFrequencies(frequencies):
    new_freq = {}
    total = sum(frequencies.values())
    for key in frequencies:
        new_freq[key] = frequencies[key] / total
    return new_freq

def calculateIntervals(frequencies):
    intervals = []
    current = 0
    for (letter, freq) in frequencies.items():
        intervals.append( (current, current+freq, letter) )
        current += freq
    return intervals



def generateTwoValues(intervals):
    """ Generate two values following the frequency intervals.
    Warning, This depends on the state of random

    """
    res = []
    for _ in range(2):
        r = random.random()
        for (x,y,l) in intervals:
            if r < y:
                res.append(l)
                break
    return res

def generateList(freq, seed, number_of_bits):
    """ freq must be normalized here, i.e. sum(freq.values()) = 1 """
    assert( abs(1.0 - sum(freq.values())) < 0.00001 )

    random.seed(seed)
    intervals = calculateIntervals(freq)
    res = []
    # Produce the data string
    # good_bits are bits that are not duplicates
    good_bits = 0
    prev = 0

    while good_bits < number_of_bits:
        (v1,v2) = generateTwoValues(intervals)
        if v1 != v2:
            good_bits += 1
        res.append(v1)
        res.append(v2)
    return res

def encodeBinaryData(binaryDataArray, frequencies, seed):
    # print("binary setting seed: ", seed)
    random.seed(seed)

    res = generateList(frequencies, seed, len(binaryDataArray))

    # Now we swap
    # Better way without indexing?
    i = 0
    bit_index = 0
    while i < len(res)-1:

        # Just skip it
        if res[i] == res[i+1]:
            i += 2
            continue

        # swap if one bit
        if binaryDataArray[bit_index]:
            tmp = res[i]
            res[i] = res[i+1]
            res[i+1] = tmp

        bit_index += 1
        i += 2

        # We are done
        if bit_index == len(binaryDataArray):
            break

    return " ".join(res[:i])

def decodeStringData(stringData, frequencies, seed):
    random.seed(seed)
    bits = []

    stringData = "".join([c for c in stringData if c != " "])

    doubles = 0
    # count doubles
    for i in range(len(stringData)-1):
        if stringData[i] == stringData[i+1]:
            doubles += 1

    res = generateList(frequencies, seed, len(stringData))

    resListIndex = 0
    stringDataIndex = 0
    while stringDataIndex < len(stringData)-1:

        # Just skip it if two consecutive values are the same
        if res[resListIndex] == res[resListIndex+1]:
            stringDataIndex += len(res[resListIndex]) + len(res[resListIndex+1])
            resListIndex += 2
            continue

        stringDataWord = stringData[stringDataIndex:stringDataIndex+len(res[resListIndex])]
        nextWordIndex = stringDataIndex+len(stringDataWord)
        nextStringDataWord = stringData[nextWordIndex:nextWordIndex+len(res[resListIndex+1])]

        # Check if words are swapped or not
        if res[resListIndex] == stringDataWord and res[resListIndex+1] == nextStringDataWord:
            bits.append(0)
        else:
            bits.append(1)

        # Independent of order, we skip two words worth of length
        stringDataIndex += len(res[resListIndex]) + len(res[resListIndex+1])
        resListIndex += 2

    return bits




# Based on https://stackoverflow.com/a/55120897
def binary_converter(string):
    """ String to array of bits """
    bits = []
    for character in string:
        binstr =  bin(ord(character))[2:].zfill(8)
        for bit in binstr:
            if bit == "1":
                bits.append(1)
            else:
                bits.append(0)
    return bits

def decode_binary_string(s):
    """ String of bits to string """
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))


# Usable functions

def encode(msg, frequencies, seed=10):
    frequencies = normalizeFrequencies(frequencies)
    bitMsgArray = binary_converter(msg)
    res = encodeBinaryData(bitMsgArray, frequencies, seed)
    return res

def decode(encodedMsg, frequencies, seed=10):
    frequencies = normalizeFrequencies(frequencies)
    bitsOrg = decodeStringData(encodedMsg, frequencies, seed)
    orgStr = decode_binary_string("".join([chr(ord('0')+bit) for bit in bitsOrg]))
    return orgStr








