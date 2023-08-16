import ast
from collections import defaultdict


# handle list comprehension
# handle dictionary comprehension

# handle slicing and indexing

def check_slicing(tokens):
    if type(tokens) == ast.Subscript:
        # we are slicing the value.value.id
        # check value

        if type(tokens.value) == ast.Name:
            # indexing
            to_be_sliced = tokens.value.id

        elif type(tokens.value) == ast.Call:
            to_be_sliced = tokens.value.value.func.id
            pseudo.append(f"Of the return values of <function> {to_be_sliced} take only the")
        if type(tokens.slice) == ast.Tuple:
            # slicing
            pass
        elif type(tokens.slice) == ast.Constant:
            pseudo.append(f"the element with index:")
            # indexing
            constant = tokens.slice.value
            pseudo.append(f"{constant}")
            pseudo.append(f"from <iterable> '{to_be_sliced}',")
        elif type(tokens.slice) == ast.Name:
            pseudo.append(f"the element with index:")
            # example if parse[pos]
            constant = tokens.slice.id
            pseudo.append(f"{constant}")
            pseudo.append(f"from <iterable> '{to_be_sliced}',")
        elif type(tokens.slice) == ast.BinOp:
            pseudo.append(f"the element with index:")
            # example if parse[pos + 1]
            check_type(tokens.slice.left)
            pseudo.append(check_operator(tokens.slice.op))
            check_type(tokens.slice.right)
            pseudo.append(f"from <iterable> '{to_be_sliced}',")

        elif type(tokens.slice) == ast.Slice:

            # all three indexes [1:3:4]
            if tokens.slice.lower and tokens.slice.lower and tokens.slice.step:
                pseudo.append(f"the elements")
                starting_from_index = tokens.slice.lower.value if type(
                    tokens.slice.lower) == ast.Constant else tokens.slice.lower.id
                pseudo.append(f"from <index>: <slice-lower> {starting_from_index}")
                until_index = tokens.slice.upper.value if type(
                    tokens.slice.upper) == ast.Constant else tokens.slice.upper.id
                pseudo.append(f"until <index>: <slice-upper> {until_index}")
                jumping_index = tokens.slice.step.value
                pseudo.append(f" with step size: <slice-step> {jumping_index}")
                pseudo.append(f"in <iterable> '{to_be_sliced}',")
            # only lower index [1:]
            if tokens.slice.lower and not tokens.slice.upper and not tokens.slice.step:
                pseudo.append(f"the elements")
                starting_from_index = tokens.slice.lower.value if type(
                    tokens.slice.lower) == ast.Constant else tokens.slice.lower.id
                pseudo.append(f"from <index>: <slice-lower> {starting_from_index} until the end")
                pseudo.append(f"in <iterable> {to_be_sliced},")
            # only upper index [:3]
            if tokens.slice.upper and not tokens.slice.lower and not tokens.slice.step:

                pseudo.append(f"the elements")
                if type(tokens.slice.upper) == ast.Constant:
                    until_index = tokens.slice.upper.value
                elif type(tokens.slice.upper) == ast.Name:
                    until_index = tokens.slice.upper.id
                elif type(tokens.slice.upper) == ast.Call:
                    until_index = f"the return value of <function> {tokens.slice.upper.func.id} with arguments {tokens.slice.upper.args[0].id}"
                # until_index = tokens.slice.upper.value if type(tokens.slice.upper) == ast.Constant else tokens.slice.upper.id
                pseudo.append(f"from <index>: 0 until the <index>: <slice-upper> {until_index}")
                pseudo.append(f"in <iterable> {to_be_sliced},")
            # only step size [1:3]
            if tokens.slice.lower and tokens.slice.upper and not tokens.slice.step:
                pseudo.append(f"the elements")
                starting_from_index = tokens.slice.lower.value if type(
                    tokens.slice.lower) == ast.Constant else tokens.slice.lower.id
                pseudo.append(f"from <index>: <slice-lower> {starting_from_index}")
                if type(tokens.slice.upper) == ast.Constant:
                    until_index = tokens.slice.upper.value
                elif type(tokens.slice.upper) == ast.Name:
                    until_index = tokens.slice.upper.id
                elif type(tokens.slice.upper) == ast.Call:
                    until_index = f"the return value of <function> {tokens.slice.upper.value.func.id} with arguments {tokens.slice.upper.value.args[0].id}"

                pseudo.append(f"until <index>: <slice-upper> {until_index}")
                pseudo.append(f"in <iterable> {to_be_sliced},")
            if not tokens.slice.lower and not tokens.slice.upper and not tokens.slice.step:
                pseudo.append(f"all elements in <iterable> {to_be_sliced},")


# pos += lista[pos]

pseudo = []
variables_types = defaultdict()


def checkBinOp(value_s, variable_name=None):
    if type(value_s) == ast.BinOp:
        pseudo.append("a <expression>")


def process_dict_comp(value_s):
    # generator = for x in numbers
    # please notice I make pseudocode only for one generator
    generation = value_s.generators[0]
    target = generation.target.id
    if isinstance(generation.iter, ast.Tuple):
        pseudo.append(f"To <create> <dict> <iterate> each <list-element> {target} over <iterable> <tuple>")
        check_tuple(generation.iter, "<tuple>")
    elif isinstance(generation.iter, ast.List):
        pseudo.append(f"To <create> <dict> <iterate> each <list-element> {target} over <iterable> <list>")
        check_list(generation.iter, "<list>")
    elif isinstance(generation.iter, ast.Name):
        pseudo.append(f"To <create> <dict> <iterate> each <list-element> {target} over <iterable> ")
        pseudo.append(generation.id)

    if isinstance(value_s.key, ast.Name):
        key = value_s.key.id
        pseudo.append(f"the <keys> of the <dict> are {key}")
    elif isinstance(value_s.key, ast.Constant):
        key = value_s.key.value
        pseudo.append(f"the <keys> of the <dict> are {key}")
    elif isinstance(value_s.key, ast.Tuple):
        pseudo.append("the <keys> of the <dict> are <tuples>")
        check_tuple(value_s.key, "<tuple>")
    elif isinstance(value_s.key, ast.List):
        pseudo.append("the <values> of the <dict> are <lists>")
        check_list(value_s.key, "<list>")
    elif isinstance(value_s.key, ast.BinOp):
        pseudo.append("To create the <keys> of the <dict> apply the following <operation>:")
        check_type(value_s.key.left)
        pseudo.append(check_operator(value_s.key.op))
        check_type(value_s.key.right)

    if isinstance(value_s.value, ast.Name):
        value = value_s.value.id
        pseudo.append(f"the <values> of the <dict> are {value}")
    elif isinstance(value_s.value, ast.Constant):

        value = value_s.value.value
        pseudo.append(f"the <values> of the <dict> are {value}")
    elif isinstance(value_s.value, ast.Tuple):
        pseudo.append("the <values> of the <dict> are <tuples>")
        check_tuple(value_s.value, "<tuple>")
    elif isinstance(value_s.value, ast.List):
        pseudo.append("the <values> of the <dict> are <lists>")
        check_list(value_s.key, "<list>")
    elif isinstance(value_s.value, ast.BinOp):
        pseudo.append("To create the <values> of the <dict> apply the following <operation>:")
        check_type(value_s.value.left)
        pseudo.append(check_operator(value_s.value.op))
        check_type(value_s.value.right)


def process_list_comp(variable_name, value_s):
    # generator = for x in numbers
    generation = value_s.generators[0]

    target = generation.target.id

    if isinstance(generation.iter, ast.Tuple):
        iterable = "<tuple>"
        check_tuple(generation.iter, iterable)
    elif isinstance(generation.iter, ast.List):
        iterable = "<list>"
        check_list(generation.iter, iterable)
    elif isinstance(generation.iter, ast.Name):
        iterable = generation.iter.id
    pseudo.append(
        f" To <create> {variable_name} <iterate> over <iterable> {iterable}, take each <list-element> as {target} from {iterable}.")
    if isinstance(value_s.elt, ast.BinOp):
        # example [x + 1 for x in numbers] or [x**2 for x in numbers]
        operator = check_operator(value_s.elt.op)
        left = value_s.elt.left.id
        right = value_s.elt.right.value
        pseudo.append(f"for each {left} in <iterable> apply this <operation>:  {left} {operator} {right}")

    if len(generation.ifs) > 0:
        if len(generation.ifs) == 1:
            pseudo.append("if the following condition is met:")
            pseudo.append("<if-statement>")
            for token in generation.ifs:
                if_statement(token)
        else:
            pseudo.append(f"if the following {len(generation.ifs)} conditions are met:")
            pseudo.append("<if-statement>")
            for token in generation.ifs:
                if_statement(token)
    else:
        pseudo.append(".")


def check_tag(pseudo, name):
    pseudo = " ".join(pseudo)
    pseudo = pseudo.split()
    if name in pseudo:

        if name == "<class>" or name == "<function>":
            name_index = pseudo.index(name)
            tag = pseudo[name_index - 1: name_index][0]
            return tag
        else:
            return "<function>"
    else:
        return "<class>"


def check_type(value_s, variable_name=None):  # 1, object
    if type(value_s) == ast.UnaryOp:
        if type(value_s.op) == ast.USub:
            pseudo.append(f"'- {value_s.operand.value}'")
    if type(value_s) == ast.DictComp:
        pseudo.append(f"{variable_name} is a <dict-comprehension>.")
        process_dict_comp(value_s)
        pass
    elif type(value_s) == ast.ListComp:
        pseudo.append(f"{variable_name} is a <list-comprehension>.")
        process_list_comp(variable_name, value_s)
        pass
    elif type(value_s) == ast.Attribute:
        to_applied_on = value_s.value.id
        applied_method = value_s.attr
        pseudo.append(f"<method> {applied_method} is applied on <variable> {to_applied_on}")
    elif type(value_s) == ast.Subscript:
        check_slicing(value_s)
    elif type(value_s) == ast.Expr:
        if type(value_s.value) == ast.Call:
            if type(value_s.value.func) == ast.Attribute:
                attribute_name = value_s.value.func.attr
                to_be_applied_on = value_s.value.func.value.id
                pseudo.append(f"apply the <method> '{attribute_name}' on '{to_be_applied_on}'")
                if len(value_s.value.args) > 0:
                    pseudo.append(f"with the following <arguments>:")
                    n = 0
                    for arg in value_s.value.args:
                        pseudo.append(f"argument-{n + 1}")
                        n += 1
                        check_type(arg)
            else:
                pseudo.append(f"call the <function> {value_s.value.func.id}.")
                if len(value_s.value.args) > 0:
                    pseudo.append(f"with the following <arguments>:")
                    n = 0
                    for arg in value_s.value.args:
                        pseudo.append(f"argument-{n + 1}")
                        n += 1
                        check_type(arg)


        else:
            check_type(value_s.value)
    elif type(value_s) == ast.BinOp:

        left = value_s.left
        right = value_s.right
        operator = value_s.op
        check_type(left)
        operator = check_operator(operator)
        pseudo.append(operator)
        check_type(right)
    elif type(value_s) == ast.Sub:
        pseudo.append("<subtract>")
    elif type(value_s) == ast.Add:
        pseudo.append("<add>")
    elif type(value_s) == ast.Mult:
        pseudo.append("<multiply>")
    elif type(value_s) == ast.Div:
        pseudo.append("<divide>")
    elif type(value_s) == ast.Call:

        if type(value_s.func) == ast.Attribute:
            attribute = value_s.func.attr

            pseudo.append(f"<attribute> {attribute} is applied to")
            check_type(value_s.func.value)
            if len(value_s.args) > 0:
                pseudo.append(f"give <attribute> {attribute} following arguments:")
                n = 0
                for arg in value_s.args:
                    pseudo.append(f"argument-{n + 1}")
                    n += 1
                    check_type(arg)
        elif type(value_s.func) == ast.Name:
            # check whether its a class or a function tag
            class_tag = check_tag(pseudo, value_s.func.id)
            if variable_name is not None:
                pseudo.append(
                    f"a new instance of {class_tag} {value_s.func.id} is being created and assigned to {variable_name},")
                if len(value_s.args) > 0:
                    pseudo.append(f"give {class_tag} following arguments:")
                    n = 0
                    for arg in value_s.args:
                        pseudo.append(f"argument-{n + 1}")
                        n += 1
                        check_type(arg)
                    pseudo.append(".")
            else:
                if value_s.func.id:
                    pseudo.append(f"<function> {value_s.func.id}")
                if len(value_s.args) > 0:
                    pseudo.append(f" call <function> with following arguments:")
                    n = 0
                    for arg in value_s.args:
                        pseudo.append(f"argument-{n + 1}")
                        n += 1
                        check_type(arg)
                else:
                    pseudo.append("<function>")
                    if len(value_s.args) > 0:
                        pseudo.append(f"call <function> with following arguments:")
                        n = 0
                        for arg in value_s.args:
                            pseudo.append(f"argument-{n + 1}")
                            n += 1
                            check_type(arg)

        else:
            class_tag = check_tag(pseudo, value_s.func.id)
            # example a = funct()
            if variable_name is not None:
                pseudo.append(
                    f"a new instance of {class_tag} '{value_s.func.id}' is being created and assigned to <variable> '{variable_name}'")
                pseudo.append(f"give '{value_s.func.id}' following arguments:")
                if len(value_s.args) > 0:
                    n = 0
                    for arg in value_s.args:
                        pseudo.append(f"argument-{n + 1}")
                        n += 1
                        check_type(arg)
            else:
                if value_s.func.id:
                    pseudo.append(f" <function> '{value_s.func.id}'")
                if len(value_s.args) > 0:
                    pseudo.append(f" give '{value_s.func.id}' with following arguments:")
                    n = 0
                    for arg in value_s.args:
                        pseudo.append(f"argument-{n + 1}")
                        n += 1
                        check_type(arg)
                else:
                    pseudo.append("<function>")
                    if len(value_s.args) > 0:
                        pseudo.append(f" call <function> with following arguments:")
                        n = 0
                        for arg in value_s.args:
                            pseudo.append(f"argument-{n + 1}")
                            n += 1
                            check_type(arg)
    elif type(value_s) == ast.List:
        if variable_name is not None:
            variables_types[variable_name] = "<list>"
            pseudo.append(f"{variable_name} <is-defined-as> <list>.")
        else:
            pseudo.append("a <list>")
        check_list(value_s, "<list>")

    elif type(value_s) == ast.Dict:
        if variable_name is not None:
            variables_types[variable_name] = "<dict>"
            pseudo.append(f"{variable_name} <is-defined-as> <dict>.")
        else:
            pseudo.append("a <dict>")
        check_dict(value_s, "<dict>")

    elif type(value_s) == ast.Tuple:
        if variable_name:
            variables_types[variable_name] = "<tuple>"
            pseudo.append(f"{variable_name} <is-defined-as> <tuple>.")
        else:
            pseudo.append("a <tuple>")
        check_tuple(value_s, "<tuple>")

    elif type(value_s) == ast.Constant:

        constant_type = value_s.value
        new_type = type(constant_type).__name__
        if variable_name is not None:
            variables_types[variable_name] = f"<{new_type}>"
            pseudo.append(f"{variable_name} <is-defined-as> <{new_type}>:")
        check_constant(value_s, f"<{new_type}>")
    elif type(value_s) == ast.Name:
        if value_s.id in variables_types:
            pseudo.append(f"the {variables_types[value_s.id]} {value_s.id}")
        else:
            pseudo.append(f"<variable> '{value_s.id}'")


def check_list(token, tag):
    # we are now entering a list

    if len(token.elts) > 0:
        pseudo.append(f"The {tag} contains following elements:")
        for element in token.elts:
            check_type(element)
    else:
        pseudo.append(f"This is an <empty> {tag}.")


def check_dict(token, tag):
    if len(token.keys) > 0:
        pseudo.append(f"The {tag} contains following key and value pairs:")
        for key, value in zip(token.keys, token.values):
            pseudo.append("<key>")
            check_type(key, key.value)
            pseudo.append("<value>")
            check_type(value, value.value)
    else:
        pseudo.append(f"This is an <empty> {tag}.")


def check_tuple(token, tag):
    if len(token.elts) > 0:
        pseudo.append(f"The {tag} contains following elements:")
        for element in token.elts:
            if type(element) == ast.Constant:

                check_type(element, element.value)
            elif type(element) == ast.Name:

                check_type(element, element.id)
            elif type(element) == ast.BinOp:
                check_type(element)


    else:
        pseudo.append(f"This is an <empty> {tag}.")


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

            pseudo.append(f"{tag} {value}")
        else:
            pseudo.append(f"This is an empty {tag}")
    else:
        pseudo.append(f"{tag} {value}")


# check types of arguments and variables in order to find some appropriate metaphors for them.
def check_typing(annotation):
    if type(annotation) == ast.Subscript:
        if annotation.value.id == "Dict":
            key_value = []
            for elt in annotation.slice.elts:
                key_value.append(check_typing(elt))
            key_value = "-".join(key_value)
            return f"dictionary of {key_value}s"
        if annotation.value.id == "Set":
            element_type = check_typing(annotation.slice)
            return f"set of {element_type}s"

        if annotation.value.id == "Tuple":
            element_type = check_typing(annotation.slice)
            return f"tuple of {element_type}s"
        if annotation.value.id == "List":
            element_type = check_typing(annotation.slice)

            return f"list of {element_type}s"

    if type(annotation) == ast.Name:
        if annotation.id == "int":
            return "integer"
        if annotation.id == "str":
            return "string"
        if annotation.id == "float":
            return "float"
        if annotation.id == "bool":
            return "boolean"
        # pass if annotation.id == Set, Dict, List, Tuple without elements like char: Set = set()
    else:
        return


variable2type = defaultdict()


def check_ann_variables(tokens):
    variable_type = check_typing(tokens.annotation)

    if type(tokens.target) == ast.Attribute:  # only in classes self.
        if tokens.target.value.id == "self":
            pseudo.append(f"set <self-attribute> {tokens.target.attr} to")
            check_type(tokens.value, tokens.value.id)
            # story.append(f"to the value <class-attribute> {tokens.value.id}")

    if type(tokens.target) == ast.Name:  # char: List[int] = Lista[:0], p: int = 0
        variable2type[tokens.target.id] = variable_type

        # when variable is a tuple, list, dict, num, string, boolean, None

        pseudo.append(
            f"called {tokens.target.id}:")

        check_type(tokens.value, tokens.target.id)
    if type(tokens.target) == ast.Subscript:  # Lista[0]: int = 3
        # handled in check_variable
        pass


def check_variables(tokens):
    # tokens.targets is a list
    for target in tokens.targets:

        if type(target) == ast.Attribute:
            if target.value.id == "self":
                pseudo.append(f"set <self-attribute> {target.attr} to")
                check_type(tokens.value, tokens.value.id)
                # story.append(f"to the value <class-attribute> {tokens.value.id}")
        if type(target) == ast.Tuple:
            # when you define more than one variable at the same time
            if type(tokens.value) == ast.Call:
                variables_to_be_defined = " and ".join(
                    [f" <variable> {str(target.id)}" for target in tokens.targets[0].elts])
                variables_to_be_defined_ = ", ".join(
                    [f" <variable> {str(target.id)}" for target in tokens.targets[0].elts])
                pseudo.append(
                    f"set {variables_to_be_defined}.")
                check_type(tokens.value, variables_to_be_defined_)
            else:
                variables_to_be_defined = "and ".join(
                    [f" <variable> {str(target.id)}" for target in tokens.targets[0].elts])
                pseudo.append(
                    f"set {variables_to_be_defined} respectively to the values:")

                for target, value in zip(target.elts, tokens.value.elts):
                    check_type(value, str(target.id))  # variable_name, value

        if type(target) == ast.Name:

            # when variable is a tuple, list, dict, num, string, boolean, None
            if f"set <variable> {target.id}." not in pseudo:
                pseudo.append(f"set <assigned-variable> {target.id}.")
            else:
                pseudo.append(f"change the value of <variable> {target.id}:")

            check_slicing(tokens.value)

            check_type(tokens.value, target.id)
        if type(target) == ast.Subscript:
            if type(target.value) == ast.Name:
                iterable = target.value.id
                pseudo.append(f"set")
                check_slicing(target)
                pseudo.append(f"equal to")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.id)
            elif type(target.value) == ast.Attribute:
                pseudo.append(f"set the <self-attribute>.{target.value.attr}.")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.attr)

            elif type(target.value) == ast.Subscript:
                pseudo.append(f"set <variable> {target.value.value.id}.")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.value.id)

            elif type(target.value) == ast.Call:
                pseudo.append(f"set <variable> {target.value.func.id}.")
                check_slicing(tokens.value)
                check_type(tokens.value, target.value.func.id)


def check_operator(operator):
    if isinstance(operator, ast.Mod):
        return "<modulo>"
    if isinstance(operator, ast.Eq):
        return "<is-equal-to>"

    elif isinstance(operator, ast.NotEq):
        return "<is-not-equal-to>"

    elif isinstance(operator, ast.Lt):
        return "<is-less-than>"

    elif isinstance(operator, ast.LtE):
        return "<less-or-equal>"

    elif isinstance(operator, ast.Gt):
        return "<greater-than>"

    elif isinstance(operator, ast.GtE):
        return "<greater-or-equal>"

    elif isinstance(operator, ast.Is):
        return "<is>"

    elif isinstance(operator, ast.IsNot):
        return "<is-not>"

    elif isinstance(operator, ast.In):
        return "<is-in>"

    elif isinstance(operator, ast.NotIn):
        return "<is-not-in>"
    elif isinstance(operator, ast.Or):
        return "<or>"
    elif isinstance(operator, ast.And):
        return "<and>"
    elif isinstance(operator, ast.Not):
        return "<not>"
    elif isinstance(operator, ast.Invert):
        return "<invert>"
    elif isinstance(operator, ast.Pow):
        return "<at-the-power-of>"
    elif isinstance(operator, ast.Mult):
        return "<times>"
    elif isinstance(operator, ast.Div):
        return "<divided-by>"
    elif isinstance(operator, ast.Add):
        return "<plus>"
    elif isinstance(operator, ast.Sub):
        return "<minus>"
    elif isinstance(operator, ast.FloorDiv):
        return "<floor-divided-by>"
    else:
        raise Exception("Operator not supported")


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
                pseudo.append(operator)
            else:
                if_statement(value, while_=True)

    if isinstance(token, ast.Name):
        # example if list:
        check_type(token)
        pseudo.append("exists")
    if isinstance(token, ast.Compare):
        left = token.left
        right = token.comparators[0]

        pseudo.append("as long as")
        pseudo.append("<while-left>")
        check_type(left)
        # check_slicing(left)

        operator = check_operator(token.ops[0])
        pseudo.append(operator)
        pseudo.append("<while-right>")

        check_type(right)
        # check_slicing(right)


def if_statement(token, add_operator=False, while_=False):
    tag_left = "<while-left>" if while_ else "<if-left>"
    tag_right = "<while-right>" if while_ else "<if-right>"
    if isinstance(token, ast.BoolOp):
        operator = check_operator(token.op)

        # add_operator = check_condition_pos(node.values)
        for index, value in enumerate(token.values):
            if index < len(token.values) - 1:
                # element if not at last position
                if_statement(value, add_operator)
                pseudo.append(operator)
            else:
                if_statement(value)

    if isinstance(token, ast.Name):
        # example if list:
        check_type(token)
        pseudo.append("exists")
    if isinstance(token, ast.Compare):
        left = token.left
        right = token.comparators[0]

        pseudo.append(f"{tag_left}")
        check_type(left)
        # check_slicing(left)

        operator = check_operator(token.ops[0])
        pseudo.append(operator)
        pseudo.append(f"{tag_right}")

        check_type(right)
        # check_slicing(right)


argument2type = defaultdict()


def check_token(token, class_=False):
    if isinstance(token, ast.FunctionDef):
        # set the tag <method> if it is a class method
        function_method_tag = "<method>" if class_ else "<function>"
        function_arguments_ = ""
        function_arguments = []
        pseudo.append(f'write {function_method_tag} {token.name}')
        if len(token.args.args) > 0:
            pseudo.append('with following arguments:')
            for arg_node in token.args.args:
                if arg_node.annotation:  # each arg should be annotated
                    type_ = check_typing(arg_node.annotation)
                    argument2type[arg_node.arg] = type_
                    pseudo.append(f"'{arg_node.arg}' as a {type_}")
                    function_arguments.append(f"{type_}")

            # check defaults
            pseudo.append(f' {function_arguments_}')
        check_default(token.args.defaults, function_arguments)
        if has_body(token):
            pseudo.append("<inside-body>")
            for t in token.body:
                check_token(t)
        return "function"
    elif isinstance(token, ast.If):
        pseudo.append("<if-statement>")
        if_statement(token.test)

        if has_body(token):
            pseudo.append("<inside-body>")
            for t in token.body:
                check_token(t)
        else:
            check_token(token)
        if token.orelse:
            if isinstance(token.orelse[0], ast.If):
                pseudo.append("<elif-statement>")
                pseudo.append("In the case that ")

                check_token(token.orelse[0])  # elif statement
            else:
                pseudo.append("<else-statement>")
                pseudo.append("In any other case")  # else statement
                for t in token.orelse:
                    check_token(t)

        return "if"
    elif isinstance(token, ast.Assign):
        pseudo.append("<assignment>")
        check_variables(token)
        return "assignment"
    elif isinstance(token, ast.AnnAssign):
        # in this case, variables are annotated with their types as well
        check_ann_variables(token)
    elif isinstance(token, ast.AugAssign):
        if type(token.target) == ast.Name:
            pseudo_code = f"we now <increment> <variable> {token.target.id} by"

            if type(token.op) == ast.Div:
                pseudo_code = pseudo_code.replace("<increment>", "<subtract>")
            elif type(token.op) == ast.Mult:
                pseudo_code = pseudo_code.replace("<increment>", "<multiply>")
            elif type(token.op) == ast.Add:
                pass
            elif type(token.op) == ast.Sub:
                pseudo_code = pseudo_code.replace("<increment>", "<decrement>")
            pseudo.append(pseudo_code)

            check_type(token.value)
        return "augmented-assignment"
    # TODO list and dictionary comprehension
    elif isinstance(token, ast.For):
        # for loop
        pseudo.append("<for-loop>")

        if type(token.target) == ast.Tuple:
            pseudo.append(f"iterate: for each")
            iterating_elements = []
            for element in token.target.elts:
                iterating_elements.append(element.id)
            pseudo.append(", ".join(iterating_elements))
        else:
            pseudo.append(f"iterate: for each element defined as")
            check_type(token.target)
        pseudo.append(f"over")
        if type(token.iter) is ast.Call:

            if type(token.iter.func) == ast.Attribute:

                attribute = token.iter.func.attr
                pseudo.append(f"the sequence generated by <attribute> {attribute};")

                pseudo.append(f"<attribute> {attribute} is applied to")
                check_type(token.iter.func.value)
                if len(token.iter.args) > 0:
                    pseudo.append(f", give {attribute} following arguments:")
                    n = 0
                    for arg in token.iter.args:
                        pseudo.append(f"argument-{n + 1}")
                        # pseudo.append(",")
                        n += 1
                        check_type(arg)
            elif type(token.iter.func) == ast.Name:

                function_name = token.iter.func.id
                pseudo.append(f"the sequence generated by <function> '{token.iter.func.id}',")
                if len(token.iter.args) > 0:
                    pseudo.append(f"give '{token.iter.func.id}' following arguments:")
                    n = 0
                    for arg in token.iter.args:
                        pseudo.append(f"argument-{n + 1}")

                        n += 1
                        check_type(arg)
                        # pseudo.append(",")
                    pseudo.append(".")

        else:
            check_type(token.iter)
        if has_body(token):
            pseudo.append("<inside-body>")
            for t in token.body:
                check_token(t)
        return "for"
    elif isinstance(token, ast.Expr):
        check_type(token)
    elif isinstance(token, ast.While):
        pseudo.append("<while-loop>")
        while_loop(token.test)
        if has_body(token):
            pseudo.append("<inside-body>")
            for t in token.body:
                check_token(t)
        else:
            check_token(token)
        if token.orelse:
            if isinstance(token.orelse[0], ast.If):
                pseudo.append("<elif-statement>")
                pseudo.append("In the case that ")

                check_token(token.orelse[0])  # elif statement
            else:
                pseudo.append("<else-statement>")
                pseudo.append("In any other case")  # else statement
                for t in token.orelse:
                    check_token(t)
        return ("while-loop")
    elif isinstance(token, ast.With):
        pass
    elif isinstance(token, ast.Try):
        pass
    elif isinstance(token, ast.Assert):
        pass
    elif isinstance(token, ast.ClassDef):
        class_name = token.name
        pseudo.append("<start-class>")
        pseudo.append(f"define <class> {class_name} ,")
        if has_body(token):
            pseudo.append("<inside-body>")
            for t in token.body:
                check_token(t, True)
        return f"class"
    elif isinstance(token, ast.Delete):
        if len(token.targets) > 0:

            for target in token.targets:
                pseudo_code = f"<delete>"
                pseudo.append(pseudo_code)
                if isinstance(token.targets[0], ast.Subscript):
                    pseudo.append(
                        f"the element at <index>: {token.targets[0].slice.value} from {token.targets[0].value.id},")
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
    elif isinstance(token, ast.Import):
        if len(token.names) > 0:

            for library in token.names:
                asname = f"with alias {library.asname}" if library.asname else ""

                pseudo.append(f" <import> the <library> {library.name} {asname}")
        return "import"
    elif isinstance(token, ast.ImportFrom):
        if len(token.names) > 0:

            for library in token.names:
                asname = f"with alias {library.asname}" if library.asname else ""

                pseudo.append(f" <import> <class> {library.name} {asname} from the <library> {token.module},")
        return "import"
    elif isinstance(token, ast.Global):
        pass
    elif isinstance(token, ast.While):
        pass
    elif isinstance(token, ast.With):
        pass
    elif isinstance(token, ast.Raise):
        pass
    elif isinstance(token, ast.Try):
        pass
    elif isinstance(token, ast.Assert):
        pass
    elif isinstance(token, ast.AsyncWith):
        pass
    elif isinstance(token, ast.AsyncFor):
        pass
    elif isinstance(token, ast.AsyncFunctionDef):
        pass

    elif isinstance(token, ast.Pass):
        pseudo.append("<pass>")
        pseudo.append("Here you're not supposed to do anything.")
        return "pass"
    elif isinstance(token, ast.Return):

        init = ""
        returned_values = []
        if type(token.value) == ast.Call:
            pass
        if type(token.value) == ast.BinOp:
            pass
        if type(token.value) == ast.Dict:
            pseudo.append("<function> returns a <dict>")
            check_dict(token.value, "<dict>")
        if type(token.value) == ast.Tuple:
            pseudo.append("<function> returns a <tuple>")
            check_tuple(token.value, "<tuple>")
        if type(token.value) == ast.List:
            pseudo.append("<function> returns a list")
            check_list(token.value, "<list>")

        if type(token.value) == ast.Name:
            init = "<function> returns "
            # check_constant(node, "<constant>")
            returned_values.append(str(token.value.id))
        if type(token.value) == ast.Constant:
            init = "<function> returns "
            # check_constant(node, "<constant>")

            returned_values.append(str(token.value.value))
        if has_body(token):
            pseudo.append("<inside-body>")
            for t in token.body:
                check_token(t)
        returned_values = ", ".join(returned_values)
        pseudo.append(f"{init}{returned_values}")
        return "return"
    elif isinstance(token, ast.Break):

        pseudo.append("<break>")
    elif isinstance(token, ast.Continue):
        pseudo.append("<continue>")
        pseudo.append("Move to the next iteration.")
    else:
        pass


def check_default(default_values, arguments):
    if len(default_values) > 0:
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
            arguments = arguments[len(processed_default_values):]

            arguments = ", ".join(arguments)
            processed_default_values = [f"<default-value> {str(value)}" for value in processed_default_values]
            processed_default_values = ", ".join(processed_default_values)
            pseudo.append(
                f'{arguments} have default values: {processed_default_values}')
        if len(processed_default_values) == len(arguments):
            arguments = ", ".join(arguments)
            processed_default_values = [f"<default-value> {str(value)}" for value in processed_default_values]
            processed_default_values = ", ".join(processed_default_values)
            pseudo.append(f'The arguments: {arguments} have default values: {processed_default_values}')

    else:
        return


def has_body(node):
    if hasattr(node, 'body'):
        # print(ast.dump((node.body[0])))

        return True
    # elif hasattr(node, 'children'):
    #     for child in node.children:
    #         if has_body(child):
    #             return True
    return False


function_code = """
def isValid( s: str) -> bool:
    stack = []
    parenthesis = {")": "(", "]": "[", "}": "{"}
    for char in s:
        if char in "({[":

            stack.append(char)

        elif char in ")}]":
            # if not
            if not stack or stack[-1] != parenthesis[char]:
                return False
            stack.pop()

    return len(stack) == 0

"""
try:
    parsed_ast = ast.parse(function_code.replace("is not", "!="))

    # print AST tree
    # print(ast.dump(parsed_ast))

#in case the code cannot be processed by AST due to syntactic, indentation errors.
except (IndentationError, SyntaxError, TypeError, NameError, AttributeError, ValueError, KeyError, IndexError) as error:

    for exception_type in error.__class__.__bases__:
        print(f"An error of type {exception_type.__name__} occurred: {error}")

if isinstance(parsed_ast, ast.Module):
    pseudo.append("<start-code>")
    for node in parsed_ast.body:

        node_name = check_token(node)

        if node_name is not None:
            pseudo.append(f"<end-of-node-{node_name}>")
        else:
            pseudo.append(f"<end-of-node>")

new_pseudo = []
class_in_code = None
new_line_tags = ["<end-of-node-assignment>", "<assignment>", "<start-code>", "<end-of-node-class-",
                 "<end-of-node-function-", "<end-of-node-if-", "<end-of-node-while-", "<if-statement>", "<for-loop>",
                 "<while-loop>", "else-statement", "elif-statement"]
for sentence in pseudo:
    sentence = sentence.replace("  ", " ")
    sentence = sentence.strip()
    sentence = sentence.replace(",,", ",")

    if f"call <function> {class_in_code}." in sentence:
        sentence = sentence.replace(f"call <function> {class_in_code}.",
                                    f"create an instance of class {class_in_code}.")
    for tag in new_line_tags:
        if tag in sentence:
            sentence = sentence + "\n"
    new_pseudo.append(sentence)

with open("pseudo_before", "w") as file:
    file.write("".join(new_pseudo))
