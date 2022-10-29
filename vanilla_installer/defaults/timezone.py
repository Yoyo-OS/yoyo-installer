# keyboard.py
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

import sys
import time
import subprocess
import contextlib
from gi.repository import Gtk, Gio, GLib, Adw

from vanilla_installer.models.timezones import all_timezones, get_current_timezone, get_preview_timezone



@Gtk.Template(resource_path='/org/vanillaos/Installer/gtk/default-timezone.ui')
class VanillaDefaultTimezone(Adw.Bin):
    __gtype_name__ = 'VanillaDefaultTimezone'

    btn_next = Gtk.Template.Child()
    row_preview = Gtk.Template.Child()
    combo_country = Gtk.Template.Child()
    combo_city = Gtk.Template.Child()
    str_list_country = Gtk.Template.Child()
    str_list_city = Gtk.Template.Child()

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step
        
        # set up the string list for keyboard layouts
        for country, _ in all_timezones.items():
            self.str_list_country.append(country)
        
        # set up current timezone
        current_country, current_city = get_current_timezone()
        for country, _ in all_timezones.items():
            if country == current_country:
                self.combo_country.set_selected(list(all_timezones.keys()).index(country))
                self.__on_country_selected(None, None)

                for index, city in enumerate(all_timezones[country]):
                    if city == current_city:
                        self.combo_city.set_selected(index)
                        break

                break

        # signals
        self.btn_next.connect("clicked", self.__window.next)
        self.combo_country.connect("notify::selected", self.__on_country_selected)
        self.combo_city.connect("notify::selected", self.__on_city_selected)

    def get_finals(self):
        return {}
    
    def __on_country_selected(self, combo, param):
        self.str_list_city.splice(0, self.str_list_city.get_n_items())

        country_index = self.combo_country.get_selected()
        country = list(all_timezones.keys())[country_index]
        for timezone in all_timezones[country]:
            self.str_list_city.append(timezone)
            
        self.combo_city.set_selected(0)

    def __on_city_selected(self, combo, param):
        country_index = self.combo_country.get_selected()
        country = list(all_timezones.keys())[country_index]
        city_index = self.combo_city.get_selected()

        with contextlib.suppress(IndexError):
            city = all_timezones[country][city_index]
            _time, _date = get_preview_timezone(country, city)
            
            self.row_preview.set_title(_time)
            self.row_preview.set_subtitle(_date)