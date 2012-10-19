#!/usr/bin/env python
####
#    Copyright Plymouth Marine Laboratory (PML) 2012
#
#    This file is part of the PML earthserver portal.
#
#    PML earthserver portal is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PML earthserver portal is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PML earthserver portal.  If not, see <http://www.gnu.org/licenses/>.
####
from flask_script import Command, Manager

from petascope_cache import app

manager = Manager(app)


class SyncDB(Command):
    """
    Initializes the database tables.
    """
    def run(self):
        from petascope_cache import db
        from petascope_cache.models import Cached_WCPS
        print "creating database"
        db.drop_all()
        db.create_all()
        db.session.commit()
    
   
        






class Test(Command):
    """
    Runs the application's test suite.
    """
    def run(self):
        import os
        from unittest import TestLoader, TextTestRunner
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        loader = TestLoader()
        test_suite = loader.discover(cur_dir)
        runner = TextTestRunner(verbosity=2)
        runner.run(test_suite)



manager.add_command('syncdb', SyncDB())
manager.add_command('test', Test())
manager.run()











