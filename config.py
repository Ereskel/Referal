from environs import Env

env = Env()
env.read_env()

token = env.str('token')
admins = env.list('admin')
#moder_id = env.str('moder_id')



channel = '@'
admin_user = '@'
admins_id = 
amount_per_one = 0.05
minimal_vivod = 3
usd_or_rub = 'rub'
# На выбор несколько валют
currency = 'USDT'

