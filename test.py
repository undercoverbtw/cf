import time
import logging
import os
from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('cloudflare_bypass.log', mode='w')
    ]
)

def get_chromium_options(browser_path: str, arguments: list, proxy: str = None) -> ChromiumOptions:
    """
    Configures and returns Chromium options, including proxy settings.
    
    :param browser_path: Path to the Chromium browser executable.
    :param arguments: List of arguments for the Chromium browser.
    :param proxy: Proxy address in the form 'host:port', with optional 'username:password@host:port'.
    :return: Configured ChromiumOptions instance.
    """
    options = ChromiumOptions()
    options.set_argument('--auto-open-devtools-for-tabs', 'true')  # we don't need this anymore
    options.set_paths(browser_path=browser_path)
    
    for argument in arguments:
        options.set_argument(argument)
    
    if proxy:
        # Set the proxy argument for Chromium
        options.set_argument(f'--proxy-server={proxy}')
    
    return options

def main():
    # Chromium Browser Path
    isHeadless = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    if isHeadless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")
    
    # Windows Example
    # browser_path = os.getenv('CHROME_PATH', r"C:/Program Files/Google/Chrome/Application/chrome.exe")

    # Optional: Add proxy from environment variable
    proxy = os.getenv('PROXY', "http://rrest751_gmail_com-country-any-sid-bgnirgzi9anklat-filter-medium:bbfefr2wyj@gate.nodemaven.com:8080")  # Example: 'username:password@proxy_host:proxy_port' or 'proxy_host:proxy_port'

    # Arguments to make the browser better for automation and less detectable.
    arguments = [
        "-no-first-run",
        "-force-color-profile=srgb",
        "-metrics-recording-only",
        "-password-store=basic",
        "-use-mock-keychain",
        "-export-tagged-pdf",
        "-no-default-browser-check",
        "-disable-background-mode",
        "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "-deny-permission-prompts",
        "-disable-gpu",
        "-accept-lang=en-US",
    ]

    options = get_chromium_options(browser_path, arguments, proxy)

    # Initialize the browser
    driver = ChromiumPage(addr_or_opts=options)
    try:
        logging.info('Navigating to the demo page.')
        driver.get('https://gota.io/web')

        # Where the bypass starts
        logging.info('Starting Cloudflare bypass.')
        cf_bypasser = CloudflareBypasser(driver)

        # If you are solving an in-page captcha (like the one here: https://seleniumbase.io/apps/turnstile),
        # use cf_bypasser.click_verification_button() directly instead of cf_bypasser.bypass().
        cf_bypasser.bypass()

        logging.info("Enjoy the content!")
        logging.info("Title of the page: %s", driver.title)

        # Sleep for a while to let the user see the result if needed
        time.sleep(5)
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    finally:
        logging.info('Closing the browser.')
        driver.quit()
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()
