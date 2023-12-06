import unittest

from flask import url_for

from test.test_flask import TestBase


class TestCommonPages(TestBase):

    def test_home_page(self):
        response = self.client.get(
            url_for("common.portfolio_main"),
            follow_redirects=True
        )

        self.assert200(response)
        self.assertIn(b"Hello its me", response.data)
        self.assertIn(b"Projects", response.data)
        self.assertIn(b'<footer class="bg-light-purple-gradient">', response.data)

    def test_projects_page(self):
        response = self.client.get(
            url_for("common.portfolio_projects"),
            follow_redirects=True
        )

        self.assert200(response)
        self.assertIn(b'<a href="https://github.com/JJerome-NM/NM-WebSockets">NM-WebSockets</a>', response.data)
        self.assertNotIn(b'<footer class="bg-light-purple-gradient">', response.data)

    def test_contacts_page(self):
        response = self.client.get(
            url_for("common.portfolio_contacts"),
            follow_redirects=True
        )

        self.assert200(response)
        self.assertIn(b'mykhailo.khalabarchuk.21@pnu.edu.ua', response.data)
        self.assertIn(b'<a href="https://www.linkedin.com/in/mykhailo-khalabarchuk-26376528b/">', response.data)
        self.assertIn(b'<a href="https://github.com/JJerome-NM">', response.data)
        self.assertNotIn(b'<footer class="bg-light-purple-gradient">', response.data)

    def test_skills_page(self):
        response = self.client.get(
            url_for("common.portfolio_skills"),
            follow_redirects=True
        )

        self.assert200(response)
        self.assertIn(b'My skills', response.data)
        self.assertIn(b'<a class="skill" href="/common/skills/0">Java Core</a>', response.data)
        self.assertIn(b'<a class="skill" href="/common/skills/1">Java Spring</a>', response.data)
        self.assertNotIn(b'<footer class="bg-light-purple-gradient">', response.data)

    def test_get_skill_page(self):
        response = self.client.get(
            url_for("common.portfolio_skills", id=0),
            follow_redirects=True
        )

        self.assert200(response)
        self.assertIn(b'Java Core', response.data)
        self.assertIn(b'Java Core, often referred to as', response.data)
        self.assertNotIn(b'<footer class="bg-light-purple-gradient">', response.data)


if __name__ == '__main__':
    unittest.main()
