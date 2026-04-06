import time
from selenium.webdriver.chrome.service import Service
import logging
from selenium.webdriver.common.by import By
from selenium import webdriver
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# CHANGEZ CE LIEN AVEC VIDEO

TIKTOK_URL   = "https://www.tiktok.com/@user/video/1234567890123456789"
SERVICE_URL  = "https://zefame.com/free-tiktok-views"
INTERVAL_MIN = 5
COUNTDOWN_S  = 65
HEADLESS     = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)


def make_driver(headless: bool) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def dismiss_maintenance_popup(driver: webdriver.Chrome):
    try:
        btns = driver.find_elements(By.XPATH,
            "//button[contains(text(),'Compris')] | //button[contains(text(),'OK')] | //button[contains(text(),'Fermer')]"
        )
        for btn in btns:
            try:
                js_click(driver, btn)
                log.info("Popup maintenance ferme.")
            except Exception:
                pass
        time.sleep(1)
    except Exception:
        pass


def parse_cooldown(text: str) -> int:
    minutes = 0
    seconds = 0
    m = re.search(r'(\d+)\s*m', text)
    s = re.search(r'(\d+)\s*s', text)
    if m:
        minutes = int(m.group(1))
    if s:
        seconds = int(s.group(1))
    return minutes * 60 + seconds


def check_cooldown(driver: webdriver.Chrome) -> int:
    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "attendre encore" in page_text.lower() or "wait" in page_text.lower():
            wait_s = parse_cooldown(page_text)
            if wait_s > 0:
                return wait_s
    except Exception:
        pass
    return 0


def run_cycle(driver: webdriver.Chrome, cycle: int) -> bool:
    log.info(f"Cycle #{cycle}")
    driver.get(SERVICE_URL)
    time.sleep(3)

    dismiss_maintenance_popup(driver)

    try:
        wait = WebDriverWait(driver, 15)
        input_field = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='text'], input[placeholder*='lien'], input[placeholder*='TikTok'], input[placeholder*='tiktok'], input[placeholder*='Collez']")
        ))
        driver.execute_script("arguments[0].value = '';", input_field)
        input_field.send_keys(TIKTOK_URL)
        log.info("Lien colle dans le champ.")
    except TimeoutException:
        log.error("Champ de saisie introuvable.")
        return False

    try:
        btn = driver.find_element(By.XPATH,
            "//button[contains(text(),'Obtenir')] | //input[@value='Obtenir']"
        )
        js_click(driver, btn)
        log.info("Bouton Obtenir clique.")
    except NoSuchElementException:
        log.error("Bouton Obtenir pas la.")
        return False

    time.sleep(2)

    cooldown = check_cooldown(driver)
    if cooldown > 0:
        log.warning(f"Cooldown detecte : {cooldown}s d'attente.")
        log.info(f"Pause de {cooldown + 5}s...")
        time.sleep(cooldown + 5)
        log.info("Reprise apres cooldown.")
        return run_cycle(driver, cycle)

    log.info(f"Compte rebours en cours ({COUNTDOWN_S}s)...")
    for remaining in range(COUNTDOWN_S, 0, -5):
        log.info(f"{remaining}s restantes...")
        time.sleep(5)

    try:
        wait2 = WebDriverWait(driver, 10)
        success = wait2.until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Succes') or contains(text(),'succes') or contains(text(),'obtiendrez')]")
        ))
        log.info(f"Succes : {success.text.strip()[:80]}")
    except TimeoutException:
        log.warning("Message de succes non detecte.")

    try:
        back_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(),'Retour')] | //button[contains(text(),'Retour')]")
        ))
        js_click(driver, back_btn)
        log.info("Retour aux service.")
    except TimeoutException:
        log.info("Bouton Retour pas trouve.")

    return True


def main():
    log.info("=" * 50)
    log.info(" Vue tiktok")
    log.info(f"Video  : {TIKTOK_URL}")
    log.info(f"Cycle  : toutes les {INTERVAL_MIN} min")
    log.info("=" * 50)

    driver = make_driver(HEADLESS)
    cycle = 0

    try:
        while True:
            cycle += 1
            success = run_cycle(driver, cycle)
            status = "OK" if success else "ERREUR"
            log.info(f"{status} - prochain cycle dans {INTERVAL_MIN} min.\n")
            time.sleep(INTERVAL_MIN * 60)

    except KeyboardInterrupt:
        log.info("Shut down.")
    finally:
        driver.quit()
        log.info("Navigateur ferme.")


if __name__ == "__main__":
    main()
