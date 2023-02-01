import Config
import pprint

if __name__ == "__main__":
    conf = Config.ProjectConfigHandler()
    pprint.pprint(conf.export())