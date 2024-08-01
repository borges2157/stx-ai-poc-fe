import yaml


class YamlParser:

    @staticmethod
    def parse_yaml():
        with open("../providers.yml") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def controller(self):
        print('Initiating parse.')
        data_loaded = self.parse_yaml()
        print('Parse complete. Listing objects:')
        for provider in data_loaded:
            print('Provider: ' + provider)


if __name__ == '__main__':
    app = YamlParser()
    app.controller()
