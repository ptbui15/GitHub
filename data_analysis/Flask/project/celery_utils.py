from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


"""
brew services start rabbitmq     //start 
brew services stop  rabbitmq     //stop
brew services restart rabbitmq   //restart 

celery -A background worker --loglevel=INFO

sudo lsof -i -P -n | grep LISTEN
"""