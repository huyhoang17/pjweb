from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from accounts.models import UserProfile
from companys.models import CompanyProfile
from job.models import JobsInfo

import glob
import json
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Migrate data from json file to django models'

    def __init__(self):
        self.path_file_suffix = "/*.json"
        # self.unknown = "unknown"

    def read_json_file_data(self, path_file):
        with open(path_file) as f:
            out = f.read()
            data = json.loads(out)
        return data

    def get_user_admin(self, user_admin):
        try:
            user_admin = User.objects.get(username=user_admin)
            user_acc = UserProfile.objects.get(user=user_admin)
            user_acc.user = user_admin
            return user_acc
        except User.DoesNotExist:
            logger.debug('User Admin does not exist !')
        except UserProfile.DoesNotExist:
            logger.debug('User Profile does not exist !')

    def add_arguments(self, parser):
        parser.add_argument('user_admin', nargs='+', type=str)
        parser.add_argument('path_json_folder', nargs='+', type=str)

    def handle(self, *args, **options):
        path_files = glob.glob(
            options['path_json_folder'][0] + self.path_file_suffix
        )
        unknown = "unknown"
        user_admin = self.get_user_admin(options['user_admin'][0])
        for path_file in path_files:
            jobs = self.read_json_file_data(path_file)
            for job in jobs:
                try:
                    company_name = job.get('company', unknown)
                    company = CompanyProfile.objects.create(
                        name=company_name
                    )
                    company.membership_set.create(account=user_admin)
                    company.name = job.get('company', unknown)
                    company.address = job.get('address', unknown)
                    company.city = job.get('province', 'Ha Noi')
                    company.size = job.get('size', unknown)
                    company.save()

                    job_item = JobsInfo.objects.create(
                        name=job.get('name', unknown))
                    job_item.user = user_admin
                    job_item.company = company
                    job_item.description = job.get('work', unknown)
                    job_item.url = job.get('url', unknown)
                    job_item.experience = job.get('specialize', unknown)
                    job_item.welfare = job.get('welfare', unknown)
                    job_item.skill = job.get('skill', unknown)
                    job_item.save()
                except Exception as e:
                    logger.debug(e)
            self.stdout.write(self.style.SUCCESS(
                'Successfully migrate data from {} file - user: {}'.format(
                    path_file.split('/')[-1], user_admin)))
