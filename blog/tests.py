import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from playwright.sync_api import sync_playwright

class MyViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        # cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_login(self):
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/admin/")
        page.wait_for_selector('text=Django administration')
        page.fill('[name=username]', 'myuser')
        page.fill('[name=password]', 'secret')
        page.click('text=Log in')
        assert len(page.eval_on_selector(".errornote", "el => el.innerText")) > 0
        page.close()