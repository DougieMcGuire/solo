import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_chrome_driver_path():
    data_file = 'data.txt'
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            for line in file:
                if line.startswith('path='):
                    path = line.split('=', 1)[1].strip().strip('"')
                    if os.path.exists(path):
                        return path
    
    path = input("Please enter the path to your Chrome driver (e.g., D:\\chromedriver-win64\\chromedriver.exe): ")
    path = path.strip().strip('"')
    
    if os.path.isdir(path):
        path = os.path.join(path, 'chromedriver.exe')
    
    with open(data_file, 'w') as file:
        file.write(f"path={path}")
    
    return path

def setup_selenium():
    chrome_driver_path = get_chrome_driver_path()
    
    if not os.path.exists(chrome_driver_path):
        print(f"Error: ChromeDriver not found at {chrome_driver_path}")
        return None

    chrome_options = Options()
    chrome_options.add_argument("--app=https://web.snapchat.com")  # Open in app mode (kiosk-like)
    chrome_options.add_argument("--window-size=1200,800")  # Set specific window size
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-breakpad")
    chrome_options.add_argument("--disable-client-side-phishing-detection")
    chrome_options.add_argument("--disable-component-update")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
    chrome_options.add_argument("--disable-hang-monitor")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-prompt-on-repost")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-web-resources")
    chrome_options.add_argument("--enable-automation")
    chrome_options.add_argument("--enable-fast-unload")
    chrome_options.add_argument("--force-fieldtrials=*BackgroundTracing/default/")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--safebrowsing-disable-auto-update")
    chrome_options.add_argument("--password-store=basic")
    chrome_options.add_argument("--use-mock-keychain")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}\\AppData\\Local\\Google\\Chrome\\User Data")  # Use default profile
    chrome_options.add_argument("--profile-directory=Default")  # Ensure the default profile is used
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.page_load_strategy = 'eager'

    try:
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Selenium: {e}")
        return None

def delete_element(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].remove();", element)
        print(f"Deleted element: {xpath}")
    except Exception as e:
        print(f"Error deleting element {xpath}: {e}")

def expand_element(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].style.width='calc(100% - 340px)'; arguments[0].style.height='100%'; arguments[0].style.position='fixed'; arguments[0].style.top='0'; arguments[0].style.left='0';", element)
        print(f"Expanded element: {xpath}")
    except Exception as e:
        print(f"Error expanding element {xpath}: {e}")

def add_buttons(driver):
    script = """
    // Add a container for the UI elements
    var container = document.createElement('div');
    container.id = 'solo-container';
    container.style.position = 'fixed';
    container.style.top = '10px';
    container.style.right = '10px';
    container.style.width = '300px';
    container.style.height = 'calc(100% - 20px)';
    container.style.padding = '20px';
    container.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    container.style.color = 'white';
    container.style.borderRadius = '10px';
    container.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.5)';
    container.style.zIndex = 1000;
    document.body.appendChild(container);

    // Add a title
    var title = document.createElement('h2');
    title.innerHTML = 'Solo';
    title.style.textAlign = 'center';
    title.style.marginBottom = '20px';
    container.appendChild(title);

    // Add Group Name Input
    var groupNameLabel = document.createElement('label');
    groupNameLabel.innerHTML = 'Group Name:';
    groupNameLabel.style.display = 'block';
    groupNameLabel.style.marginBottom = '5px';
    container.appendChild(groupNameLabel);

    var groupNameInput = document.createElement('input');
    groupNameInput.type = 'text';
    groupNameInput.placeholder = 'Enter group name';
    groupNameInput.id = 'groupNameInput';
    groupNameInput.style.width = '100%';
    groupNameInput.style.padding = '10px';
    groupNameInput.style.marginBottom = '20px';
    groupNameInput.style.border = 'none';
    groupNameInput.style.borderRadius = '5px';
    groupNameInput.style.backgroundColor = '#333';
    groupNameInput.style.color = 'white';
    container.appendChild(groupNameInput);

    // Add Speed Slider
    var speedLabel = document.createElement('label');
    speedLabel.innerHTML = 'Speed:';
    speedLabel.style.display = 'block';
    speedLabel.style.marginBottom = '5px';
    container.appendChild(speedLabel);

    var speedSlider = document.createElement('input');
    speedSlider.type = 'range';
    speedSlider.min = '100';
    speedSlider.max = '2000';
    speedSlider.value = '500';
    speedSlider.id = 'speedSlider';
    speedSlider.style.width = '100%';
    speedSlider.style.marginBottom = '20px';
    container.appendChild(speedSlider);

    // Add Timer Dropdown
    var timerLabel = document.createElement('label');
    timerLabel.innerHTML = 'Run for:';
    timerLabel.style.display = 'block';
    timerLabel.style.marginTop = '20px';
    timerLabel.style.marginBottom = '5px';
    container.appendChild(timerLabel);

    var timerDropdown = document.createElement('select');
    timerDropdown.id = 'timerDropdown';
    timerDropdown.style.width = '100%';
    timerDropdown.style.padding = '10px';
    timerDropdown.style.marginBottom = '20px';
    timerDropdown.style.border = 'none';
    timerDropdown.style.borderRadius = '5px';
    timerDropdown.style.backgroundColor = '#333';
    timerDropdown.style.color = 'white';

    var timerOptions = [
        { value: 0, text: 'Until Stopped' },
        { value: 60000, text: '1 minute' },
        { value: 300000, text: '5 minutes' },
        { value: 1800000, text: '30 minutes' },
        { value: 3600000, text: '1 hour' },
        { value: 7200000, text: '2 hours' },
        { value: 10800000, text: '3 hours' },
        { value: 14400000, text: '4 hours' },
        { value: 18000000, text: '5 hours' },
        { value: 21600000, text: '6 hours' },
        { value: 25200000, text: '7 hours' },
        { value: 28800000, text: '8 hours' },
        { value: 32400000, text: '9 hours' },
        { value: 36000000, text: '10 hours' },
        { value: 39600000, text: '11 hours' },
        { value: 43200000, text: '12 hours' },
        { value: 86400000, text: '1 day' }
    ];

    timerOptions.forEach(function(option) {
        var opt = document.createElement('option');
        opt.value = option.value;
        opt.innerHTML = option.text;
        timerDropdown.appendChild(opt);
    });

    container.appendChild(timerDropdown);

    // Add Run Sequence Button
    var runSequenceButton = document.createElement('button');
    runSequenceButton.innerHTML = 'Start';
    runSequenceButton.style.width = '100%';
    runSequenceButton.style.padding = '10px';
    runSequenceButton.style.border = 'none';
    runSequenceButton.style.borderRadius = '5px';
    runSequenceButton.style.backgroundColor = '#28a745';
    runSequenceButton.style.color = 'white';
    runSequenceButton.style.fontSize = '16px';
    runSequenceButton.style.cursor = 'pointer';
    container.appendChild(runSequenceButton);

    // Add Snaps Sent Counter
    var snapsSentLabel = document.createElement('label');
    snapsSentLabel.innerHTML = 'Snaps Sent:';
    snapsSentLabel.style.display = 'block';
    snapsSentLabel.style.marginTop = '20px';
    snapsSentLabel.style.marginBottom = '5px';
    container.appendChild(snapsSentLabel);

    var snapsSentCounter = document.createElement('div');
    snapsSentCounter.id = 'snapsSentCounter';
    snapsSentCounter.innerHTML = '0';
    snapsSentCounter.style.fontSize = '24px';
    snapsSentCounter.style.fontWeight = 'bold';
    snapsSentCounter.style.textAlign = 'center';
    snapsSentCounter.style.marginBottom = '20px';
    snapsSentCounter.style.color = '#28a745';
    container.appendChild(snapsSentCounter);

    // Add Snaps per Second Counter
    var snapsPerSecondLabel = document.createElement('label');
    snapsPerSecondLabel.innerHTML = 'Snaps per Second:';
    snapsPerSecondLabel.style.display = 'block';
    snapsPerSecondLabel.style.marginBottom = '5px';
    container.appendChild(snapsPerSecondLabel);

    var snapsPerSecondCounter = document.createElement('div');
    snapsPerSecondCounter.id = 'snapsPerSecondCounter';
    snapsPerSecondCounter.innerHTML = '0.00';
    snapsPerSecondCounter.style.fontSize = '24px';
    snapsPerSecondCounter.style.fontWeight = 'bold';
    snapsPerSecondCounter.style.textAlign = 'center';
    snapsPerSecondCounter.style.color = '#17a2b8';
    container.appendChild(snapsPerSecondCounter);

    // Add Night Mode Button
    var nightModeButton = document.createElement('button');
    nightModeButton.innerHTML = 'Night Mode';
    nightModeButton.style.width = '100%';
    nightModeButton.style.padding = '10px';
    nightModeButton.style.border = 'none';
    nightModeButton.style.borderRadius = '5px';
    nightModeButton.style.backgroundColor = '#6c757d';
    nightModeButton.style.color = 'white';
    nightModeButton.style.fontSize = '16px';
    nightModeButton.style.cursor = 'pointer';
    nightModeButton.style.marginTop = '20px';
    container.appendChild(nightModeButton);

    // Add Credits Button
    var creditsButton = document.createElement('button');
    creditsButton.innerHTML = 'Credits';
    creditsButton.style.width = '100%';
    creditsButton.style.padding = '10px';
    creditsButton.style.border = 'none';
    creditsButton.style.borderRadius = '5px';
    creditsButton.style.backgroundColor = '#17a2b8';
    creditsButton.style.color = 'white';
    creditsButton.style.fontSize = '16px';
    creditsButton.style.cursor = 'pointer';
    creditsButton.style.marginTop = '10px';
    container.appendChild(creditsButton);

    creditsButton.onclick = function() {
        window.open('https://dougie.wtf', '_blank');
    };

    // Night Mode functionality
    var isNightMode = false;
    var nightModeOverlay;

    nightModeButton.onclick = function() {
        if (!isNightMode) {
            // Enter Night Mode
            nightModeOverlay = document.createElement('div');
            nightModeOverlay.style.position = 'fixed';
            nightModeOverlay.style.top = '0';
            nightModeOverlay.style.left = '0';
            nightModeOverlay.style.width = '100%';
            nightModeOverlay.style.height = '100%';
            nightModeOverlay.style.backgroundColor = 'black';
            nightModeOverlay.style.zIndex = '9999';
            nightModeOverlay.style.display = 'flex';
            nightModeOverlay.style.flexDirection = 'column';
            nightModeOverlay.style.justifyContent = 'center';
            nightModeOverlay.style.alignItems = 'center';

            var nightModeCounter = document.createElement('div');
            nightModeCounter.id = 'nightModeCounter';
            nightModeCounter.innerHTML = document.getElementById('snapsSentCounter').innerHTML;
            nightModeCounter.style.fontSize = '48px';
            nightModeCounter.style.fontWeight = 'bold';
            nightModeCounter.style.color = 'white';
            nightModeCounter.style.marginBottom = '20px';
            nightModeOverlay.appendChild(nightModeCounter);

            var exitNightModeButton = document.createElement('button');
            exitNightModeButton.innerHTML = 'Exit Night Mode';
            exitNightModeButton.style.padding = '10px 20px';
            exitNightModeButton.style.border = 'none';
            exitNightModeButton.style.borderRadius = '5px';
            exitNightModeButton.style.backgroundColor = '#28a745';
            exitNightModeButton.style.color = 'white';
            exitNightModeButton.style.fontSize = '16px';
            exitNightModeButton.style.cursor = 'pointer';
            exitNightModeButton.onclick = function() {
                document.body.removeChild(nightModeOverlay);
                isNightMode = false;
            };
            nightModeOverlay.appendChild(exitNightModeButton);

            document.body.appendChild(nightModeOverlay);
            isNightMode = true;

            // Update night mode counter
            var nightModeObserver = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting && isNightMode) {
                    document.getElementById('nightModeCounter').innerHTML = document.getElementById('snapsSentCounter').innerHTML;
                }
            }, { threshold: 1 });

            nightModeObserver.observe(nightModeCounter);
        }
    };

    var running = false;
    var intervalId;
    var snapsSent = 0;
    var startTime;
    var timerEndTime;
    var speed = parseInt(document.getElementById('speedSlider').value);

    function updateCounters() {
        requestAnimationFrame(function() {
            document.getElementById('snapsSentCounter').textContent = snapsSent;
            var elapsedTime = (performance.now() - startTime) / 1000;
            var snapsPerSecond = snapsSent / elapsedTime;
            document.getElementById('snapsPerSecondCounter').textContent = snapsPerSecond.toFixed(2);
        });
    }

    var debounceTimer;
    speedSlider.oninput = function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            speed = parseInt(speedSlider.value);
            if (running) {
                clearInterval(intervalId);
                intervalId = setInterval(runSequence, speed === 2000 ? 0 : speed * 5);
            }
        }, 100);
    };

    runSequenceButton.onclick = function() {
        if (running) {
            clearInterval(intervalId);
            runSequenceButton.innerHTML = 'Start';
            runSequenceButton.style.backgroundColor = '#28a745';
            running = false;
        } else {
            var timerDuration = parseInt(document.getElementById('timerDropdown').value);
            runSequenceButton.innerHTML = 'Stop';
            runSequenceButton.style.backgroundColor = '#dc3545';
            running = true;
            snapsSent = 0;
            startTime = performance.now();
            timerEndTime = timerDuration > 0 ? startTime + timerDuration : 0;

            function runSequence() {
                if (!running) return;
                
                if (timerEndTime > 0 && performance.now() >= timerEndTime) {
                    clearInterval(intervalId);
                    runSequenceButton.innerHTML = 'Start';
                    runSequenceButton.style.backgroundColor = '#28a745';
                    running = false;
                    return;
                }

                var cameraButton = document.evaluate("/html/body/main/div[1]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/button[1]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                var sendToButton = document.evaluate("/html/body/main/div[1]/div/div/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/button[2]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                var groupName = document.getElementById('groupNameInput').value;
                var groupButton = document.evaluate("//*[contains(text(), '" + groupName + "')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                var finalSendButton = document.evaluate("/html/body/main/div[1]/div/div/div[1]/div/div/div[1]/div/div/div/div/div[1]/div/form/div[2]/button", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

                if (cameraButton) cameraButton.click();
                var checkSendToButton = setInterval(function() {
                    var sendToButton = document.evaluate("/html/body/main/div[1]/div/div/div[1]/div/div/div[1]/div/div/div/div/div[2]/div[2]/button[2]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (sendToButton) {
                        sendToButton.click();
                        clearInterval(checkSendToButton);
                        var checkGroupButton = setInterval(function() {
                            var groupButton = document.evaluate("//*[contains(text(), '" + groupName + "')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (groupButton) {
                                groupButton.click();
                                clearInterval(checkGroupButton);
                                var checkFinalSendButton = setInterval(function() {
                                    var finalSendButton = document.evaluate("/html/body/main/div[1]/div/div/div[1]/div/div/div[1]/div/div/div/div/div[1]/div/form/div[2]/button", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                    if (finalSendButton) {
                                        finalSendButton.click();
                                        clearInterval(checkFinalSendButton);
                                        // Increment the counter
                                        snapsSent++;
                                        updateCounters();
                                    }
                                }, speed === 1000 ? 0 : speed);
                            }
                        }, speed === 1000 ? 0 : speed);
                    }
                }, speed === 1000 ? 0 : speed);

                requestIdleCallback(runSequence, { timeout: speed === 1000 ? 0 : speed * 5 });
            }

            intervalId = setInterval(runSequence, speed === 2000 ? 0 : speed * 5);
        }
    };

    var snapObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                // Check if the added node is the confirmation message for sent snap
                if (mutation.addedNodes[0].textContent.includes("Snap sent")) {
                    snapsSent++;
                    updateCounters();
                }
            }
        });
    });

    // Start observing the document with the configured parameters
    snapObserver.observe(document.body, { childList: true, subtree: true });

    document.body.appendChild(container);
    """
    driver.execute_script(script)
    print("Added buttons, input, counters, Night Mode, Credits, and Timer to the page")

if __name__ == "__main__":
    driver = setup_selenium()
    if driver:
        try:
            driver.get("https://web.snapchat.com")
            
            # Delete specified elements
            delete_element(driver, "/html/body/main/div[1]/div[2]")
            delete_element(driver, "/html/body/main/div[1]/div[1]")
            delete_element(driver, "/html/body/main/div[1]/div/div/div[2]/div/div[1]")
            delete_element(driver, "/html/body/main/div[1]/div/div/div[2]")  # New element to delete
            
            # Expand specified element
            expand_element(driver, "/html/body/main/div[1]/div/div/div")
            
            # Add buttons and input to the page
            add_buttons(driver)
            
            while True:
                try:
                    driver.window_handles
                except:
                    driver.quit()
                    sys.exit()
        finally:
            driver.quit()
    else:
        print("Failed to initialize WebDriver.")
