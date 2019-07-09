from utilities import driver
from behave import use_fixture

def before_tag(context, tag):
    context.driverpath = None
    context.browsertype = context.config.userdata["browser"]
    context.server = context.config.userdata["server"]
    context.relative_url = context.config.userdata["relative_url"]
    context.params = context.config.userdata["params"]
    context.logpath = context.config.userdata["logpath"]
    context.timeout = int(context.config.userdata["timeout"])
    context.driver_version = context.config.userdata["driver_version"]
    context.postgres_user = context.config.userdata["postgres_user"]
    context.postgres_pass = context.config.userdata["postgres_pass"]
    context.postgres_host = context.config.userdata["postgres_host"]
    context.postgres_port = context.config.userdata["postgres_port"]
    context.postgres_db = context.config.userdata["postgres_db"]
    context.ckan_user = context.config.userdata["ckan_user"]
    context.ckan_password = context.config.userdata["ckan_password"]
    context.redis_server = context.config.userdata["redis_server"]
    context.redis_port = int(context.config.userdata["redis_port"])
    context.solr_url = context.config.userdata["solr_url"]
    context.UI = False

    if context.config.verbose:
        print("run:", context.browsertype)
    if tag == 'UI':
        context.UI = True
        if context.browsertype == "firefox":
            use_fixture(driver.firefox_driver, context)
        elif context.browsertype == "chrome":
            use_fixture(driver.chrome_driver, context)

def after_step(context, step):
    if step.status != "passed":
        if context.UI:
            use_fixture(driver.screenshot, context)

