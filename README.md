# PSR DB POPULATOR

A tool to populate an empty DB with reproducible noise. By noise we mean what we were getting by running PSRs in a fresh clone of the production DB
- Orgs from customers
- Jobs running


This tool emulates the data you can find in production environments
- Orgs, users, jobs per org, running jobs, num of engines etc follow the same distribution as observed in production
- Some variables must be rewritten (which can also be done with this tool) such as engines/SVS IP etc
- Everything will ideally work as it does in prod (e.g. we won't need to turn subscriptions off, we won't get credential errors or connectivity issues from customer jobs trying to interact with a non-reachable engine).


# How to run the tool
Make sure your python interpreter has all the required dependencies to run this project.
You can either run `pip install -r requirements.txt` or use the dockerized version of the tool (more on this later)

```
python --sch-url ${SCH_URL} --random-seed ${RANDOM_SEED} --action create|test
```

# Containerized version
If you don't trust your system's interpreter, you want to make sure that results are as exact as possible between many different runs or you just like Docker because it adds an extra layer of complexity and makes you feel smart, you can build and run the tool from its own docker image
`docker build -t psr_populator`


# Creating Reproducible DB Dumps
A DB dump is generated taking into account the following three variables:
- Git commit/tag (either checkout or `docker pull` any released version)
- RNG seed (--random-seed)
- Target SCH version (--sch-version) since it affects the SDK version we will load


# What's out of scope?
- Engines can be anything since we are only concerned about the DB here, so the same DB dump using mock SDCs will give a completely different result than if ran using CSP engines
- This tool implements "passive noise" e.g. it doesn't emulate customers creating or deleting stuff
- Since part of the passive noise entails "ghost orgs" running scheduled tasks this might make PSRs a bit harder to analyze. However, since PSR tests are randomly ran for extended period of times we can trust the law of big numbers to deem such randomness as irrelevant
- There are many entities such as job run histories, audits and other stuff that might vary between runs

These other items should be either handled elsewhere or we should at least acknowledge the noise introduced by them


# Why this tool?
Prod data, although trivial to obtain, is not consistent across PSRs. We wanted to still be able to run PSRs using that "background noise" since it's the most realistic environment we could ever come up with but we wanted to make it reproducible.
## Why are creating the DB Dump offline each time we want to run a PSR? Wouldn't it be enough to just create one and keep reusing it?
That would be great if DB updates weren't a thing, but unfortunately they are.


# TODO LIST
- Figure out what information should we get from production data and how
- Do a study using the obtained data
- Define a data model for "SCH noise" that can represent the observed data and its underlying distributions
- Write some code so we can use the previous data model to automatically create 
