import sys
from pathlib import Path
import pytest

root = Path(__file__).parent.parent
sys.path.append(str(root))


from job_array import JobArray


class TestSubmitSampleJob:

    def test_submit_sample_job(self):
        jobs = JobArray(
            name="test_sample",
            output_file="",
            node=1,
            cpus=1,
            gpus=1,
            arrays=4,
            mem_per_cpu=1,
            time=0.512,
            email="mc4536@princeton.edu"
        )

        jobs.module_load("anaconda3/2020.11")
        jobs.add_prestep("conda activate tf24")
        jobs.submit([
            "python3 sample_job.py param1-1 param2-1",
            "python3 sample_job.py param1-2 param2-2",
            "python3 sample_job.py param1-3 param2-3",
            "python3 sample_job.py param1-4 param2-4",
            "python3 sample_job.py param1-5 param2-5"
        ])


if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])
