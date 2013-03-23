#################################################################################
#   Author: Collin Mitchell
#     Date: 2013 March 15th
#  Version: 0.2
#     Data: Unit is the base template for all members of the Combatant Program.
#           You are welcome to borrow, inherit, or otherwise use this class base.
#           Name |  Initiative | Initiative Modifier |
#  History: [March 19 2013]
#           Removed the tag variable as it ended up being useless.
#           Did the same with Nat20 stat; ditto problem. Combatant.py has been
#           updated to ignore them entirely.
#################################################################################
# import random as r

class Unit:
   def __init__(self, name, init, init_mod):
      self.name      = name
      self.init_mod  = init_mod
      self.init      = init
   
   def setInit(self, num):
      self.init = num

   def totalInit(self):
      return self.init + self.init_mod
