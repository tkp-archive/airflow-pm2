import os

# from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

# from airflow.utils.operator_helpers import context_to_airflow_vars

# from .pm2 import makedirs, tempdir, pid, start, restart, stop, reload
from .pm2 import makedirs, tempdir, pid, start, stop, reload


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

        # the pm2 ecosystem json
        self.ecosystem = ecosystem

        if filename:
            # if file already exists

            # keep path to it
            self.filename = filename

            # set dirname, can ignore
            self.dirname = os.path.dirname(filename)

        else:
            # if file does not exist, make a temporary one
            self.filename = os.path.join(tempdir(), "{}.json".format(self.task_id))

            # set dirname, can ignore
            self.dirname = os.path.dirname(filename)

        if not os.path.exists(self.filename):
            # make directory
            makedirs(self.dirname)

            # open file
            with open(self.filename, "w") as fp:
                # write the ecosystem file
                fp.write(self.ecosystem)

    def execute(self, context):
        # if running, stop and restart
        if pid(self.filename):
            # stop existing job
            stop(self.filename)

        # reload ecosystem
        reload(self.filename)

        # start ecosystem
        start(self.filename)

    def on_kill(self):
        # if running, stop and restart
        if pid(self.filename):
            # stop existing job
            stop(self.filename)
