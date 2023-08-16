import pandas as pd
import random
from collections import defaultdict
import math

df_introduction = pd.read_excel("docs/metaphors.xlsx", 'introduction')
df_function = pd.read_excel("docs/metaphors.xlsx", "functions")
df_for = pd.read_excel("docs/metaphors.xlsx", "for")
# def find_synonyms(word):
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())
#     return list(synonyms)


settings = df_introduction['SETTINGS'].dropna().str.lower().tolist()
adjectives = df_introduction['ADJECTIVES'].dropna().str.lower().tolist()
narrators = df_introduction['NARRATORS'].dropna().str.lower().tolist()
character_data = df_introduction["CHARACTERS"].dropna().tolist()
character_names = [item.split(',')[0].strip() for item in character_data]
character_descriptions = [item.split(',')[1].strip().lower() for item in character_data]
character_gender = [item.split(',')[2].strip().lower() for item in character_data]

time_settings = df_introduction['PERIOD'].dropna().tolist()
action = df_introduction['ACTION'].dropna().tolist()
# pick random story items
random_time_setting = random.choice(time_settings)
random_setting = random.choice(settings)

random_adjective = random.choice(adjectives)
random_narrator = random.choice(narrators)
random_character = random.choice(character_names)
random_character_description = character_descriptions[character_names.index(random_character)]

# I need the character profession in order to find an appropriate allegory for functions in the context where the protagonist lives.
character_profession = character_data[character_names.index(random_character)].split(",")[3]
function_metaphors = df_function[character_profession.strip()].dropna().tolist()
random_function_metaphor = random.choice(function_metaphors)
# accomplish = random.choice(
# find_synonyms("fulfill") + ["undertake", "accomplish", "carry out", "fulfill", "execute", "perform", "achieve",
#            "complete", "realize", "conduct", "finish", "effectuate"])
random_character_adjectives = df_introduction["CHARACTER ADJECTIVES"].dropna().str.lower().tolist()
random_for_loop_metaphors = df_for["metaphors"].dropna().str.lower().tolist()
random_iterate_synonyms = df_for["iterate"].dropna().str.lower().tolist()
character_pronouns = defaultdict()
if character_gender[character_names.index(random_character)] == "woman":
    character_pronouns["subject"] = "she"
    character_pronouns["object"] = "her"
    character_pronouns["possessive"] = "her"
elif character_gender[character_names.index(random_character)] == "man":
    character_pronouns["subject"] = "he"
    character_pronouns["object"] = "him"
    character_pronouns["possessive"] = "his"


def setting():
    return random_setting


def character_name():
    return random_character


def character_pronoun(pronoun):
    return character_pronouns[pronoun]


def character_with_adjective():
    return f"{random.choice(random_character_adjectives)} {random_character.split()[0]}"


def generate_story_introduction():  # generate story introduction
    # 1. pick random story items
    return f"{random_time_setting}, {random_setting} {random_adjective} {random_narrator} wanted to tell a story about {random_character_description}, {random_character}."


def generate_function_metaphor():
    return f"The {character_with_adjective()} had to {random_function_metaphor}. "


def paraphrase_for_loop():
    return f"Like {random.choice(random_for_loop_metaphors)}"


def introduce_for_loop():
    return f"All of a sudden, {character_pronouns['subject']} found {character_pronouns['object']}self in a situation where {character_pronouns['subject']} had to compute something repeatedly."


def paraphrase_iterate():
    return f"{random.choice(random_iterate_synonyms)}"


def generate_arguments_metaphor():
    return f"The tools {character_pronouns['subject']} needed in order to begin included"


def generate_type_metaphor(variable):
    df_types = pd.read_excel("docs/metaphors.xlsx", 'types')
    if variable != "":
        if variable == "mutuable ordered object":
            variable = "<list>"

        type_metaphors = df_types[variable].dropna().str.lower().tolist()
        return random.choice(type_metaphors)


def isnan(value):
    try:

        return math.isnan(float(value))
    except:
        return False


def paraphrase_built_in_method(built_in, ast_arguments, class_=None):
    arguments = []
    for arg in ast_arguments:
        try:
            arguments.append(str(arg.id))
        except:
            arguments.append(str(arg.func.id))
    df_types = pd.read_excel("docs/metaphors.xlsx", 'built_in')
    if built_in in df_types["method"].values:
        # save the index of the method
        index = df_types.index[df_types["method"] == built_in].item()

        paraphrase = df_types.at[index, "paraphrase"]
        if class_ is not None:
            if not isnan(paraphrase):
                paraphrase = paraphrase.replace('{element}', class_)
                if len(arguments) > 0:
                    arguments = " ".join(arguments)
                    return f"{paraphrase} {arguments}"
                else:
                    return ""
            else:
                return ""
        else:
            if not isnan(paraphrase):
                if len(arguments) > 0:
                    arguments = " ".join(arguments)
                    return f"{paraphrase} {arguments}"
                else:
                    return ""
            else:
                return ""
    else:
        return ""
