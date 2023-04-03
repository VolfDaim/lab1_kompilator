class ParserError(Exception):
    pass


class Parser:
    def __init__(self, json_string):
        self.json_string = json_string
        self.pos = 0

    def parse(self):
        value, pos = self.parse_value(self.json_string, self.pos)
        self.skip_whitespace(self.json_string, pos)
        if pos != len(self.json_string):
            raise ParserError('Прочитан символ, не входящий в алфавит на позиции {}'.format(pos))
        return value

    def parse_value(self, json_string, pos):
        self.skip_whitespace(json_string, pos)
        if json_string[pos:pos + 4] == 'null':
            return None, pos + 4
        elif json_string[pos:pos + 4] == 'true':
            return True, pos + 4
        elif json_string[pos:pos + 5] == 'false':
            return False, pos + 5
        elif json_string[pos] == "'":
            return self.parse_string(json_string, pos + 1)
        elif json_string[pos].isdigit() or json_string[pos] == '-':
            return self.parse_number(json_string, pos)
        elif json_string[pos] == '{':
            return self.parse_object(json_string, pos)
        elif json_string[pos] == '[':
            return self.parse_array(json_string, pos)
        else:
            raise ParserError('Прочитан символ, не входящий в алфавит на позиции {}'.format(pos))

    def parse_string(self, json_string, pos):
        end_pos = pos
        while end_pos < len(json_string):
            if json_string[end_pos] == '\\':
                end_pos += 2
            elif json_string[end_pos] == "'":
                return json_string[pos:end_pos], end_pos + 1
            else:
                end_pos += 1
        raise ParserError('Прочитан символ, не входящий в алфавит на позиции {}'.format(pos))

    def parse_number(self, json_string, pos):
        end_pos = pos
        while end_pos < len(json_string) and (
                json_string[end_pos].isdigit() or json_string[end_pos] in ('.', 'e', 'E', '-', '+')):
            end_pos += 1
        try:
            return int(json_string[pos:end_pos]), end_pos
        except ValueError:
            return float(json_string[pos:end_pos]), end_pos

    def parse_object(self, json_string, pos):
        result = {}
        pos += 1
        self.skip_whitespace(json_string, pos)
        if json_string[pos] == '}':
            return result, pos + 1
        while True:
            key, pos = self.parse_string(json_string, pos + 1)
            self.skip_whitespace(json_string, pos)
            value, pos = self.parse_value(json_string, pos + 1)
            result[key] = value
            self.skip_whitespace(json_string, pos)
            if json_string[pos] == '}':
                return result, pos + 1
            elif json_string[pos] != ',':
                raise ParserError('На позиции {} неожиданный символ: ожидалось } или ,'.format(pos))
            pos += 1

    def parse_array(self, json_string, pos):
        result = []
        pos += 1
        self.skip_whitespace(json_string, pos)
        if json_string[pos] == ']':
            return result, pos + 1
        while True:
            value, pos = self.parse_value(json_string, pos)
            result.append(value)
            self.skip_whitespace(json_string, pos)
            if json_string[pos] == ']':
                return result, pos + 1
            elif json_string[pos] != ',':
                raise ParserError('На позиции {} неожиданный символ: ожидалось ] или ,'.format(pos))
            pos += 1

    def skip_whitespace(self, json_string, pos):
        while pos < len(json_string) and json_string[pos] in (' ', '\t', '\n', '\r'):
            pos += 1
