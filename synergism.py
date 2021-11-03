"""Reads a synergism save file and displays contents in a GUI"""

import base64
import json
import tkinter as tk
import uuid
from tkinter import ttk
from tkinter.filedialog import askopenfilename


class App(tk.Tk):
    """Application window"""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()

        self.file_contents = 0

        self.title('Synergism Reader')

        self.btn_choose_file = ttk.Button(
            self, text='Open a Synergism Save File...', command=self.open_file)
        self.tree = ttk.Treeview(self, columns='Values', height=40)
        self.tree.column('Values', width=500, anchor='center')
        self.tree.heading('Values', text='Values')

        self.scroll_bar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_bar.set)

        self.tree.grid(row=0, column=0, pady=2)
        self.scroll_bar.grid(row=0, column=1)
        self.btn_choose_file.grid(row=1, column=0, columnspan=2, pady=2)

    def open_file(self):
        """Opens a file picker and read file"""
        file_name = askopenfilename(
            title='Choose a save file...', filetypes=(('Synergism Save', '.txt'),))

        with open(file_name, 'r', encoding='utf-8') as file:
            encoded_file = file.read()

        self.file_contents = json.loads(base64.b64decode(encoded_file))
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
