# When Psygotchi encounters a Wifi SSID during a scan it will use a 
# 1 way cryptographic algorithm to prep it for calculation

# when the hash is calulated all of the Letters are discarded and then the 
# numbers are added up and divided by the length of the numbers only hash
# and then converted into an integer

# Food preference is measure from 1/10(Horrible) to 10/10(Amazing!)
# We are testing hashlib's different algorithms to see the split petween food scores
# From Wifi SSID's

import hashlib
import secrets
import re

def iterate_hash_functions():
    """Generator expression to create a list of all the hash functions in hashlib."""
    for name in hashlib.__all__:
        if not name.startswith("_"):
            yield getattr(hashlib, name)

# Iterate over the list of hash functions and try each one.
overall_scores = {}
runs = 10
for i in range(runs):
  print("")
  print(f"------> run {i+1}/{runs} <------")
  print("")
  scores = {}
  test_string = secrets.token_hex(8)
  for hash_function in iterate_hash_functions():
    try:
      hasher = hash_function()
      hasher.update(test_string.encode('utf-8'))
      digest = hasher.hexdigest()
      digest = str(re.sub('\D', '', hasher.hexdigest()))
      digest_list = list(digest)
      x = 0
      for i in digest_list:
        i = int(i)
        x += i
      
      x = x / len(digest_list)
      x = int(x)
      print(f"---> {hash_function.__name__} <---")
      print(f"Digest: {digest} ")
      print(f"Length: {len(digest)}")
      print(f"Food Score: {x} / 10")
      scores[hash_function.__name__] = x
    except TypeError:
      continue
  top_algo_name = ""
  top_algo_score = 0
  for hash_algo, value in scores.items():
    # print(hash_algo)
    # print(value)
    if top_algo_score < value:
      top_algo_name = hash_algo
      top_algo_score = value
  # print(f'Top : {top_algo_name} : {top_algo_score}')
  try:
    overall_scores[top_algo_name] += 1
  except KeyError:
    overall_scores[top_algo_name] = 0
    overall_scores[top_algo_name] += 1

overall_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
print("")
print ("Overall Score Breakdown :")
for i in overall_scores:
  print(f"{i[0]} -> {i[1]:,}")

 