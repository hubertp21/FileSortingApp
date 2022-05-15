import os
import shutil
import uuid

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

Builder.load_file("menu.kv")


class MyLayout(Widget):
    def pressed(self):
        list_files(self.filechooser.path, self.folder.text, self.extension.text)


class P(FloatLayout):
    def update(self, text):
        self.error_label.text = text


class FileApp(App):
    filechooser = ObjectProperty(None)
    folder = ObjectProperty(None)
    extension = ObjectProperty(None)

    def build(self):
        return MyLayout()


def show_popup(error_type, text):
    show = P()
    show.update(text)
    popup_window = Popup(title="SYSTEM MESSAGE " + str(error_type), content=show, size_hint=(None, None), size=(300, 200))

    popup_window.open()


def list_files(directory_path, folder_name, extension):
    files = os.listdir(directory_path)
    extension_length = len(extension)
    new_folder_path = os.path.join(directory_path, folder_name)

    can_be_written = checkIf(files, extension_length, folder_name, directory_path, new_folder_path)

    if can_be_written == 1:
        pass
    else:
        return can_be_written

    os.mkdir(new_folder_path)

    for file in files:
        length = len(file)
        if file[length - extension_length: length] == extension:
            source = os.path.join(directory_path, file)
            shutil.move(source, new_folder_path)


def checkIf(files, extension_length, folder_name, directory_path, new_folder_path):
    if len(files) == 0:
        show_popup(100, "NO FILES")
        return 100

    elif extension_length == 0:
        show_popup(101, "NO EXTENSION SELECTED")
        return 101

    elif folder_name == "":
        show_popup(102, "NO FOLDER NAME SELECTED")
        return 102

    elif not permitted(directory_path):
        show_popup(103, "WRITING IS NOT PERMITTED")
        return 103

    elif os.path.exists(new_folder_path):
        show_popup(104, "PATH ALREADY EXISTS")
        return 104
    else:
        show_popup(1, "PATH SUCCESSFULLY CREATED")
        return 1


def permitted(path):
    dummypath = os.path.join(path, str(uuid.uuid4()))
    try:
        with open(dummypath, 'w'):
            pass
        os.remove(dummypath)
        return True
    except IOError:
        return False


if __name__ == "__main__":
    FileApp().run()
