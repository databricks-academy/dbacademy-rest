from dbacademy.dbrest import DBAcademyRestClient
from dbacademy.rest.common import ApiContainer


class JobsClient(ApiContainer):
    def __init__(self, client: DBAcademyRestClient):
        self.client = client      # Client API exposing other operations to this class

    def create(self, params):
        if "notebook_task" in params:
            print("*"*80)
            print("* DEPRECATION WARNING")
            print("* You are using the Jobs 2.0 version of create as noted by the existence of the notebook_task parameter.")
            print("* Please upgrade to the 2.1 version.")
            print("*"*80)
            return self.create_2_0(params)
        else:
            return self.create_2_1(params)

    def create_2_0(self, params):
        return self.client.execute_post_json(f"{self.client.endpoint}/api/2.0/jobs/create", params)

    def create_2_1(self, params):
        return self.client.execute_post_json(f"{self.client.endpoint}/api/2.1/jobs/create", params)

    def run_now(self, job_id: str, notebook_params: dict = None):
        payload = {
            "job_id": job_id
        }
        if notebook_params is not None:
            payload["notebook_params"] = notebook_params

        return self.client.execute_post_json(f"{self.client.endpoint}/api/2.0/jobs/run-now", payload)

    def get(self, job_id):
        return self.get_by_id(job_id)

    def get_by_id(self, job_id):
        return self.client.execute_get_json(f"{self.client.endpoint}/api/2.0/jobs/get?job_id={job_id}")

    def get_by_name(self, name):
        jobs = self.list()
        for job in jobs:
            if name == job.get("settings").get("name"):
                job_id = job["job_id"]
                return self.get_by_id(job_id)
        return None

    def list(self, offset: int = 0, limit: int = 25, expand_tasks: bool = False):

        target_url = f"{self.client.endpoint}/api/2.0/jobs/list?limit={limit}&expand_tasks={expand_tasks}"
        response = self.client.execute_get_json(target_url)
        all_jobs = response.get("jobs", list())

        while response.get("has_more", False):
            offset += limit
            response = self.client.execute_get_json(f"{target_url}&offset={offset}")
            all_jobs.extend(response.get("jobs", list()))

        return all_jobs

    def delete_by_job_id(self, job_id):
        return self.client.execute_post_json(f"{self.client.endpoint}/api/2.0/jobs/delete", {"job_id": job_id})

    def delete_by_name(self, jobs, success_only: bool):
        if type(jobs) == dict:
            job_list = list(jobs.keys())
        elif type(jobs) == list:
            job_list = jobs
        elif type(jobs) == str:
            job_list = [jobs]
        else:
            raise TypeError(f"Unsupported type: {type(jobs)}")

        # Get a list of all jobs
        jobs = self.list()

        assert type(success_only) == bool, f"Expected \"success_only\" to be of type \"bool\", found \"{success_only}\"."
        # print(f"Deleting successful jobs only: {success_only}")

        deleted = 0
        # s = "s" if len(jobs) != 1 else ""
        # print(f"Found {len(jobs)} job{s} total")

        for job_name in job_list:
            for job in jobs:
                if job_name == job["settings"]["name"]:
                    job_id = job["job_id"]

                    runs = self.client.runs().list_by_job_id(job_id)
                    # s = "s" if len(runs) != 1 else ""
                    # print(f"Found {len(runs)} run{s} for job {job_id}")
                    delete_job = True

                    for run in runs:
                        state = run.get("state")
                        result_state = state.get("result_state", None)
                        life_cycle_state = state.get("life_cycle_state", None)

                        if success_only and life_cycle_state != "TERMINATED":
                            delete_job = False
                            print(f""" - The job "{job_name}" was not "TERMINATED" but "{life_cycle_state}", this job must be deleted manually""")
                        if success_only and result_state != "SUCCESS":
                            delete_job = False
                            print(f""" - The job "{job_name}" was not "SUCCESS" but "{result_state}", this job must be deleted manually""")

                    if delete_job:
                        print(f"Deleting job #{job_id}, \"{job_name}\"")
                        for run in runs:
                            run_id = run.get("run_id")
                            print(f""" - Deleting run #{run_id}""")
                            self.client.runs().delete(run_id)

                        self.delete_by_job_id(job_id)
                        deleted += 1

        print(f"Deleted {deleted} jobs")
