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

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import SimpleTestCase
from django_webtest import WebTest
from sst.actions import *
from sst.cases import SSTTestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from arches.app.views.main import auth
from django.contrib.sessions.middleware import SessionMiddleware
import subprocess
import sys
import time

class UnitTests(SimpleTestCase):
    def setUp(self):
        super(UnitTests, self).setUp()
        self.user = User.objects.create_user('test', 'test@archesproject.org', 'password')
        self.user.save()

    def test_login(self):
        factory = RequestFactory()
        request = factory.post(reverse('auth'), {'username': 'test', 'password': 'password'})
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = auth(request)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.get('location') == reverse('home'))

    def tearDown(self):
        super(UnitTests, self).tearDown()
        self.user.delete()


# see WebTest API for more:
# http://webtest.readthedocs.org/en/latest/api.html
class FunctionalTests(WebTest):
    def setUp(self):
        super(FunctionalTests, self).setUp()
        self.user = User.objects.create_user('test', 'test@archesproject.org', 'password')
        self.user.save()

    def test_login(self):
        index = self.app.get('/')
        login = index.click('Login')
        login_form = login.forms['login-form']
        login_form['username'] = 'test'
        login_form['password'] = 'password'
        response = login_form.submit('submit')
        self.assertTrue(response.status_code == 302)
        response = response.follow()
        assert 'Welcome test - Logout' in response

    def tearDown(self):
        super(FunctionalTests, self).tearDown()
        self.user.delete()


class AutomationTests(SSTTestCase):
    def setUp(self):
        super(AutomationTests, self).setUp()
        self.user = User.objects.create_user('test', 'test@archesproject.org', 'password')
        self.user.save()
        self.server = subprocess.Popen([sys.executable,settings.PACKAGE_ROOT + '/../manage.py','runserver','8080','--settings=hip.settings_tests'])
        # give it a moment to start up.
        time.sleep(1)

    def test_login(self):
        set_base_url('http://localhost:8080/')
        go_to(reverse('home'))
        click_link('auth-link')
        write_textfield(get_element(name='username'), 'test')
        write_textfield(get_element(name='password'), 'password')
        click_button('login-btn')
        assert_text_contains('auth-link', 'WELCOME TEST - LOGOUT')

    def tearDown(self):
        super(AutomationTests, self).tearDown()
        self.user.delete()
        self.server.kill()
