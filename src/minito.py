import sys
import csv
import urwid

FILL_CHAR = ' '
INPUT_BOX_PROMPT = "> "

filename = "untitled"

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


class Minito:

    def exit_program(self):
        raise urwid.ExitMainLoop()

    def on_key_press(self, key):
        match key:
            case 'q' | 'Q':
                self.exit_program()
            case "tab":
                self.switch_focus()
            case "enter":
                self.process_input_box()
            case "ctrl x":
                if filename == "untitled":
                    self.input_state = "creating-file"
                    self.input_box.set_title("Enter Filename to Save")
                else:
                    self.input_state = "exiting"
                    self.input_box.set_title("Save Changes? (yes/no)")
 
    # switches between body and footer of the main_frame
    def switch_focus(self):
        current_focus = self.main_frame.focus_part
        if current_focus == "body":
            self.main_frame.focus_position = "footer"
        elif current_focus == "footer":
            self.main_frame.focus_position = "body"
        else:
            self.main_frame.focus_position = "footer"

    def get_input_box_text(self):
        return self.input_box_edit_widget.get_edit_text()

    def process_input_box(self):
        global filename

        # stop if input box is empty
        text = self.get_input_box_text()
        if text == "":
            return
        
        match self.input_state:
            case "task":
                self.add_task(text, False)
            case "creating-file":
                filename = f".\\{self.get_input_box_text()}.csv"
                self.title_text.set_text(f"MINITO - {filename}")
                self.save_file()
                self.exit_program()
            case "exiting":
                self.exiting()

        # clear the input box
        self.input_box_edit_widget.set_edit_text("")

    def add_task(self, text, state):
        checkbox = CustomCheckBox(("task-normal", text), state=state)
        if state == True:
            checkbox.apply_completed_effect()
        self.todo_pile.widget_list.append(checkbox)

    def save_file(self):
        with open(filename, 'w') as file:
            file.write("Task,State\n")
            for checkbox in self.todo_pile.widget_list[1:]:
                state = "True" if checkbox.get_state() == True else "False"
                file.write(f"\"{checkbox.get_label()}\",{state}\n")

    def exiting(self):
        user_input = self.get_input_box_text()
        if user_input == "yes":
            self.save_file()
            self.exit_program()
        elif user_input == "no":
            self.exit_program()

    def load_from_file(self):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            for entry in data:
                self.add_task(entry["Task"], True if entry["State"] == "True" else False)

    def __init__(self):
        self.input_state = "task"  # "saving", "creating-file"

        # setting filename if passed through
        if len(sys.argv) == 2:
            self.filename = sys.argv[1]

        self.input_box_edit_widget = urwid.Edit(INPUT_BOX_PROMPT)
        self.input_box = urwid.LineBox(self.input_box_edit_widget, title="Add Task", title_align="left")

        todo_widget_list = [urwid.Text("")]  # the Text object is required so that when all tasks are gone, the program doesn't break
        self.todo_pile = urwid.Pile(widget_list=todo_widget_list)

        if filename != "untitled":
            self.load_from_file()
        
        self.title_text = urwid.Text("MINITO - " + filename, align="center")
        self.main_frame = urwid.Frame(
            header=self.title_text,
            body=urwid.Filler(self.todo_pile, valign="top"),
            footer=self.input_box,
            focus_part="footer"
        )

        loop = urwid.MainLoop(self.main_frame, palette=palette, unhandled_input=self.on_key_press)
        loop.run()


minito: Minito

if __name__ == "__main__":
    minito = Minito()
