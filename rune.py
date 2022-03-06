import pyautogui

class Rune():
    ''' class defining runes'''

    def __init__(self):
        self.region_blanks = (1520,0,450,1180)
        self.hand = self.find_hand()
    
    
    def make_rune(self):
        
        blank = self.find_blank()

        pyautogui.moveTo(blank)
        pyautogui.click()
        pyautogui.dragTo(self.hand,button= 'left', duration =0.5)

        self.use_spell()
        pyautogui.click()
        pyautogui.dragTo(blank,button= 'left', duration =0.5)


    def find_blank(self):

        blank = pyautogui.locateCenterOnScreen("blank_rune.png", region = self.region_blanks, confidence = 0.95)

        if blank is None:
            self.logout()
        else:
            return blank
    def find_hand(self):
        hand = pyautogui.locateCenterOnScreen('hand.png', region = self.region_blanks, confidence = 0.90)
        return hand

    

x = Rune()

x.make_rune()