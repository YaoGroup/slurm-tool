import logging
import sys
from pathlib import Path
import pytest

root = Path(__file__).parent.parent
sys.path.append(str(root))


from job_array import JobArray, RedirectOuput


class TestRedirectOutput:

    def test_redirect(self, tmp_path):
        redirector = RedirectOuput(tmp_path, name="test_redirect")
        jobs = [
            "python script.py --output mydirectory",
            "python script.py --output_dir mydirectory"
            "python script.py -o mydirectory",
            "python --output dir script.py",
            "python --output_dir script.py",
            "python -o dir script.py -o mydirectory"
        ]
        for job in jobs:
            with pytest.raises(ValueError):
                redirector.redirect([job], 4)

        jobs = [
            "ls --output mydirectory",
            "ls -o mydirectory",
            "ls --output_dir mydirectory",
            "python output"
            "python output_dir",
            "python --output_dir-my_file script.py",
            "python script.py --output-my_file",
            "python script -o-my_file"
        ]
        redirector.redirect(jobs, 4)


class TestSubmitSampleJob:

    def test_submit_sample_job(self, tmp_path, caplog):
        jobs = JobArray(
            name="test_sample",
            output_dir="/scratch/gpfs/mc4536/",
            node=1,
            cpus=1,
            gpus=2,
            arrays=15,
            mem_per_cpu=4,
            time=0.512,
            email="mc4536@princeton.edu"
        )

        jobs.set_env("tf24")
        jobs.submit([
            "python -c 'import tensorflow as tf; print(tf.__version__)'",
            "python -c 'from pathlib import Path; print(Path.cwd())'",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
            "python /home/mc4536/slurm_tool/_test/sample_store-files.py",
        ])


if __name__ == "__main__":
    pytest.main(["--log-cli-level=DEBUG", "-s", "-v", __file__])
