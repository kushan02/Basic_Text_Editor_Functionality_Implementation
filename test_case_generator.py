import random
import string

for i in range(0, 10):
    with open("tests/large/test_large_{}.txt".format(i), "w") as f:
        for j in range(random.randint(555555, 999999)):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for k in range(random.randint(1, 10)))
            f.write(result_str + " ")

    print("Generated test_large_{}.txt".format(i))

for i in range(0, 10):
    with open("tests/medium/test_medium_{}.txt".format(i), "w") as f:
        for j in range(random.randint(77777, 99999)):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for k in range(random.randint(1, 10)))
            f.write(result_str + " ")

    print("Generated test_medium_{}.txt".format(i))

for i in range(0, 10):
    with open("tests/small/test_small_{}.txt".format(i), "w") as f:
        for j in range(random.randint(500, 1000)):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for k in range(random.randint(1, 10)))
            f.write(result_str + " ")

    print("Generated test_small_{}.txt".format(i))
