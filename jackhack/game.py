class Game:
  def __init__(self, *args, **kwargs):
    print("In Game")
    print(args)
    print(kwargs)
    self.player_name_from_game = kwargs["player_name"]

  def foo(self):
    print("FOO!")
