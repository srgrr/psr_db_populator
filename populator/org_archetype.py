import logging
from collections import namedtuple
from populator.rng import random_string, random_integer, choice
config_interval = namedtuple("interval", "min max")


class OrgArchetype(object):

    def __init__(self,
                 archetype_name: str,
                 enable_subs: bool,
                 max_users: int,
                 max_job_runs: int,
                 max_scheduled_runs: int,
                 max_engines: int,
                 max_pipelines: int,
                 users: config_interval,
                 engines: config_interval,
                 pipelines: config_interval,
                 active_jobs: config_interval,
                 inactive_jobs: config_interval,
                 scheduled_tasks: config_interval,
                 subscriptions: config_interval
                 ):
        logging.debug(f"Creating org archetype from args {locals()}")
        self.archetype_name = archetype_name
        self.enable_subs = enable_subs
        self.max_users = max_users
        self.max_job_runs = max_job_runs
        self.max_scheduled_runs = max_scheduled_runs
        self.max_engines = max_engines
        self.max_pipelines = max_pipelines
        self.users = users
        self.engines = engines
        self.pipelines = pipelines
        self.active_jobs = active_jobs
        self.inactive_jobs = inactive_jobs
        self.scheduled_tasks = scheduled_tasks
        self.subscriptions = subscriptions

        def _interval_error_msg(interval, max_value, feature):
            return f"Specified interval for {feature}={interval} may potentially exceed org config for max {feature}={max_value}"

        assert self.users.max <= self.max_users, _interval_error_msg(self.users, self.max_users, "users")
        assert self.engines.max <= self.max_engines, _interval_error_msg(self.engines, self.max_engines, "engines")
        assert self.pipelines.max <= self.max_pipelines, _interval_error_msg(self.pipelines, self.max_pipelines, "pipelines")
        assert self.active_jobs.max <= self.max_job_runs, _interval_error_msg(self.active_jobs, self.max_job_runs, "active jobs")
        assert self.scheduled_tasks.max <= self.max_scheduled_runs, _interval_error_msg(self.scheduled_tasks, self.max_scheduled_runs, "scheduled tasks")

    def get_specific_instance(self):
        org_name = random_string(10)
        ret = {
            "org_name": org_name,
            "enable_subs": self.enable_subs,
            "max_users": self.max_users,
            "max_jobs_runs": self.max_job_runs,
            "max_scheduled_runs": self.max_scheduled_runs,
            "max_engines": self.max_engines,
            "max_pipelines": self.max_pipelines
        }
        logging.debug(f"Creating specific org with name {org_name}")
        # Create some users
        ret["users"] = []
        num_users = random_integer(self.users.min, self.users.max)
        for user_idx in range(num_users):
            username = random_string(5)
            ret.get("users").append(
                {
                    "json-id": user_idx,
                    "username": username,
                    "role": "sys-admin"
                }
            )
        logging.debug(f"Org will have {num_users} users")
        # "Create" some engines
        num_engines = random_integer(self.engines.min, self.engines.max)
        ret["engines"] = []
        for engine_idx in range(num_engines):
            ret.get("engines").append(
                {
                    "json-id": engine_idx,
                    "labels": "all"
                }
            )
        logging.debug(f"Org will have {num_engines} engines")
        # Create some pipelines
        num_pipelines = random_integer(self.pipelines.min, self.pipelines.max)
        ret["pipelines"] = []
        for pipeline_idx in range(num_pipelines):
            ret.get("pipelines").append(
                {
                    "json-id": pipeline_idx,
                    "owner": random_integer(0, num_users - 1)
                }
            )
        logging.debug(f"Org will have {num_pipelines} pipelines")
        # Create some jobs
        num_inactive_jobs = random_integer(self.inactive_jobs.min, self.inactive_jobs.max)
        ret["jobs"] = []
        for inactive_job_idx in range(num_inactive_jobs):
            ret.get("jobs").append(
                {
                    "json-id": inactive_job_idx,
                    "pipeline": random_integer(0, num_pipelines - 1),
                    "status": "INACTIVE",
                    "owner": random_integer(0, num_users - 1)
                }
            )
        logging.debug(f"Org will have {num_inactive_jobs} inactive jobs")
        num_active_jobs = random_integer(self.active_jobs.min, self.active_jobs.max)
        for active_job_idx in range(num_active_jobs):
            ret.get("jobs").append(
                {
                    "json-id": active_job_idx,
                    "pipeline": random_integer(0, num_pipelines - 1),
                    "status": "ACTIVE",
                    "owner": random_integer(0, num_users - 1)
                }
            )
        logging.debug(f"Org will have {num_active_jobs} active jobs")
        # Create some scheduled tasks
        num_scheduled_tasks = random_integer(self.scheduled_tasks.min, self.scheduled_tasks.max)
        ret["scheduled_tasks"] = []
        for scheduled_task_idx in range(num_scheduled_tasks):
            ret.get("scheduled_tasks").append(
                {
                    "json-id": scheduled_task_idx,
                    # inactive jobs are just there to make the database bigger
                    "job": random_integer(0, num_active_jobs - 1),
                    "action": choice(["start", "stop"]),
                    # 1-minute cron masks starting at random seconds
                    "second": random_integer(0, 59),
                    "owner": random_integer(0, num_users - 1)

                }
            )
        logging.debug(f"Org will have {num_scheduled_tasks} scheduled tasks")
        # Create some subscriptions (doesn't matter if subs are enabled or not)
        num_subscriptions = random_integer(self.subscriptions.min, self.subscriptions.max)
        ret["subscriptions"] = []
        for subscription_idx in range(num_subscriptions):
            ret.get("subscriptions").append(
                {
                    "json-id": subscription_idx,
                    "job": random_integer(0, num_active_jobs - 1),
                    "kind": choice(["INACTIVE->ACTIVE", "ACTIVE->INACTIVE"]),
                    "owner": random_integer(0, num_users - 1)
                }
            )
        logging.debug(f"Org will have {num_subscriptions} subscriptions")
        return ret

    @staticmethod
    def _str2interval(interval_value: str):
        lo, hi = map(int, interval_value.split(","))
        return config_interval(lo, hi)

    @staticmethod
    def from_archetype(org_name, archetype_config):
        return OrgArchetype(
            org_name,
            bool(archetype_config.get("global-configs", "enable-subs")),
            int(archetype_config.get("global-configs", "max-users")),
            int(archetype_config.get("global-configs", "max-job-runs")),
            int(archetype_config.get("global-configs", "max-scheduled-runs")),
            int(archetype_config.get("global-configs", "max-engines")),
            int(archetype_config.get("global-configs", "max-pipelines")),
            OrgArchetype._str2interval(archetype_config.get("population", "users")),
            OrgArchetype._str2interval(archetype_config.get("population", "engines")),
            OrgArchetype._str2interval(archetype_config.get("population", "pipelines")),
            OrgArchetype._str2interval(archetype_config.get("population", "active-jobs")),
            OrgArchetype._str2interval(archetype_config.get("population", "inactive-jobs")),
            OrgArchetype._str2interval(archetype_config.get("population", "scheduled-tasks")),
            OrgArchetype._str2interval(archetype_config.get("population", "subscriptions"))
        )
