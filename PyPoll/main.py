import sys
import csv

def main():
    #ensure command line criteria is met
    if len(sys.argv) != 3:
        print("Must have 3 arguments: program.py file.csv file.txt")
        sys.exit()
    elif is_valid_pyfile(sys.argv[0]) and is_valid_csvfile(sys.argv[1]):
        #create dictionary of csv file
        try:
            results = read_results(sys.argv[1])
        except KeyError:
            print(".csv format/header is incorrect, you may have the wrong .csv file")
        else:
            #total number of votes cast
            total_votes = len(results)
            #complete list of candidates who received votes and total number of votes each candidate received
            votes = candidate_votes(results)
            #winner of popular vote
            winner = election_winner(votes)
            #print election analysis to terminal
            print(
                f"\nElection Results\n"
                f"------------------------------------\n"
                f"Total Votes: {total_votes:,}\n"
                f"------------------------------------\n",end=""
                )
            for _ in votes:
                print(f"{_['candidate']} {_['votes']/total_votes*100:.3f}% ({_['votes']:,})\n",end="")
            print(
                f"------------------------------------\n"
                f"Winner: {winner['winner']}\n"
                f"------------------------------------\n"
                )

            #write election analysis file
            with open(sys.argv[2], "w") as file:
                file.write(
                f"\nElection Results\n"
                f"------------------------------------\n"
                f"Total Votes: {total_votes:,}\n"
                f"------------------------------------\n"
                )
            with open(sys.argv[2], "a") as file:
                for _ in votes:
                    file.write(f"{_['candidate']} {_['votes']/total_votes*100:.3f}% ({_['votes']:,})\n")
            with open(sys.argv[2], "a") as file:
                file.write(
                f"------------------------------------\n"
                f"Winner: {winner['winner']}\n"
                f"------------------------------------\n"
                )

def is_valid_pyfile(sysarg):
    try:
        path, extention = sysarg.split(".")
    except ValueError:
        print("Must have valid file extention: .py")
        sys.exit()
    else:
        if extention == "py":
            return True
        else:
            print("Only .py file allowed")
            sys.exit()

def is_valid_csvfile(sysarg):
    try:
        path, extention = sysarg.split(".")
    except ValueError:
        print("Must have valid file extention: .csv")
        sys.exit()
    else:
        if extention == "csv":
            return True
        else:
            print("Only .csv file allowed")
            sys.exit()

def read_results(r):
    #read results in csv file and save to dictionary
    results = []
    with open(r,"r",newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append({"ballot_id": row["Ballot ID"], "county": row["County"], "candidate": row["Candidate"]})
    return results

def candidate_votes(c):
    #create candidate list from read results dictionary
    #tabulate votes using candidate list and results dictionary
    candidate_list = []
    candidate_votes = []
    candidate = c[0].get("candidate")
    candidate_list.append(candidate)
    votes = 0
    for _ in c:
        if _["candidate"] in candidate_list:
            continue
        elif _["candidate"] not in candidate_list:
            candidate_list.append(_["candidate"])
    for candidate in candidate_list:
        for _ in c:
            if _["candidate"] == candidate:
                votes = votes + 1
        candidate_votes.append({"candidate": candidate, "votes": votes})
        votes = 0
    return candidate_votes

def election_winner(w):
    #calculate winner
    most_votes = 0
    winner = "candidate"
    for _ in w:
        if _["votes"] > most_votes:
            winner = _["candidate"]
            most_votes = _["votes"]
    return {"winner": winner, "most_votes": most_votes}

if __name__ == "__main__":
    main()