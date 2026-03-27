import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    result = {}
    with open(sys.argv[1], newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            # Convert the other values to integers
            result[name] = {key: int(value) for key, value in row.items() if key != "name"}
    # print(f"Dict to lookup: {result}")

    # TODO: Read DNA sequence file into a variable
    # Open a text file for reading
    with open(sys.argv[2], 'r') as f:
        # Read the entire content of the file
        content = f.read()

    # TODO: Find longest match of each STR in DNA sequence
    str_counts = {}
    for str in reader.fieldnames[1:]:
        str_counts[str] = longest_match(content, str)
    # print(f"Dict given: {str_counts}")

    # TODO: Check database for matching profiles
    for key in result.keys():
        if result[key] == str_counts:
            print(key)
            return
    print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
