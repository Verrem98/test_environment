import simpy

def Train(env, name, train_cap, load_time, drive_time):


        # Request one of its charging spots
        print(f'{name} entering waiting line at {env.now}')
        with train_cap.request() as req:
            yield req

            print(f'{name} entering train at {env.now}')
            yield env.timeout(load_time)

            print(f'{name} starting ride at {env.now}')
            yield env.timeout(drive_time)
            print(f'{name} leaving ride at {env.now}')

env = simpy.Environment()
train_cap = simpy.Resource(env, capacity=8)

for i in range(300):
    env.process(Train(env, f'Person {i+1}', train_cap, 20, 100))


env.run()