"""Utiliiies that help interface with users."""

def PromptUser(msg):
  ans = raw_input("{} [Y/n]: ".format(msg))
  if ans == "Y":
    return True
  else:
    return False
