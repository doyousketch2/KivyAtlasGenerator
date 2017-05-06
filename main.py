#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##=========================================================
##  atlas.py                                    21 Apr 2017
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

from  kivy .app           import  App               ##  GUI
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

WIDTH  = 400
HEIGHT  = 600

##=========================================================
##  script  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Window .size  = ( WIDTH, HEIGHT )
Builder .load_file('./atlas.kv')  ##  Kivy is buggy, needed for ScreenManager


class FileScreen(Screen):

  def select(self, *args):
    self .selection  = args[1][0]
    try:
      atlas .selected  = self .selection
      self .label .text  = atlas .selected
    except:  pass


  def choice(self):

    atlas .path, atlas .ext  = os .path .splitext( atlas .selected )

    if '/' in atlas .path:  ##  Unix, Linux, Android, Mac OSX, iOS
      atlas .filename  = atlas .path .split('/')[-1]
    else:  ##  the other OS
      atlas .filename  = atlas .path .split('\\')[-1]
    print(atlas .filename)

    atlas .img  = Image( source = atlas .selected )
    atlas .tex  = atlas .img .texture

    atlas .X  = atlas .img .texture_size[0]
    atlas .Y  = atlas .img .texture_size[1]

    atlas .imgW  = atlas .img .texture_size[0]  = atlas .img .texture_size[0] * 2
    atlas .imgH  = atlas .img .texture_size[1]  = atlas .img .texture_size[1] * 2

    Window .size  = ( atlas .imgW,  atlas .imgH )
    self .manager .switch_to( TileScreen() )



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TileScreen(Screen):

  def cross(self):

    with self .canvas:
      Color( 1, 0, 0,  0.2 )  ##  red highlight

      posit  = ( atlas .X,  0 )
      siz  = ( atlas .high,  atlas .imgH )
      atlas .recthoriz  = Rectangle( pos = posit,  size = siz )

      posit  = ( 0,  atlas .Y )
      siz  = ( atlas .imgW,  atlas .wide )
      atlas .rectvert  = Rectangle( pos = posit,  size = siz )


      Color( 0, 0, 0,  0.5 )  ##  black padding

      posit  = ( atlas .X + atlas .high,  0 )
      siz  = ( atlas .padX,  atlas .imgH )
      atlas .horizpad  = Rectangle( pos = posit,  size = siz )

      posit  = ( 0,  atlas .Y )
      siz  = ( atlas .imgW,  -atlas .padY )
      atlas .vertpad  = Rectangle( pos = posit,  size = siz )


  def ok(self):
    atlas .eachX  = atlas .wide + atlas .padX
    atlas .eachY  = atlas .high + atlas .padY

    atlas .originX  = atlas .recthoriz .pos[0]
    atlas .originY  = atlas .rectvert .pos[1]

    while atlas .originX - atlas .eachX > 0:
      atlas .originX  -= atlas .eachX

    while atlas .originY + atlas .eachY < atlas .imgH:
      atlas .originY  += atlas .eachY

    self .manager .switch_to( OkayScreen() )


  def updateX(self):
    atlas .recthoriz .pos   = ( atlas .X,  0 )
    atlas .recthoriz .size  = ( atlas .wide,  atlas .imgH )

    atlas .horizpad  .pos   = ( atlas .X + atlas .wide,  0 )
    atlas .horizpad  .size  = ( atlas .padX,  atlas .imgH )


  def updateY(self):
    atlas .rectvert .pos   = ( 0,  atlas .imgH - atlas .Y )
    atlas .rectvert .size  = ( atlas .imgW,  atlas .high )

    atlas .vertpad  .pos   = ( 0,  atlas .imgH - atlas .Y )
    atlas .vertpad  .size  = ( atlas .imgW,  -atlas .padY )


  def horiz(self, x, w):
    atlas .X  += x
    atlas .wide  += w
    if atlas .X < 0:  atlas .X  = 0
    if atlas .wide < 0:  atlas .wide  = 0
    TileScreen .updateX(self)


  def vert(self, y, h):
    atlas .Y  -= y
    atlas .high  += h
    if atlas .Y < 0:  atlas .Y  = 0
    if atlas .high < 0:  atlas .high  = 0
    TileScreen .updateY(self)


  def gapx(self, x):
    atlas .padX  += x
    if atlas .padX < 0:  atlas .padX  = 0
    TileScreen .updateX(self)


  def gapy(self, y):
    atlas .padY  -= y
    if atlas .padY < 0:  atlas .padY  = 0
    TileScreen .updateY(self)



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class OkayScreen(Screen):

  def back(self):
    self .manager .switch_to( TileScreen() )


  def populate(self):

    if len(atlas .origin) == 0:
      while atlas .originX + (atlas .columns + 1) * atlas .eachX < atlas .imgW:
        atlas .columns += 1

      while atlas .originY - (atlas .rows + 1) * atlas .eachY > 0:
        atlas .rows += 1

      howmany  = int(atlas .columns * atlas .rows)

      atlas .sprite = [0] * howmany
      atlas .origin = [0] * howmany
      atlas .posX   = [0] * howmany
      atlas .posY   = [0] * howmany
      atlas .name   = [0] * howmany
      atlas .ribbon = [0] * 4

      alphabet  = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',

                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
      i  = -1
      for y in range(atlas .rows):
        for x in range(atlas .columns):
          i += 1
          if y > len(alphabet):  ##  so we don't run out of letters;  A, AA, AAA, AAAA, etc.
            a  = alphabet[y % len(alphabet)] * int(y / len(alphabet) + 1)
          else:
            a  = alphabet[y]

          atlas .name[i]  = '%s%s' % (a,  x + 1)

    OkayScreen .update(self)


  def toggle(self):

    if atlas .naming < 1:
      if len(atlas .origin) > 0:
        mX  = Window .mouse_pos[0]
        mY  = Window .mouse_pos[1]

        xx  = int(( mX - atlas .originX ) / atlas .eachX )
        yy  = int(( atlas .originY - mY ) / atlas .eachY )

        i  = yy * atlas .columns + xx

        if atlas .sprite[i] .pos == (atlas .imgW,  atlas .imgH):
          atlas .sprite[i] .pos  = atlas .origin[i]
        else:
          atlas .origin[i]  = atlas .sprite[i] .pos
          atlas .sprite[i] .pos  = (atlas .imgW,  atlas .imgH)


  def nametiles(self):
    atlas .naming = 1


  def gettext(self):
    print(atlas .textinput .text)
    atlas .name[atlas .i]  = atlas .textinput .text

##  kivy doesn't allow you to pass args to button functions,
##  so these are simple redundant 'callbacks'

  def appendup(self):
    atlas .textinput .text += atlas .ribbon[0]


  def appenddown(self):
    atlas .textinput .text += atlas .ribbon[1]


  def appendleft(self):
    atlas .textinput .text += atlas .ribbon[2]


  def appendright(self):
    atlas .textinput .text += atlas .ribbon[3]


  def reset(self):
    atlas .textinput .text  = atlas .name[atlas .i]


  def clear(self):
    atlas .textinput .text  = ''


  def rename(self):
    if atlas .textinput != 0:
      self .remove_widget(atlas .textinput)
      self .remove_widget(atlas .reset)
      self .remove_widget(atlas .clear)

##  kivy doesn't have a way to test if a widget exists,
##  so you have to try: remove, except: pass

      try:  self .remove_widget(atlas .butup)
      except:  pass

      try:  self .remove_widget(atlas .butdown)
      except:  pass

      try:  self .remove_widget(atlas .butleft)
      except:  pass

      try:  self .remove_widget(atlas .butright)
      except:  pass

      atlas .textinput  = 0

    if atlas .naming > 0:
      if len(atlas .origin) > 0:
        mX  = Window .mouse_pos[0]
        mY  = Window .mouse_pos[1]

        xx  = int(( mX - atlas .originX ) / atlas .eachX )
        yy  = int(( atlas .originY - mY ) / atlas .eachY )

        atlas .i  = yy * atlas .columns + xx

        print(atlas .name[atlas .i])

        atlas .textinput  = TextInput(text = atlas .name[atlas .i],  multiline = False,  size_hint = (0.2, 0.05))

        if mY - 50 < 0:
          ypos  = mY + 50
        else:
          ypos  = mY - 50

        atlas .textinput .pos  = (atlas .imgW / 4, ypos)
        atlas .textinput .bind(on_text_validate  = OkayScreen .gettext)

        if yy > 0:  ##  up
          atlas .ribbon[0]  = atlas .name[ atlas .i - atlas .columns ]
          atlas .butup  = Button(text = atlas .ribbon[0],  pos = (atlas .imgW / 4, ypos + 50),  size_hint = (.1, .055))
          atlas .butup .bind(on_release = OkayScreen .appendup)
          self .add_widget(atlas .butup)

        if yy < atlas .rows:  ##  down
          atlas .ribbon[1]  = atlas .name[ atlas .i + atlas .columns ]
          atlas .butdown  = Button(text = atlas .ribbon[1],  pos = (atlas .imgW / 4, ypos - 50),  size_hint = (.1, .055))
          atlas .butdown .bind(on_release = OkayScreen .appenddown)
          self .add_widget(atlas .butdown)

        if xx > 0:  ##  left
          atlas .ribbon[2]  = atlas .name[ atlas .i - 1 ]
          atlas .butleft  = Button(text = atlas .ribbon[2],  pos = (atlas .imgW / 8, ypos - 50),  size_hint = (.1, .055))
          atlas .butleft .bind(on_release = OkayScreen .appendleft)
          self .add_widget(atlas .butleft)

        if xx + 1 < atlas .columns:  ##  right
          atlas .ribbon[3]  = atlas .name[ atlas .i + 1 ]
          atlas .butright  = Button(text = atlas .ribbon[3],  pos = (atlas .imgW / 8 * 3, ypos - 50),  size_hint = (.1, .055))
          atlas .butright .bind(on_release = OkayScreen .appendright)
          self .add_widget(atlas .butright)

        atlas .reset  = Button(text = 'Reset',  pos = (atlas .imgW / 8, ypos + 50),  size_hint = (.1, .055),  background_color = (.2, .2, .2,  .9))
        atlas .reset .bind(on_press = OkayScreen .reset)

        atlas .clear  = Button(text = 'Clear',  pos = (atlas .imgW / 8 * 3, ypos + 50),  size_hint = (.1, .055),  background_color = (.2, .2, .2,  .9))
        atlas .clear .bind(on_press = OkayScreen .clear)

        self .add_widget(atlas .reset)
        self .add_widget(atlas .clear)
        self .add_widget(atlas .textinput)
        atlas .textinput .focus  = True


  def generate(self):
    JSONlist  = ['{']
    JSONlist .append('  "' + atlas .filename + atlas .ext + '": {')

    i  = 0
    tile  = 0
    while i < len(atlas .sprite):
      if atlas .sprite[i] .pos != (atlas .imgW,  atlas .imgH):

        xx  = int(atlas .posX[i] / 2)
        yy  = int(atlas .posY[i] / 2)
        ww  = int(atlas .wide / 2)
        hh  = int(atlas .high / 2)

        string  = '    "%s":  [ %s, %s,  %s, %s],' % ( atlas .name[i], xx, yy, ww, hh )
        JSONlist .append( string )
        tile += 1
      i += 1

    JSONlist[-1]  = ',' .join( JSONlist[-1] .split(',')[:-1] )  ##  remove trailing comma on last entry

    JSONlist .append('  }')
    JSONlist .append('}')

    Output  = '\n' .join(JSONlist)  ##  stringify list

    print('Writing\n')
    with open('data/' + atlas .filename + '.atlas', 'w') as fileOut:
      fileOut .write(Output)

    print('Written to data/' + atlas .filename + '.atlas')
    sys .exit()


  def update(self):
    i  = -1
    for y in range(atlas .rows):
      for x in range(atlas .columns):
        i += 1

        atlas .posX[i]  = atlas .originX + x * atlas .eachX
        atlas .posY[i]  = atlas .originY - (y + 1) * atlas .eachY

        posit  = ( atlas .posX[i],  atlas .posY[i] )
        siz  = ( atlas .wide,  atlas .high )

        if atlas .sprite[i] == 0:
          with self .canvas:
            Color( 1, 0, 0,  0.2 )
            atlas .sprite[i]  = Rectangle( pos = posit,  size = siz )

        elif atlas .sprite[i] .pos != (atlas .imgW,  atlas .imgH):
          atlas .sprite[i] .pos  = posit
          atlas .sprite[i] .size  = siz


  def horiz(self, x, w):
    atlas .originX  += x
    atlas .wide  += w
    atlas .eachX  = atlas .wide + atlas .padX
    if atlas .X < 0:  atlas .X  = 0
    if atlas .wide < 0:  atlas .wide  = 0
    OkayScreen .update(self)


  def vert(self, y, h):
    atlas .originY  += y
    atlas .high  += h
    atlas .eachY  = atlas .high + atlas .padY
    if atlas .Y < 0:  atlas .Y  = 0
    if atlas .high < 0:  atlas .high  = 0
    OkayScreen .update(self)


  def gapx(self, x):
    atlas .padX  += x
    atlas .eachX  = atlas .wide + atlas .padX
    if atlas .padX < 0:  atlas .padX  = 0
    OkayScreen .update(self)


  def gapy(self, y):
    atlas .padY  += y
    atlas .eachY  = atlas .high + atlas .padY
    if atlas .padY < 0:  atlas .padY  = 0
    OkayScreen .update(self)



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class atlas(App):
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

  butup    = 0
  butdown  = 0
  butleft  = 0
  butright = 0

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
  atlas() .run()


##=========================================================
##  eof  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

