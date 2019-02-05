import numpy as np
import os
import time
import argparse

class PDGame():
  def __init__(self):
    self.normal_form = [[[-10, -10], [-25, 0]],
                  [[0, -25], [-20, -20]]]

  def round(self, p1, p2):
    if (p1 == 'C' and p2 == 'C'):
      return self.normal_form[0][0]
    elif (p1 == 'C' and p2 == 'D'):
      return self.normal_form[0][1]
    elif (p1 == 'D' and p2 == 'C'):
      return self.normal_form[1][0]
    elif (p1 == 'D' and p2 == 'D'):
      return self.normal_form[1][1]
    else:
      print("Error! Wrong plays")
      return 0, 0

class Player():
  def __init__(self, filename):
      data = open(filename, 'r')
      data = [line for line in data]
      self.authors = data[0]
      self.name = data[1]
      self.n = int(data[2])
      self.current_state = 0
      self.states = {i:['C', i, i]  for i in range(self.n)}
      self.utility = []
        
      for i, transition in enumerate(data[3:]):
        turn = transition.split(',')
        strategy = turn[0]
        cState = int(turn[1])
        dState = int(turn[2])
        self.states[i] = [strategy, cState, dState]

      print(self.states)

  def add_utility(self, u):
    self.utility.append(u)

  def get_utility(self):
    return np.mean(self.utility)

  def play(self, opponent):
    if opponent == 'C':
      turn = self.states[self.current_state][0]
      self.current_state = self.states[self.current_state][1]
      return turn
    elif opponent == 'D':
      turn = self.states[self.current_state][0]
      self.current_state = self.states[self.current_state][2]
      return turn
    else:
      print("Error! Wrong turn")
      return 'C'
        

def play(player1, player2, iter):
  p1_play = 'C'
  p2_play = 'C'
  game = PDGame()
  for i in range(iter):
    p1_play = player1.play(p2_play)
    p2_play = player2.play(p1_play)
    u1, u2 = game.round(p1_play, p2_play)
    player1.add_utility(u1)
    player2.add_utility(u2)
    print("Round ", iter, "Player 1: (", p1_play, player1.current_state, u1, "), Player 2: (",
        p2_play, player2.current_state, u2, ")")


  print("Total payoff of Player 1:", player1.get_utility())
  print("Total payoff of Player 2:", player2.get_utility())


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Iterated Prisoners Dilemma Tournament')
  parser.add_argument('--player1', '-p1', default='basic1.txt', help='Strategy of Player 1')
  parser.add_argument('--player2', '-p2', default='basic8.txt', help='Strategy of Player 2')
  parser.add_argument('--iter', '-i', type=int, default=1000, help='Number of times the game is played')

  args = parser.parse_args()
  player1 = Player(args.player1)
  player2 = Player(args.player2)

  play(player1, player2, args.iter)


