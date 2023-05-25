% Facts for word to digit conversion
word(zero, 0).
word(one, 1).
word(two, 2).
word(three, 3).
word(four, 4).
word(five, 5).
word(six, 6).
word(seven, 7).
word(eight, 8).
word(nine, 9).
word(ten, 10).
word(eleven, 11).
word(twelve, 12).
word(thirteen, 13).
word(fourteen, 14).
word(fifteen, 15).
word(sixteen, 16).
word(seventeen, 17).
word(eighteen, 18).
word(nineteen, 19).
word(twenty, 20).
word(thirty, 30).
word(forty, 40).
word(fifty, 50).
word(sixty, 60).
word(seventy, 70).
word(eighty, 80).
word(ninety, 90).
word(hundred, 100).
word(thousand, 1000).

% Rule to convert a single word to a number
word_to_digit(Word, Digit) :-
    word(Word, Digit).

% Rule to convert a compound word to a number
word_to_digit(Word, Digit) :-
    compound_word(Word, Prefix, Suffix),
    word(Prefix, PrefixValue),
    word(Suffix, SuffixValue),
    Digit is PrefixValue + SuffixValue.

% Helper rule to handle compound words
compound_word(Compound, Prefix, Suffix) :-
    atom_concat(Prefix, Suffix, Compound),
    word(Prefix, _),
    word(Suffix, _).

% Rule to convert a written number to digits
convert_to_digits(WrittenNumber, Digits) :-
    atomic_list_concat(Words, ' ', WrittenNumber),
    convert_words(Words, Digits).

% Rule to convert a list of words to digits
convert_words([], 0).
convert_words([Word], Digit) :-
    word_to_digit(Word, Digit).
convert_words([Word1, Word2 | Rest], Digit) :-
    word_to_digit(Word1, Value1),
    word_to_digit(Word2, Value2),
    Value1 < Value2,
    convert_words(Rest, SubDigit),
    Digit is Value1 * Value2 + SubDigit.
convert_words([Word1, Word2 | Rest], Digit) :-
    word_to_digit(Word1, Value1),
    word_to_digit(Word2, Value2),
    Value1 >= Value2,
    convert_words([Word2 | Rest], SubDigit),
    Digit is Value1 + SubDigit.


/*  Test cases:
?- convert_to_digits('zero', Digits).
Digits = 0.

?- convert_to_digits('twenty', Digits).
Digits = 20.

?- convert_to_digits('fifty six', Digits).
Digits = 56.

?- convert_to_digits('eighty four', Digits).
Digits = 84.

?- convert_to_digits('one hundred', Digits).
Digits = 100.

?- convert_to_digits('seven hundred forty two', Digits).
Digits = 742.

?- convert_to_digits('nine hundred ninety', Digits).
Digits = 990.

?- convert_to_digits('one thousand', Digits).
Digits = 1000. */