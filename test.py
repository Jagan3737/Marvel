import string

num_list = list(range(0, 10))
num_string_list = [str(x) for x in num_list]

print(num_string_list+list(string.ascii_lowercase))
print()