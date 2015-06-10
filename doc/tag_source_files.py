#!/usr/bin/env python
'''Script that inserts a commit id in the source files that accompaby the html files

   This is useful when people download the source files and start editting and
   e-mailing them instead of using GIT.
'''

import subprocess, os, sys
from fnmatch import fnmatch


def iter_txt_files(root):
    for dn, subdns, fns in os.walk(root):
        for fn in fns:
            if fnmatch(fn, '*.txt'):
                yield os.path.join(dn, fn)


def main(root):
    try:
        # get the current commit ID
        commit_id = subprocess.check_output(['git', 'log', '-n1', '--pretty=oneline']).split()[0]
        version = None
        print 'Tagging files in %s with commit id %s' % (root, commit_id)
    except subprocess.CalledProcessError:
        # not in a git directory, then get the current version instead
        from conf import release
        version = release
        commit_id = None
        print 'Tagging files in %s with version %s' % (root, version)

    for fn_txt in iter_txt_files(root):
        with open(fn_txt) as f:
            lines = f.readlines()
        if lines[1].startswith('    DOCUMENTATION BUILT FROM'):
            lines = lines[3:]
        lines.insert(0, '\n')
        if commit_id is not None:
            lines.insert(0, '    DOCUMENTATION BUILT FROM COMMIT ID: %s\n' % commit_id)
        else:
            lines.insert(0, '    DOCUMENTATION BUILT FROM VERSION: %s\n' % version)
        lines.insert(0, '.. \n')
        with open(fn_txt, 'w') as f:
            f.writelines(lines)

if __name__ == '__main__':
    main(sys.argv[1])
