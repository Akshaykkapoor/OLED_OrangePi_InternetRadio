
###-------comments for testing-----#
#####---messsing up more #####
#import OLED_MPC_Python
import os
import sys
import subprocess
import time
import textwrap
from time       import sleep, strftime
from datetime   import datetime
from subprocess import *
from pyA20.gpio import gpio
from pyA20.gpio import connector
from pyA20.gpio import port
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont, ImageDraw
import sys;
import time
#
#def define_buttons():#Define PIN numbers for switches
gpio.init()
button_prev = port.PA0 #PIN 11
button_next = port.PA14  #PIN 23
button_gsm  = port.PA6  #PIN 7
button_vup  = port.PA18  #PIN 18
button_vdown = port.PA19 #PIN 16
button_pause = port.PA13 #PIN 24

#---------------------------------------------------------------------------#
#def setGPIO():#set the input GPIO for buttons

gpio.setcfg(button_prev, gpio.INPUT)
gpio.setcfg(button_next, gpio.INPUT)
gpio.setcfg(button_gsm,  gpio.INPUT)
gpio.setcfg(button_vup,  gpio.INPUT)
gpio.setcfg(button_vdown, gpio.INPUT)
gpio.setcfg(button_pause, gpio.INPUT)

#Enable pullup resistor

gpio.pullup(button_prev, gpio.PULLUP)
gpio.pullup(button_next, gpio.PULLUP)
gpio.pullup(button_gsm,  gpio.PULLUP)
gpio.pullup(button_vup,  gpio.PULLUP)
gpio.pullup(button_vdown, gpio.PULLUP)
gpio.pullup(button_pause,  gpio.PULLUP)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
# Define Device Type , I2C port and padding characters
device = sh1106(port=0, address=0x3C)  # rev.1 users set port=0
font = ImageFont.load_default()
str_pad = " " * 24

#------------------------------------------------------------------------------#  
def read_switches():#Reading the switch for inputs 

  sw_prev = 1
  sw_next = 1
  sw_gsm  = 1
  sw_vup = 1
  sw_vdown = 1
  sw_pause  = 1


  # Initialize
  got_prev = False
  got_next = False
  got_gsm = False
  got_vup = False
  got_vdown = False
  got_pause = False

  # Read switches
  sw_prev = gpio.input(button_prev)
  sw_next = gpio.input(button_next)
  sw_gsm  = gpio.input(button_gsm)
  sw_vup = gpio.input(button_vup)
  sw_vdown = gpio.input(button_vdown)
  sw_pause  = gpio.input(button_pause)

  if sw_prev == 0:
    got_prev = True
  if sw_next == 0:
    got_next = True
  if sw_gsm  == 0:
    got_gsm = True
  if sw_vup == 0:
    got_vup = True
  if sw_vdown == 0:
    got_vdown = True
  if sw_pause == 0:
    got_pause = True

  if(got_next):
    return 2
  if(got_prev):
    return 1
  if (got_gsm):
    return 3
  if(got_vup):
    return 4
  if(got_vdown):
    return 5
  if (got_pause):
    return 6
    return 0

    sleep(0.4)
  
#----------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------#        
def stream_station():# Reading MPC process status to capture data to show on screen
        process1 = subprocess.Popen('mpc current', shell=True, stdout=subprocess.PIPE)
        status1 = process1.communicate()[0]
        Stream_station = str_pad + status1
        return Stream_station

#----------------------------------------------------------------------------------#
def get_volume(): # Reading MPC process status to capture data to show on screen       
        process2 = subprocess.Popen('mpc volume', shell=True, stdout=subprocess.PIPE)
        Volume_Status = process2.communicate()[0]
        return (Volume_Status)
     
         
#------------------------------------------------------------------------------------# 

#----------------------------------------------------------------------------------#        
def playing_status():# Reading MPC process status to capture data to show on screen
        process1 = subprocess.Popen('mpc', shell=True, stdout=subprocess.PIPE)
        status1 = process1.communicate()[0]
        statusLines = status1.split('\n')
      # Extract the songName (first line)
        #songN = statusLines[0]
        #listN = statusLines[1]
        Playing_status = statusLines[1]
        return Playing_status

#----------------------------------------------------------------------------------#       
               

#------------------------------------------------------------------------------------#
def run_cmd(cmd):#execute the shell command
  p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
  output = p.communicate()[0]
  return output

      

#------------------------------------------------------------------------------------#        
               
def scroll_line1(title1,title2, title3,key_press):# String title is to be scrolled on OLED display  
        for i in range (0, len(title1)):
                lcd_text1 = title1[i:(i+23)]
                key_press = read_switches()
                if key_press != None:
                    print(key_press)#-----just for debugging purposes----------------#
                    Radio()
                with canvas(device) as draw:
                          draw.text((0, 0), lcd_text1, font=font, fill=255)
                          draw.text((0, 20), title2, font=font, fill=255)
                          draw.text((0, 30), title3, font=font, fill=255)
                          time.sleep(0.1)  

#------------------------------------------------------------------------------------#   
#------------------------------------------------------------------------------------#        
               
def display_line2(title2):# String title is to be scrolled on OLED display  
          with canvas(device) as draw:
              draw.text((0, 20), title2, font=font, fill=255)
               
#------------------------------------------------------------------------------------#            

#-------------reading switches-------------------------------------------------------#
def Radio():
    while 1:
        #time.sleep(0.4)
        LCD_Line1 = stream_station()
        LCD_Line2 = get_volume()
        status = playing_status()
        LCD_Line3 = status[:10]
        
        key_value = read_switches()
       
        print(key_value) #--Just for debugging ----#
        if key_value == None:
            time.sleep(0.2)
            #break
            #display_line2(LCD_Line2)
            scroll_line1(LCD_Line1,LCD_Line2,LCD_Line3, key_value)
            
           
        if key_value == 4:
            time.sleep(0.2)
            run_cmd("mpc volume +5")
            LCD_Line2 = get_volume()
            #display_line2(LCD_Line2)
            scroll_line1(LCD_Line1,LCD_Line2,LCD_Line3, key_value)
            
        if key_value == 5:
            time.sleep(0.2)
            run_cmd("mpc volume -5")
            LCD_Line2 = get_volume()
            #display_line2(LCD_Line2)
            scroll_line1(LCD_Line1,LCD_Line2,LCD_Line3, key_value)
            
        if key_value == 6:
            time.sleep(0.2)
            run_cmd("mpc toggle")
            #LCD_Line2 = get_volume()
            #display_line2(LCD_Line2)
            status = playing_status()
            LCD_Line3 = status[:10]
            #split_status = staus[:3]
            #print(status[:10])#---------------just for testing purposes -----#
            #time.sleep(10)
            scroll_line1(LCD_Line1,LCD_Line2,LCD_Line3, key_value)
            
        if key_value == 2:
            time.sleep(0.2)
            run_cmd("mpc next")
            LCD_Line1 = stream_station()
            #display_line2(LCD_Line2)
            scroll_line1(LCD_Line1,LCD_Line2,LCD_Line3, key_value)
            
        if key_value == 1:
            time.sleep(0.2)
            run_cmd("mpc prev")
            LCD_Line1 = stream_station()
            #display_line2(LCD_Line2)
            scroll_line1(LCD_Line1,LCD_Line2,LCD_Line3, key_value)               
    #time.sleep(0.4)
#------------------------------------------------------------------------------------#
#----------Program flow starts from here onwards-------------------------------------#
    
       

Radio()
    
