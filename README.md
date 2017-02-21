# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We examine each unit for any two boxes with the same pair of digits, this will 
   form the constraint rule on all other boxes of the unit, so we iterate over the unit 
   and eliminate any of the pairs' digits from the box if exist. 
   We added such strategy to the other strategies in reduce_puzzle() and by iterating over
   all strategies we reduce the search space until we reach a solution or no further 
   change to the puzzle state.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku enforce a new rule of having the numbers 1 to 9 appear only once in each diagonal boxes.
   This rule is applied by considering each diagonal as a unit ('diagonal_units' in the code) to be examined and 
   enforced while we solve the puzzle using the constraint startegies.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.