tags_translation = {"<is-defined-as>": "is defined as a", "<end-of-node-if>": "","<end-of-node-import>": "",
                    "<end-of-node-function>": ",\n(END OF FUNCTION)\n",
                    "<end-of-node>": ",\n(END OF NODE)\n", "<float>": "decimal number", "<str>": "the string",
                    '<int>': "the number", '<iterable>': '', '<function>': 'the function', '<slice-lower>': '',
                    '<slice-upper>': '', '<slice-step>': '', '<expression>': 'mathematical expression',
                    '<create>': 'create', '<dict>': 'dictionary', '<iterate>': 'iterate/ go through',
                    '<list-element>': 'element of the list', '<tuple>': 'tuple', '<list>': 'list',
                    '<keys>': 'keys of the dictionary', '<tuples>': 'tuples', '<values>': 'values of the dictionary',
                    '<lists>': 'lists', '<operation>': 'operation', '<if-statement>': ',\n(START OF IF STATEMENT)\n',
                    '<dict-comprehension>': 'dictionary comprehension', '<list-comprehension>': 'list comprehension',
                    '<method>': 'the method', '<variable>': 'the variable', '<subtract>': 'subtract', '<add>': 'add',
                    '<multiply>': 'multiply', '<divide>': 'divide', '<attribute>': 'attribute', '<class>': 'the class',
                    '<empty>': 'empty', '<key>': 'key of the dictionary', '<value>': 'the value',
                    '<self-attribute>': 'the self attribute',
                    '<class-attribute>': 'the attribute of the class',
                    '<modulo>': 'modulo (check the remainder of the division)', '<is-equal-to>': 'is equal to',
                    '<is-not-equal-to>': 'is not equal to', '<is-less-than>': 'is less than',
                    '<less-or-equal>': 'is less or equal', '<greater-than>': 'is greater than',
                    '<greater-or-equal>': 'is greater or equal to', '<is>': 'is', '<is-not>': 'is not',
                    '<is-in>': 'is contained in', '<is-not-in>': 'is not contained in', '<or>': 'or', '<and>': 'and',
                    '<not>': 'is not', '<invert>': 'inverted', '<at-the-power-of>': 'at the power of', '<times>': '*',
                    '<divided-by>': '/', '<plus>': '+', '<minus>': '-', '<while-left>': '',"<end-of-node-while-loop>": "(end of while loop)",
                    '<while-right>': '', '<if-left>': 'if', '<if-right>': '', '<arguments>': 'arguments',
                    '<self>': 'self', '<inside-body>': '', '<elif-statement>': ',\n(ELIF STATEMENT)\n',
                    '<else-statement>': ',\n(ELSE STATEMENT)\n', '<assignment>': '\n(ASSIGNMENT OF VARIABLE)\n',
                    '<increment>': 'increment', '<decrement>': 'decrement', '<for-loop>': ',\n(FOR-LOOP)\n',
                    '<while-loop>': ',\n(WHILE-LOOP)\n', '<start-class>': '', '<delete>': 'remove', '<index>': 'index',
                    '<import>': 'import', '<library>': 'library', '<pass>': 'PASS', '<constant>': 'constant',
                    '<break>': 'BREAK', '<continue>': '', '<default-value>': 'default value', "arguments": "arguments",
                    '<start-code>': '(START OF CODE)', '<end-of-node-assignment>': '', "<end-of-node-for>": "", "<assigned-variable>": "the variable", "<end-of-node-class>": "(End of class)"}
pseudo_after = open('pseudo', 'w')

with open('pseudo_before', 'r') as f:
    for line in f:
        line = line.strip()
        splitted_line = line.split()
        for word in tags_translation.keys():
            line = line.replace(word, tags_translation[word])

        cleaned_line = line.replace("  ", " ")

        cleaned_line = cleaned_line.replace(" ,", ",")

        pseudo_after.write(cleaned_line)

pseudo_after.close()
