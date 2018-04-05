def write2DArrayToLatexTable(self, data, thead, format, caption, label):
        """writes an 2d-array (list of lists) to an formatted latex table

        Arguments:
        data    -- 2darray, list of rows, each row is a list of data
        thead    -- list of descriptions for columns, is used as first row
        format   -- list of formatting rules, how to convert numbers into strings
        caption  -- caption of table in latex
        label    -- label of table in latex
        """
        if len(thead) == len(format):
            l = len(thead)
            i = '  '  # indentation
            self.writeline(r'\begin{table}[H]')
            self.writeline(r'\caption{%s}' % caption)
            self.writeline(r'\begin{center}')
            self.writeline(r'\begin{tabular}{' + '|c' * l + '|}')
            self.writeline(i + r'\hline')
            self.writeline(i + ' & '.join(thead) + r' \\ \hline')
            for row in data:
                self.writeline(i + ' & '.join(format) % tuple(row) + r' \\ \hline')
            self.writeline('\\end{tabular}')
            self.writeline('\\end{center}')
            self.writeline('\\label{' + label + '}')
            self.writeline('\\end{table}')
        else:
            print("WARNING[TxtFile.write2DArrayToLatexTable]: lists have to be the same length.")