"""Utiliiies that help interface with users."""

def PromptUser(self, msg):
  ans = raw_input("{} [Y/n]: ".format(msg))
  if ans == "Y":
    return True
  else:
    return False
