class BaseConfig(object):
    VK_TOKEN = '1fe7ce1542f80ded456d1c65dc8daca77aa29e539977159f1a9501bf2bd789f960c4497fea25713e6bd57'
    SECRET_KEY = 'cbdjwlxmcnd2lort'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1/dstubot'
    ENV = 'DevelopmentConfig'
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgres://cmalhdadykrvvc:645ec287e2d2c1593dfcf429a4738e5a022db27999a9d3f02ca260bc714f11d6@ec2-54-217-219-235.eu-west-1.compute.amazonaws.com:5432/dfh21ke69pne2k'
    SQLALCHEMY_DATABASE_URI1 = 'postgres://postgres:taketake@dstubot.c1r6usn8actc.us-east-2.rds.amazonaws.com:5432/dstubot'
    ENV = 'ProductionConfig'
    DEBUG = False
    TESTING = False


Config = DevelopmentConfig

#uTJzWrzTaWkqARVISptC



