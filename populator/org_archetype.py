import logging
from collections import namedtuple
from populator.rng import random_string
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
        logging.debug(f"Creating org from args {locals()}")
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
        ret = {
            "org_name": random_string(10),
            "enable_subs": self.enable_subs,
            "max_users": self.max_users,
            "max_jobs_runs": self.max_job_runs,
            "max_scheduled_runs": self.max_scheduled_runs,
            "max_engines": self.max_engines,
            "max_pipelines": self.max_pipelines
        }
        logging.debug(f"Creating specific org '{ret.get('org_name')}'")
        # Create some users
        pass
        # "Create" some engines
        pass
        # Create some pipelines
        pass
        # Create some jobs
        pass
        # Create some scheduled tasks
        pass
        # Create some subscriptions (doesnt't matter if subs are enabled or not)
        pass
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
