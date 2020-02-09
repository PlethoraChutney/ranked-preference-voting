import pandas as pd
from collections import Counter
import random
import argparse

class Voter:
    def __init__(self, timestamp, votes):
        self.timestamp = timestamp
        self.votes = [x for x in votes if str(x) != 'nan']
        self.current_vote = ''

    def __repr__(self):
        return f'Voter {self.timestamp}, votes: {self.votes}'

    def poll_voter(self):
        try:
            self.current_vote = self.votes.pop(0)
        except IndexError:
            self.current_vote = 'No preference'

def make_voters(csv):
    votes = pd.read_csv(csv)
    list_votes = votes.values.tolist()
    voters = []
    for i in range(votes.shape[0]):
        row = list_votes[i]
        new_voter = Voter(row[0], row[1:])
        voters.append(new_voter)

    return voters


def run_election(voters, seats):

    majority_threshold = len(voters) / (1 + seats)
    print(f'Number of voters: {len(voters)}')
    print(f'Number of seats: {seats}')
    print(f'Majority threshold: {majority_threshold}\n')

    election_complete = False
    i = 0
    for voter in voters:
        voter.poll_voter()

    knocked_out = []

    while i < len(voters):
        i += 1
        print(f'Round {i} of voting:')
        current_votes = [v.current_vote for v in voters]
        per_candidate = Counter(current_votes)
        print(dict(per_candidate))

        majority_winners = [x[0] for x in per_candidate.most_common() if x[1] > majority_threshold]

        if len(majority_winners) == seats:
            election_complete = 'majority winners'
            break
        elif len([x for x in per_candidate if x != 'No preference']) == seats:
            election_complete = 'elimination'
            break
        elif len([x for x in per_candidate if x != 'No preference']) > seats:
            least_popular = per_candidate.most_common()[-1]
            if least_popular[0] == 'No preference':
                least_popular = per_candidate.most_common()[-2]

            least_populars = [x[0] for x in per_candidate.most_common() if x[1] == least_popular[1] and x[0] != 'No preference']

            if len(least_populars) == 1:
                knocked_out.append(least_populars[0])
                print(f'Least popular candidate: {least_populars[0]}. Reassigning their votes.')
            else:
                to_knock = random.choice(least_populars)
                knocked_out.append(to_knock)
                print(f'Least popular candidates: {least_populars}.\nRandomly chose {to_knock}, reassigning their votes.')
            for voter in voters:
                while voter.current_vote in knocked_out:
                    voter.poll_voter()
        else:
            break
        print()

    if election_complete:
        print(f'Election complete by {election_complete}')
        return [x[0] for x in per_candidate.most_common()[0:seats]]
    else:
        print('Somehow, the election failed')

parser = argparse.ArgumentParser(description = 'Run a ranked choice election.')
parser.add_argument('votes', help = 'A .csv file containing ')
parser.add_argument('seats', help = 'Number of seats available', type = int)
args = parser.parse_args()

def main():
    voters = make_voters(args.votes)
    return run_election(voters, args.seats)

if __name__ == '__main__':
    print(f'Winner(s): {main()}')
