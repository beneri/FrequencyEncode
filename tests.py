import unittest
from  freqEncode import *


class TestStringMethods(unittest.TestCase):

    def getEnglishFreq(self):
        return { 'E' : 12.0,
                        'T' : 9.10,
                        'A' : 8.12,
                        'O' : 7.68,
                        'I' : 7.31,
                        'N' : 6.95,
                        'S' : 6.28,
                        'R' : 6.02,
                        'H' : 5.92,
                        'D' : 4.32,
                        'L' : 3.98,
                        'U' : 2.88,
                        'C' : 2.71,
                        'M' : 2.61,
                        'F' : 2.30,
                        'Y' : 2.11,
                        'W' : 2.09,
                        'G' : 2.03,
                        'P' : 1.82,
                        'B' : 1.49,
                        'V' : 1.11,
                        'K' : 0.69,
                        'X' : 0.17,
                        'Q' : 0.11,
                        'J' : 0.10,
                        'Z' : 0.07 }

    def getEnglishWordsFreq(self):
        return {'the':  0.056271872,
                'of':   0.033950064,
                'and':  0.029944184,
                'to':   0.025956096,
                'in':   0.017420636,
                'i':    0.011764797,
                'that': 0.011073318,
                'was':  0.010078245,
                'his':  0.008799755,
                'he':   0.008397205}



    def test_generateList(self):
        self.assertEqual(generateList({'a': 0.5, 'b': 0.5}, 10, 1), ['b', 'a'] )
        self.assertEqual(generateList({'a': 0.5, 'b': 0.5}, 10, 2), ['b', 'a', 'b', 'a'] )
        self.assertEqual(generateList({'a': 0.5, 'b': 0.5}, 10, 3), ['b', 'a', 'b', 'a', 'b', 'b', 'b', 'a'] )

        # Change seed
        self.assertEqual(generateList({'a': 0.5, 'b': 0.5}, 1337, 1), ['b', 'b', 'a', 'b'])
        self.assertEqual(generateList({'a': 0.5, 'b': 0.5}, 1337, 2), ['b', 'b', 'a', 'b', 'a', 'b'])
        self.assertEqual(generateList({'a': 0.5, 'b': 0.5}, 1337, 3), ['b', 'b', 'a', 'b', 'a', 'b', 'a', 'b'])


        freq = normalizeFrequencies(self.getEnglishFreq())
        self.assertEqual(generateList(freq, 10, 1), ['S', 'I'] )
        self.assertEqual(generateList(freq, 10, 2), ['S', 'I', 'R', 'T'] )
        self.assertEqual(generateList(freq, 10, 3), ['S', 'I', 'R', 'T', 'C', 'C', 'H', 'T'] )

        # Check that we get asser error if frequencies are not normalized
        with self.assertRaises(AssertionError):
            generateList({'a': 100, 'b': 200}, 10, 3)


    def test_encodeBinaryData(self):
        self.assertEqual(encodeBinaryData([0], {'a': 0.5, 'b': 0.5}, 10), 'b a')
        self.assertEqual(encodeBinaryData([1], {'a': 0.5, 'b': 0.5}, 10), 'a b')

        self.assertEqual(encodeBinaryData([0,0], {'a': 0.5, 'b': 0.5}, 10), 'b a b a')
        self.assertEqual(encodeBinaryData([0,1], {'a': 0.5, 'b': 0.5}, 10), 'b a a b')
        self.assertEqual(encodeBinaryData([1,0], {'a': 0.5, 'b': 0.5}, 10), 'a b b a')
        self.assertEqual(encodeBinaryData([1,1], {'a': 0.5, 'b': 0.5}, 10), 'a b a b')

        # Using English
        freq = normalizeFrequencies(self.getEnglishFreq())
        self.assertEqual(encodeBinaryData([0,0], freq, 10), 'S I R T')
        self.assertEqual(encodeBinaryData([1,1], freq, 10), 'I S T R')

        # Using Words
        freq = normalizeFrequencies(self.getEnglishWordsFreq())
        self.assertEqual(encodeBinaryData([0,0], freq, 10), 'to and to the')
        self.assertEqual(encodeBinaryData([1,1], freq, 10), 'and to the to')
        self.assertEqual(encodeBinaryData([1, 0, 0, 1, 0, 1, 1, 0, 0, 0], freq, 10), 'and to to the i that the to and of his the the he that to of of to and in to')

    def helper_decodeEncoded(self, binaryData, freq, seed):
        encodedData = encodeBinaryData(binaryData, freq, seed)
        return decodeStringData(encodedData, freq, seed)



    def test_decodeStringData(self):
        self.assertEqual(decodeStringData('b a', {'a': 0.5, 'b': 0.5}, 10), [0])
        self.assertEqual(decodeStringData('a b', {'a': 0.5, 'b': 0.5}, 10), [1])

        self.assertEqual(decodeStringData('b a b a', {'a': 0.5, 'b': 0.5}, 10), [0,0])
        self.assertEqual(decodeStringData('b a a b', {'a': 0.5, 'b': 0.5}, 10), [0,1])
        self.assertEqual(decodeStringData('a b b a', {'a': 0.5, 'b': 0.5}, 10), [1,0])
        self.assertEqual(decodeStringData('a b a b', {'a': 0.5, 'b': 0.5}, 10), [1,1])


        # Encode and decode back
        self.assertEqual( self.helper_decodeEncoded([1], {'a': 0.5, 'b': 0.5}, 10), [1])
        self.assertEqual( self.helper_decodeEncoded([1,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,1], {'a': 0.5, 'b': 0.5}, 10), [1,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,1])

        freq = normalizeFrequencies(self.getEnglishFreq())
        self.assertEqual( self.helper_decodeEncoded([1,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,1], freq, 1337), [1,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,1])

        freq = normalizeFrequencies(self.getEnglishWordsFreq())
        self.assertEqual( self.helper_decodeEncoded([1,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,1], freq, 1337), [1,0,1,0,0,0,1,1,1,1,0,1,1,1,0,0,1,1,0,0,1,0,1,0,1])



    def test_encode(self):
        self.assertEqual(encode("hello", {'a': 0.5, 'b': 0.5}, 10), 'b a a b b b a b b a b a b a b b a a b a b b a b b b b a a a a b b a a b a a b b a a a a a b b b a b b a a b b a b a a b a a a b a a a a b b a b a a b a a a a a b a b b a b b b b a a a a a b b a a b a a a b a a a a a b a a a a b b b a b b b a a b b b b b a b b a b b b a b b b a b a b b b a a a a a a b b a b b b b a a b b a a b')

    def test_deocde(self):
        self.assertEqual(decode('b a a b b b a b b a b a b a b b a a b a b b a b b b b a a a a b b a a b a a b b a a a a a b b b a b b a a b b a b a a b a a a b a a a a b b a b a a b a a a a a b a b b a b b b b a a a a a b b a a b a a a b a a a a a b a a a a b b b a b b b a a b b b b b a b b a b b b a b b b a b a b b b a a a a a a b b a b b b b a a b b a a b', {'a': 0.5, 'b': 0.5}, 10), "hello")



if __name__ == '__main__':
    unittest.main()

