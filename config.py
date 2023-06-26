from environs import Env

env = Env()
env.read_env()

token = env.str('token')
admins = env.list('admin')
#moder_id = env.str('moder_id')



channel = '@ttttxtxer'
admin_user = '@Salerix'
admins_id = 1605439713
amount_per_one = 0.05
minimal_vivod = 3
usd_or_rub = 'rub'
currency = 'USDT'
#channel = env.str('channel')
#admin_user = env.str('admin_user')
#admins_id = env.list('admins_id')
#amount_per_one = env.str('amount_per_one')
#minimal_vivod = env.str('minimal_vivod')
#usd_or_rub = env.str('usd_or_rub')
#currency = env.str('currency')

