def write2DArrayToLatexTable(self, data, thead, format):
        """writes a list of lists to a formatted latex table

        Arguments:
        data    -- 2darray, list of rows, each row is a list of data
        thead    -- list of descriptions for columns, is used as first row
        format   -- list of formatting rules, how to convert numbers into strings

        """
        if len(thead) == len(format):
            l = len(thead)
            i = '  '  # indentation
            self.writeline(r'\begin{center}')
            self.writeline(r'\begin{tabular}{' + '|c' * l + '|}')
            self.writeline(i + r'\hline')
            self.writeline(i + ' & '.join(thead) + r' \\ \hline')
            for row in data:
                self.writeline(i + ' & '.join(format) % tuple(row) + r' \\ \hline')
            self.writeline('\\end{tabular}')
            self.writeline('\\end{center}')
        else:
            print("WARNING[TxtFile.write2DArrayToLatexTable]: lists have to be the same length.")