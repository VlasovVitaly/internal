#!/usr/bin/env python
import glob
import os
import os.path

incoming_dir = "lang/incoming"
po_dir = "lang/po"
pot_file = "lang/po/cataclysm-dda.pot"

langs = {
    'de'    : 'German',
    'es_AR' : 'Argentinian',
    'es_ES' : 'Spanish',
    'fr'    : 'French',
    'it_IT' : 'Italian',
    'ja'    : 'Japanese',
    'ko'    : 'Korean',
    'ru'    : 'Russian',
    'zh_CN' : 'Chinese',
    'zh_TW' : 'Taiwan'
}

msgmerge_args = '--backup=none -N -U -F -v'

def merge_translations():
    to_update = glob.glob("{}/*.po".format(incoming_dir))
    if not to_update:
        print("Nothing to update")
        return

    for fp in to_update:
        po_name = os.path.basename(fp)
        lang_name = po_name.split('.')[0]
        pot_fname = os.path.join(po_dir, po_name)

        print("msgmerge {} {} {}".format(msgmerge_args, fp, pot_file))
        os.system("msgmerge {} {} {}".format(msgmerge_args, fp, pot_file))
        print("mv {} {}".format(fp, pot_fname))
        os.system("mv {} {}".format(fp, pot_fname))
        print("git add {}".format(pot_fname))
        os.system("git add {}".format(pot_fname))
        long_name = langs[lang_name]
        print("git commit -m \"{} update\".".format(long_name))
        os.system("git commit -m \"{} update\".".format(long_name))

    os.system("git log -{}".format(len(to_update) + 1))
    print("-" * 16 + '\nAll languages was updated')
if __name__ == '__main__':
    merge_translations()
