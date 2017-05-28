from django.core.management.base import BaseCommand
from django.db import DataError

from job.models import JobsInfo

import glob
import logging
import json

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Migrate data from json file to django models'

    def __init__(self):
        super().__init__()
        self.path_file_suffix = "/*.json"
        # self.unknown = "unknown"

    def read_json_file_data(self, path_file):
        with open(path_file) as f:
            out = f.read()
            data = json.loads(out)
        return data

    def add_arguments(self, parser):
        parser.add_argument('path_json_folder', nargs='+', type=str)

    def handle(self, *args, **options):
        path_files = glob.glob(
            options['path_json_folder'][0] + self.path_file_suffix
        )
        unknown = "unknown"
        for path_file in path_files:
            jobs = self.read_json_file_data(path_file)
            for job in jobs:
                name = job.get('name', unknown)
                try:
                    # company = CompanyProfile.objects.create(
                    #     name=job.get('company', unknown),
                    #     address=job.get('address', unknown),
                    #     city=job.get('province', 'Ha Noi'),
                    #     size=job.get('size', unknown)
                    # )
                    # company.membership_set.create(account=user_admin)
                    # company.save()

                    job_item = JobsInfo.objects.create(
                        name=name,
                        # company=company,
                        description=job.get('work', unknown),
                        url=job.get('url', unknown),
                        experience=job.get('specialize', unknown),
                        wage=job.get('wage', unknown),
                        welfare=job.get('welfare', unknown),
                        skill=job.get('skill', unknown),
                    )
                    job_item.save()
                except DataError as e:
                    logger.debug("{}: {}".format(path_file.split("/")[-1]), e)

                self.stdout.write(
                    self.style.SUCCESS(
                        "{}: Successfully migrate job: {}".format(
                            path_file.split("/")[-1], name))
                )
