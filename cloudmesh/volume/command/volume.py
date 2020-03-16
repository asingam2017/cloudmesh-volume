from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.variables import Variables
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.shell.command import map_parameters
from cloudmesh.volume.Provider import Provider
from cloudmesh.common.parameter import Parameter
import textwrap
from cloudmesh.common.util import banner
from cloudmesh.management.configuration.arguments import Arguments
from cloudmesh.mongo.CmDatabase import CmDatabase


class VolumeCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_volume(self, args, arguments):
        """
        ::

          Usage:
            volume register which
            volume register [NAME] [--cloud=CLOUD] [ARGUMENTS...]
            volume list [NAMES]
                        [--vm=VM]
                        [--region=REGION]
                        [--cloud=CLOUD]
                        [--refresh]
                        [--dryrun]
            volume create [NAME]
                      [--label=LABEL]
                      [--size=SIZE]
                      [--volumetype=TYPE]
                      [--description=DESCRIPTION]
                      [--dryrun]
                      [ARGUMENTS...]
            volume add VM NAME
            volume remove VM NAME
            volume delete [NAME]
            volume migrate NAME FROM_VM TO_VM
            volume sync FROM_VOLUME TO_VOLUME

          This command manages volumes accross different clouds

          Arguments:
              NAME   the name of the volume

          Options:
              --vm=VMNAME        The name of the virtual machine
              --region=REGION    The name of the region
              --cloud=CLOUD      The name of the cloud
              --refresh          If refresh the information is taken from the cloud
              --volumetype=TYPE  The type of the volume

          Description:

             TBD
        """
        VERBOSE(arguments)

        # name = arguments.NAME
        # path = arguments.PATH

        map_parameters(arguments,
                       "cloud",
                       "vm",
                       "region",
                       "refresh",
                       "dryrun"
                       )

        variables = Variables()
        arguments.output = Parameter.find("output",
                                          arguments,
                                          variables,
                                          "table")
        cm = CmDatabase()

        if arguments.list and arguments.refresh:
            banner(f'get in if arguments.list, arguments.list={arguments.list}')
            print("arguments.NAMES",arguments)

            if arguments.NAMES:
                arguments.NAMES = list(arguments.NAMES.split(","))
                #find record in mondoDB through volume names

                for name in arguments.NAMES:
                    entry = cm.find_name(name)[0]['cm']
                    name = entry['cloud']
                    provider = Provider(name=name)
                    result = provider.list(**arguments)
                    print(provider.Print(result,
                                         kind='volume',
                                         output=arguments.output))


            elif arguments.cloud:
                banner(f'get in arguments.cloud, arguments.cloud = {arguments.cloud}')
                provider = Provider(name=arguments.cloud)
                result = provider.list(**arguments)
                print(provider.Print(result,
                                      kind='volume',
                                      output=arguments.output))

            elif arguments.vm:
                #need to add vm name to volume when doing volume add
                #get record from mongoDB through vm name --> get cloud --> Provider(name=cloud)
                raise NotImplementedError


            elif arguments.region:
                #find mongoDB record through region --> get cloud --> Provider(name=cloud)

                raise NotImplementedError


        elif arguments.list and arguments.refresh == False:
            #print out results in mongoDB
            if arguments.NAMES:
                arguments.NAMES = list(arguments.NAMES.split(","))
                # find record in mondoDB through volume names

                for name in arguments.NAMES:
                    result = cm.find_name(name)
                    print(provider.Print(result,
                                         kind='volume',
                                         output=arguments.output))

            elif arguments.cloud:
                result = cm.find(cloud=arguments.cloud, kind="volume")
                print(provider.Print(result,
                                     kind='volume',
                                     output=arguments.output))

            elif arguments.vm:
                #need to add vm name to volume when doing volume add
                raise NotImplementedError
                result = cm.find(vm=arguments.vm, kind='volume')
                print(provider.Print(result,
                                     kind='volume',
                                     output=arguments.output))

            elif arguments.region:
                raise NotImplementedError
                result = cm.find(region=arguments.region, kind='volume')
                print(provider.Print(result,
                                     kind='volume',
                                     output=arguments.output))

        return ""

'''
        def get_last_volume():
            Console.error("Get last volume not yet implemented")
            raise NotImplementedError

        VERBOSE(arguments)

        variables = Variables()
        name = arguments.NAME or variables["volume"] or get_last_volume()

        path = arguments.PATH

        map_parameters(arguments,
                       "volumetype",
                       "cloud",
                       "vm",
                       "region"
                       "cloud",
                       "refresh"
                       )

        if arguments.register and arguments.which:

            providers = Provider.get_kind()

            Console.info("Available Volume Cloud Providers")
            print()
            print("    " + "\n    ".join(providers))
            print()

        elif arguments.register:

            Console.info("Registering a volume to cloudmesh yaml")

            parameters = Parameter.arguments_to_dict(arguments.ARGUMENTS)

            print()
            print("    Name:", name)
            print("    Cloud:", arguments.cloud)
            print("    Arguments:", parameters)
            print()

            raise NotImplementedError


        elif arguments.list:

            if arguments.NAMES:

                raise NotImplementedError
                names = Parameter.expand(arguments.NAMES)

                for name in names:
                    # kind = cm.kind
                    provider = Provider(name=name)
                    # result = provider.list(???)
                    result = provider.list()

            elif arguments.cloud:

                provider = Provider(name=arguments.cloud)
                result = provider.list()


            print(provider.Print(result,
                                 kind='volume',
                                 output=arguments.output))
            return ""

        elif arguments.create:

            parameters = Parameter.arguments_to_dict(arguments.ARGUMENTS)

            print(parameters)

        elif arguments.delete:

            name = arguments.NAME

            if name is None:
                # get name form last created volume
                raise NotImplementedError

            provider = Provider(name=name)
            provider.delete(name=name)

        elif arguments.migrate:

            print(arguments.name)
            print(arguments.FROM_VM)
            print(arguments.TO_VM)

            raise NotImplementedError

        elif arguments.sync:

            print(arguments.FROM_VOLUME)
            print(arguments.TO_VOLUME)

            raise NotImplementedError

        elif arguments.add:

            Console.info("Add a volume to a vm")

            print(arguments.NAME)
            print(arguments.VM)

            raise NotImplementedError

        elif arguments.remove:

            Console.info("Remove a volume from a vm")

            print(arguments.NAME)
            print(arguments.VM)

            raise NotImplementedError

        return ""
'''