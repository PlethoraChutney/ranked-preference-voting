# Ranked preference voting
## Concept
This script allows voters to rank their candidates, rather than vote for their favorite.
If they stop ranking candidates, their vote will switch to 'No preference'. It can be
used in multi-member elections as well, in which case the threshold for an outright victory
is the number of voters divided by one plus the number of seats. This replicates the difficulty
of winning a one-member district with over half the vote.

## Algorithm
In each round of voting, we first check for an outright victory. If a number of candidates equal
to the number of seats wins an outright victory (i.e., they have more than `n / (s + 1)` votes, 
where `n` is the number of voters and `s` the number of seats), the election is over and those
candidates have won.

Otherwise, we next check the number of remaining candidates. If only a number of candidates equal
to the number of seats remains, those candidates win. This condition differs from outright victory
because it is possible for "No preference" to accumulate too many voters for enough candidates
to win outright.

If none of these end conditions are met, we find the candidates with the least votes. If there
are more than one, one of them is chosen at random. This candidate's votes are then transferred
to their next-favorite candidate, or to "No preference" if that voter has no more ranked candidates.

This process repeats until the seats are filled.

## What to watch for
It's important to pay attention to the output of the script. If one of the seats is decided by
cointoss (e.g., you have three seats and two of the final four candidates are tied), you may
want to consider another mechanism by which you can pick the more-preferred candidate.
