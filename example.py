import freqEncode
import sys
import argparse

def csvToFreq(freqfile):
    freq = {}
    freq_data = open(freqfile, "r")
    for line in freq_data:
        if line != "\n":
            parts = line.split(",")
            # print(parts)
            freq[parts[0]] = float(parts[1])
    return freq

parser = argparse.ArgumentParser(description='Frequency encoding and decoding')
parser.add_argument('mode', help='"encode" or "decode" data')
parser.add_argument('--freqfile', help='CSV file frequencies')
parser.add_argument('--seed', type=int, help='Random seed used, must be same for encode and decode')

args = parser.parse_args()


# Read frequencies from CSV file
if args.freqfile:
    freq = csvToFreq(args.freqfile)
else:
    # Use English words as default
    freq = csvToFreq("englishWordsFrequency.csv")

# Set random seed, 10 for default
random_seed = 10
if args.seed:
    random_seed = args.seed

if args.mode == "encode":
    data = ""
    while 1:
        new_data = sys.stdin.readline()
        data += new_data
        if not new_data:
            break
    # print(data)
    print( freqEncode.encode(data, freq, random_seed) )
elif args.mode == "decode":
    print( freqEncode.decode(input(), freq, random_seed), end="" )


