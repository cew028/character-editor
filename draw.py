def frame(width: int = 100, contents: list = []) -> None:
    """This function takes as an input a width (default 100) and a list of strings to write.
    It then draws a frame around the written strings (with line breaks after each string).
    It has built-in line breaks for lines longer than the width inputted."""
    print("\n╔", end="")
    for i in range(width-2):
        print("═", end="")
    print("╗")
    for content in contents:
        list_of_lines = content.split("\n") # This takes the {content} and produces a list of strings of the lines.
        for line in list_of_lines:
            white_space = width-len(line)-2-1 # The 2 is for the left and right edges of the frame, the 1 is for the leading white space before {line}.
            if white_space > 0:
                # This line fits inside of the frame.
                print(f"║ {line}" + white_space*" " + "║")
            else:
                # This line doesn't fit.
                line_temp = ""
                list_of_words = line.split(" ") # This takes the {line} and produces a list of strings of the words.
                while len(list_of_words) > 0:
                    line_temp += list_of_words[0] + " "
                    list_of_words.pop(0)
                    if len(list_of_words) != 0:
                        if len(line_temp)+len(list_of_words[0]) > width-2-2: # The first 2 is for the frame and the second 2 is for the white space.
                            # If adding the next word makes the line_temp too long.
                            white_space_line = width-len(line_temp)-2-1
                            print(f"║ {line_temp}" + white_space_line*" " + "║")
                            line_temp = ""
                    else:
                        # There are no more words, so print whatever's left.
                        white_space_line = width-len(line_temp)-2-1
                        print(f"║ {line_temp}" + white_space_line*" " + "║")
                        line_temp = ""
    print("╚", end="")
    for i in range(width-2):
        print("═", end="")
    print("╝")

def picture(file = None) -> None:
    """This function takes in a text file of an ASCII picture.
    It then draws the picture in the command prompt."""
    with open(file, encoding = "utf-8") as f:
        print(f.read())