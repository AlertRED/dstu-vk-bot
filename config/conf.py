class Config:
    VK_TOKEN ='1fe7ce1542f80ded456d1c65dc8daca77aa29e539977159f1a9501bf2bd789f960c4497fea25713e6bd57'

    SECRET_KEY = 'qwerrt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = DATABASE = 'postgresql://postgres:1234@127.0.0.1/dstubot_test'
    SQLALCHEMY_DATABASE_URI = DATABASE = 'postgresql://postgres:1234@127.0.0.1/dstubot'
    # SQLALCHEMY_DATABASE_URI = DATABASE = 'postgres://cmalhdadykrvvc:645ec287e2d2c1593dfcf429a4738e5a022db27999a9d3f02ca260bc714f11d6@ec2-54-217-219-235.eu-west-1.compute.amazonaws.com:5432/dfh21ke69pne2k'

    # FLASK_ADMIN_SWATCH = 'cerulean'

    # set FLASK_APP=web_app.run:flask_app
    # flask db init
    # flask db migrate
    # flask db upgrade
