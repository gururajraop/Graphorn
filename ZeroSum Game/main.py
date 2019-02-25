import numpy as np
import os
import time
import argparse
import nashpy as nash


class ZSGame():
  def __init__(self, Rowena, Collin, threshold):
    self.G = nash.Game(Rowena, Collin)
    self.threshold = threshold

  def print(self):
    print(self.G)

  def nash_equilibrium(self):
    p_r = []
    p_c = []
    for eq in self.G.support_enumeration():
      p_r.append(eq[0])
      p_c.append(eq[1])

    print("The nash equilibrium probabilities are:")
    for index, _ in enumerate(p_r):
      print("(p={}, q={})".format(p_r[index][0], p_c[index][0]))




if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Iterated Prisoners Dilemma Tournament')
  parser.add_argument('--threshold', '-t', type=float, default=1e-6, help='threshold of probability changes between iterations')

  args = parser.parse_args()
  Rowena = [[1, -1], [-1, 1]]
  Collin = [[-1, 1], [1, -1]]
  #Rowena = [[1, 2], [3, 0]]
  #Collin = [[0, 2], [3, 1]]
  game = ZSGame(Rowena, Collin, args.threshold)
  game.nash_equilibrium()




