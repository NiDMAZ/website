import types

class HtmlTableCreator(object):
    def __init__(self):
        self.table = []
        self.html_table = ''
        self.header = None

    def add_header(self, table_header):
        self.header = self._generate_row(table_header)

    def add_row(self, data):
        self.table.append(self._generate_row(data))

    def get_header(self):
        return self.header

    def _generate_row(self, data):
        data_type = type(data)
        if types.StringType == data_type:
            return data.split(',')
        elif types.TupleType == data_type:
            return [i for i in data]
        else:
            return data

    def get_table(self):
        _table = self.table
        _table.sort()
        _table.insert(0, self.get_header())
        return _table

    def _generate_html_table(self):
        self.html_table = list2htmltable(self.get_table())
        return True

    def get_html_table(self):
        if self._generate_html_table():
            return self.html_table


def list2htmltable(input):
    out = '<div>'
    out += '<table class="table table-hover table-responsive">'
    header = input[0]
    headerindex = None
    for i, row in enumerate(input):
        out += "<tr>"
        tag = 'td'
        if headerindex is not None and row[headerindex] == colval:
            tag = 'td'
        if i == 0:
            tag = 'th'
        for j, c in enumerate(row):
            thiscell = "<{tag}>" + str(c) + "</{tag}>"
            out += thiscell.format(tag=tag)
        out += "</tr>\n"
    out += "</table>"
    out += '</div>'
    return out
