# Gregor will help us, can only do this after the abstract base class is defined
# Example can find under
#
# cloudmesh-cloud/cloudmesh/compute/*,
# cloudmesh-cloud/cloudmesh/vm/command,
# cloudmesh-storage/cloudmesh/storage/*
import os
import json

from cloudmesh.volume.VolumeABC import VolumeABC
from cloudmesh.common.util import banner
from cloudmesh.common.Shell import Shell
from cloudmesh.configuration.Config import Config

class Provider(VolumeABC):
    #kind = "multipass"

    def __init__(self, name=None, configuration="~/.cloudmesh/cloudmesh.yaml"):
        conf = Config(configuration)["cloudmesh"]
        # self.user = conf["profile"]
        #self.spec = conf["cloud"][name]
        self.cloud = name
        #cred = self.spec["credentials"]
        #deft = self.spec["default"]
        self.kind = self.spec["cm"]["kind"]
        super().__init__(name, conf)

        print(self.cloud)
        #print(self.cloudtype)

        #
        # BUG: the test must be self.kind and not self.cloud
        #

        self.provider = self.get(self.kind)

    def get(self, kind):

        if self.kind == "multipass":
            from cloudmesh.volume.multipass.Provider import \
                Provider as MulitpassProvider
            self.provider = MulitpassProvider(self.cloud)

        elif self.kind == "aws":
            from cloudmesh.volume.aws.Provider import \
                Provider as AwsProvider
            self.provider = AwsProvider(self.cloud) #

        return self.provider


    def create(self, name=None):  #, **args):
        #banner(f"mount {name}")
        # #os.system(f"multipass mount /Users/ashok/multipass-mount  {name}")

        self.provider.create(name)
        """
        name = args["name"]
        def create(self,
                   name=None,
                   zone=None,
                   size=None,
                   voltype="gp2",
                   iops=1000,
                   kms_key_id=None,
                   outpost_arn=None,
                   image=None,
                   snapshot=None,
                   encrypted=False,
                   source=None,
                   description=None,
                   tag_key=None,
                   tag_value=None,
                   multi_attach_enabled=True,
                   dryrun=False):
        """

    def mount(self, path=None,name=None):
        self.provider.mount(path,name)

    # @DatabaseUpdate
    # def list(self, name=None):
    #    #(...)
    #    # list of dicts