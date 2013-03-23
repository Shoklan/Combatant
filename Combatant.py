###########################################################################################
#   Author: Collin Mitchell
#     Date: 19 March 2013
#  Version: 0.9
#     Data: Program designed to create a visual initiative recording. I'm hoping that
#           by doing that it frees up the DM to focus more on what is going on in combat
#           and less about looking over a scrap of paper worrying about who goes next;
#           Now they will always know.
#  History: 
#           [March 20 2013]
#           Changed the layout to use grid instead of pack; I'm hoping it makes the
#           buttons a bit more consistent and wont wobble as the user clicks next. It
#           should work fine, but if not I'll need to research and find something more
#           useful. Everything currently works aside from the Ready section. That should
#           be working by the end of the night.
###########################################################################################
from unit         import Unit                                # Unit for saving stats
from Tkinter      import *                                   # GUI elements
from tkFileDialog import *                                   # save and load features
import pickle                                                # in/out of files
import random as r                                           # generate init; if blank
# import sys                                                 # No idea; lets delete it

###########################################################################################
# Combatant core class
# auto calls the lower functions necessary for running
class Combatant(Frame):
   def __init__(self, parent=None):
      Frame.__init__(self, parent)
      self.pack(fill=BOTH, expand=YES)
      self.master.title('Combat Initiative Simulator')
      self.unitList  = []
      self.readyList = []
      self.makeMenuFrame()
      self.readyFrame   = self.makeReadyFrame()
      self.contentFrame = self.makeContentFrame()

   ########################################################################################
   # Creates the menu of buttons at the top. I could have used a legit menu, but I didn't
   # like not having the commands immediately available for such a simple program; it does
   # not need a complex menu system with dropdowns and all that extra fluff
   # Buttons: Next - Shifts the order.
   #          New  - Clears all entries.
   #          Import - Adds units without clearing current ones.
   #          Add    - Adds a unit via dialog
   #          Load   - Clears the current units; then adds units from file
   #                 + Can just be NEW + IMPORT commands; also, move next to Import
   #          Save   - Save current units to a file
   #                 + FEATURE: call on window close to save current units
   #          Sort   - Moves units in list based on initiative
   #          Quit   - Closes the program: duh.
   def makeMenuFrame(self):
      menuFrame = Frame(self, bd=2)
      menuFrame.pack(fill=X, side=TOP)
      Button(menuFrame, text='Next',   command= self.onNext).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Reroll', command= self.onReroll).pack(side=LEFT, expand=YES, fill=BOTH)
      Button(menuFrame, text='New',    command= self.onNew).pack(side=LEFT,    expand=YES, fill=BOTH)
      Button(menuFrame, text='Import', command= self.onImport).pack(side=LEFT, expand=YES, fill=BOTH)
      Button(menuFrame, text='Load',   command= self.onLoad).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Add',    command= self.onAdd).pack(side=LEFT,    expand=YES, fill=BOTH)
      Button(menuFrame, text='Save',   command= self.onSave).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Sort',   command= self.onSort).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Quit',   command= self.quit).pack(side=LEFT,     expand=YES, fill=BOTH)

   ########################################################################################
   # Creates the readyFrame at the bottom of the window;
   # fills with units in readyList; if none present, no frame exists
   # If the frame is loaded on program creation it messes up the contentFrame expansion
   def makeReadyFrame(self):
      readyFrame = Frame(self, bd=2, relief=RAISED)
      readyFrame.pack(fill=X, side=BOTTOM)
      for item in self.readyList:
         frame = Frame(readyFrame)
         Label(frame, text=item.name).pack(side=LEFT, expand=YES, fill=Y)
         funcReturn = (lambda name=item.name: self.onReturn(name))
         Button(frame, text='Return', command=funcReturn).pack(side=LEFT, expand=YES, fill=BOTH)
         frame.pack(expand=YES, fill=BOTH)
      return readyFrame

   ########################################################################################
   # This is where the magic is!
   # Creates the contentFrame itself; uses the unitList global data structure to produce
   # a frame for each unit. It uses the pos = 1 to guide user and make inserting units
   # from the readyList easier. I don't know how to do drag and drop yet, but that is on
   # the agenda eventually.
   # The real magic, however, goes to lambda and the funcRemove/funcReady. Do not remove
   # those!if you alter them, then when the frame gets created the buttons will autodelete
   # the unit on creation leaving you with an empty unitList; drove me insane.
   def makeContentFrame(self):
      contentFrame = Frame(self, relief=SUNKEN)
      contentFrame.pack(expand=YES, fill=BOTH)
      pos = 1
      for item in self.unitList:
      #   OLD METHOD: PACK; may wish to change back later
      #
      #   funcRemove = (lambda name=item.name: self.onRemove(name))
      #   funcReady =  (lambda name=item.name: self.onReady(name))
      #   frame = Frame(contentFrame, bd=2, relief=SUNKEN)
      #   Label(frame,  text=pos).pack(side=LEFT, expand=YES, fill=Y)
      #   Label(frame,  text=item.name).pack(side=LEFT, expand=YES, fill=Y)
      #   Label(frame,  text=item.totalInit()).pack(side=LEFT, expand=YES, fill=Y)
      #   b1 = Button(frame, text='Remove', command=funcRemove)
      #   b1.pack(side=RIGHT, expand=YES, fill=Y)
      #   b2 = Button(frame, text='Ready',  command=funcReady)
      #   b2.pack(side=RIGHT, expand=YES, fill=Y)
      #   frame.pack(side=TOP, expand=NO, fill=X)
      #   pos += 1
         
         l1 = Label(contentFrame,  text=pos,                                     relief=SUNKEN, width=10)
         l2 = Label(contentFrame,  text=item.name,                               relief=SUNKEN, width=50)
         funcAlterInit = (lambda name=item.name: self.onNewInit(name))
         funcRemove    = (lambda name=item.name: self.onRemove(name))
         funcReady     = (lambda name=item.name: self.onReady(name))
         b1 = Button(contentFrame, text=item.totalInit(), command=funcAlterInit, relief=SUNKEN, width=10)
         b2 = Button(contentFrame, text='Ready',          command=funcReady,     relief=SUNKEN, width=20)
         b3 = Button(contentFrame, text='Remove',         command=funcRemove,    relief=SUNKEN, width=20)

         l1.grid(row=pos, column=0, sticky=NSEW)
         l2.grid(row=pos, column=1, sticky=NSEW)
         b1.grid(row=pos, column=2, sticky=NSEW)
         b2.grid(row=pos, column=3, sticky=NSEW)
         b3.grid(row=pos, column=4, sticky=NSEW)

         pos += 1
      contentFrame.columnconfigure(0, weight=1)
      contentFrame.columnconfigure(1, weight=1)
      contentFrame.columnconfigure(2, weight=1)
      contentFrame.columnconfigure(3, weight=1)
      contentFrame.columnconfigure(4, weight=1)
      return contentFrame

   ########################################################################################
   # redraw contentFrame; return reference to frame
   def remakeContentFrame(self):
      self.contentFrame.forget()
      self.contentFrame = self.makeContentFrame()

   ########################################################################################
   # redraw readyFrame; return reference to frame
   def remakeReadyFrame(self):
      self.readyFrame.forget()
      self.readyFrame = self.makeReadyFrame()

   ########################################################################################
   # Move the units in the list, then redraw
   def onNext(self):
      saveUnit = self.unitList.pop(0)
      self.unitList.append(saveUnit)
      self.remakeContentFrame()

   ########################################################################################
   # Clear all units and redraw   
   def onNew(self):
      self.onRemoveAll()
      self.remakeContentFrame()

   #########################################################################################
   # Add Unit to UnitList entries;
   # User does not need to submit initiative; the program can randomize it when left empty
   # Creates dialog, then creates object: simple. Hoping to make this smaller sometime soon
   # since it looks so ugly like this.
   def onAdd(self):
      def getEntries():
         if nameEntry.get() != '' and initModEntry.get() != '':
            if initEntry.get() == '':
               theInit = r.randint(1,20)
            else:
               theInit = int(initEntry.get())
            self.unitList.append( Unit( nameEntry.get(),                   # Unit Name
                                        theInit,                           # Unit Initaitive
                                        int(initModEntry.get())))          # Unit Initiative Mod
            popup.destroy()
         else:
            popup.destroy()

      popup = Toplevel()
      popup.title('Combatant Information')

      nameFrame = Frame(popup)                                                 # This section sets up
      nameLabel = Label(nameFrame, width=18, text='Name')                      # to get the Unit Name;
      nameEntry = Entry(nameFrame)                                            
      nameFrame.pack(side=TOP, fill=X)                                         
      nameLabel.pack(side=LEFT)                                                
      nameEntry.pack(side=LEFT, expand=YES, fill=X)                            

      initFrame = Frame(popup)                                                 # This section sets up
      initLabel = Label(initFrame, width=18, text='Initiative')                # to get the Unit Initiaitve
      initEntry = Entry(initFrame)                                             
      initFrame.pack(side=TOP, fill=X)
      initLabel.pack(side=LEFT)
      initEntry.pack(side=LEFT, expand=YES, fill=BOTH)
      
      initModFrame = Frame(popup)                                              # This section sets up
      initModLabel = Label(initModFrame, width=18, text='Initiative Modifier') # to get Unit InitiativeMod
      initModEntry = Entry(initModFrame)
      initModFrame.pack(side=TOP, fill=X)
      initModLabel.pack(side=LEFT)
      initModEntry.pack(side=LEFT, expand=YES, fill=X)

      buttonFrame = Frame(popup)                                               # Submit or ignore
      buttonFrame.pack(expand=YES, fill=BOTH)
      Button(buttonFrame, text='Submit', command=getEntries).pack(side=LEFT, expand=YES, fill=BOTH)
      Button(buttonFrame, text='Cancel', command=popup.destroy).pack(side=RIGHT, expand=YES, fill=BOTH)
      
      popup.grab_set()                                                         # Lock the users
      popup.focus_set()                                                        # attention on the input
      popup.wait_window()                                                      # dialog

      self.remakeContentFrame()                                                # redraw

   ########################################################################################
   # Gets units from file; does not remove current units
   def onImport(self):
      filename = askopenfilename()
      if filename:
         target = open(filename, 'rb')
         tempList = pickle.load(target)
         for item in tempList:
            self.unitList.append(item)
         target.close()
         self.remakeContentFrame()

   ########################################################################################
   # Gets units from file; remove current units
   def onLoad(self):
      filename = askopenfilename(initialdir = '.')
      if filename:
         self.onRemoveAll()
         target = open(filename)
         self.unitList = pickle.load(target)
         target.close()
         self.remakeContentFrame()

   ########################################################################################
   # Moves units from contentFrame/unitList to readyFrame/readyList
   def onReady(self, name):
      for item in self.unitList:
         if item.name == name:
            self.readyList.append(item)
            self.unitList.pop(self.unitList.index(item))
            self.remakeReadyFrame()
            self.remakeContentFrame()
            break

   ########################################################################################
   # Remove a unit from combat
   def onRemove(self, name):
      for item in self.unitList:
         if item.name == name:
            self.unitList.pop(self.unitList.index(item))
            break
      self.remakeContentFrame()

   ########################################################################################
   # Remove all units from combat
   def onRemoveAll(self):
      while len(self.unitList) != 0: self.unitList.pop()

   ########################################################################################
   # Save unitList to file for future use
   def onSave(self):
      filename = asksaveasfilename(initialdir = '.')
      if filename:
         target = open(filename, 'w')
         pickle.dump(self.unitList, target)
         target.close()

   ########################################################################################
   # Sorts units in unitList
   # This needs to be rewritten to notbe as bad. recSort is a cool idea, but it seems to
   # cause more problems than it solves. I also want a dialog in here and it's not letting
   # me do that.
   def onSort(self):
      def recSort():
         max = tempList[0]
         for item in tempList:
            if item.name == max.name                : continue
            elif item.totalInit() > max.totalInit() : max = item
            elif item.totalInit() == max.totalInit():
               if item.init_mod > max.init_mod:
                  max = item
               else: continue
         self.unitList.append(max)
         tempList.pop(tempList.index(max))
         if tempList != []: recSort()
         else: 
            self.remakeContentFrame()  

      if self.unitList == []: return
      else:
         tempList = []
         while len(self.unitList) != 0: tempList.append(self.unitList.pop(0))
         recSort()

   ########################################################################################
   # Returns a unit from readyList to unitList where user asks them to be placed.
   # If the location is greater than unitList length, it will append to the end
   # automatically
   def onReturn(self, name):
      def getPosition():
         if entry.get() == '': newPosition = 0
         else                : newPosition = int(entry.get())
         for item in self.readyList:
            if item.name == name:
               unit = self.readyList.pop(self.readyList.index(item))
               break
         
         if newPosition-1 >= len(self.unitList): self.unitList.append(unit)
         else                                  : self.unitList.insert(newPosition-1, unit)
         popup.destroy()

      popup = Toplevel()
      Label(popup, text='Select position for Unit: ').pack(side=TOP)
      entry = Entry(popup)
      entry.pack()
      Button(popup, text='Submit', command=getPosition).pack(side=BOTTOM)
      popup.grab_set()
      popup.focus_set()
      popup.wait_window()

      self.remakeReadyFrame()
      self.remakeContentFrame()

   ########################################################################################
   # Takes the name of a unit, prompts for new initiative (reminding of init_mod), then
   # sets the new units initiative.
   def onNewInit(self, name):
      def getAnsert():
         if entry.get() != '': target.init = int(entry.get())
         popup.destroy()

      for item in self.unitList:
         if item.name == name: target = item

      popup = Toplevel()
      l1= Label(popup, text='<New Initiative> + <' + item.init_Mod + '>: ')
      entry = Entry(popup)
      b1 = Button(popup, text='Submit', command=getAnswer)
      l1.pack(side=TOP)
      b1.pack(side=BOTTOM)
      entry.pack()
      popup.grab_set()
      popup.focus_set()
      popup.wait_window()

   ########################################################################################
   # Rerolls all of the units initiatives in the current window; this will not change the
   # units initiative modifier though.
   def onReroll(self):
      for item in self.unitList:
         item.init = r.randint(1,20)
      self.remakeContentFrame()

###########################################################################################
# If called from commandline, start the program.
# This will need to be a .pyw file and converted to an exe at a later date
if __name__ == '__main__': Combatant().mainloop()
