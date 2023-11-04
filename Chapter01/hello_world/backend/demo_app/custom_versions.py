from rest_framework.versioning import URLPathVersioning


class DefaultDemoAppVersion(URLPathVersioning):
    allowed_versions = ['v1']
    version_param = 'version'


class DemoViewVersion(DefaultDemoAppVersion):
    allowed_versions = ['v1', 'v2', 'v3']


class AnotherViewVersion(DefaultDemoAppVersion):
    allowed_versions = ['v1', 'v2']
