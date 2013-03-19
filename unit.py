#################################################################################
#   Author: Collin Mitchell
#     Date: 2013 March 15th
#  Version: 0.1
#     Data: Unit is the base template for all members of the Combatant Program.
#           You are welcome to borrow, inherit, or otherwise use this class base.
#           Name | Tag [(e)nemy or (a)lly] | Initiative | Initiative Modifier |
#           Natural20 [0 to treat as 20, 1 to treat as 30]
# Updates: Null
#################################################################################
# import random as r

class Unit:
   def __init__(self, name, tag, init, init_mod, nat20=0):
      self.name      = name
      self.init_mod  = init_mod
      self.tag       = tag                      # tag can be 'e' for enemy or 'a' for ally; no neutral
      self.init      = init
   ################ Potential add on idea later #############################
   # def getInit(self):                            # convert natural 20 -> 30
   #   theInit = r.randint(1,20)
   #   if nat20 == 1: 
   #      if theInit == 20: return 30
   #   else: return theInit
   ##########################################################################
   def setInit(self, num):
      self.init = num
   def totalInit(self):
      return self.init + self.init_mod
