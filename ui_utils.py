"""Utiliiies that help interface with users."""

def PromptUser(msg):
  ans = raw_input("{} [Y/n]: ".format(msg))
  if ans == "Y":
    return True
  else:
    return False

def GetInputFromUser(msg):
  """Gets input from the user, as a string."""
  return raw_input("{}: ".format(msg))
