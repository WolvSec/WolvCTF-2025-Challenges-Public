This honestly might just be brute forceable, not sure how hard it would be to simulate 2^48 possibilities of password.

For the intended rev solution, this is a simple adder; essentially create a diagram of what the gates are and you'll be able to see patterns. Another possible way to do this is just to generate your own synth file using yosys and diff that from the given synth file, but I haven't really tested this for repeatability.

011101010110111001001100001100000110001101001011