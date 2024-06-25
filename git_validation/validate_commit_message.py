import re
import sys


def validate_commit_message(message):
    pattern = re.compile(r'^(feat|fix|docs|style|refactor|test|chore)(\(\w+\))?: .{1,50}\n\n.{1,}\n\n(Closes #\d+)?$',
                         re.DOTALL)
    return pattern.match(message) is not None


def main():
    commit_message_filepath = sys.argv[1]
    with open(commit_message_filepath, 'r') as file:
        commit_message = file.read().strip()

    if validate_commit_message(commit_message):
        print("Commit message is valid.")
        sys.exit(0)
    else:
        print("Invalid commit message format.")
        sys.exit(1)


if __name__ == "__main__":
    main()