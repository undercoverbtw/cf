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

def get_chromium_options(browser_path: str, arguments: list, proxy_server_url: str = true) -> ChromiumOptions:
    """
    Configures and returns Chromium options, including proxy settings if provided.
    
    :param browser_path: Path to the Chromium browser executable.
    :param arguments: List of arguments for the Chromium browser.
    :param proxy_server_url: Proxy address in the form 'host:port', with optional 'username:password@host:port'.
    :return: Configured ChromiumOptions instance.
    """
    options = ChromiumOptions()
    options.set_paths(browser_path=browser_path)
    
    # Set up proxy if provided
    if proxy_server_url:
        options.set_argument(f'--proxy-server={proxy_server_url}')
    
    for argument in arguments:
        options.set_argument(argument)
    
    return options

def main():
    # Check if the browser should run in headless mode
    isHeadless = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    if isHeadless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    # Path to the Chromium browser executable
    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")

    # Proxy URL (you can replace this with your actual proxy URL)
    proxy_server_url = 'gate.nodemaven.com:8080:rrest751_gmail_com-country-any-sid-omljulpnc4ih9da-filter-medium:bbfefr2wyj'



    # Browser arguments to make the browser better for automation and less detectable
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

    # Get configured Chromium options with proxy
    options = get_chromium_options(browser_path, arguments, proxy_server_url)

    # Initialize the browser
    driver = ChromiumPage(addr_or_opts=options)
    
    try:
        logging.info('Navigating to the demo page.')
        driver.get('https://whatsmyip.org')

        # Start Cloudflare bypass
        logging.info('Starting Cloudflare bypass.')
        cf_bypasser = CloudflareBypasser(driver)

        # Bypass Cloudflare if needed
        cf_bypasser.bypass()

        # Log the page title to confirm success
        logging.info("Title of the page: %s", driver.title)

        # Sleep for a while to let the user see the result if needed
        time.sleep(5)

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    
    finally:
        logging.info('Closing the browser.')
        driver.quit()  # Ensure browser closes properly
        
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()
