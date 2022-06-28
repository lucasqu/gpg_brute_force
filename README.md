# gpg_brute_force

This program will try to get the passphrase for your secret key back.

Just run `python brute_force.py <file>` (`<file>` has been encrypted by the key you want to brute force).
This only works if you have the corresponding secret key.

In `brute_force.py` you have to modify the variable `password_tree`.
Each subarray of password_tree corresponds to a possible branch. All branches are sequentially put together in all possible combinations.
Each of these combinations are piped to `gpg` and tested.

In case you run this program multiple times you will be asked whether you want to safe the passwords you already checked to a file.
If you rerun the program it will only check the passwords, which are not that file.
During the checking you can interrupt the program with `ctrl-c`. Then you will be prompted whether you want to safe the passwords you checked
until the interruption.

# Example
```
password_tree = [
["def", "g", "hijk"],
["efg"],
["a", ""],
]
```
This would yield the `3*1*2 = 6` combinations
```
['defefga', 'defefg', 'gefga', 'gefg', 'hijkefga', 'hijkefg'].
```
