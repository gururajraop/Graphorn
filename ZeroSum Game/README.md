# Fictitious play
A simple program to simulate the fictitious play for a two player, two action zero sum game

## **Requirements:**
* Programs: Python3
* Packages: numpy, nashpy, matplotlib

## How to run
```
python main.py
```
One can also add the command line arguments to generate their own zer-sum game. By default it will play matching pennies game.

To give your own game pass the utilities of player 1 in top-left, top-right, bottom-left and bottom-right order. It can be done as below
```
python main.py -u1 <top-left-utility> -u2 <top-right-utility> -u3 <bottom-left-utility> -u4 <bottom-right-utility>
```

To specify the threshold please use -t argument. Default value is 1e-6
```
python main.py -t 0.001
```
