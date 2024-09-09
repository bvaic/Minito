import sys
import csv
import urwid

FILL_CHAR = ' '
INPUT_BOX_PROMPT = "> "

filename = "untitled"
file_created = False
input_state = "task"  # "saving", "creating-file"

input_box_edit_widget: urwid.Edit
input_box: urwid.LineBox
main_frame: urwid.Frame
todo_pile: urwid.Pile
title_text: urwid.Text

palette = [
    ("task-normal", "default,bold", "default"),
    ("task-completed", "default,strikethrough", "default")
]


# adds and removes attr on text based on state of checkbox
class CustomCheckBox(urwid.CheckBox):
    def apply_completed_effect(self):
        self.set_label(("task-completed", self.get_label()))

    def keypress(self, size, key: str):
        if key == "backspace":
            todo_pile.widget_list.remove(self)
            return
            
        if key != "enter":
            return super().keypress(size, key)
        
        # when ENTER pressed on this checkbox, apply attr if completed else remove attr
        if self.get_state() == False:
            self.apply_completed_effect()
        else:
            self.set_label(("task-normal", self.get_label()))

        return super().keypress(size, key)  # keeping the main functionality of the checkbox


def exit_program():
    raise urwid.ExitMainLoop()


def on_key_press(key):
    global input_state

    match key:
        case 'q' | 'Q':
            exit_program()
        case "tab":
            switch_focus()
        case "enter":
            process_input_box()
        case "ctrl x":
            if filename == "untitled":
                input_state = "creating-file"
                input_box.set_title("Enter Filename to Save")
            else:
                input_state = "exiting"
                input_box.set_title("Save Changes? (yes/no)")

    
# switches between body and footer of the main_frame
def switch_focus():
    current_focus = main_frame.focus_part
    if current_focus == "body":
        main_frame.focus_position = "footer"
    elif current_focus == "footer":
        main_frame.focus_position = "body"
    else:
        main_frame.focus_position = "footer"


def get_input_box_text():
    return input_box_edit_widget.get_edit_text()


def process_input_box():
    global filename

    # stop if input box is empty
    text = get_input_box_text()
    if text == "":
        return
    
    match input_state:
        case "task":
            add_task(text, False)
        case "creating-file":
            filename = f".\\{get_input_box_text()}.csv"
            title_text.set_text(f"MINITO - {filename}")
            save_file()
            exit_program()
        case "exiting":
            exiting()

    # clear the input box
    input_box_edit_widget.set_edit_text("")


def add_task(text, state):
    checkbox = CustomCheckBox(("task-normal", text), state=state)
    if state == True:
        checkbox.apply_completed_effect()
    todo_pile.widget_list.append(checkbox)


def save_file():
    with open(filename, 'w') as file:
        file.write("Task,State\n")
        for checkbox in todo_pile.widget_list[1:]:
            state = "True" if checkbox.get_state() == True else "False"
            file.write(f"\"{checkbox.get_label()}\",{state}\n")


def exiting():
    user_input = get_input_box_text()
    if user_input == "yes":
        save_file()
        exit_program()
    elif user_input == "no":
        exit_program()


def load_from_file():
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
        for entry in data:
            add_task(entry["Task"], True if entry["State"] == "True" else False)

def main():
    global input_box_edit_widget
    global input_box
    global todo_pile
    global main_frame
    global filename
    global title_text

    # setting filename if passed through
    if len(sys.argv) == 2:
        filename = sys.argv[1]

    input_box_edit_widget = urwid.Edit(INPUT_BOX_PROMPT)
    input_box = urwid.LineBox(input_box_edit_widget, title="Add Task", title_align="left")

    todo_widget_list = [urwid.Text("")]  # the Text object is required so that when all tasks are gone, the program doesn't break
    todo_pile = urwid.Pile(widget_list=todo_widget_list)

    if filename != "untitled":
        load_from_file()
    
    title_text = urwid.Text("MINITO - " + filename, align="center")
    main_frame = urwid.Frame(
        header=title_text,
        body=urwid.Filler(todo_pile, valign="top"),
        footer=input_box,
        focus_part="footer"
    )

    loop = urwid.MainLoop(main_frame, palette=palette, unhandled_input=on_key_press)
    loop.run()


if __name__ == "__main__":
    main()
