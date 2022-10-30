# window.py
#
# Copyright 2022 mirkobrombin
# Copyright 2022 muqtadir
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from gi.repository import Gtk, Gio, GLib, Adw

from vanilla_installer.utils.builder import Builder
from vanilla_installer.utils.parser import Parser
from vanilla_installer.utils.processor import Processor
from vanilla_installer.utils.run_async import RunAsync

from vanilla_installer.views.progress import VanillaProgress
from vanilla_installer.views.done import VanillaDone


@Gtk.Template(resource_path='/org/vanillaos/Installer/gtk/window.ui')
class VanillaWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'VanillaWindow'

    carousel = Gtk.Template.Child()
    btn_back = Gtk.Template.Child()
    toasts = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # this starts the builder and generates the widgets
        # to put in the carousel
        self.__builder = Builder(self)
        self.recipe = self.__builder.recipe

        # system views
        self.__view_progress = VanillaProgress(self, self.recipe.get("tour", {}))
        self.__view_done = VanillaDone(self)

        # this builds the UI with the widgets generated by the builder
        self.__build_ui()

        # connect system signals
        self.__connect_signals()

    def __connect_signals(self):
        self.btn_back.connect("clicked", self.back)
        self.carousel.connect("page-changed", self.__on_page_changed)

    def __build_ui(self):
        for widget in self.__builder.widgets:
            self.carousel.append(widget)

        self.carousel.append(self.__view_progress)
        self.carousel.append(self.__view_done)

    def __on_page_changed(self, *args):
        def process():
            # process the final data
            return Processor.run(
                self.recipe.get("log_file", "/tmp/vanilla_installer.log"), 
                self.recipe.get("pre_run", []),
                self.recipe.get("post_run"),
                finals
            )

        def on_done(result, *args):
            self.__view_done.set_result(result)
            self.next()

        cur_index = self.carousel.get_position()
        page = self.carousel.get_nth_page(cur_index)

        if page not in [self.__view_progress, self.__view_done]:
            self.btn_back.set_visible(cur_index != 0.0)
            return

        self.btn_back.set_visible(False)

        # keep the btn_back button locked if this is the last page
        if page == self.__view_done:
            return

        # collect all the finals
        finals = self.__builder.get_finals()

        # run the process in a thread
        RunAsync(process, on_done)

    def next(self, *args):
        cur_index = self.carousel.get_position()
        page = self.carousel.get_nth_page(cur_index + 1)
        self.carousel.scroll_to(page, True)

    def back(self, *args):
        cur_index = self.carousel.get_position()
        page = self.carousel.get_nth_page(cur_index - 1)
        self.carousel.scroll_to(page, True)
    
    def toast(self, message, timeout=3):
        toast = Adw.Toast.new(message)
        toast.props.timeout = timeout
        self.toasts.add_toast(toast)
