import numpy as np
import os
import time
import argparse
import nashpy as nash
import matplotlib.pyplot as plt

class ZSGame():
  def __init__(self, Rowena, Collin, actions, threshold):
    self.Rowena = Rowena
    self.Collin = Collin
    self.threshold = threshold

    self.Game = {'Rowena': {},
                 'Collin': {},
                 'Actions': actions}
    self.Game['Rowena'].update({actions[0]: Rowena[0]})
    self.Game['Rowena'].update({actions[1]: Rowena[1]})
    self.Game['Collin'].update({actions[0]: [Collin[0][0], Collin[1][0]]})
    self.Game['Collin'].update({actions[1]: [Collin[0][1], Collin[1][1]]})
    print(self.Game)

  def nash_equilibrium(self):
    p_r = []
    p_c = []
    game = nash.Game(self.Rowena, self.Collin)
    for eq in game.support_enumeration():
      p_r.append(eq[0])
      p_c.append(eq[1])

    print("The nash equilibrium probabilities are:")
    for index, _ in enumerate(p_r):
      print("(p={}, q={})".format(p_r[index][0], p_c[index][0]))

  def fictitious_play(self):
    A1 = self.Game['Actions'][0]
    A2 = self.Game['Actions'][1]
    R_action, C_action = A2, A2
    R_count = 1 if R_action == "A1" else 0
    C_count = 1 if C_action == "A1" else 0
    iteration = 1
    R_probs = []
    C_probs = []
    R_prob = R_count / iteration
    C_prob = C_count / iteration
    R_probs.append(R_prob)
    C_probs.append(C_prob)

    RoC_r = [0]
    RoC_c = [0]
    #print("\n\n({},{}) = ({}, {})".format(R_action, C_action, R_prob, C_prob))
    while True:
      if C_prob >= 0.5:
        if self.Game['Rowena'][A1][0] > self.Game['Rowena'][A2][0]:
          R_action = A1
          R_count += 1
        else:
          R_action = A2
      else:
        if self.Game['Rowena'][A1][1] > self.Game['Rowena'][A2][1]:
          R_action = A1
          R_count += 1
        else:
          R_action = A2
      if R_prob >= 0.5:
        if self.Game['Collin'][A1][0] > self.Game['Rowena'][A2][0]:
          C_action = A1
          C_count += 1
        else:
          C_action = A2
      else:
        if self.Game['Collin'][A1][1] > self.Game['Collin'][A2][1]:
          C_action = A1
          C_count += 1
        else:
          C_action = A2
      iteration = iteration + 1
      R = R_count / iteration
      C = C_count / iteration
      R_probs.append(R)
      C_probs.append(C)

      upper = abs(np.log(abs(R - R_prob)))
      lower = np.log(iteration)
      RoC_r.append(upper / lower)
      upper = abs(np.log(abs(C - C_prob)))
      RoC_c.append(upper / lower)
      #print("({},{}) = ({}, {})".format(R_action, C_action, R, C))
      if (abs(R_prob - R) < self.threshold) and (abs(C_prob - C) < self.threshold):
        R_prob = R
        C_prob = C
        break
      else:
        R_prob = R
        C_prob = C

    print("Convergence complete after", iteration, " iterations")
    print("After the convergence the EMS values are {} and {}".format(R_prob, C_prob))

    y = list(range(iteration))
    fig, ax = plt.subplots()
    ax.plot(y, R_probs, color='g', label='Rowena\'s EMS')
    ax.plot(y, C_probs, color='b', label='Collin\'s EMS')
    ax.legend(loc='upper right', shadow=False, fontsize='x-large')
    plt.xlabel('Iteration-->')
    plt.show()
    fig2, ax2 = plt.subplots()
    ax2.plot(y, RoC_r, 'b--', label='Rowena\'s RoC')
    ax2.plot(y, RoC_c, 'r--', label='Collin\'s RoC')
    ax2.legend(loc='upper right', shadow=False, fontsize='x-large')
    plt.xlabel('Iteration-->')
    plt.show()




if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Iterated Prisoners Dilemma Tournament')
  parser.add_argument('--u1', '-u1', type=int, default=1,  help='Top-Left utility for player1')
  parser.add_argument('--u2', '-u2', type=int, default=-1, help='Top-Right utility for player1')
  parser.add_argument('--u3', '-u3', type=int, default=-1, help='Bottom-Left utility for player1')
  parser.add_argument('--u4', '-u4', type=int, default=1, help='Bottom-Right utility for player1')
  parser.add_argument('--threshold', '-t', type=float, default=1e-6, help='threshold of probability changes between iterations')
  args = parser.parse_args()

  u1, u2, u3, u4 = args.u1, args.u2, args.u3, args.u4
  Rowena = [[u1, u2], [u3, u4]]
  Collin = [[-u1, -u2], [-u3, -u4]]
  actions = ['H', 'T']
  game = ZSGame(Rowena, Collin, actions, args.threshold)
  game.nash_equilibrium()

  game.fictitious_play()




