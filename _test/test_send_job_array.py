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
            output_dir="",
            node=1,
            cpus=1,
            gpus=2,
            arrays=4,
            mem_per_cpu=4,
            time=0.512,
            email="mc4536@princeton.edu"
        )

        jobs.set_env("tf24")
        jobs.submit([
            "python -c 'import tensorflow as tf; print(tf.__version__)'",
            "python ./test/sample_list-gpus.py"
        ])


if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])
