class OutsideOptionScopeError(Exception):
    """Raised if you try to answer a question with something that does not answer it."""
    pass

def multiple_choice(question: str = "", options: list = []) -> str:
    """This function takes as input a question and a list of answers (strings).
    It outputs the answer selected."""
    options_letters = []
    for i in range(0,len(options)):
        options_letters.append(chr(ord('@')+i+1))
    print(f"\n{question}")
    for i in range(0,len(options)):
        print(f"[{options_letters[i]}] {options[i]}")
    while True:
        try:
            answer = str(input(">"))
            if answer.capitalize() not in options_letters:
                raise OutsideOptionScopeError
        except (ValueError, OutsideOptionScopeError):
            print("\nThat is not a valid choice.")
            print("Please select one of the given options.")
            continue
        else:
            final_answer = options[ord(answer.capitalize())-1-ord('@')] # This is the term in the list you selected.
            break
    return final_answer

def open_response(question: str = "", options: list =[]) -> str:
    """This function takes as input a question and a list of answers (strings).
    It doesn't show the player the answers.
    When the player types an answer, it checks if what they typed appears in the list of options.
    If it does, it outputs the chosen option.
    If the player's answer matches multiple options, this function outputs the last one."""
    print(f"\n{question}")
    final_answer = ""
    while True:
        try:
            answer = str(input(">"))
            for option in options:
                if option.casefold() in answer.casefold(): # Check if any option is a substring of what the player wrote, case insensitively.
                    final_answer = option
            if final_answer == "":
                raise OutsideOptionScopeError
        except (ValueError, OutsideOptionScopeError):
            print("\nI don't understand.")
            print("Please try again.")
            continue
        else:
            break
    return final_answer

def open_response_number(question: str = "", options: list =[]) -> str:
    """This is a copy of open_response() where your options are ints."""
    print(f"\n{question}")
    final_answer = ""
    while True:
        try:
            answer = int(input(">"))
            for option in options:
                if option == answer:
                    final_answer = option
            if final_answer == "":
                raise OutsideOptionScopeError
        except (ValueError, OutsideOptionScopeError):
            print("\nThat is outside the allowed scope.")
            print("Please try again.")
            print(f"\n{question}")
            continue
        else:
            break
    return final_answer
    
def unbounded_open_response(question: str = "", prompt = ">") -> str:
    """This is a copy of open_response() that doesn't have a set list of 'correct' answers."""
    print(f"\n{question}")
    final_answer = ""
    while True:
        try:
            final_answer = str(input(prompt))
        except (ValueError, OutsideOptionScopeError):
            print("\nI don't understand.")
            print("Please try again.")
            continue
        else:
            break
    return final_answer