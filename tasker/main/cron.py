import pdb

from .models import SimpleModel


def my_scheduled_job():
    pdb.set_trace()
    print('I am CRON!')
    mymodel = SimpleModel()
    mymodel.title = 'new cron'
    mymodel.save()
    SimpleModel(title='axcac').save()
