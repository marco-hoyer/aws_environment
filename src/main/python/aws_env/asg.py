__author__ = 'mhoyer'

import instance
from boto.ec2 import autoscale


class Asg(object):

    def __init__(self, instance_id = None, region="eu-west-1"):
        self.aws = autoscale.connect_to_region(region)
        assert self.aws, "Could not establish connection to ec2 api"
        self.local_instance = instance.Ec2Instance(instance_id)
        self.asg_instance_view = self._get_asg_instance_view()

    def _get_asg_instance_view(self):
        return self.aws.get_all_autoscaling_instances(instance_ids=[self.local_instance.id])[0]

    def instance_lifecycle_state(self):
        return self.asg_instance_view.lifecycle_state

    def name(self):
        return self.asg_instance_view.group_name

    def instance_health_status(self):
        return self.asg_instance_view.health_status

    def launch_config_name(self):
        return self.asg_instance_view.launch_config_name


if __name__ == "__main__":
    asg = Asg()
    print asg.launch_config_name()
    print asg.instance_health_status()
