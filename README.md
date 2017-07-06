# Reinforcement Learning to Discover Betting Strategy

Draft

## Case Study : *The Sting* (1973)

Whenever I express my love for movies, often times people ask me what my all-time favorite movie is. This is very hard question to answer since I cannot compare 2 movies with the same criteria. Should I go for the old classic *Casablanca*, or my childhood memory of *Star Wars* franchise? Or even the nostalgia to my homeland, *Yojimbo* and *Tokyo Story*? Even though it seems just impossible to tell my 'all-time favorite', the up-lifting opening sequence of *The Sting* always has a special place in me.

This Oscar winning crime comedy is the revenge story of young conman set in 70's Chicago. Young hustler accidentally steals money from the infamous gangster, and loses his partner. To revenge for the loss of his partner, , he decides to play the largest set-up to  

### Previous Study
Poker bot is one of the hardest bot to create. Recently the cutting-edge technology of Carnegie Mellon University finally beat the professional player for the first time in the history. There are multiple factors to make this problem particularly challenging.

1. Indeterministic Probability Space

  The probability of winning / losing changes over time in the duration of time. Also within the same deal. For example,

2. Too much unknowns

  Supervised learning method will require set of inputs and corresponding labels. This means, the artificial intelligence needs to have ground truths to draw statistical inference. Reinforcement learning will allow agents to learn the optimal policy by "trials and errors", however this method needs to have information from the game state. Poker is very challenging since players don't know not only the opponents hands, but also his own hands until the end of the game. The decision process (raise of fold) takes place while there are many unknowns, which makes it hard to play.

3. Players can bluff and beat the odds.

  Finally the best player will play bluff to make other players believe he has certain hands. This will enter a study of human behavior and psychology, and statistical analysis and optimization often struggles to learn. From this reason, human player can usually outsmart artificial intelligence.

### Problems
In order to teach AI to gamble, we need to simplify the problem a lot. The objective of this project is to teach how to "bet", and not necessarily how to win poker. I wanted to see my bot will compromise small lost in the current game play to achieve overall win. For above reasons, I decided to implement Bacarrat.

### Why Bacarrat
Bacarrat is the perfect game to teach AI especially if you are interested in betting strategy. Also it is probability most statistically strategical game in casino. I chose Bacarrat for the following reasons.

1. AI can simply keep betting on the dealer.

  It is, in fact, the most common strategy to keep betting on dealer (you can also bet on player but it is less profitable). The player also has an option to bet on tie, but the expected value is the lowest and even human player will never play this way. This will allow AI to only focus on betting strategy rather than the game play itself.

2. We know the ground truth for the probability space

  This could be the strongest asset of Bacarrat. The game knows the exact probability of winning and losing, and this value does not change. Ok. If you go to the actual casino, there are some tables that

3. This game is all about shot/long-term betting strategy

### Game State
The reinforcement learning will train the agent to find the optimal function, mapping the game environment to the game command. I looked through the existing strategies of Bacarrat are all independent from the result of game (whether or not dealer wins), but it considers following criteria.
1. How many games have been played
2. How much money the player has won / lost so far
3. How many consecutive games the player has won / lost
4. Total wins / total lost within past x games (long-time and short-term)
