#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##=========================================================
##  app.py                                    21 Apr 2017
##
##  Generates a Kivy Atlas from spritesheet
##
##  Eli Leigh Innis
##  Twitter :  @ Doyousketch2
##  Email :  Doyousketch2 @ yahoo.com
##
##  GNU GPLv3                 gnu.org/licenses/gpl-3.0.html
##=========================================================
##  required  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##  you'll need kivy:
##  (debian)
##        sudo pip3 install kivy
##  (linux)
##        sudo python3 -m pip install kivy
##  (mac)
##        sudo easy_install pip
##        python -m pip install kivy
##  (win)
##        py -m pip install kivy
##=========================================================
##  libs  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import  os
import  sys

from  kivy .app           import  App                ## GUI
from  kivy .graphics       import *
from  kivy .lang            import  Builder
from  kivy .uix .image       import  Image
from  kivy .uix  .boxlayout   import  BoxLayout
from  kivy .uix    .behaviors  import  DragBehavior
from  kivy .graphics .texture   import  Texture
from  kivy .graphics             import  Color, Rectangle
from  kivy .uix .screenmanager   import  ScreenManager, Screen
from  kivy .uix .screenmanager  import  NoTransition
from  kivy .core .window       import  Window
from  kivy .uix .textinput    import  TextInput
from  kivy .uix .label       import  Label
from  kivy .uix .button     import  Button

##=========================================================
##  config  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WIDTH  = 800
HEIGHT  = 600

##=========================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Window .size  = ( WIDTH, HEIGHT )
Builder .load_file('./atlas.kv')   ## Kivy is buggy, needed for ScreenManager


class FileScreen(Screen):

  def select(self, *args):
    self .selection  = args[1][0]
    try:
      app .selected  = self .selection
      self .label .text  = app .selected
    except:  pass


  def choice(self):

    app .path,  app .ext  = os .path .splitext( app .selected )

    if '/' in app .path:   ## Unix, Linux, Android, Mac OSX, iOS
      app .filename  = app .path .split('/')[-1]
    else:   ## the other OS
      app .filename  = app .path .split('\\')[-1]
    print(app .filename)

    app .img  = Image( source = app .selected )
    app .tex  = app .img .texture

    app .X  = app .img .texture_size[0]
    app .Y  = app .img .texture_size[1]

    app .imgW  = app .img .texture_size[0]  = app .img .texture_size[0] * 2
    app .imgH  = app .img .texture_size[1]  = app .img .texture_size[1] * 2

    Window .size  = ( app .imgW,  app .imgH )
    self .manager .switch_to( TileScreen() )



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TileScreen(Screen):

  def cross(self):

    with self .canvas:
      Color( 1, 0, 0,  0.2 )   ## red highlight

      posit  = ( app .X,  0 )
      siz  = ( app .high,  app .imgH )
      app .recthoriz  = Rectangle( pos = posit,  size = siz )

      posit  = ( 0,  app .Y )
      siz  = ( app .imgW,  app .wide )
      app .rectvert  = Rectangle( pos = posit,  size = siz )


      Color( 0, 0, 0,  0.5 )   ## black padding

      posit  = ( app .X + app .high,  0 )
      siz  = ( app .padX,  app .imgH )
      app .horizpad  = Rectangle( pos = posit,  size = siz )

      posit  = ( 0,  app .Y )
      siz  = ( app .imgW,  -app .padY )
      app .vertpad  = Rectangle( pos = posit,  size = siz )


  def ok(self):
    app .eachX  = app .wide + app .padX
    app .eachY  = app .high + app .padY

    app .originX  = app .recthoriz .pos[0]
    app .originY  = app .rectvert .pos[1]

    while app .originX - app .eachX > 0:
      app .originX  -= app .eachX

    while app .originY + app .eachY < app .imgH:
      app .originY  += app .eachY

    self .manager .switch_to( OkayScreen() )


  def updateX(self):
    app .recthoriz .pos   = ( app .X,  0 )
    app .recthoriz .size  = ( app .wide,  app .imgH )

    app .horizpad  .pos   = ( app .X + app .wide,  0 )
    app .horizpad  .size  = ( app .padX,  app .imgH )


  def updateY(self):
    app .rectvert .pos   = ( 0,  app .imgH - app .Y )
    app .rectvert .size  = ( app .imgW,  app .high )

    app .vertpad  .pos   = ( 0,  app .imgH - app .Y )
    app .vertpad  .size  = ( app .imgW,  -app .padY )


  def horiz(self, x, w):
    app .X  += x
    app .wide  += w
    if app .X < 0:  app .X  = 0
    if app .wide < 0:  app .wide  = 0
    TileScreen .updateX(self)


  def vert(self, y, h):
    app .Y  -= y
    app .high  += h
    if app .Y < 0:  app .Y  = 0
    if app .high < 0:  app .high  = 0
    TileScreen .updateY(self)


  def gapx(self, x):
    app .padX  += x
    if app .padX < 0:  app .padX  = 0
    TileScreen .updateX(self)


  def gapy(self, y):
    app .padY  -= y
    if app .padY < 0:  app .padY  = 0
    TileScreen .updateY(self)



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OkayScreen(Screen):

  def back(self):
    self .manager .switch_to( TileScreen() )


  def populate(self):

    if len(app .origin) == 0:
      while app .originX + (app .columns + 1) * app .eachX < app .imgW:
        app .columns += 1

      while app .originY - (app .rows + 1) * app .eachY > 0:
        app .rows += 1

      howmany  = int(app .columns * app .rows)

      app .sprite = [0] * howmany
      app .origin = [0] * howmany
      app .posX   = [0] * howmany
      app .posY   = [0] * howmany
      app .name   = [0] * howmany
      app .ribbon = [0] * 4

      alphabet  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',

                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
      i  = -1
      for y in range(app .rows):
        for x in range(app .columns):
          i += 1
          if y > len(alphabet):   ## so we don't run out of letters;  A, AA, AAA, AAAA, etc.
            a  = alphabet[y % len(alphabet)] * int(y / len(alphabet) + 1)
          else:
            a  = alphabet[y]

          app .name[i]  = '%s%s' % (a,  x + 1)

    OkayScreen .update(self)


  def toggle(self):

    if app .naming < 1:
      if len(app .origin) > 0:
        mX  = Window .mouse_pos[0]
        mY  = Window .mouse_pos[1]

        xx  = int(( mX - app .originX ) / app .eachX )
        yy  = int(( app .originY - mY ) / app .eachY )

        i  = yy * app .columns + xx

        if app .sprite[i] .pos == (app .imgW,  app .imgH):
          app .sprite[i] .pos  = app .origin[i]
        else:
          app .origin[i]  = app .sprite[i] .pos
          app .sprite[i] .pos  = (app .imgW,  app .imgH)


  def nametiles(self):
    ## Kivy sux again...  I dunno what the trick is.
    ## They let you remove some widgets, but not others?
    '''
    self .remove_widget( self .ids .rename )
    self .remove_widget( self .ids .okhp )
    self .remove_widget( self .ids .okhm )
    self .remove_widget( self .ids .okhup )
    self .remove_widget( self .ids .okhdn )
    self .remove_widget( self .ids .okhgp )
    self .remove_widget( self .ids .okhgm )

    self .remove_widget( self .ids .okvp )
    self .remove_widget( self .ids .okvm )
    self .remove_widget( self .ids .okvl )
    self .remove_widget( self .ids .okvr )
    self .remove_widget( self .ids .okvgp )
    self .remove_widget( self .ids .okvgm )
    '''
     ## instead, I cheated, by shoving all these buttons
     ## to the top-right corner of the screen,
     ## so they still exist, you just can't see them.
     ## in the .kv file:   pos_hint  = { 'x': 1, 'y': 1 }
    app .naming = 1


  def gettext(self):
    print(app .textinput .text)
    app .name[app .i]  = app .textinput .text

##  kivy doesn't allow you to pass args to button functions,
##  so these are simple redundant 'callbacks'

  def appendup(self):
    app .textinput .text += app .ribbon[0]


  def appenddown(self):
    app .textinput .text += app .ribbon[1]


  def appendleft(self):
    app .textinput .text += app .ribbon[2]


  def appendright(self):
    app .textinput .text += app .ribbon[3]


  def reset(self):
    app .textinput .text  = app .name[app .i]


  def clear(self):
    app .textinput .text  = ''


  def rename(self):
    if app .textinput != 0:
      self .remove_widget(app .textinput)
      self .remove_widget(app .reset)
      self .remove_widget(app .clear)

      ##  Kivy doesn't have a way to test if a widget exists,
      ##  so you have to try:  remove,  except: pass

      try:  self .remove_widget(app .btnUp)
      except:  pass

      try:  self .remove_widget(app .btnDown)
      except:  pass

      try:  self .remove_widget(app .btnLeft)
      except:  pass

      try:  self .remove_widget(app .btnRight)
      except:  pass

      app .textinput  = 0

    if app .naming > 0:
      if len(app .origin) > 0:
        mX  = Window .mouse_pos[0]
        mY  = Window .mouse_pos[1]

        xx  = int(( mX - app .originX ) / app .eachX )
        yy  = int(( app .originY - mY ) / app .eachY )

        app .i  = yy * app .columns + xx

        print(app .name[app .i])

        app .textinput  = TextInput(text = app .name[app .i],  multiline = False,  size_hint = (0.15, 0.05))

        if mX - 320 < 0:
          xpos  = mX + 150
        else:
          xpos  = mX - 200

        if mY - 150 < 0:
          ypos  = mY + 150
        else:
          ypos  = mY - 100

        app .textinput .pos  = (xpos - 50,  ypos - 50)
        app .textinput .bind(on_text_validate  = OkayScreen .gettext)

        if yy > 0:   ## up
          app .ribbon[0]  = app .name[ app .i - app .columns ]
          app .btnUp  = Button(text = app .ribbon[0],  pos = (xpos,  ypos - 10),  size_hint = (.07, .055))
          app .btnUp .bind(on_release = OkayScreen .appendup)
          self .add_widget(app .btnUp)

        if yy + 1 < app .rows:   ## down
          app .ribbon[1]  = app .name[ app .i + app .columns ]
          app .btnDown  = Button(text = app .ribbon[1],  pos = (xpos,  ypos - 100),  size_hint = (.07, .055))
          app .btnDown .bind(on_release = OkayScreen .appenddown)
          self .add_widget(app .btnDown)

        if xx > 0:   ## left
          app .ribbon[2]  = app .name[ app .i - 1 ]
          app .btnLeft  = Button(text = app .ribbon[2],  pos = (xpos - 120,  ypos - 100),  size_hint = (.07, .055))
          app .btnLeft .bind(on_release = OkayScreen .appendleft)
          self .add_widget(app .btnLeft)

        if xx + 1 < app .columns:   ## right
          app .ribbon[3]  = app .name[ app .i + 1 ]
          app .btnRight  = Button(text = app .ribbon[3],  pos = (xpos + 120,  ypos - 100),  size_hint = (.07, .055))
          app .btnRight .bind(on_release = OkayScreen .appendright)
          self .add_widget(app .btnRight)

        app .reset  = Button(text = 'Reset',  pos = (xpos - 120,  ypos - 10),  size_hint = (.07, .055),  background_color = (.2, .2, .2,  .9))
        app .reset .bind(on_press = OkayScreen .reset)

        app .clear  = Button(text = 'Clear',  pos = (xpos + 120,  ypos - 10),  size_hint = (.07, .055),  background_color = (.2, .2, .2,  .9))
        app .clear .bind(on_press = OkayScreen .clear)

        self .add_widget(app .reset)
        self .add_widget(app .clear)
        self .add_widget(app .textinput)
        app .textinput .focus  = True


  def generate(self):
    JSONlist  = ['{']
    JSONlist .append('  "' + app .filename + app .ext + '": {')

    i  = 0
    tile  = 0
    while i < len(app .sprite):
      if app .sprite[i] .pos != (app .imgW,  app .imgH):

        xx  = int(app .posX[i] / 2)
        yy  = int(app .posY[i] / 2)
        ww  = int(app .wide / 2)
        hh  = int(app .high / 2)

        string  = '    "%s":  [ %s, %s,  %s, %s],' % ( app .name[i], xx, yy, ww, hh )
        JSONlist .append( string )
        tile += 1
      i += 1

    JSONlist[-1]  = ',' .join( JSONlist[-1] .split(',')[:-1] )   ## remove trailing comma on last entry

    JSONlist .append('  }')
    JSONlist .append('}')

    Output  = '\n' .join(JSONlist)   ## stringify list

    print('Writing\n')
    with open('data/' + app .filename + '.app', 'w') as fileOut:
      fileOut .write(Output)

    print('Written to data/' + app .filename + '.app')
    sys .exit()


  def update(self):
    i  = -1
    for y in range(app .rows):
      for x in range(app .columns):
        i += 1

        app .posX[i]  = app .originX + x * app .eachX
        app .posY[i]  = app .originY - (y + 1) * app .eachY

        posit  = ( app .posX[i],  app .posY[i] )
        siz  = ( app .wide,  app .high )

        if app .sprite[i] == 0:
          with self .canvas:
            Color( 1, 0, 0,  0.2 )
            app .sprite[i]  = Rectangle( pos = posit,  size = siz )

        elif app .sprite[i] .pos != (app .imgW,  app .imgH):
          app .sprite[i] .pos  = posit
          app .sprite[i] .size  = siz


  def horiz(self, x, w):
    app .originX  += x
    app .wide  += w
    app .eachX  = app .wide + app .padX
    if app .X < 0:  app .X  = 0
    if app .wide < 0:  app .wide  = 0
    OkayScreen .update(self)


  def vert(self, y, h):
    app .originY  += y
    app .high  += h
    app .eachY  = app .high + app .padY
    if app .Y < 0:  app .Y  = 0
    if app .high < 0:  app .high  = 0
    OkayScreen .update(self)


  def gapx(self, x):
    app .padX  += x
    app .eachX  = app .wide + app .padX
    if app .padX < 0:  app .padX  = 0
    OkayScreen .update(self)


  def gapy(self, y):
    app .padY  += y
    app .eachY  = app .high + app .padY
    if app .padY < 0:  app .padY  = 0
    OkayScreen .update(self)



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class app(App):
  icon  = 'icon.png'
  title  = "Kivy Atlas Generator   ::   by Doyousketch2"

  sm  = ScreenManager( transition = NoTransition() )
  selected  = 'icon.png'

  path  = 'data/icon'
  filename  = 'icon'
  ext  = '.png'

  imgW    = 0
  imgH    = 0
  originX = 0
  originY = 0

  columns = 0
  rows    = 0
  eachX   = 0
  eachY   = 0

  X     = 4
  wide  = 42
  padX  = 4

  Y     = 4
  high  = 42
  padY  = 4

  recthoriz = 0
  rectvert  = 0
  horizpad  = 0
  vertpad   = 0

  origin = []
  sprite = []
  posX   = []
  posY   = []
  name   = []
  ribbon = []

  i  = 0
  naming  = 0
  textinput  = 0
  img  = Image( source = selected )
  tex  = img .texture

  btnUp    = 0
  btnDown  = 0
  btnLeft  = 0
  btnRight = 0

  clear  = 0
  reset  = 0

  def build(self):
    self .sm .add_widget( FileScreen( name = 'FileScreen') )
    self .sm .add_widget( TileScreen( name = 'TileScreen') )
    self .sm .add_widget( OkayScreen( name = 'OkayScreen') )
    return self .sm


##=========================================================
##  main  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
  app() .run()


##=========================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
