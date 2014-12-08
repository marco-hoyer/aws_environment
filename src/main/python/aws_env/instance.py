__author__ = 'mhoyer'

from boto import ec2
from boto import utils
from boto.exception import EC2ResponseError


class Ec2Instance(object):

    def __init__(self, instance_id = None, region="eu-west-1"):
        self.aws = ec2.connect_to_region(region)
        assert self.aws, "Could not establish connection to ec2 api"
        self.id = instance_id or self._get_local_instance_id()

    def _get_local_instance_id(self):
        return utils.get_instance_metadata()['instance-id']

    def _get_ec2_instance_data(self):
        reservations = self.aws.get_all_reservations(instance_ids=[self.id])
        reservation = reservations[0]
        assert len(reservation.instances) == 1
        return reservation.instances[0]

    def _get_tags(self):
        return self._get_ec2_instance_data().tags

    def private_dns_name(self):
        return self._get_ec2_instance_data().private_dns_name

    def public_dns_name(self):
        return self._get_ec2_instance_data().public_dns_name

    def subnet_id(self):
        return self._get_ec2_instance_data().subnet_id

    def key_name(self):
        return self._get_ec2_instance_data().key_name

    def interfaces(self):
        #TODO: List parsing
        return self._get_ec2_instance_data().interfaces

    def image_id(self):
        return self._get_ec2_instance_data().image_id

    def az(self):
        return self._get_ec2_instance_data()._placement

    def ami_launch_index(self):
        return self._get_ec2_instance_data().ami_launch_index

    def region(self):
        return self._get_ec2_instance_data().region.name

    def launch_time(self):
        return self._get_ec2_instance_data().launch_time

    def instance_type(self):
        return self._get_ec2_instance_data().instance_type

    def private_ip_address(self):
        return self._get_ec2_instance_data().private_ip_address

    def vpc_id(self):
        return self._get_ec2_instance_data().vpc_id

    def security_group(self):
        # TODO: List parsing
        return self._get_ec2_instance_data().groups


if __name__ == "__main__":
    instance = Ec2Instance()

    #print instance.aws.get_all_instance_status()
    print vars(instance._get_ec2_instance_data())
    print instance.vpc_id()
    print instance.security_group()