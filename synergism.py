"""Reads a synergism save file and displays contents in a GUI"""

import base64
import binascii
import json
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
import uuid


class App(tkinter.Tk):
    """Application window"""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()

        self.file_contents = {}

        self.title('Synergism Reader')

        self.tree = tkinter.ttk.Treeview(self, columns='Values', height=40)
        self.tree.column('0', width=300)
        self.tree.column('Values', width=300, anchor='center')
        self.tree.heading('Values', text='Values')

        self.scroll_bar = tkinter.ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_bar.set)

        self.tree.pack(side='left')
        self.scroll_bar.pack(side='left', fill='y')

        self._open_file()

    def _open_file(self):
        """Opens a file picker and read file"""
        file_name = tkinter.filedialog.askopenfilename(
            title='Choose a Synergism save file...', filetypes=(('Synergism Save', '.txt'),))

        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                encoded_file = file.read()
        except FileNotFoundError:
            return

        try:
            self.file_contents = json.loads(
                base64.b64decode(encoded_file, validate=True))
        except binascii.Error:
            showerror(title='Invalid File!',
                      message='The chosen file is an invalid save file. Please choose another one!')
            self._open_file()
            return

        # Clear then re-populate the Treeview
        self.tree.delete(*self.tree.get_children())
        self._dict_to_tree('', self.file_contents)

    def _dict_to_tree(self, parent, dictionary):
        """Recursive method to populate a Treeview with dict contents"""
        for key in dictionary:
            uid = uuid.uuid4()
            if isinstance(dictionary[key], dict):
                self.tree.insert(parent, 'end', uid, text=key)
                self._dict_to_tree(uid, dictionary[key])
            elif isinstance(dictionary[key], list):
                self.tree.insert(parent, 'end', uid, text=str(key) + '[]')
                self._dict_to_tree(
                    uid, dict([(i, x) for i, x in enumerate(dictionary[key])]))
            else:
                value = dictionary[key]
                if value is None:
                    value = 'None'
                self.tree.insert(parent, 'end', uid, text=key, value=value)


def main():
    """Program starts here"""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
