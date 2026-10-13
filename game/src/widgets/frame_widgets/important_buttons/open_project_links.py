from ._base_button import ImportantButton, open_in_browser

PROJECT_URL = "https://github.com/tate-awesome/cybersecurity-game"


class OpenProjectRepository(ImportantButton):
    '''Opens the project's source repository in the user's browser.'''
    LABEL = "title_footer_links_repository"
    TOOLTIP = "title_footer_tooltips_repository"
    POPOUT = True

    def on_click(self):
        open_in_browser(PROJECT_URL)


class ReportAnIssue(ImportantButton):
    '''Opens the project's issue tracker in the user's browser.'''
    LABEL = "title_footer_links_issues"
    TOOLTIP = "title_footer_tooltips_issues"
    POPOUT = True

    def on_click(self):
        open_in_browser(f"{PROJECT_URL}/issues")
