import threading
import time
from random import randint, shuffle, uniform

import keyboard
import numpy as np
import pyautogui
from PIL import ImageGrab



class Bot:
    

    def __init__(self):
        self.bot_on = True
        self.char = input('paladin or mage?')
        self.hotkey = input('select hotkey to be used')
        self.not_enough_mana = (26, 26, 26) # pixels where mana bar is grey (not enough mana)
        self.enough_mana = (114,96,255)
        self.empty_screen = (24,23,24) # pixels of battle list when nobody is around
        self.nobody_on_screen = True
        self.region_blanks = (1520,0,450,1180)
        self.hand = self.find_hand()

    def run_bot(self):
        ''' main class to run the bot'''
        pyautogui.FAILSAFE = True ## moving to the top left corner turns the bot off

        time.sleep(2) # pause to select medivia's screen

        if self.char[0].lower() == "p":
            while self.bot_on is True:
                self.eat_food()
                self.anti_afk()
                time.sleep(1)
                self.use_spell()
                self.run_pz_checks()
        if self.char[0].lower() == "m":
            while self.bot_on is True:
                self.eat_food()
                self.anti_afk()
                time.sleep(1)
                self.make_rune()
                # self.run_pz_checks()

    def make_rune(self):
        
        if self._check_mana() == self.enough_mana:
            rng = randint(3,7)
            print(rng)
            for _ in range(rng):
                self.move_blankand_press()

                

    def move_blankand_press(self):

        blank = self.find_blank()

        pyautogui.moveTo(blank)
        pyautogui.click()
        pyautogui.dragTo(self.hand,button= 'left', duration =0.9)
        time.sleep(0.1)
        keyboard.press_and_release(self.hotkey)
        pyautogui.click()
        pyautogui.dragTo(blank,button= 'left', duration =0.4)
        time.sleep(1)   

    def find_blank(self):

        blank = pyautogui.locateCenterOnScreen("blank_rune.png", region=self.region_blanks, confidence = 0.95)

        if blank is None:
            print('bank is none')
            self.logout()                    
        else:
            print('blank found')
            return blank

    def find_hand(self):
        hand = pyautogui.locateCenterOnScreen('hand.png', region = self.region_blanks, confidence = 0.90)
        return hand

    def eat_food(self):
        ''' eat food (left side of the screen - mushroom)'''
        food = self._locate_food_screen()
        if type(food) != None:
            rng_factor = randint(1,60)
            if rng_factor == 2:
                pyautogui.moveTo(food)
                pyautogui.doubleClick(button='right')
            else:
                pass
        else:
            self._move_to_safety() # moves to safety, switches the bot off.
            self.logout() # logout function

    def use_spell(self):
        ''' uses a hotkey if mana is high enough'''
        if self._check_mana() == self.enough_mana:
            keyboard.press_and_release(self.hotkey)
        else: 
            pass 

    def run_pz_checks(self):
        ''' runs pz checks - moves char back to safety or out from pz depending
        on the battle list pixels (if chard showed up or not)'''
        self._move_to_safety()
        while self.nobody_on_screen is False and self.bot_on is True:
            self._move_out_from_pz()
    
    def anti_afk(self):
        ' anti afk movements + rng element to make char moves rarely'
        random_delays = []
        arrow_keys = ['left','right','up','down']
        
        
        for i in range(1,6):#randomizing variable for delays in between of movements
            rng = uniform(0.13,0.4)
            random_delays.append(rng)
            shuffle(arrow_keys)
        
        rng_move = randint(1,400)
        
        if rng_move ==1:
            keyboard.press('ctrl')
            pyautogui.press(arrow_keys[0])
            time.sleep(random_delays[0])
            pyautogui.press(arrow_keys[0])
            time.sleep(random_delays[3])
            pyautogui.press(arrow_keys[1])
            time.sleep(random_delays[4])
            pyautogui.press('down')#so that we always end up facing south
            keyboard.release('ctrl')
        
        elif rng_move ==2:
            keyboard.press('ctrl')
            pyautogui.press(arrow_keys[2])
            time.sleep(random_delays[1])
            pyautogui.press(arrow_keys[3])
            time.sleep(random_delays[2])
            pyautogui.press('down') #so that we always end up facing south
            keyboard.release('ctrl')
        else:
            pass

    def _move_to_safety(self):
        '''moves char to safety if sb shows up on the screen
        sets noboy_on_screen to False'''
        if self._check_pixels_battle_list() != self.empty_screen:

            time.sleep(3)
            pyautogui.press('up')
            self.nobody_on_screen = False
    
    def _move_out_from_pz(self):
        print('break while char is in pz - 120 sec and recheck')
        time.sleep(15) # break so that code does not run like mad when char in pz
        if self._check_pixels_battle_list() == self.empty_screen:
            pyautogui.press('down')
            self.nobody_on_screen = True

    def _check_pixels_battle_list(self):
        '''function gives x and y coordinates of the food (mushroom) on the screen (left side)'''
        cord_x,cord_y = self._locate_1spot_battle_list()
        pxls = ImageGrab.grab().getpixel((cord_x,cord_y))
        print(f' pxls of battle list {pxls}')
        return pxls


    def _locate_1spot_battle_list(self):
        ''' locates battle list - will be used to see if somebody pops up on the screen 
        (battle list on the right side of the screen)'''
        
        battle_list = pyautogui.locateCenterOnScreen("battle_list.png", region = (1400,0,500,1170),confidence =0.90)
        x,y = battle_list # battle list center x,y
        x = x-30 # 30 pixels to the left 
        y = y +30 # 30 pixels towards bottom

        return (x,y)
    
    def _check_mana(self):
        ''' checks mana - will be used for using spell function - health bar
        needs to be set to the top right corner of the screen'''
        
        mana = pyautogui.screenshot('ss_mana.png',region = (1894,114,1,1))
        pxls_mana = mana.getpixel((0,0)) # 0,0 because the ss has only 1 pixel
        return pxls_mana

    def _locate_food_screen(self):
        '''locates mushroom on the right side of the screen and returns it'''

        food = pyautogui.locateCenterOnScreen('ham.png', region = self.region_blanks, confidence = 0.80)
        if food != None:
            return food
        else:
            food = pyautogui.locateCenterOnScreen("mushroom.png",region = (0,0,400,1170),confidence =0.50)
            return food
   
    
    def logout(self):
        '''log out '''
        keyboard.press('ctrl')
        keyboard.press('q')
        time.sleep(0.5)
        keyboard.release('ctrl')
        print('bot turned off')
        time.sleep(0.1)
        self.bot_on = False
        
       

if __name__ == "__main__":
    bot = Bot()
    bot.run_bot()