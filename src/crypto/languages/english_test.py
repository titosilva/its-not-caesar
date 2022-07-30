from crypto.languages.english import EnglishLanguage

def test_remove_nonalphabet_chars__should__transform_all_letters_to_lower_and_remove_spaces():
    language = EnglishLanguage()
    text = 'ABACAXI eh MELHOR que MoRaNgO'

    prepared = language.remove_nonalphabet_chars(text)

    assert prepared == 'abacaxiehmelhorquemorango'

def test_remove_nonalphabet_chars__should__normalize_text_accents():
    language = EnglishLanguage()
    text = 'ABACAXI é MELHOR que MoRaNgO. - João Tito, 2022'

    prepared = language.remove_nonalphabet_chars(text)

    assert prepared == 'abacaxiemelhorquemorangojoaotito'

def test_english_characteristic__should__be_close_to_expected():
    language = EnglishLanguage()
    real_characteristic = language.compute_characteristic()
    expected_characteristic = 0.06015

    assert abs(expected_characteristic - real_characteristic) < 0.05

def test_english_digrams_loading():
    language = EnglishLanguage()
    frequencies = language.get_digram_frequencies()
    assert len(frequencies) > 0
