pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
windowsdir = join_paths(pkgdatadir, 'yoyo_installer/windows')

sources = [
  '__init__.py',
  'main_window.py',
  'dialog.py',
  'dialog_output.py',
]

install_data(sources, install_dir: windowsdir)
