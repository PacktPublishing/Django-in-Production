from django.test.runner import DiscoverRunner


class FillData:
    def setup_databases(self, *args, **kwargs):
        temp = super(FillData, self).setup_databases(*args, **kwargs)
        print("### Populating Test Cases Database ###")
        # Create any data
        print("### Database populated ############")
        return temp


class CustomRunner(FillData, DiscoverRunner):
    pass