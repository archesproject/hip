'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
#!/usr/bin/env python
import os
import sys

# assumes you've installed the following:
#   - python 2.7
#   - pip
#   - java
#   - postgres 9 (must be running with the default settings expected by arches)

if __name__ == "__main__":
    ARCHES_DIR = os.path.abspath(os.path.join(os.getcwd(), 'arches'))
    HIP_DIR = os.path.abspath(os.path.join(os.getcwd(), 'hip'))
    os.system('git clone https://github.com/archesproject/arches.git %s' % (ARCHES_DIR))
    os.system('git clone https://github.com/archesproject/hip.git %s' % (HIP_DIR))
    os.system('sudo pip install fabric')
    os.system('sudo pip install honcho')
    os.chdir(os.path.join(ARCHES_DIR, 'arches'))
    os.system('fab dev_setup')
    if sys.platform == 'win32':
        python_exe = os.path.join(ARCHES_DIR, 'virtualenv', 'ENV', 'Scripts', 'python')
    else:
        python_exe = os.path.join(ARCHES_DIR, 'virtualenv', 'ENV', 'bin', 'python')
    os.chdir(HIP_DIR)
    os.system('%s manage.py packages --operation setup' % (python_exe))
