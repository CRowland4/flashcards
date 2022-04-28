import copy
import helpers
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--import_from', default=None)
parser.add_argument('--export_to', default=None)


class Flashcards:
    """
    Flashcards in this class are stored in a dictionary as 'term': 'definition' pairs.
    """
    def __init__(self):
        self.flashcards = {}  # Flashcards with the form <term>:<definition>
        self.flashcard_misses = {}  # Missed counts with the form <term>:<number of times missed>
        self.args = parser.parse_args()
        self.commands = [
            'add',
            'remove',
            'import',
            'export',
            'ask',
            'exit',
            'log',
            'hardest card',
            'reset stats'
        ]

    def main(self):
        if self.args.import_from:
            self._initial_import()

        while True:
            command_prompt = f"Choose an action ({', '.join(self.commands)}):\n"
            command = input(command_prompt)
            helpers.output.write(command_prompt + '\n')
            helpers.output.write(command + '\n')
            if command in self.commands:
                action = getattr(self, '_' + command.replace(' ', '_'))
                action()
            else:
                invalid_message = "Invalid command."
                print(invalid_message)
                helpers.output.write(invalid_message + '\n')

    def _set_flashcard_misses(self):
        """Initializes the flashcard_misses attribute as a dict whose terms are the same as flashcards; term:0"""
        for term in self.flashcards.keys():
            self.flashcard_misses[term] = 0

        return

    def _add(self):
        """Adds a new user-created card to the flashcards attribute."""
        new_card_pair = helpers.create_single_card(self.flashcards)
        self.flashcards[new_card_pair[0]] = new_card_pair[1]
        add_card_notification = f'The pair ("{new_card_pair[0]}":"{new_card_pair[1]}") has been added.'
        print(add_card_notification)
        helpers.output.write(add_card_notification + '\n')
        return

    def _remove(self):
        """Removes the card specified via user input if it exists."""
        term_prompt = 'Which card? (enter the prompt of the card you want to remove)\n'
        term = input(term_prompt)
        helpers.output.write(term_prompt + '\n')
        helpers.output.write(term + '\n')
        existing_term = helpers.existing_term(term, self.flashcards)
        if existing_term:
            del self.flashcards[term]
            card_removal_message = "The card has been removed."
            print(card_removal_message)
            helpers.output.write(card_removal_message + '\n')
            return

        unable_to_remove_message = f"Can't remove {term}: there is no such card."
        print(unable_to_remove_message)
        helpers.output.write(unable_to_remove_message + '\n')
        return

    def _import(self):  # Files should contain cards in the format <term>:<definition>
        """Adds cards to the flashcards attribute from the user-specified file, favoring the file in the case
        of a duplicate."""
        file_name = input("File name:\n")  # Should include extension
        helpers.output.write("File name:\n" + '\n')
        helpers.output.write(file_name + '\n')

        if not os.path.exists(f'{os.getcwd()}/{file_name}'):
            print("File not found.")
            helpers.output.write("File not found." + '\n')
            return

        import_information = helpers.add_imported_cards(file_name, self.flashcards)  # (updated_cards, cards_added)
        self.flashcards = copy.deepcopy(import_information[0])
        load_message = f"{import_information[1]} cards have been loaded."
        print(load_message)
        helpers.output.write(load_message + '\n')
        return

    def _export(self):
        file_name = input("File name:\n")
        helpers.output.write("File name:\n" + '\n')
        helpers.output.write(file_name + '\n')

        count = 0
        with open(file_name, 'w') as file:
            for term, value in self.flashcards.items():
                file.write(f'{term},{value}\n')
                count += 1

        export_message = f'{count} cards have been saved.'
        print(export_message)
        helpers.output.write(export_message + '\n')

    def _ask(self):
        """Quizzes the user."""
        self._set_flashcard_misses()
        helpers.give_flashcards_quiz(self.flashcards, self.flashcard_misses)
        return

    def _exit(self):
        helpers.exit_program(self.args.export_to, self.flashcards)

    def _log(self):
        helpers.save_log()

    def _hardest_card(self):
        helpers.get_hardest_card(self.flashcard_misses)

    def _reset_stats(self):
        for term in self.flashcard_misses.keys():
            self.flashcard_misses[term] = 0

        print("Card statistics have been reset.")
        helpers.output.write("Card statistics have been reset." + '\n')

        return

    def _initial_import(self):
        file_name = self.args.import_from
        import_information = helpers.add_imported_cards(file_name, self.flashcards)  # (updated_cards, cards_added)
        self.flashcards = copy.deepcopy(import_information[0])
        load_message = f"{import_information[1]} cards have been loaded."
        print(load_message)
        helpers.output.write(load_message + '\n')
        return


stage_5 = Flashcards()
stage_5.main()


