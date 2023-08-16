tags = ["<start-class>","<start-code>", "<end-of-node-", "<end-of-node>", "<iterable>", "<function>", "<method>", "<slice-lower>", "<slice-upper>", "<slice-step>",
        "<expression>", "<variable>", "<subtract>", "<add>", "<multiply>", "<divide>", "<attribute>", "<class>", "<list>", "<dict>", "<str>", "<int>", "<float>", "<bool>", "<tuple>", "<set>", "<slice>",
        "<empty>", "<key>", "<value>", "<self-attribute>", "<class-attribute>", "<is-equal-to>", "<is-not-equal-to>",
        "<is-smaller-than>", "<smaller-or-equal>", "<greater-than>", "<greater-or-equal>", "<is>", "<is-not>", "<is-in>",
        "<is-not-in>", "<if-left>", "<if-right>", "<inside-body>", "<if-statement>", "<self>", "<elif-statement>", "<increment>", "<for-loop>",
        "<index>","<import>", "<library>", "<pass>", "<continue>", "<default-value>", "<delete>" ]
#TODO separate nouns ("variable"), from event ("for-loop", class, function), from verbs (import, delete, enter")
introduction = "Once upon a time, there was a <character-profession> named <character-name> who wanted to explain <possessive> code to <possessive> <character-role> in form of a story."
assignments = "To create a story, <character-name> explained, you first need to pick some important story elements. So first make sure you have following elements: <story-elements> "

with open("pseudo.txt", "r") as pseudo_code:
    pseudo = pseudo_code.read()
    if "<class>" in pseudo:
        pseudo = pseudo.replace("<start-code>", introduction)
