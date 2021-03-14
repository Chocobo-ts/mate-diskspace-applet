#!/usr/bin/python3

# now Ctrl+C will break program if you run it in terminal
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
#--------------------------------------------------------
import subprocess
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('MatePanelApplet', '4.0')
from gi.repository import Gtk
from gi.repository import MatePanelApplet
from gi.repository import GLib  # timeout_add


def applet_fill(applet):
    global label
    box = Gtk.Box()
    applet.add(box)
    label = Gtk.Label()
    box.add(label)
    applet.show_all()
    update_label()
    GLib.timeout_add(1000, update_label)


def update_label():
    text = get_value()
    label.set_markup(text)
    return True

def get_value():
    exclude = '/run\|/boot/efi' # regexp for grep -ve
    mounts = subprocess.check_output('df -lh| grep -e "^/dev/" | grep -ve "%s"' % exclude, shell=True).splitlines()
    result = ''
    for line in mounts:
      subline = line.split(b'%')
      mpoint = subline.pop()
      subline = subline[0].split()
      dev = subline[0]
      devname = dev.split(b'/')[-1]
      label = subprocess.check_output('blkid -s LABEL -o value %s' % dev.decode(),shell=True)
      if label:
         name = label.rstrip()
      else:
         name = mpoint
      result = result + name.decode() + ': <b>' + subline[-1].decode() + '%</b>    '
#    result = result[:-1]
    return result


def applet_factory(applet, iid, data):
    if iid != "DiskSpaceApplet":
       return False
    applet_fill(applet)
    return True


MatePanelApplet.Applet.factory_main("DiskSpaceAppletFactory", True,
                            MatePanelApplet.Applet.__gtype__,
                            applet_factory, None)

