class Metrics:

    def __init__(self):

        self.data = {}

    def add(self, name, value):

        self.data[name] = value

    def report(self):

        print()

        print("=" * 80)

        print("PIPELINE METRICS")

        print("=" * 80)

        for k, v in self.data.items():

            print(f"{k:25} {v}")