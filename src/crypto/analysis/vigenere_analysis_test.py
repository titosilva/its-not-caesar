from crypto.algorithms.vigenere import VigenereCipher
from crypto.analysis.vigenere_analysis import VigenereAnalyser
from languages.english import EnglishLanguage
from languages.portuguese import PortugueseLanguage
from utils import dict_to_ordered_tuples

sample_text = '''
The "computable" numbers may be described briefly as the real
numbers whose expressions as a decimal are calculable by finite means.
Although the subject of this paper is ostensibly the computable numbers.
it is almost equally easy to define and investigate computable functions
of an integral variable or a real or computable variable, computable
predicates, and so forth. The fundamental problems involved are,
however, the same in each case, and I have chosen the computable numbers
for explicit treatment as involving the least cumbrous technique. I hope
shortly to give an account of the relations of the computable numbers,
functions, and so forth to one another. This will include a development
of the theory of functions of a real variable expressed in terms of com-
putable numbers. According to my definition, a number is computable
if its decimal can be written down by a machine.
In §§ 9, 10 I give some arguments with the intention of showing that the
computable numbers include all numbers which could naturally be
regarded as computable. In particular, I show that certain large classes
of numbers are computable. They include, for instance, the real parts of
all algebraic numbers, the real parts of the zeros of the Bessel functions,
the numbers IT, e, etc. The computable numbers do not, however, include
all definable numbers, and an example is given of a definable number
which is not computable.
Although the class of computable numbers is so great, and in many
Avays similar to the class of real numbers, it is nevertheless enumerable.
In § 81 examine certain arguments which would seem to prove the contrary.
By the correct application of one of these arguments, conclusions are
reached which are superficially similar to those of Gbdelf. These resu
have valuable applications. In particular, it is shown (§11) that the
Hilbertian Entscheidungsproblem can have no solution.
In a recent paper Alonzo Church f has introduced an idea of "effective
calculability", which is equivalent to my "computability", but is very
differently defined. Church also reaches similar conclusions about the
EntscheidungsproblemJ. The proof of equivalence between "computa-
bility" and "effective calculability" is outlined in an appendix to the
present paper. We have said that the computable numbers are those whose decimals
are calculable by finite means. This requires rather more explicit
definition. No real attempt will be made to justify the definitions given
until we reach § 9. For the present I shall only say that the justification
lies in the fact that the human memory is necessarily limited.
We may compare a man in the process of computing a real number to ;i
machine which is only capable of a finite number of conditions q 1: q 2 . .... q I;
which will be called " m-configurations ". The machine is supplied with a
" t a p e " (the analogue of paper) running through it, and divided into
sections (called "squares") each capable of bearing a "symbol". At
any moment there is just one square, say the r-th, bearing the symbol <2>(r)
which is "in the machine". We may call this square the "scanned
square ". The symbol on the scanned square may be called the " scanned
symbol". The "scanned symbol" is the only one of which the machine
is, so to speak, "directly aware". However, by altering its m-configu-
ration the machine can effectively remember some of the symbols which
it has "seen" (scanned) previously. The possible behaviour of the
machine at any moment is determined by the ra-configuration q n and the
scanned symbol <S (r). This pair q n , © (r) will be called the '' configuration'':
thus the configuration determines the possible behaviour of the machine.
In some of the configurations in which the scanned square is blank (i.e.
bears no symbol) the machine writes down a new symbol on the scanned
square: in other configurations it erases the scanned symbol. The
machine may also change the square which is being scanned, but only by
shifting it one place to right or left. In addition to any of these operations
the m-configuration may be changed. Some of the symbols written down will 
form the sequence of figures which is the decimal of the real number
which is being computed. The others are just rough notes to "assist the
memory ". It will only be these rough notes which will be liable to erasure.
It is my contention that these operations include all those which are used
in the computation of a number. The defence of this contention will be
easier when the theory of the machines is familiar to the reader. In the
next section I therefore proceed with the development of the theory and
assume that it is understood what is meant by "machine", "tape",
"scanned", etc.
'''

sample_key = 'testcipher'
sample_key_2 = 'ab'

def test_language_detection_for_english():
    cipher = VigenereCipher()
    ciphertext = cipher(sample_text, key=sample_key)
    max_key_length = 30

    english = EnglishLanguage()
    analyser = VigenereAnalyser()
    detected_language = analyser.detect_language(ciphertext, possible_languages=[english], max_key_length=max_key_length)

    assert len(ciphertext) > 0 and detected_language == english

    portuguese = PortugueseLanguage()
    detected_language = analyser.detect_language(ciphertext, [portuguese], max_key_length=max_key_length)
    assert detected_language is None

def test_key_length_characteristic_computing__should__give_must_probable_keys():
    cipher = VigenereCipher()
    ciphertext = cipher(sample_text, key=sample_key)
    english = EnglishLanguage()
    analyser = VigenereAnalyser()

    # Use this max key length on testing to avoid getting repeated key results
    # For example, if the true size of the key is 2 and we test it with 4, 
    # 4 will also be a possible key. If the true key is 'ba', 'baba' is also a possible key,
    # as the result of using 'ba' is the same of using 'baba'
    max_key_length = 2 * len(sample_key) + 1

    characteristics_by_key_length = analyser.compute_avg_characteristic_diff_by_key_length(ciphertext, english, max_key_length=max_key_length)
    characteristics_tuples = dict_to_ordered_tuples(characteristics_by_key_length)

    assert len(sample_key) in map(lambda ct: ct[0], characteristics_tuples[0:3])

def test_computing_of_most_probable_keys():
    cipher = VigenereCipher()
    ciphertext = cipher(sample_text, key=sample_key_2)
    english = EnglishLanguage()
    analyser = VigenereAnalyser()

    # Use this max key length on testing to avoid getting repeated key results
    # For example, if the true size of the key is 2 and we test it with 4, 
    # 4 will also be a possible key. If the true key is 'ba', 'baba' is also a possible key,
    # as the result of using 'ba' is the same of using 'baba'
    max_key_length = 2 * len(sample_key_2) - 1

    characteristics_by_key_length = analyser.compute_avg_characteristic_diff_by_key_length(ciphertext, english, max_key_length=max_key_length)
    characteristics_tuples = dict_to_ordered_tuples(characteristics_by_key_length)

    # print(analyser.get_most_probable_key(ciphertext, english, characteristics_tuples[0][0]))
    # print(analyser.get_most_probable_key(ciphertext, english, characteristics_tuples[1][0]))
    print(analyser.get_most_probable_key_v2(ciphertext, english, characteristics_tuples[2][0]))


    