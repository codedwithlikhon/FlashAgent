from __future__ import annotations

from browser_use import BrowserProfile, BrowserSession

from config.load_config import config


class BrowserFactory:
    def __init__(self) -> None:
        self.user_agent = config['browser']['user-agent']
        self.browser_profile_alive = self._get_browser_profile()

    def create_shared_session(self, headless: bool = True, **kwargs) -> BrowserSession:
        return BrowserSession(
            headless=headless,
            browser_profile=self.browser_profile_alive,
            user_data_dir=None,
            **kwargs,
        )

    def _get_browser_profile(self) -> BrowserProfile:
        return BrowserProfile(
            headless=False,
            wait_for_network_idle_page_load_time=3.0,
            viewport={"width": 1280, "height": 1100},
            user_agent=self.user_agent,
            highlight_elements=False,
            viewport_expansion=500,
            keep_alive=False,
            chromium_sandbox=False,
        )


browser_factory = BrowserFactory()
