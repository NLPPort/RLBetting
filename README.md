# Reinforcement Learning to Discover Betting Strategy

Draft
## Inspiration : *The Sting* (1973)

As an avid movie lover, one of the toughest question to answer is: 'what's your all-time favorite movie?'. Certainly, it seems almost impossible to pick *my favorite movie of all-time*, however, the up-lifting opening sequence of *The Sting (1973)* with the melody of *The Entertainer* will always have a special place in my heart.

This Oscar winning crime comedy is the story of 2 con artists; the young and fearless Hooker played by Robert Redford, and the old and experienced Henry played by Paul Newman. Both conmen seek revenge on a Chicago mob boss, Lonnegan, who murdered one of their mutual fellows. In spite of the juxtaposition between their characteristics, 2 conmen show the chemistry and plan the biggest set-up to win their money back from Lonnegan.

If you have not seen this old classic, you must experience the climax of their set-up without any spoilers. Since the first time I saw this movie, I have been captured by the charming acting, riveting twists and skillful film-crafting.

Without spoiling too much, the concept of their scheme is **take small losses, but never miss big wins**.

This inspired me to answer a following question:
**Can machine learning understand the concept of accepting loss for the sake of large wins in the future?**

### Problems
Conventional supervised learning requires a set of inputs and respective labels. For example, the model will predict the optimal hands to play based on current environment such as the amount of money you have, how strong your current hands are, how lucky you feel today. This means we need to know the optimal actions to take given the input even before training the model.

The challenge of our situation is that we don't know the optimal solution when we start the simulation. This means, our model needs to explore the environment without any previous knowledge and develop the strategy to the game through their experiences. This technique is called **reinforcement learning**. We are going to simulate the situation of accepting loss for the larger win using this concept.
For this purpose, I concluded that the card game **baccarat** and the discovery of the optimal betting strategy would be a perfect simulation.

### Why Baccarat
Baccarat is one of the simplest games in casino similar to black jack. The twist is, you don't even need to know how to play. The players only need to guess the result of the next game and bet on it. There are only 3 options: player will win, banker(dealer) will win, or they will tie. If the player guesses correctly, he will get the money back based on how much he best. There are mainly 2 reasons to why I chose this particular situation for the training environment.

* **Player can simply keep betting on the dealer.**

  Here it is. This is the golden rule. In Baccarat, you will get higher return if you guess tie correctly, but it is the riskiest odds to play. In fact, it is already known the **exact** probability and expected value of each guess. Of course, in real life, you could feel lucky or the table you sit could produce more wins for player. In theory, however, if you play the game of Baccarat long enough, each hands should converge to the following probability. Hence, our model can simply keep betting on the banker; the hands with highest expected value.


  |        | Probability of Winning |  Return | Expected Value  |
  |--------|------------------------|---------|-----------------|
  | Player |          .4462         |  +1     |   -0.012351     |
  | Banker |          .4585         |  +.95   |   -0.010579     |
  | Tie    |          .0953         |  +8     |   -0.143596     |


* **This game is all about short/long-term betting strategy**

  The existing strategy of Baccarat is all about the repetition of betting pattern. All strategies expect players to bet on banker all the time. It's a systematic betting pattern that can be evaluated mathematically. For example, the famous 1324 system works as follows. Starting from 1 unit of your bet, you will bet progressively with the sequence of 1 unit, 3 units, 2 units, 4 units until you lose. If you lose, you  start over from 1. If you reach to 4, you will also start over as well. As you see, this process is programming friendly due to its systematic nature. From this reason, our learning model is able to simplify the gaming situation and only focus on the discovery of this betting pattern.   




### Game State
The reinforcement learning will train the agent to find the optimal function, mapping the game environment to the game command. I looked through the existing strategies of Bacarrat are all independent from the result of game (whether or not dealer wins), but it considers following criteria.
1. How many games have been played
2. How much money the player has won / lost so far
3. How many consecutive games the player has won / lost
4. Total wins / total lost within past x games (long-time and short-term)
