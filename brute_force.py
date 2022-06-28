from itertools import product
from pathlib import Path
from sys import argv
import math
from colorama import Fore
from subprocess import run, DEVNULL

password_tree = [
    ["def", "g", "hijk"],
    ["efg"],
    ["a", ""],
]

def get_password_combinations(password_tree, idx,
                              password_combinations=[""]):
    """
    A recursive function, which aims to find all possible password
    combinations.
    
    Parameters:
    -----------
    password_tree : array
        Each subarray contains strings, which the password could contain.
        The order of the subarrays corresponds to the order of the string
        combinations.
    password_combinations : array
        Array of possible password combinations. It consists of combinations
        up to `password_tree[idx]`. By default `[""]` in order to have an
        array to append to.
    idx : int
        Current index of `password_tree`.

    Returns:
    --------
    password_combinations : array
        Password combinations up to the index `idx` of `password_tree`.
    """
    # if index is not in password_tree
    if idx > len(password_tree)-1 :
        return password_combinations
    # extend old combinations
    extended_combinations = []
    for tree_branch in product(password_combinations, password_tree[idx]):
        extended_combinations += ["".join(tree_branch)]
    # rerun with extended combinations and later index
    return get_password_combinations(password_tree, idx+1,
                                     extended_combinations)

def check_new(possible_passwords, filename="already_tested.txt"):
    """
    Check which passwords have already been tested.

    Parameters:
    -----------
    possible_passwords : array
        List of password combinations according to `password_tree`.
    filename : string
        Name of a file in the directory of the script, where the tested
        passwords are stored.

    Returns:
    --------
    new_passwords : array
        Passwords that haven't been checked before.
    new_count : int
        Length of the `new_passwords` array.
    """
    if not Path(filename).exists():
        Path(filename).touch()

    with open(filename, "r+") as file:
        already_tested = file.read().splitlines()
        same_passwords = set(already_tested).intersection(possible_passwords)
        possible_passwords = set(possible_passwords)
        new_passwords = list(possible_passwords - same_passwords)

    poss_count = len(possible_passwords)
    same_count = len(same_passwords)
    new_count = len(new_passwords)

    if poss_count == same_count:
        print(f"All {poss_count} passwords for these combinations " \
              + "have already been checked.")
        quit()
    if poss_count != new_count:
        print("Reduced checkable passwords from " \
              + f"{poss_count} to {new_count},\n" \
              + f"because {same_count} passwords have already been tested.")
    return new_passwords, new_count

def store_passwords(new_passwords, filename="already_tested.txt"):
    """
    stores `new_passwords` inside `filename`

    Parameters:
    -----------
    new_passwords : array
        Array of passwords, which can be saved.
    filename : string
        Storage location.
    """
    if input(f"Add {len(new_passwords)} new passwords " \
             + f"to {filename}? [y/n]: ") == "y":
        with open(filename, "a+") as file:
            file.write("\n".join(new_passwords))
            file.write("\n")


def main():
    #user_id = "your_user_id"
    test_file = argv[1]

    gpg_decryption_command = [
        "gpg",
        "--decrypt",
        # set file descriptor to 0 to read from stdin
        "--passphrase-fd", "0",
        "--pinentry-mode", "loopback",
        # the user id name, I think thats not required
        #"--recipient", user_id,
        # a test file you want to decrypt
        test_file
    ]

    possible_passwords = get_password_combinations(password_tree, 0)

    new_passwords, new_count = check_new(possible_passwords)

    preceding_0s = math.ceil(math.log10(new_count))

    for i, possible_password in enumerate(new_passwords, start=1):
        try:
            print(f'[{str(i).zfill(preceding_0s)}/{new_count}]\n'
                  + '==> checking ' \
                  + f'\"{Fore.YELLOW}{possible_password}{Fore.WHITE}\"',
                  end="\t")
            password = possible_password.encode('UTF-8')
            rc = run(gpg_decryption_command,
                     input=password,
                     stdout=DEVNULL,
                     stderr=DEVNULL).returncode

            if rc == 0:
                print(f'{Fore.GREEN}success{Fore.WHITE}')
                quit()
            else:
                print(f'{Fore.RED}failed{Fore.WHITE}')

        except KeyboardInterrupt:
            print("")
            store_passwords(new_passwords[:i-1])
            quit()

    store_passwords(new_passwords)

if __name__ == "__main__":
    main()
