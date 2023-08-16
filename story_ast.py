import ast
from extract_story_parts import *

variable2type = defaultdict()


def check_slicing(tokens):
    if type(tokens) != ast.Subscript:
        return

    if type(tokens.value) == ast.Name:
        # indexing
        to_be_sliced = tokens.value.id

    elif type(tokens.value) == ast.Call:
        to_be_sliced = tokens.value.value.func.id
        story.append(f"Of the return values of <function> '{to_be_sliced}' take only the")
    if type(tokens.slice) == ast.Tuple:
        # slicing
        pass
    elif type(tokens.slice) == ast.Constant:
        story.append(f"the element with index")

        # indexing
        constant = tokens.slice.value
        story.append(f"{constant}")
        story.append(f"from the object '{to_be_sliced}'")
    elif type(tokens.slice) == ast.Name:

        story.append(f"the element with index")
        # example if parse[pos]
        constant = tokens.slice.id
        story.append(f"{constant}")
        story.append(f"from '{to_be_sliced}'")
    elif type(tokens.slice) == ast.BinOp:

        story.append(f"the element with index")
        # example if parse[pos + 1]
        check_type(tokens.slice.left)
        story.append(check_operator(tokens.slice.op))
        check_type(tokens.slice.right)
        story.append(f"from '{to_be_sliced}'")

    elif type(tokens.slice) == ast.Slice:

        # all three indexes [1:3:4]
        if tokens.slice.lower and tokens.slice.lower and tokens.slice.step:
            story.append(f"the elements")
            starting_from_index = tokens.slice.lower.value if type(
                tokens.slice.lower) == ast.Constant else tokens.slice.lower.id
            story.append(f"from <index>: <slice-lower> {starting_from_index}")
            until_index = tokens.slice.upper.value if type(
                tokens.slice.upper) == ast.Constant else tokens.slice.upper.id
            story.append(f"until <index>: <slice-upper> {until_index}")
            jumping_index = tokens.slice.step.value
            story.append(f" with step size: <slice-step> {jumping_index}")
            story.append(f"in <iterable> '{to_be_sliced}'")
        # only lower index [1:]
        if tokens.slice.lower and not tokens.slice.upper and not tokens.slice.step:
            story.append(f"the elements")
            starting_from_index = tokens.slice.lower.value if type(
                tokens.slice.lower) == ast.Constant else tokens.slice.lower.id
            story.append(f"from <index>: <slice-lower> {starting_from_index} until the end")
            story.append(f"in <iterable> '{to_be_sliced}'")
        # only upper index [:3]
        if tokens.slice.upper and not tokens.slice.lower and not tokens.slice.step:

            story.append(f"the elements")
            if type(tokens.slice.upper) == ast.Constant:
                until_index = tokens.slice.upper.value
            elif type(tokens.slice.upper) == ast.Name:
                until_index = tokens.slice.upper.id
            elif type(tokens.slice.upper) == ast.Call:
                until_index = f"the return value of <function> {tokens.slice.upper.func.id} with arguments {tokens.slice.upper.args[0].id}"
            # until_index = tokens.slice.upper.value if type(tokens.slice.upper) == ast.Constant else tokens.slice.upper.id
            story.append(f"from <index>: 0 until the <index>: <slice-upper> {until_index}")
            story.append(f"in <iterable> '{to_be_sliced}'")
        # only step size [1:3]
        if tokens.slice.lower and tokens.slice.upper and not tokens.slice.step:
            story.append(f"the elements")
            starting_from_index = tokens.slice.lower.value if type(
                tokens.slice.lower) == ast.Constant else tokens.slice.lower.id
            story.append(f"from <index>: <slice-lower> {starting_from_index}")
            if type(tokens.slice.upper) == ast.Constant:
                until_index = tokens.slice.upper.value
            elif type(tokens.slice.upper) == ast.Name:
                until_index = tokens.slice.upper.id
            elif type(tokens.slice.upper) == ast.Call:
                until_index = f"the return value of <function> {tokens.slice.upper.value.func.id} with arguments {tokens.slice.upper.value.args[0].id}"

            story.append(f"until <index>: <slice-upper> {until_index}")
            story.append(f"in '{to_be_sliced}'")
        if not tokens.slice.lower and not tokens.slice.upper and not tokens.slice.step:
            story.append(f"all elements in '{to_be_sliced}'")


story = []
variables_types = defaultdict()


def checkBinOp(value_s):
    if type(value_s) == ast.BinOp:
        story.append("a <expression>")


def process_dict_comp(value_s):
    # generator = for x in numbers
    # please notice I make pseudocode only for one generator
    generation = value_s.generators[0]
    target = generation.target.id
    if isinstance(generation.iter, ast.Tuple):
        story.append(f"To <create> <dict> <iterate> each <list-element> {target} over <iterable> <tuple>")
        check_tuple(generation.iter, "immutable ordered object")
    elif isinstance(generation.iter, ast.List):
        story.append(f"To <create> <dict> <iterate> each <list-element> {target} over <iterable> <list>")
        check_list(generation.iter, "mutable ordered object")
    elif isinstance(generation.iter, ast.Name):
        story.append(f"To <create> <dict> <iterate> each <list-element> {target} over <iterable> ")
        story.append(generation.id)

    if isinstance(value_s.key, ast.Name):
        key = value_s.key.id
        story.append(f"the <keys> of the <dict> are {key}")
    elif isinstance(value_s.key, ast.Constant):
        key = value_s.key.value
        story.append(f"the <keys> of the <dict> are {key}")
    elif isinstance(value_s.key, ast.Tuple):
        story.append("the <keys> of the <dict> are <tuples>")
        check_tuple(value_s.key, "immutable ordered object")
    elif isinstance(value_s.key, ast.List):
        story.append("the <values> of the <dict> are <lists>")
        check_list(value_s.key, "mutable ordered object")
    elif isinstance(value_s.key, ast.BinOp):
        story.append("To create the <keys> of the <dict> applied the following <operation>:")
        check_type(value_s.key.left)
        story.append(check_operator(value_s.key.op))
        check_type(value_s.key.right)

    if isinstance(value_s.value, ast.Name):
        value = value_s.value.id
        story.append(f"the <values> of the <dict> are {value}")
    elif isinstance(value_s.value, ast.Constant):

        value = value_s.value.value
        story.append(f"the <values> of the <dict> are {value}")
    elif isinstance(value_s.value, ast.Tuple):
        story.append("the <values> of the <dict> are <tuples>")
        check_tuple(value_s.value, "immutable ordered object")
    elif isinstance(value_s.value, ast.List):
        story.append("the <values> of the <dict> are <lists>")
        check_list(value_s.key, "mutable ordered object")
    elif isinstance(value_s.value, ast.BinOp):
        story.append(
            f"To create the <values> of the <dict> the {character_with_adjective()} applied the following <operation>:")
        check_type(value_s.value.left)
        story.append(check_operator(value_s.value.op))
        check_type(value_s.value.right)


def process_list_comprehension(variable_name, value_s):
    # generator = for x in numbers
    generation = value_s.generators[0]

    target = generation.target.id

    if isinstance(generation.iter, ast.Tuple):
        iterable = "immutable ordered object"
        check_tuple(generation.iter, iterable)
    elif isinstance(generation.iter, ast.List):
        iterable = "mutable ordered object"
        check_list(generation.iter, iterable)
    elif isinstance(generation.iter, ast.Name):
        iterable = generation.iter.id
    story.append(
        f" To <create> {variable_name} <iterate> over <iterable> {iterable}, take each <list-element> as {target} from {iterable}.")
    if isinstance(value_s.elt, ast.BinOp):
        # example [x + 1 for x in numbers] or [x**2 for x in numbers]
        operator = check_operator(value_s.elt.op)
        left = value_s.elt.left.id if type(value_s.elt.left) == ast.Name else value_s.elt.left.value
        right = value_s.elt.right.id if type(value_s.elt.right) == ast.Name else value_s.elt.left.value
        story.append(
            f"for each {left} in <iterable> the {character_with_adjective()} applied this <operation>:  {left} {operator} {right}")

    if len(generation.ifs) > 0:
        if len(generation.ifs) == 1:
            story.append("if the following condition is met:")
            # story.append("<if-statement>")
            for token in generation.ifs:
                if_statement(token)
        else:
            story.append(f"if the following {len(generation.ifs)} conditions are met:")
            # story.append("<if-statement>")
            for token in generation.ifs:
                if_statement(token)
    else:
        story.append(".")


def check_tag(pseudo, name):
    pseudo = " ".join(pseudo)
    pseudo = pseudo.split()
    if name in pseudo and name != "set":

        name_index = pseudo.index(name)
        tag = pseudo[name_index - 1: name_index][0]
        return tag
    else:
        return "<function>"


def check_type(value_s, variable_name=None):  # 1, object
    if type(value_s) == ast.Starred:
        iterable = value_s.value.id
        story.append(
            f"the unpacked version of '{iterable}'. This was possible only thanks to the magic of the asterisk.")

    if type(value_s) == ast.DictComp:
        story.append(f"'{variable_name}' is a <dict-comprehension>.")
        process_dict_comp(value_s)

    elif type(value_s) == ast.ListComp:
        story.append(f"'{variable_name}' is a <list-comprehension>.")
        process_list_comprehension(variable_name, value_s)

    elif type(value_s) == ast.Attribute:
        to_applied_on = value_s.value.id
        applied_method = value_s.attr
        story.append(f"<method> {applied_method} is applied on <variable> {to_applied_on},")
    elif type(value_s) == ast.Subscript:
        check_slicing(value_s)
    elif type(value_s) == ast.Expr:
        if type(value_s.value) == ast.Call:
            if type(value_s.value.func) == ast.Attribute:
                # hier sind wir
                attribute_name = value_s.value.func.attr
                to_be_applied_on = value_s.value.func.value.id
                story.append(
                    f"{character_pronoun('subject')} performed the trick '{attribute_name}' on {to_be_applied_on}.")
                if len(value_s.value.args) > 0:
                    story.append(
                        f"But '{attribute_name}' needed extra properties to work. So {character_pronoun('subject')} dropped in")
                    # n = 0
                    for arg in value_s.value.args:
                        # story.append(f"argument-{n + 1}")
                        # n += 1
                        check_type(arg)
            else:
                function_name = value_s.value.func.id
                arguments = []
                story.append(character_pronoun('subject'))


                story.append(f"{paraphrase_built_in_method(function_name, value_s.value.args)}")



        else:
            check_type(value_s.value)
    elif type(value_s) == ast.BinOp:

        left = value_s.left
        right = value_s.right
        operator = value_s.op
        check_type(left)
        operator = check_operator(operator)
        story.append(operator)
        check_type(right)
    elif type(value_s) == ast.Sub:
        story.append("<subtract>")
    elif type(value_s) == ast.Add:
        story.append("<add>")
    elif type(value_s) == ast.Mult:
        story.append("<multiply>")
    elif type(value_s) == ast.Div:
        story.append("<divide>")
    elif type(value_s) == ast.Call:

        if type(value_s.func) == ast.Attribute:
            attribute = value_s.func.attr
            story.append("<attribute>")
            story.append(f"<attribute> {attribute} is applied to")
            check_type(value_s.func.value)
            arguments = []

            if len(value_s.args) > 0:
                if paraphrase_built_in_method(value_s.func.id, value_s.args) == "":
                    story.append(f"<method> with following arguments:")
                    # n = 0
                    for arg in value_s.args:
                        # story.append(f"argument-{n + 1}")
                        # n += 1
                        argument = arg.id
                        arguments.append(argument)
                        check_type(arg)
                else:
                    story.append(paraphrase_built_in_method(value_s.func.id, value_s.args))

        elif type(value_s.func) == ast.Name:
            # check whether it's a class or a function tag

            class_tag = check_tag(story, value_s.func.id)

            arguments = []
            if len(value_s.args) > 0:
                if paraphrase_built_in_method(value_s.func.id, value_s.args) == "":

                    story.append(f"{class_tag} with following arguments:")

                    for arg in value_s.args:
                        argument = arg.id
                        arguments.append(argument)
                        check_type(arg)
                else:
                    story.append(paraphrase_built_in_method(value_s.func.id, value_s.args))


        else:
            class_tag = check_tag(story, value_s.func.id)

            # example a = funct()
            if variable_name:
                story.append(
                    f"a new instance of {class_tag} {value_s.func.id} is being created and assigned to <variable> {variable_name}")
                story.append(f" <function> with following arguments:")
                if len(value_s.args) > 0:
                    # n = 0
                    for arg in value_s.args:
                        # story.append(f"argument-{n + 1}")
                        # n += 1
                        check_type(arg)
            else:
                if value_s.func.id:
                    story.append(f" <function> {value_s.func.id}")
                if len(value_s.args) > 0:
                    story.append(f"<function> with following arguments:")
                    # n = 0
                    for arg in value_s.args:
                        # story.append(f"argument-{n + 1}")
                        # n += 1
                        check_type(arg)
                else:
                    story.append("<function>")
                    if len(value_s.args) > 0:
                        story.append(f"<function> with following arguments:")
                        # n = 0
                        for arg in value_s.args:
                            # story.append(f"argument-{n + 1}")
                            # n += 1
                            check_type(arg)
    elif type(value_s) == ast.List:
        if variable_name is not None:
            variables_types[variable_name] = "<list>"
            # story.append(f"{variable_name} <is-defined-as> <list>.")
        else:
            story.append("a <list>")
        check_list(value_s, "mutable ordered object")

    elif type(value_s) == ast.Dict:
        if variable_name is not None:
            variables_types[variable_name] = "<dict>"
            # story.append(f"{variable_name} <is-defined-as> <dict>.")
        else:
            story.append("a <dict>")
        check_dict(value_s, "<dict>")

    elif type(value_s) == ast.Tuple:
        if variable_name:
            variables_types[variable_name] = "<tuple>"
            # story.append(f"{variable_name} <is-defined-as> <tuple>.")
        else:
            story.append("a <tuple>")
        check_tuple(value_s, "immutable ordered object")

    elif type(value_s) == ast.Constant:

        constant_type = value_s.value
        new_type = type(constant_type).__name__
        if variable_name is not None:
            variables_types[variable_name] = f"{new_type}"
            # story.append(f"{variable_name} <is-defined-as> <{new_type}>:")
        check_constant(value_s, f"{new_type}")
    elif type(value_s) == ast.Name:
        # if value_s.id in variables_types:
        #
        #     #story.append(f"the {variables_types[value_s.id]} {value_s.id}")
        #     story.append(f"{value_s.id}")
        # else:
        story.append(f"'{value_s.id}'")


def check_list(token, tag):
    # we are now entering a list
    list_elements = []
    if len(token.elts) > 0:

        for element in token.elts:
            element_value = element.value if type(element) == ast.Constant else element.id
            list_elements.append(str(element_value))
        elements = ",".join(list_elements)
        story.append(f"the {generate_type_metaphor(tag)}, which had to contain these elements: {elements}.")
    else:
        story.append(f"This was an empty {tag}.")


def check_dict(token, tag):
    if len(token.keys) > 0:
        story.append(f"The {generate_type_metaphor(tag)} had to contain following key and value pairs:")
        for key, value in zip(token.keys, token.values):
            story.append("<key>")
            check_type(key, key.value)
            story.append("<value>")
            check_type(value, value.value)
    else:
        story.append(f"This is an <empty> {tag}.")


def check_tuple(token, tag):
    tuple_elements = []
    if len(token.elts) > 0:

        for element in token.elts:
            element_value = element.value if type(element) == ast.Constant else element.id
            tuple_elements.append(str(element_value))
        elements = ",".join(tuple_elements)
        story.append(f"The {generate_type_metaphor(tag)} had to contain these elements: {elements}.")


    else:
        story.append(f"This is an <empty> {tag}.")


def check_constant(token, tag):
    value = token.value

    tag = type(value).__name__
    if tag == "NoneType":
        tag = "none"
    if tag == "Name":
        tag = "str"
    tag = f"<{tag}>"

    if type(value).__name__ == "str":

        value = f'"{value}"'
        if len(value) > 0:

            story.append(f"{value}")
        else:
            story.append(f"This is an empty {tag}")
    else:
        story.append(f"{value},")


def check_annotated_variables(tokens):
    variable_type = check_typing(tokens.annotation)

    if type(tokens.target) == ast.Attribute:  # only in classes self.
        if tokens.target.value.id == "self":
            story.append(f"set <self-attribute> {tokens.target.attr} to")
            check_type(tokens.value, tokens.value.id)
            # story.append(f"to the value <class-attribute> {tokens.value.id}")

    if type(tokens.target) == ast.Name:  # char: List[int] = Lista[:0], p: int = 0
        variable2type[tokens.target.id] = variable_type

        # when variable is a tuple, list, dict, num, string, boolean, None

        story.append(
            f"the {character_with_adjective()} needed {generate_type_metaphor(variable2type[tokens.target.id])} called {tokens.target.id}:")

        check_type(tokens.value, tokens.target.id)
    # if type(tokens.target) == ast.Subscript:  # Lista[0]: int = 3
    #     # handled in check_variable
    #     pass


def check_variables(tokens):
    # tokens.targets is a list
    for target in tokens.targets:

        if type(target) == ast.Attribute:
            if target.value.id == "self":
                story.append(f"set <self-attribute> {target.attr} to")
                check_type(tokens.value, tokens.value.id)
                # story.append(f"to the value <class-attribute> {tokens.value.id}")
        if type(target) == ast.Tuple:
            # when you define more than one variable at the same time
            if type(tokens.value) == ast.Call:
                variables_to_be_defined = " and ".join(
                    [f" <variable> {str(target.id)}" for target in tokens.targets[0].elts])
                variables_to_be_defined_ = ", ".join(
                    [f" <variable> {str(target.id)}" for target in tokens.targets[0].elts])
                story.append(
                    f"set {variables_to_be_defined}.")
                check_type(tokens.value, variables_to_be_defined_)
            else:
                variables_to_be_defined = "and ".join(
                    [f" <variable> {str(target.id)}" for target in tokens.targets[0].elts])
                story.append(
                    f"set {variables_to_be_defined} respectively to the values:")

                for target, value in zip(target.elts, tokens.value.elts):
                    check_type(value, str(target.id))  # variable_name, value

        if type(target) == ast.Name:

            # when variable is a tuple, list, dict, num, string, boolean, None
            if f"set <variable> {target.id}." not in story:
                story.append(f"the {character_with_adjective()} set '{target.id}' equal to :")
            else:
                story.append(f"the {character_with_adjective()} changes the value of '{target.id}':")

            check_slicing(tokens.value)

            check_type(tokens.value, target.id)
        if type(target) == ast.Subscript:
            if type(target.value) == ast.Name:
                iterable = target.value.id
                story.append(f"set")
                check_slicing(target)
                story.append(f"equal to")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.id)
            elif type(target.value) == ast.Attribute:
                story.append(f"set the <self-attribute>.{target.value.attr}.")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.attr)

            elif type(target.value) == ast.Subscript:
                story.append(f"set <variable> {target.value.value.id}.")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.value.id)

            elif type(target.value) == ast.Call:
                story.append(f"set <variable> {target.value.func.id}.")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.func.id)


def check_operator(operator):
    if isinstance(operator, ast.Mod):
        return "modulo"
    if isinstance(operator, ast.Eq):
        return "was equal to"

    elif isinstance(operator, ast.NotEq):
        # return "<is-not-equal-to>"
        return "was not equal to"
    elif isinstance(operator, ast.Lt):
        # return "<is-less-than>"
        return "was smaller than"

    elif isinstance(operator, ast.LtE):
        # return "<less-or-equal>"
        return "was smaller or equal to"
    elif isinstance(operator, ast.Gt):
        # return "<greater-than>"
        return "was greater than"
    elif isinstance(operator, ast.GtE):
        # return "<greater-or-equal>"
        return "was greater than or equal to"
    elif isinstance(operator, ast.Is):
        # return "<is>"
        return "was"
    elif isinstance(operator, ast.IsNot):
        # return "<is-not>"
        return "was not"
    elif isinstance(operator, ast.In):
        # return "<is-in>"
        return "was contained in"
    elif isinstance(operator, ast.NotIn):
        # return "<is-not-in>"
        return "was not contained in"
    elif isinstance(operator, ast.Or):
        # return "<or>"
        return "or"
    elif isinstance(operator, ast.And):
        # return "<and>"
        return "and"
    elif isinstance(operator, ast.Not):
        # return "<not>"
        return "was not"
    elif isinstance(operator, ast.Invert):
        # return "<invert>"
        return "inverted"
    elif isinstance(operator, ast.Pow):
        # return "<at-the-power-of>"
        return "at the power of"
    elif isinstance(operator, ast.Mult):
        # return "<times>"
        return "multiplied by"
    elif isinstance(operator, ast.Div):
        # return "<divided-by>"
        return "divided by"
    elif isinstance(operator, ast.Add):
        # return "<plus>"
        return "plus"
    elif isinstance(operator, ast.Sub):
        # return "<minus>"
        return "minus"
    elif isinstance(operator, ast.FloorDiv):
        return "<floor-divided-by>"


def process_bool_op(token):
    for value in token.values:
        if isinstance(value, ast.BoolOp):
            return value


def while_loop(token, add_operator=False):
    if isinstance(token, ast.BoolOp):
        operator = check_operator(token.op)

        # add_operator = check_condition_pos(node.values)
        for index, value in enumerate(token.values):
            if index < len(token.values) - 1:
                # element if not at last position
                if_statement(value, add_operator, while_=True)
                story.append(operator)
            else:
                if_statement(value, while_=True)

    if isinstance(token, ast.Name):
        # example if list:
        check_type(token)
        story.append("exists")
    if isinstance(token, ast.Compare):
        left = token.left
        right = token.comparators[0]

        story.append(". As long as")
        # story.append("<while-left>")
        check_type(left)
        check_slicing(left)

        operator = check_operator(token.ops[0])
        story.append(operator)
        # story.append("<while-right>")

        check_type(right)
        check_slicing(right)


def if_statement(token, add_operator=False, while_=False):
    tag_left = "" if while_ else f"the {character_with_adjective()} checked whether"
    # tag_right = "<while-right>" if while_ else "<if-right>"
    if isinstance(token, ast.BoolOp):
        operator = check_operator(token.op)

        # add_operator = check_condition_pos(node.values)
        for index, value in enumerate(token.values):
            if index < len(token.values) - 1:
                # element if not at last position
                if_statement(value, add_operator)
                story.append(operator)
            else:
                if_statement(value)

    if isinstance(token, ast.Name):
        # example if list:
        check_type(token)
        story.append("exists")
    if isinstance(token, ast.Compare):
        left = token.left
        right = token.comparators[0]

        story.append(f"{tag_left}")
        check_type(left)
        # check_slicing(left)

        operator = check_operator(token.ops[0])
        story.append(operator)
        # story.append(f"{tag_right}")

        check_type(right)
        # check_slicing(right)


# check types of arguments and variables in order to find some appropriate metaphors for them.
def check_typing(annotation):
    if type(annotation) == ast.Subscript:
        if annotation.value.id == "Dict":
            key_value = []
            for elt in annotation.slice.elts:
                key_value.append(check_typing(elt))
            key_value = "-".join(key_value)
            return f"dict-of-{key_value}"
        if annotation.value.id == "Set":
            element_type = check_typing(annotation.slice)
            return f"set-of-{element_type}"

        if annotation.value.id == "Tuple":
            element_type = check_typing(annotation.slice)
            return f"tuple-of-{element_type}"
        if annotation.value.id == "List":
            element_type = check_typing(annotation.slice)

            return f"list-of-{element_type}"

    if type(annotation) == ast.Name:
        if annotation.id == "int":
            return "int"
        if annotation.id == "str":
            return "str"
        if annotation.id == "float":
            return "float"
        if annotation.id == "bool":
            return "bool"
        # pass if annotation.id == Set, Dict, List, Tuple without elements like char: Set = set()


argument2type = defaultdict()

return_value_type = ""

import_library = ""
def check_node(node, node_=""):

    """
    :param node: current ast node
    :param node_: type of node
    """
    global import_library
    if isinstance(node, ast.FunctionDef):
        return_value_type = check_typing(node.returns)
        # set the tag <method> if it is a class method
        # function_method_tag = "<method>" if node_ == "class" else "<function>"

        function_arguments = []

        if len(node.args.args) > 0:

            # generate the metaphor for the concept of "function"
            story.append(generate_function_metaphor())


            story.append(
                f"This task was called '{node.name}'. The main purpose of this task was the quest of {generate_type_metaphor(return_value_type)}.")
            story.append(f"{character_pronoun('subject')} was given a magic book called {import_library} that would help {character_pronoun('object')} complete this task.")
            story.append(generate_arguments_metaphor())
            for arg_node in node.args.args:
                if arg_node.annotation:  # each arg should be annotated
                    type_ = check_typing(arg_node.annotation)
                    argument2type[arg_node.arg] = type_
                    story.append(f"{generate_type_metaphor(argument2type[arg_node.arg])} called {arg_node.arg}")
                    function_arguments.append(f"{type_}")

            # check defaults

        check_default(node.args.defaults, function_arguments)
        if has_body(node):
            # story.append("<inside-body>")
            story.append(". Within this task")

            for t in node.body:
                check_node(t, "function")
        # end of function -> return something narrative
        return "function"
    elif isinstance(node, ast.If):

        # story.append("<if-statement>")
        if_statement(node.test)

        if has_body(node):
            # story.append("<inside-body>")
            story.append(",")
            story.append(f"in this case")
            for t in node.body:
                check_node(t, "if")
        else:
            check_node(node, "if")
        if node.orelse:
            if isinstance(node.orelse[0], ast.If):
                # story.append("<elif-statement>")
                # story.append("In the case that ")

                check_node(node.orelse[0], "elif")  # elif statement
            else:
                story.append(".")
                story.append("In any other case")  # else statement
                for t in node.orelse:
                    check_node(t, "else")

        return "if"
    elif isinstance(node, ast.AnnAssign):
        # in this case, variables are annotated with their types as well
        check_annotated_variables(node)
    elif isinstance(node, ast.Assign):
        # story.append("<assignment>")
        check_variables(node)
        return "assignment"
    elif isinstance(node, ast.AugAssign):
        if type(node.target) == ast.Name:
            pseudo_code = f"{character_pronoun('subject')} enlarged '{node.target.id}' by incrementing it by"

            if type(node.op) == ast.Div:
                pseudo_code = pseudo_code.replace("<increment>", "<subtract>")
            elif type(node.op) == ast.Mult:
                pseudo_code = pseudo_code.replace("<increment>", "<multiply>")
            elif type(node.op) == ast.Add:
                pass
            elif type(node.op) == ast.Sub:
                pseudo_code = pseudo_code.replace("<increment>", "<decrement>")
            story.append(pseudo_code)

            check_type(node.value)
        return "augmented-assignment"
    # TODO list and dictionary comprehension
    elif isinstance(node, ast.For):
        # for loop

        # story.append("<for-loop>")
        story.append(introduce_for_loop())
        story.append(paraphrase_for_loop())
        story.append(f"{paraphrase_iterate()} each element defined as")

        check_type(node.target)
        story.append(f"over")
        if type(node.iter) is ast.Call:

            if type(node.iter.func) == ast.Attribute:

                attribute = node.iter.func.attr
                story.append(f"the sequence generated by the special tool '{attribute}';")

                story.append(f"<attribute> {attribute} is applied to")
                check_type(node.iter.func.value)
                if len(node.iter.args) > 0:
                    story.append(f"<attribute> with following arguments:")
                    # n = 0
                    for arg in node.iter.args:
                        # story.append(f"argument-{n + 1}")
                        # n += 1
                        check_type(arg)
            elif type(node.iter.func) == ast.Name:

                function_name = node.iter.func.id

                story.append(f"the sequence generated by the special tool '{node.iter.func.id}',")
                if len(node.iter.args) > 0:
                    story.append(f"{function_name} needed extra properties to work:")
                    # n = 0
                    for arg in node.iter.args:
                        # story.append(f"argument-{n + 1}")
                        # n += 1
                        check_type(arg)
                    story.append(".")

        else:
            check_type(node.iter)
        if has_body(node):
            # story.append("<inside-body>")
            for t in node.body:
                check_node(t, "for")
        return "for"
    elif isinstance(node, ast.Expr):
        check_type(node)
    elif isinstance(node, ast.While):
        # todo generate_metaphor()
        # story.append("<while-loop>")
        while_loop(node.test)
        if has_body(node):
            # story.append("<inside-body>")
            for t in node.body:
                check_node(t)
        else:
            check_node(node, "while")
        if node.orelse:
            if isinstance(node.orelse[0], ast.If):
                # story.append("<elif-statement>")
                # story.append("In the case that ")

                check_node(node.orelse[0], "elif")  # elif statement
            else:
                # story.append("<else-statement>")
                story.append("In any other case")  # else statement
                for t in node.orelse:
                    check_node(t, "else")
        return ("while-loop")
    elif isinstance(node, ast.With):
        pass
    elif isinstance(node, ast.Try):
        pass
    elif isinstance(node, ast.Assert):
        pass
    elif isinstance(node, ast.ClassDef):
        class_name = node.name
        story.append("<start-class>")
        story.append(f"define <class> {class_name} ,")
        if has_body(node):
            # story.append("<inside-body>")
            for t in node.body:
                check_node(t, "class")
        return f"class"
    elif isinstance(node, ast.Delete):
        if len(node.targets) > 0:

            for target in node.targets:
                pseudo_code = f"<delete>"
                story.append(pseudo_code)
                if isinstance(node.targets[0], ast.Subscript):
                    story.append(
                        f"the element at <index>: {node.targets[0].slice.value} from {node.targets[0].value.id},")
                else:
                    check_type(target)
        return "delete"
    # if isinstance(node.targets[0], ast.Name):
    #
    #     pseudo_code = f"we now <delete> the <variable> {node.targets[0].id}"
    #     story.append(pseudo_code)
    #     check_type(node.targets[0])
    # elif isinstance(node, ast.Subscript):
    #     pass
    elif isinstance(node, ast.Import):

        if len(node.names) > 0:

            for library in node.names:

                asname = f"also known as {library.asname}" if library.asname else ""
                import_library = library.name + asname
                #story.append(f" <import> the <library> {library.name} {asname}")
        return "import"
    elif isinstance(node, ast.ImportFrom):
        if len(node.names) > 0:

            for library in node.names:
                asname = f"with alias {library.asname}" if library.asname else ""

                story.append(f" <import> {library.name} {asname} from the <library> {node.module},")
        return "import"
    elif isinstance(node, ast.Global):
        pass
    elif isinstance(node, ast.While):
        pass
    elif isinstance(node, ast.For):
        pass
    elif isinstance(node, ast.With):
        pass
    elif isinstance(node, ast.Raise):
        pass
    elif isinstance(node, ast.Try):
        pass
    elif isinstance(node, ast.Assert):
        pass
    elif isinstance(node, ast.AsyncWith):
        pass
    elif isinstance(node, ast.AsyncFor):
        pass
    elif isinstance(node, ast.AsyncFunctionDef):
        pass

    elif isinstance(node, ast.Pass):
        pass
        # story.append("<pass>")
        # story.append("Here you're not supposed to do anything.")
        return "pass"
    elif isinstance(node, ast.Return):

        if node_ == "while" or node_ == "for" or node_ == "if" or node_ == "elif":
            story.append(f"Here {character_pronoun('subject')} returned with")
        elif node_ == "else":
            story.append(f" {character_pronoun('subject')} returned with")
        elif node_ == "function":
            story.append(
                f". At the end of {character_pronoun('possessive')} task, {character_name()} returned triumphant and victorious with")

        # init = ""
        returned_values = []
        if type(node.value) == ast.Call:
            function_name = node.value.func.id

            arguments = []
            if len(node.value.args) > 0:

                if paraphrase_built_in_method(function_name, node.value.args) == "":

                    story.append(f"{function_name}")
                    story.append("with following arguments:")
                    for arg in node.value.args:
                        check_type(arg)
                        arguments.append(str(arg.id))
                else:

                    story.append(paraphrase_built_in_method(node.value.func.id, node.value.args))
        if type(node.value) == ast.BinOp:
            pass
        if type(node.value) == ast.Dict:
            story.append("a <dict>")
            check_dict(node.value, "unordered mapping object")
        if type(node.value) == ast.Tuple:
            story.append("returns a immutable ordered object")
            check_tuple(node.value, "immutable ordered object")
        if type(node.value) == ast.List:
            story.append("<function> returns a list")
            check_list(node.value, "mutable ordered object")

        if type(node.value) == ast.Name:
            # init = "returns "
            # check_constant(node, "<constant>")
            returned_values.append(str(node.value.id))
        if type(node.value) == ast.Compare:
            #return value is either True of False
            # init = "returns "
            # check_constant(node, "<constant>")
            story.append(f"{generate_type_metaphor('bool')}, whose value (either True of False) derived by the truth of the following statement:")
            story.append(paraphrase_built_in_method(node.value.left.func.id, node.value.left.args))
            story.append(check_operator(node.value.ops[0]))
            comparator = node.value.comparators[0].value
            story.append(str(comparator))

        if type(node.value) == ast.Constant:
            # init = "returns "
            # check_constant(node, "<constant>")
            if node.value.value == False or node.value.value == True:
                story.append("the")
                story.append(f"{generate_type_metaphor('bool')}")
                #returned_values.append(str(node.value.value).lower())
            returned_values.append(str(node.value.value))
        if has_body(node):
            # story.append("<inside-body>")
            for t in node.body:
                check_node(t)
        returned_values = ", ".join(returned_values)
        story.append(f"'{returned_values}'")

        return "return"
    elif isinstance(node, ast.Break):
        story.append("<break>")
    elif isinstance(node, ast.Continue):
        story.append("<continue>")
        story.append("Move to the next iteration.")
    else:
        pass


def check_default(default_values, arguments):
    if len(default_values) == 0:
        return
    processed_default_values = []
    for default in default_values:
        if type(default) == ast.Constant:
            processed_default_values.append(str(default.value))
        if type(default) == ast.List:
            default_list = []
            for element in default.elts:
                default_list.append(str(element.value))
            default_list = ", ".join(default_list)
            processed_default_values.append("List with elements: " + default_list)
        if type(default) == ast.Dict:
            dict_keys = []
            default_values = []

            for key, value in zip(default.keys, default.values):
                dict_keys.append(str(key.value))
                default_values.append(str(value.value))
            dict_keys = ", ".join(dict_keys)

            default_values = ", ".join(default_values)
            processed_default_values.append(f"Dictionary with keys: {dict_keys} and values: {default_values}")
        if type(default) == ast.Tuple:
            default_tuple = []
            for element in default.elts:
                default_tuple.append(str(element.value))
            default_tuple = ", ".join(default_tuple)
            processed_default_values.append("Tuple with elements: " + default_tuple)
    if len(processed_default_values) < len(arguments):
        arguments = arguments[-len(processed_default_values):]

        arguments = ", ".join(arguments)
        processed_default_values = [f"<default-value> {str(value)}" for value in processed_default_values]
        processed_default_values = ", ".join(processed_default_values)
        story.append(
            f'{arguments} have default values: {processed_default_values}')
    if len(processed_default_values) == len(arguments):
        arguments = ", ".join(arguments)
        processed_default_values = [f"<default-value> {str(value)}" for value in processed_default_values]
        processed_default_values = ", ".join(processed_default_values)
        story.append(f'The arguments: {arguments} have default values: {processed_default_values}')


def has_body(node):
    return hasattr(node, 'body')


try:
    with open("original_code.py") as f:
        function_code = f.read()
        function_code.replace("is not", "!=")
    parsed_ast = ast.parse(function_code.replace("is not", "!="))

    #print(ast.dump(parsed_ast))


except (IndentationError, SyntaxError, TypeError, NameError, AttributeError, ValueError, KeyError, IndexError) as error:

    for exception_type in error.__class__.__bases__:
        print(f"An error of type {exception_type.__name__} occurred: {error}")

if isinstance(parsed_ast, ast.Module):
    # generate story introduction
    story.append(generate_story_introduction())
    for node in parsed_ast.body:
        node_name = check_node(node)

        # if node_name is not None:
        #     # story.append(f"<end-of-node-{node_name}>")
        #     story.append(".")
        # else:
        #     story.append(".")

new_story = []
class_in_code = None
new_line_tags = ["<end-of-node-assignment>", "<assignment>", "<start-code>", "<end-of-node-class-",
                 "<end-of-node-function-", "<end-of-node-if-", "<end-of-node-while-", "<if-statement>", "<for-loop>",
                 "<while-loop>", "else-statement", "elif-statement"]
#refactoring
for sentence in story:

    sentence = sentence.replace("  ", " ")
    sentence = sentence.strip()
    sentence = sentence.replace(",,", ",")


    if f"<function> {class_in_code}." in sentence:
        sentence = sentence.replace(f"<function> {class_in_code}.",
                                    f"create an instance of class {class_in_code}.")
    for tag in new_line_tags:
        if tag in sentence:
            sentence = sentence + "\n"
    new_story.append(sentence)

if __name__ == '__main__':
    new_story = " ".join(new_story)
    #refactoring
    new_story = new_story.replace("  ", " ").replace(" .", ".").replace(" ,", ",").replace(",.", ".").replace(",,",
                                                                                                              ",").replace(
        "..", ".").replace("the a", "the")
    new_story = new_story.replace(". the", ". The")
    with open("story", "w") as f:
        f.write(new_story)
