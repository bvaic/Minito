import sys
import csv
import json
import urwid

# Modifiable Constants
# TODO: put modifiable constants into configuration file
INPUT_BOX_PROMPT = "> "

# Definite Constants

# gets converted to json
FILE_TEMPLATE = \
{
    "formatting": {
        "spaces-between-tasks": 0
    },
    "tasks": [

    ]
}
FILE_EXTENSION = ".minito"

PALETTE = [
    ("task-normal", "default,bold", "default"),
    ("task-completed", "default,strikethrough", "default")
]


# When CheckBox switches to completed:
# - the bold will be removed
# - a strikethrough will be applied
class CustomCheckBox(urwid.CheckBox):
    def __init__(self, text, state):
        super().__init__(("task-normal", text), state=state)
        if state == True:
            self.apply_completed_effect()

    def apply_completed_effect(self):
        self.set_label(("task-completed", self.get_label()))

    def keypress(self, size, key: str):
        if key == "backspace":
            minito.todo_pile.widget_list.remove(self)
            return
            
        if key != "enter":
            return super().keypress(size, key)
        
        # when ENTER pressed on this checkbox, apply attr if completed else remove attr
        if self.get_state() == False:
            self.apply_completed_effect()
        else:
            self.set_label(("task-normal", self.get_label()))

        return super().keypress(size, key)  # keeping the main functionality of the checkbox


# A Minito class was created so that global variables could become class members
# Now, any Minito function can access a widget that is a member of the Minito class
class Minito:
    def __init__(self):
            # Input States:
            # "adding-task"             default state, input becomes a new task
            # TODO "editing-task"       input modifies a task (task contents are copied to input box for editing)
            # "entering-filename"       occurs when file is untitled, input becomes the filename
            # "save-or-not"             input is user's decision to save the file
            self.input_state = "adding-task"
            self.filename = "untitled"

            # setting filename if passed through
            if len(sys.argv) == 2:
                self.filename = sys.argv[1]

            self.input_box_edit_widget = urwid.Edit(INPUT_BOX_PROMPT)
            self.input_box = urwid.LineBox(self.input_box_edit_widget, title="Add Task", title_align="left")

            todo_widget_list = [urwid.Text("")]  # the Text object is required so that when all tasks are gone, the program doesn't break
            self.todo_pile = urwid.Pile(widget_list=todo_widget_list)

            if self.filename != "untitled":
                self.load_file()
            
            self.title_text = urwid.Text("MINITO - " + self.filename, align="center")
            self.main_frame = urwid.Frame(
                header=self.title_text,
                body=urwid.Filler(self.todo_pile, valign="top"),
                footer=self.input_box,
                focus_part="footer"
            )

            loop = urwid.MainLoop(self.main_frame, palette=PALETTE, unhandled_input=self.on_key_press)
            loop.run()

    def exit_program(self):
        raise urwid.ExitMainLoop()
    
    def set_input_state(self, new_state, new_input_box_title):
        self.input_state = new_state
        self.input_box.set_title(new_input_box_title)
        self.switch_focus_to("input-box")

    # This function can alter the input state which will change what pressing ENTER
    # on the input box does
    def on_key_press(self, key):
        match key:
            case 'q' | 'Q':
                self.exit_program()
            case "tab":
                self.switch_focus()
            case "enter":
                self.process_input_box()
            case "ctrl x":
                self.set_input_state("save-or-not", "Save? (yes/no)")

    def switch_focus(self):
        """switches between the main panel and input box"""
        current_focus = self.main_frame.focus_part
        if current_focus == "body":
            self.main_frame.focus_position = "footer"
        elif current_focus == "footer":
            self.main_frame.focus_position = "body"
        else:
            self.main_frame.focus_position = "footer"

    def switch_focus_to(self, target):
        """target must be either \"main\" or \"input-box\""""
        if target == "main":
            self.main_frame.focus_position = "body"
        elif target == "input-box":
            self.main_frame.focus_position = "footer"
        else:
            self.main_frame.focus_position = "body"

    def get_input_box_text(self):
        return self.input_box_edit_widget.get_edit_text()

    def process_input_box(self):
        """does something with the input based on input state"""
        input_box_text = self.get_input_box_text()

        if input_box_text == "":
            return
        
        match self.input_state:
            case "adding-task":
                self.add_task(input_box_text, False)
            case "entering-filename":
                self.filename = f".\\{self.get_input_box_text() + FILE_EXTENSION}"
                self.save_file()
                self.exit_program()
            case "save-or-not":
                if input_box_text == "yes":
                    if self.filename == "untitled":
                        self.set_input_state("entering-filename", "Save As...")
                    else:
                        self.save_file()
                        self.exit_program()
                elif input_box_text == "no":
                    self.exit_program()

        # clear the input box
        self.input_box_edit_widget.set_edit_text("")

    def add_task(self, text, state):
        checkbox = CustomCheckBox(text, state=state)
        self.todo_pile.widget_list.append(checkbox)

    def generate_file_contents(self):
        contents = FILE_TEMPLATE.copy()
        
        for checkbox in self.todo_pile.widget_list[1:]:
            contents["tasks"].append({
                "task": checkbox.get_label(),
                "completed": checkbox.get_state()
            })

        return json.dumps(contents, indent=4)

    def save_file(self):
        with open(self.filename, 'w') as file:
            file.write(self.generate_file_contents())

    def load_file(self):
        # TODO: check if file is a .minito
        with open(self.filename, 'r') as file:
            file_data = json.load(file)
            for task in file_data["tasks"]:
                self.add_task(task["task"], task["completed"])

    def exiting(self):
        user_input = self.get_input_box_text()
        if user_input == "yes":
            self.save_file()
            self.exit_program()
        elif user_input == "no":
            self.exit_program()


minito: Minito

if __name__ == "__main__":
    minito = Minito()
