'''
Facebook B-Day Messager
Written by Austin Born - 7/20/18

This is a python experiment to see if I can automate birthday messages on Facebook
using pyautogui for mouse control and image recognition, and the Windows Task 
Scheduler to run it. I may continue this with a beefed-up Scrapy version some day,
but due to the task scheduler's unfortunate shortcomings, I am putting it on hold
for now. Maybe I should get back into HFT bots...

Important note: Task Security option must be set to only run 
                when user is logged on. If on or not is chosen, 
                pyautogui will not work. Took 2 days to figure out...
                Essentially, if the other option is chosen, the program
                will be executed w/o a UI, rendering anything gui-related
                useless.
'''

import pyautogui, pywinauto, time, win32gui, re, logging

LOG_NAME = "Logs/Log "+time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())+".log"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=LOG_NAME,
                    filemode='w')

logging.debug('Entering main function')

# Main function body
if __name__ == "__main__":

    logging.debug('Taking screenshot')

    # Open chrome
    logging.debug('Opening chrome')
    app = pywinauto.application.Application().Start(cmd_line=u'"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" ')
    chromewidgetwin = app.Chrome_WidgetWin_1
    time.sleep(3)
    logging.debug('Setting chrome in foreground')
    hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", None)
    win32gui.SetForegroundWindow(hwnd)    

    # GO to FB Birthdays
    logging.debug('Going to FB Birthdays')
    pyautogui.click(260, 70)
    pyautogui.typewrite('Facebook.com')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.click(200, 570)
    time.sleep(4)
    pyautogui.click(200, 420)
    time.sleep(4)

    # Initialization
    logging.debug('Running through message loop')
    recentBirthdays = pyautogui.locateOnScreen('Images/FBRecentBDays.png', region=(420, 200, 240, 900))
    upcomingBirthdays = pyautogui.locateOnScreen('Images/FBRecentBDays.png', region=(420, 200, 240, 900))
    if recentBirthdays is None:
        rbflag = False
    else:
        rbflag = True
    writeMessage = pyautogui.locateOnScreen('Images/FBWriteMessage.png', region=(560, 200, 80, 900))

    # While loop
    while True:
        if recentBirthdays is not None:
            rbflag = True
        if (recentBirthdays is not None) and (writeMessage is not None) and (recentBirthdays[1] > writeMessage[1]):
            pyautogui.scroll(int((216-writeMessage[1])/2))
            time.sleep(1)
            writeMessage = pyautogui.locateCenterOnScreen('Images/FBWriteMessage.png', region=(560, 200, 80, 900))
            pyautogui.click(writeMessage)
            pyautogui.typewrite('Happy Birthday!')
            pyautogui.press('Enter')
            logging.debug('Entered birthday message on timeline')
            time.sleep(1)
            pyautogui.scroll(-20)
            time.sleep(1)
            writeMessage = pyautogui.locateOnScreen('Images/FBWriteMessage.png', region=(560, 200, 80, 900))
            recentBirthdays = pyautogui.locateOnScreen('Images/FBRecentBDays.png', region=(420, 200, 240, 900))
        elif (recentBirthdays is None) and (writeMessage is not None) and rbflag is False:
            pyautogui.scroll(int((216-writeMessage[1])/2))
            time.sleep(1)
            writeMessage = pyautogui.locateCenterOnScreen('Images/FBWriteMessage.png', region=(560, 200, 80, 900))
            pyautogui.click(writeMessage)
            pyautogui.typewrite('Happy Birthday!')
            pyautogui.press('Enter')
            logging.debug('Entered birthday message on timeline')
            time.sleep(1)
            pyautogui.scroll(-20)
            time.sleep(1)
            writeMessage = pyautogui.locateOnScreen('Images/FBWriteMessage.png', region=(560, 200, 80, 900))
            recentBirthdays = pyautogui.locateOnScreen('Images/FBRecentBDays.png', region=(420, 200, 240, 900))
        else:
            logging.debug('Finished messages')
            break
        
    app.kill()
    logging.debug('Successfully killed application')
