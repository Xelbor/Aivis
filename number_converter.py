import voice

ones = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "одну", "две", "одним", "двумя", "тремя", "четырмя", "пятью", "шестью", "семью", "восьмью", "девятью", "десятью"]
tens = ["", "десять", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
teens = ["десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
hundreds = ["", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]

def words_to_numbers(text):
    try:
        words = text.split()
        result = []
        i = 0
        while i < len(words):
            number = 0
            found_number = False
            while i < len(words) and (words[i] in ones or words[i] in tens or words[i] in teens or words[i] in hundreds or words[i] == "тысяча" or words[i] == "миллион"):
                if words[i] in ones:
                    if words[i] == "одну" or words[i] == "одним":
                        number += 1
                    elif words[i] == "две" or words[i] == "двумя":
                        number += 2
                    elif words[i] == "тремя":
                        number += 3
                    elif words[i] == "четырмя":
                        number += 4
                    elif words[i] == "пятью":
                        number += 5
                    elif words[i] == "шестью":
                        number += 6
                    elif words[i] == "семью":
                        number += 7
                    elif words[i] == "восьмью":
                        number += 8
                    elif words[i] == "девятью":
                        number += 9
                    elif words[i] == "десятью":
                        number += 10
                    else:
                        number += ones.index(words[i])
                    i += 1
                elif words[i] in tens:
                    number += tens.index(words[i]) * 10
                    i += 1
                elif words[i] in teens:
                    number += teens.index(words[i]) + 10
                    i += 1
                elif words[i] in hundreds:
                    number += hundreds.index(words[i]) * 100
                    i += 1
                elif words[i] == "тысяча":
                    number *= 1000
                    i += 1
                elif words[i] == "миллион":
                    number *= 1000000
                    i += 1
                found_number = True

            if found_number:
                result.append(str(number))
            else:
                result.append(words[i])
                i += 1

        return ' '.join(result)

    except:
        voice.va_speak("Произошла ошибка при конвертации чисел, возможно вы сказали не число")

# Пример использования
#example = 'случайное число между двумя и тремя'
#result = words_to_numbers(example)
#print(result)