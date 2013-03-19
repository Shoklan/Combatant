#
# Blank
#
from unit         import Unit
from Tkinter      import *
from tkFileDialog import *
import pickle
import random as r
import sys

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

   def makeMenuFrame(self):
      menuFrame = Frame(self, bd=2)
      menuFrame.pack(fill=X, side=TOP)
      Button(menuFrame, text='Next',   command = self.onNext).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='New',    command = self.onNew).pack(side=LEFT,    expand=YES, fill=BOTH)
      Button(menuFrame, text='Import', command = self.onImport).pack(side=LEFT, expand=YES, fill=BOTH)
      Button(menuFrame, text='Add',    command = self.onAdd).pack(side=LEFT,    expand=YES, fill=BOTH)
      Button(menuFrame, text='Remove', command = self.onRemove).pack(side=LEFT, expand=YES, fill=BOTH)
      Button(menuFrame, text='Load',   command = self.onLoad).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Save',   command = self.onSave).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Sort',   command = self.onSort).pack(side=LEFT,   expand=YES, fill=BOTH)
      Button(menuFrame, text='Quit',   command = self.quit).pack(side=LEFT,     expand=YES, fill=BOTH)

   def makeReadyFrame(self):
      readyFrame = Frame(self, bd=2, relief=RAISED)
      readyFrame.pack(fill=X, side=BOTTOM)
      return readyFrame

   def makeContentFrame(self):
      contentFrame = Frame(self, relief=SUNKEN)
      contentFrame.pack(expand=YES, fill=BOTH)
      pos = 1
      for item in self.unitList:
         frame = Frame(contentFrame, bd=2, relief=SUNKEN)
         Label(frame,  text=pos).pack(side=LEFT, expand=YES, fill=Y)
         Label(frame,  text=item.name).pack(side=LEFT, expand=YES, fill=Y)
         Label(frame,  text=item.totalInit()).pack(side=LEFT, expand=YES, fill=Y)
         frame.pack(side=TOP, expand=NO, fill=X)
         pos += 1
      return contentFrame

   def remakeContentFrame(self):
      self.contentFrame.forget()
      self.contentFrame = self.makeContentFrame()

   def remakeReadyFrame(self):
      self.readyFrame.forget()
      self.readyFrame = self.makeReadyFrame()

   def onNext(self):
      saveUnit = self.unitList.pop(0)
      self.unitList.append(saveUnit)
      self.remakeContentFrame()

   def onNew(self):
      self.onRemoveAll()
      self.remakeContentFrame()

   def onAdd(self):
      def getEntries():
         if nameEntry.get() != '' and tagEntry.get() != '' and initModEntry.get() != '':
            if initEntry.get() == '':
               theInit = r.randint(1,20)
            else:
               theInit = int(initEntry.get())
            self.unitList.append( Unit( nameEntry.get(),                   # Unit Name
                                        tagEntry.get(),                    # Unit Tag
                                        theInit,                           # Unit Initaitive
                                        int(initModEntry.get()), 0))       # Unit Initiative Mod + meh.
            popup.destroy()
         else:
            popup.destroy()

      popup = Toplevel()
      popup.title('Combatant Information')
      nameFrame = Frame(popup)
      nameLabel = Label(nameFrame, width=18, text='Name')
      nameEntry = Entry(nameFrame)
      nameFrame.pack(side=TOP, fill=X)
      nameLabel.pack(side=LEFT)
      nameEntry.pack(side=LEFT, expand=YES, fill=X)

      tagFrame = Frame(popup)
      tagLabel = Label(tagFrame, width=18,  text='Tag [(e)nemy or (a)lly]')
      tagEntry = Entry(tagFrame)
      tagFrame.pack(side=TOP, fill=X)
      tagLabel.pack(side=LEFT)
      tagEntry.pack(side=LEFT, expand=YES, fill=X)
      
      initFrame = Frame(popup)
      initLabel = Label(initFrame, width=18, text='Initiative')
      initEntry = Entry(initFrame)
      initFrame.pack(side=TOP, fill=X)
      initLabel.pack(side=LEFT)
      initEntry.pack(side=LEFT, expand=YES, fill=BOTH)
      
      initModFrame = Frame(popup)
      initModLabel = Label(initModFrame, width=18, text='Initiative Modifier')
      initModEntry = Entry(initModFrame)
      initModFrame.pack(side=TOP, fill=X)
      initModLabel.pack(side=LEFT)
      initModEntry.pack(side=LEFT, expand=YES, fill=X)

      buttonFrame = Frame(popup)
      buttonFrame.pack(expand=YES, fill=BOTH)
      Button(buttonFrame, text='Submit', command=getEntries).pack(side=LEFT, expand=YES, fill=BOTH)
      Button(buttonFrame, text='Cancel', command=popup.destroy).pack(side=RIGHT, expand=YES, fill=BOTH)
      
      popup.grab_set()
      popup.focus_set()
      popup.wait_window()

      self.remakeContentFrame()
          
   def onImport(self):
      filename = askopenfilename()
      if filename:
         target = open(filename, 'rb')
         tempList = pickle.load(target)
         for item in tempList:
            self.unitList.append(item)
         target.close()
         self.remakeContentFrame()

   def onLoad(self):
      filename = askopenfilename(initialdir = '.')
      if filename:
         self.onRemoveAll()
         target = open(filename)
         self.unitList = pickle.load(target)
         target.close()
         self.remakeContentFrame()

   def onReady(self, name):
      for unit in self.unitList:
         if unit.name == name:
            readyList.append(item)
            self.unitList.pop(self.unitList.index(item))
            self.remakeContentFrame()
            break

   def onRemove(self):
      def onPop():
         self.unitList.pop(int(submit.get())-1)
         self.remakeContentFrame()
         popup.destroy()
      popup = Toplevel()
      Label(popup, text='Postion of Person?').pack(side=TOP, expand=YES, fill=BOTH)
      submit = Entry(popup)
      submit.pack(expand=YES, fill=BOTH)
      Button(popup, text='Submit', command=onPop).pack(side=BOTTOM, expand=YES, fill=BOTH)

   def onRemoveAll(self):
      while len(self.unitList) != 0: self.unitList.pop()
            
   def onSave(self):
      filename = asksaveasfilename(initialdir = '.')
      if filename:
         target = open(filename, 'w')
         pickle.dump(self.unitList, target)
         target.close()
         
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
        
        

if __name__ == '__main__': Combatant().mainloop()
