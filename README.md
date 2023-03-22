# PSR DB POPULATOR

A tool to populate an empty DB with reproducible background noise. By noise we mean what we were getting by running PSRs in a fresh clone of the production DB
- Orgs from customers
- Jobs running


This tool emulates the data you can find in production environments
- Orgs, users, jobs per org, running jobs, num of engines etc follow the same distribution as observed in production
- Some variables must be rewritten (which can also be done with this tool) such as engines/SVS IP etc
- Everything will ideally work as it does in prod (e.g. we won't need to turn subscriptions off, we won't get credential errors or connectivity issues from customer jobs trying to interact with a non-reachable engine).


# Process overview
- Create a "DB status" represented in a JSON file. This is guaranteed to be reproducible as long as the same random seed is used along with number of orgs and overall Python env configuration
- Use this JSON file to create the user organizations in Control Hub
- Setup the engines in SCH for each org
- Use this JSON file again to start the jobs that are supposed to be active. Since we are using no specific labels for those engines we should expect uniform load balancing between all those engines
- Using that "seed JSON" again, verify that the state of the DB is consistent with what we intended to create
- Now we're ready to start the PSR itself


# How to run the tool
Make sure your python interpreter has all the required dependencies to run this project.
You can either run `pip install -r requirements.txt` or use the dockerized version of the tool (more on this later)

## Create JSON model
```
usage: PSR DB populator [-h] [--random-seed RANDOM_SEED] [--num-orgs NUM_ORGS] [--use-sample-schema] [--data-model-root DATA_MODEL_ROOT]

optional arguments:
  -h, --help            show this help message and exit
  --random-seed RANDOM_SEED
                        Random seed Default: 19071990
  --num-orgs NUM_ORGS   Num orgs Default: 10
  --use-sample-schema   Use a smaller schema instead of the real one for testing purposes Default: False
  --data-model-root DATA_MODEL_ROOT
                        Root for data model files Default: /Users/sergio/git/psr_db_populator
```

## Populate SCH DB from JSON model

```
usage: Populate SCH from JSON specification [-h] [--sch-url SCH_URL] [--sch-username SCH_USERNAME] [--sch-password SCH_PASSWORD] [--sch-authoring-sdc SCH_AUTHORING_SDC]
                                            json_file

positional arguments:
  json_file             JSON File

optional arguments:
  -h, --help            show this help message and exit
  --sch-url SCH_URL     (3x only) SCH URL Default: http://192.168.132.55:18631
  --sch-username SCH_USERNAME
                        (3x only) SCH Admin Username Default: admin@admin
  --sch-password SCH_PASSWORD
                        (3x only) SCH Admin Password Default: admin@admin
  --sch-authoring-sdc SCH_AUTHORING_SDC
                        (3x only) SCH Authoring SDC Default: http://192.168.132.55:18630
```


# Containerized version
TODO


# What's out of scope? What are the limitations?
- Engines can be anything since we are only concerned about the DB here, so the same DB dump using mock SDCs will give completely different PSR results than if ran using CSP engines
- This tool implements "passive noise" e.g. it doesn't emulate customers creating or deleting stuff. Think of all those orgs as a "ghost town"
- Since part of the passive noise entails "ghost orgs" running scheduled tasks this might make PSRs a bit harder to analyze. However, since PSR tests are randomly ran for extended period of times we can trust the law of big numbers to deem such randomness as irrelevant
- There are many entities such as job run histories, audits and other stuff that might vary between runs, although we can expect them to be similar and consistent enough to not care about the specific numbers


These other items should be either handled elsewhere or we should at least acknowledge them as sources of variance


# Why this tool?
Prod data, although trivial to obtain, is not consistent across PSRs. We wanted to still be able to run PSRs using that "background noise" since it's the most realistic environment we could ever come up but we wanted to guarantee reproducibility


## Why is this process so complex? Wouldn't it be easier to just create a DB dump and keep using it for any PSR we might like to run?
That would be certainly an option if DB upgrades weren't a thing, but unfortunately they are. Also, splitting this process into many steps, one of them being verification, will allow us to construct the background baseline PSR model offline, so it won't affect the outcome of the PSR itself. It will also give us more time to prepare such PSR as we will have virtually unlimited attempts to reconstruct the proposed DB from a fixed JSON model


# TODO LIST
- Figure out what information should we get from production data and how
- Do a study using the obtained data
- Define a data model for "SCH noise" that can represent the observed data and its underlying distributions
- Write some code so we can use the previous data model to automatically create 
- Use entrypoint scripts to all the features so it's easier to figure out what are callable modules and what are accessory files
