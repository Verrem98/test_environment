import random
import simpy


OPTIONS_DICT = {0 : {'Zwarte koffie' : [12,0]}, 1: {'Cappuccino' : [8,85]}, 2 : {'Latte' : [8,300]}, 3 : {'Heet water': [0,0]}}

# percentage when resources need to be refilled
RESOURCE_LOWER_LIMIT = 0.2
USAGE_TIME_RANGE = [40,60]
USER_QUEUE_TOL_RANGE = [3,15]
PAYMENT_FAIL_RATE = 0.05



class KoffieRuimte():

    def __init__(self, env):
        self.koffie_apparaten = simpy.Resource(env, capacity=2)

        # in mg
        self.koffie_bonen = simpy.Container(env, init = 1000, capacity= 1000)

        # in ml
        self.melk = simpy.Container(env, init = 1400, capacity= 1400)



def gebruiker(name, env, koffie_ruimte):
    print(f'Gebruiker {name} komt aan op {env.now}')
    arrival_time = env.now


    # if the user thinks the queue is too long, they walk away
    user_queue_tol = random.randint(USER_QUEUE_TOL_RANGE[0], USER_QUEUE_TOL_RANGE[1])
    if user_queue_tol < len(koffie_ruimte.koffie_apparaten.queue):
        print(f'Gebruiker {name} besluit zich niet in de rij aan te sluiten, de rij is te lang')
        return


    with koffie_ruimte.koffie_apparaten.request() as req:

        yield req

        print(f'Gebruiker {name} start het met gebruiken van koffiezetapparaat at {env.now}')

        user_choice = OPTIONS_DICT[random.randint(0,len(OPTIONS_DICT.items())-1)]

        print(f'gebruiker {name} maakt een {list(user_choice.keys())[0]}')

        koffie_bonen_req = list(user_choice.values())[0][0]
        melk_req = list(user_choice.values())[0][1]


        if (melk_req > 0):
            yield koffie_ruimte.melk.get(melk_req)
        if(koffie_bonen_req > 0):
            yield koffie_ruimte.koffie_bonen.get(koffie_bonen_req)

        yield env.timeout(random.randint(USAGE_TIME_RANGE[0], USAGE_TIME_RANGE[1]))
        print(f'Gebruiker {name} is klaar met koffiezetapparaat at {env.now}')

def gebruiker_generator(env, koffie_ruimte):
    gebruiker_count = 0
    while(True):
        env.process(gebruiker(gebruiker_count, env, koffie_ruimte))
        gebruiker_count += 1
        yield env.timeout(random.randint(30,60))


def personeel(env, koffie_bonen, melk):

    yield env.timeout(1200)
    print(f'personeel komt aan op {env.now}')
    ammount = [koffie_bonen.capacity - koffie_bonen.level, melk.capacity - melk.level]
    print(f"personeel vult koffie_bonen en melk aan")
    yield koffie_bonen.put(ammount[0])
    yield melk.put(ammount[1])


def resource_management(env, koffie_ruimte):

    while True:

        koffie_bonen = koffie_ruimte.koffie_bonen
        melk = koffie_ruimte.melk

        if (koffie_bonen.level / koffie_bonen.capacity < RESOURCE_LOWER_LIMIT) or (melk.level / melk.capacity  < RESOURCE_LOWER_LIMIT):

            print(f'Personeel krijgt melding op {env.now} dat de resources bijna op zijn')

            yield env.process(personeel(env, koffie_bonen,melk))

        yield env.timeout(10)



env = simpy.Environment()
koffie_ruimte = KoffieRuimte(env)
env.process(gebruiker_generator(env,koffie_ruimte))
env.process(resource_management(env,koffie_ruimte))

env.run(3000)