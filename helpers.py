import copy
import random
import sys
import io

output = io.StringIO()


def create_single_card(existing_cards: dict) -> tuple:
    """Creates a single flashcard via user input."""
    card_term = input('What should the card prompt be?\n')
    output.write('The card:\n' + '\n')
    output.write(card_term + '\n')
    validated_term = validate_flashcard('term', card_term, existing_cards)
    card_definition = input(f"What's the answer to this card prompt?\n")
    output.write("The definition of the card:\n" + '\n')
    output.write(card_definition + '\n')
    validated_definition = validate_flashcard('definition', card_definition, existing_cards)
    return validated_term, validated_definition


def validate_flashcard(term_or_def: str, value_to_check: str, existing_cards: dict) -> str:
    """
    Ensures that <term_or_def> (term or definition) doesn't already exist in <existing_cards>.
    If not, prompts the user to replace the offending value.
    """

    if term_or_def == 'term':
        previous_parts = list(existing_cards.keys())
    else:
        previous_parts = list(existing_cards.values())

    while True:
        if value_to_check in previous_parts:
            already_exists_message = f'This {term_or_def} already exists. Try again:\n'
            value_to_check = input(already_exists_message)
            output.write(already_exists_message + '\n')
            output.write(value_to_check + '\n')
        else:
            return value_to_check


def check_answer(user_answer: str, correct_answer: str, flashcards: dict, missed_terms_count: dict) -> str:
    """Gives feedback on the user's answer."""
    if user_answer == correct_answer:
        return 'Correct!\n'

    term = reverse_dictionary(flashcards)[correct_answer]
    missed_terms_count[term] += 1

    if user_answer in list(flashcards.values()):
        return f'Wrong. The right answer is {correct_answer}, but your definition is correct for {term}.\n'

    return f'Wrong. The right answer is "{correct_answer}".\n'


def reverse_dictionary(dictionary: dict) -> dict:
    """Returns a dictionary whose keys are <dictionary>'s values and whose values are <dictionary>'s keys."""
    reversed_dictionary = {value:key for key, value in dictionary.items()}
    return reversed_dictionary


def give_flashcards_quiz(flashcards: dict, missed_terms_count: dict):
    """Quizzes the user on the given list of flashcards."""
    if not flashcards:
        print("There are currently no cards! Choose either 'add' or 'import' to add some cards.\n")
        return

    question_count = input("How many cards?:")
    while not question_count.isdigit():
        print("Please enter an integer!\n")
        question_count = input("How many cards?:")


    question_count = int(question_count)
    output.write("How many cards?:" + '\n')
    output.write(str(question_count) + '\n')

    for _ in range(question_count):
        term = random.choice(list(flashcards.keys()))
        answer_prompt = f'Print the definition of "{term}":\n'
        user_answer = input(answer_prompt)
        output.write(answer_prompt + '\n')
        answer_feedback = check_answer(user_answer, flashcards[term], flashcards, missed_terms_count)
        print(answer_feedback)
        output.write(answer_feedback + '\n')

    return


def existing_term(term: str, flashcards: dict):
    """If a card with the given <term> exists in <flashcards>, returns that term; otherwise returns False."""
    try:
        return flashcards[term]
    except KeyError:
        return False


def add_imported_cards(file_name: str, existing_flashcards: dict):
    """Adds cards from <file_name> to <existing_cards> and returns the new dictionary. Uses card from file if
    there is a duplicate."""
    with open(f'{file_name}', 'r') as file:
        pairs = file.readlines()

    combined_flashcards = copy.deepcopy(existing_flashcards)
    for pair in pairs:
        pair = pair.strip().split(',')
        combined_flashcards[pair[0]] = pair[1]

    return combined_flashcards, len(pairs)


def exit_program(final_export_file, flashcards: dict):
    print("Bye bye!")
    output.write("Bye bye!" + '\n')

    if final_export_file:
        count = 0
        with open(final_export_file, 'w') as file:
            for term, value in flashcards.items():
                file.write(f'{term},{value}\n')
                count += 1

        export_message = f'{count} cards have been saved.'
        print(export_message)
        output.write(export_message + '\n')

    output.close()
    sys.exit()


def save_log():
    """Stores the log in a user-specified file."""
    file_name = input("File name:\n")
    output.write("File name:\n" + '\n')
    output.write(file_name + '\n')

    print("The log has been saved.")
    output.write("The log has been saved.")

    with open(file_name, 'w') as file:
        output_contents = output.getvalue()
        file.write(output_contents)

    return


def get_hardest_card(card_scores: dict):
    if not list(card_scores.values()) or set(list(card_scores.values())) == {0}:
        print("There are no cards with errors.")
        output.write("There are no cards with errors.")
        return

    hardest_score = max(list(card_scores.values()))
    hardest_card_terms = [term for term in card_scores.keys() if card_scores[term] == hardest_score]

    if len(hardest_card_terms) == 1:
        hardest_term = hardest_card_terms[0]
        count = card_scores[hardest_card_terms[0]]
        hardest_card_message = f"The hardest card is '{hardest_term}'. You have {count} errors answering it."
        print(hardest_card_message)
        output.write(hardest_card_message)
        return

    if len(hardest_card_terms) > 1:
        hardest_cards_message = f"The hardest cards are {', '.join(hardest_card_terms)}."
        print(hardest_cards_message)
        output.write(hardest_cards_message)
        return
