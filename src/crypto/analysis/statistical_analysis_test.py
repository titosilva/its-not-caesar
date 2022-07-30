from crypto.analysis.statistical_analysis import StatisticalAnalyser

def test_count_alphabet_on_text__works():
    text = 'abacaxi'
    alphabet = 'abc'

    analyser = StatisticalAnalyser()
    assert analyser.count_alphabet_on_text(text, alphabet) == {
        'a': 3,
        'b': 1,
        'c': 1,
    }

def test_count_alphabet_by_text_slice__works():
    text = 'abacaxi'
    alphabet = 'abc'
    
    analyser = StatisticalAnalyser()
    assert analyser.count_alphabet_by_text_slice(text, alphabet, 3) == [
        { 'a': 1, 'b': 0, 'c': 1, },
        { 'a': 1, 'b': 1, 'c': 0, },
        { 'a': 1, 'b': 0, 'c': 0, },
    ]