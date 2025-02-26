# azure-tools


The primary contents are a few classes that represent various things in azure. Namely 
1. Account
2. Subscription
3. ResourceGroup

With these you can iterate over an entire azure account looking for various things. 

see "disks.py" for an example of how to iterate over an account. 

The majority of these use the defaulit azure credential which is easily created by using the azure cli and running `az login`


To install this, clone the repo, create a virtual python environment (i.e. `python -m venv .venv & source .venv/bin/activate` then run `pip install -r requirements.txt`
