from lab_2.lab import Parser
import json

if __name__ == '__main__':
    file = open("js.json", encoding="utf-8")
    json_str = str(json.loads(file.read())).replace(' ', '')
    print(json_str)
    parser = Parser(json_str)
    parsed = parser.parse()

    for country in parsed["Страны"]:
        s_obl = 0
        for oblast in country["Страна"]:
            s_r = 0
            for rayon in oblast["Область"]:
                s_r += rayon["Площадь"]
            s_obl += oblast["Площадь"]
            if oblast["Площадь"] != s_r:
                print(
                    f'Ошибка! Площадь области {oblast["Название"]} не соответствует суммарной площади районов области')
                print(f'Площадь районов: {s_r}, площадь области: {oblast["Площадь"]}')
        if country["Площадь"] != s_obl:
            print(
                f'Ошибка! Площадь страны {country["Название"]} не соответствует суммарной площади областей страны')
            print(f'Площадь областей: {s_obl}, площадь страны: {country["Площадь"]}')
