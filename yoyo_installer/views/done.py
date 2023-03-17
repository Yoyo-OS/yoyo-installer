# done.py
#
# Copyright 2022 mirkobrombin
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

import subprocess
from gi.repository import Gtk, Adw

from yoyo_installer.windows.dialog_output import YoyoDialogOutput
from gettext import gettext as _

@Gtk.Template(resource_path='/org/yoyoos/Installer/gtk/done.ui')
class YoyoDone(Adw.Bin):
    __gtype_name__ = 'YoyoDone'

    status_page = Gtk.Template.Child()
    btn_reboot = Gtk.Template.Child()
    btn_close = Gtk.Template.Child()
    btn_log = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__log = None
        
        self.status_page.set_description(
            _("Restart your device to enjoy your {} experience.").format(
                self.__window.recipe["distro_name"]
            )
        )

        self.btn_reboot.connect("clicked", self.__on_reboot_clicked)
        self.btn_close.connect("clicked", self.__on_close_clicked)
        self.btn_log.connect("clicked", self.__on_log_clicked)
    
    def set_result(self, result, terminal):
        self.__terminal = terminal

        if not result:
            self.status_page.set_icon_name("dialog-error-symbolic")
            self.status_page.set_title(_("Something went wrong"))
            self.status_page.set_description(_("Please contact the distribution developers."))
            self.btn_reboot.set_visible(False)
            self.btn_close.set_visible(True)

    def __on_reboot_clicked(self, button):
        subprocess.run(['gnome-session-quit', '--reboot'])

    def __on_close_clicked(self, button):
        self.__window.close()

    def __on_log_clicked(self, button):
        dialog = YoyoDialogOutput(self.__window, self.__terminal)
        dialog.present()
