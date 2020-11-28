import os
import signal
import tempfile
from subprocess import PIPE, STDOUT, Popen
from tempfile import gettempdir

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.operator_helpers import context_to_airflow_vars


class PM2Operator(BaseOperator):
    template_fields = ("ecosystem",)
    template_fields_renderers = {"ecosystem": "javascript"}
    template_ext = (".js",)
    ui_color = "#3b1391"

    @apply_defaults
    def __init__(
        self,
        *,
        ecosystem: str,
        filename: str = "",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.ecosystem = ecosystem

        if filename:
            self.filename = filename
        else:
            self.file = tempfile.NamedTemporaryFile()
            self.filename = self.file.name
            self.file.write(ecosystem)

        self.start_command = ["pm2", "start", self.filename]
        self.restart_command = ["pm2", "restart", self.filename]
        self.stop_command = ["pm2", "stop", self.filename]

        if kwargs.get("xcom_push") is not None:
            raise AirflowException(
                "'xcom_push' was deprecated, use 'BaseOperator.do_xcom_push' instead"
            )

    def _execute(self, context, command):
        """
        Execute the ecosystem file command in a temporary directory
        which will be cleaned afterwards
        """
        self.log.info("Tmp dir root location: \n %s", gettempdir())

        # Prepare env for child process.
        env = os.environ.copy()

        if context:
            airflow_context_vars = context_to_airflow_vars(
                context, in_env_var_format=True
            )

        self.log.debug(
            "Exporting the following env vars:\n%s",
            "\n".join([f"{k}={v}" for k, v in airflow_context_vars.items()]),
        )
        env.update(airflow_context_vars)

        def pre_exec():
            # Restore default signal disposition and invoke setsid
            for sig in ("SIGPIPE", "SIGXFZ", "SIGXFSZ"):
                if hasattr(signal, sig):
                    signal.signal(getattr(signal, sig), signal.SIG_DFL)
            os.setsid()

        self.log.info("Running command: %s", " ".join(command))

        sub_process = Popen(  # pylint: disable=subprocess-popen-preexec-fn
            command,
            stdout=PIPE,
            stderr=STDOUT,
            cwd=gettempdir(),
            env=env,
            preexec_fn=pre_exec,
        )

        self.log.info("Output:")
        line = ""
        for raw_line in iter(sub_process.stdout.readline, b""):
            line = raw_line.decode("utf8").rstrip()
            self.log.info("%s", line)

        sub_process.wait()

        self.log.info("Command exited with return code %s", sub_process.returncode)

        if sub_process.returncode != 0:
            raise AirflowException(
                "Bash command failed. The command returned a non-zero exit code."
            )

        return line

    def execute(self, context):
        self._execute(context, self.start_command)

    def on_kill(self):
        self._execute(None, self.stop_command)
