import copy
import json
import random

from pprint import pprint
import matplotlib.pyplot as plt

global_cs = {}


def update_global_cs():
    with open('global_cs.json') as f:
        data = json.load(f)
    pprint(data)
    global global_cs
    global_cs = data


class U:
    def __init__(self):
        self.cs = dict()
        self.cs['doings'] = dict()

    def do(self, us):
        for key, value in self.cs['doings'].items():
            print('\tDo {}'.format(key))
            value(self, us)


class Locating(U):
    @staticmethod
    def located(su, us):
        pass

    @staticmethod
    def become_located(su, us):
        if 'located' not in su.cs['doings']:
            su.cs['doings']['located'] = Locating.located
            if 'coordinates' not in su.cs:
                su.cs['coordinates'] = copy.deepcopy(global_cs['coordinates'])

    @staticmethod
    def cease_located(su, us):
        if 'located' in su.cs['doings']:
            del su.cs['doings']['located']


class Living(U):
    @staticmethod
    def live(su, us):
        su.cs['resources'] -= su.cs['consumption_rate']

    @staticmethod
    def become_live(su, us):
        if 'live' not in su.cs['doings']:
            su.cs['doings']['live'] = Living.live
            if 'consumption_rate' not in su.cs:
                su.cs['consumption_rate'] = copy.deepcopy(global_cs['consumption_rate'])
            if 'resources' not in su.cs:
                su.cs['resources'] = copy.deepcopy(global_cs['resources'])

    @staticmethod
    def cease_live(su, us):
        if 'live' in su.cs['doings']:
            del su.cs['doings']['live']


class Moving(U):
    @staticmethod
    def move(su, us):
        for i, c in enumerate(su.cs['coordinates']):
            su.cs['coordinates'][i] += su.cs['move_distance'][i]

    @staticmethod
    def become_move(su, us):
        if 'move' not in su.cs['doings']:
            su.cs['doings']['move'] = Moving.move
            if 'coordinates' not in su.cs:
                su.cs['coordinates'] = copy.deepcopy(global_cs['coordinates'])
            if 'move_distance' not in su.cs:
                su.cs['move_distance'] = copy.deepcopy(global_cs['move_distance'])

    @staticmethod
    def update_move_distance(su, us):
        if 'move' in su.cs['doings']:
            su.cs['move_distance'] = copy.deepcopy(global_cs['move_distance'])

    @staticmethod
    def cease_move(su, us):
        if 'move' in su.cs['doings']:
            del su.cs['doings']['move']

    @staticmethod
    def moved(su, us):
        pass

    @staticmethod
    def become_moved(su, us):
        if 'moved' not in su.cs['doings']:
            su.cs['doings']['moved'] = Moving.moved
            if 'coordinates' not in su.cs:
                su.cs['coordinates'] = copy.deepcopy(global_cs['coordinates'])

    @staticmethod
    def cease_moved(su, us):
        if 'moved' in su.cs['doings']:
            del su.cs['doings']['moved']

    @staticmethod
    def global_moved(su, us):
        for u in us:
            if 'moved' in u.cs['doings']:
                for i, c in enumerate(u.cs['coordinates']):
                    u.cs['coordinates'][i] += su.cs['moved_distance'][i]

    @staticmethod
    def become_global_moved(su, us):
        if 'global_moved' not in su.cs['doings']:
            su.cs['doings']['global_moved'] = Moving.global_moved
            if 'moved_distance' not in su.cs:
                su.cs['moved_distance'] = copy.deepcopy(global_cs['moved_distance'])

    @staticmethod
    def update_global_moved(su, us):
        if 'global_moved' in su.cs['doings']:
            su.cs['moved_distance'] = copy.deepcopy(global_cs['moved_distance'])

    @staticmethod
    def cease_global_moved(su, us):
        if 'global_moved' in su.cs['doings']:
            del su.cs['doings']['global_moved']


class Gathering(U):
    @staticmethod
    def gather(su, us):
        gcs = su.cs.get('coordinates')
        for u in us:
            if 'gathered' in u.cs['doings']:
                rcs = u.cs.get('coordinates')
                if rcs == gcs:
                    su.cs['resources'] += u.cs['resources']
                    u.cs['resources'] = 0

    @staticmethod
    def become_gather(su, us):
        if 'gather' not in su.cs['doings']:
            su.cs['doings']['gather'] = Gathering.gather
            if 'coordinates' not in su.cs:
                su.cs['coordinates'] = copy.deepcopy(global_cs['coordinates'])
            if 'resources' not in su.cs:
                su.cs['resources'] = copy.deepcopy(global_cs['resources'])

    @staticmethod
    def cease_gather(su, us):
        if 'gather' in su.cs['doings']:
            del su.cs['doings']['gather']

    @staticmethod
    def gathered(su, us):
        pass

    @staticmethod
    def become_gathered(su, us):
        if 'gathered' not in su.cs['doings']:
            su.cs['doings']['gathered'] = Gathering.gathered
            if 'coordinates' not in su.cs:
                su.cs['coordinates'] = copy.deepcopy(global_cs['coordinates'])
            if 'resources' not in su.cs:
                su.cs['resources'] = copy.deepcopy(global_cs['resources'])

    @staticmethod
    def cease_gathered(su, us):
        if 'gathered' in su.cs['doings']:
            del su.cs['doings']['gathered']


class Resource(U):
    def __init__(self):
        super().__init__()
        Locating.become_located(self, [])
        Gathering.become_gathered(self, [])


class MovedResource(U):
    def __init__(self):
        super().__init__()
        Locating.become_located(self, [])
        Gathering.become_gathered(self, [])
        Moving.become_moved(self, [])


class Picker(U):
    def __init__(self):
        super().__init__()
        Living.become_live(self, [])
        Locating.become_located(self, [])
        Moving.become_move(self, [])
        Gathering.become_gather(self, [])


class Wind(U):
    def __init__(self):
        super().__init__()
        Moving.become_global_moved(self, [])


def main():
    update_global_cs()
    d = 10
    d2 = 1
    n_p = 1
    n_r = 5
    n_mr = 10
    us = []
    ps = []
    for i in range(n_p):
        global_cs['coordinates'] = [random.randint(-d, d), random.randint(-d, d)]
        ps.append(Picker())
    us.extend(ps)
    rs = []
    for i in range(n_r):
        global_cs['coordinates'] = [random.randint(-d, d), random.randint(-d, d)]
        rs.append(Resource())
    us.extend(rs)
    mrs = []
    for i in range(n_mr):
        global_cs['coordinates'] = [random.randint(-d, d), random.randint(-d, d)]
        mrs.append(MovedResource())
    us.extend(mrs)
    w = Wind()
    us.append(w)
    plt.ion()
    cnt = 0
    while len(ps) > 0:
        cnt += 1
        print('Step {}'.format(cnt))
        do_wind = random.choice([True, False])
        if do_wind:
            Moving.become_global_moved(w, us)
            global_cs['moved_distance'] = [random.randint(-d2, d2), random.randint(-d2, d2)]
            Moving.update_global_moved(w, us)
        else:
            Moving.cease_global_moved(w, us)
        for p in ps:
            global_cs['move_distance'] = [random.randint(-d2, d2), random.randint(-d2, d2)]
            Moving.update_move_distance(p, us)
        for u in us:
            print('U: {}'.format(u.__class__.__name__))
            u.do(us)
        for p in ps:
            if p.cs['resources'] <= 0:
                ps.remove(p)
                us.remove(p)
        for r in rs:
            if r.cs['resources'] <= 0:
                rs.remove(r)
                us.remove(r)
        for mr in mrs:
            if mr.cs['resources'] <= 0:
                mrs.remove(mr)
                us.remove(mr)
        plt.clf()
        xs = []
        ys = []
        ss = []
        cs = []
        for p in ps:
            xs.append(p.cs['coordinates'][0])
            ys.append(p.cs['coordinates'][1])
            ss.append(0.01 * p.cs['resources'] ** 2 + 2)
            cs.append('r')
        plt.scatter(xs, ys, s=ss, c=cs, alpha=0.5, label='pickers')
        xs = []
        ys = []
        ss = []
        cs = []
        for r in rs:
            xs.append(r.cs['coordinates'][0])
            ys.append(r.cs['coordinates'][1])
            ss.append(0.01 * r.cs['resources'] ** 2 + 2)
            cs.append('g')
        plt.scatter(xs, ys, s=ss, c=cs, alpha=0.5, label='resources')
        xs = []
        ys = []
        ss = []
        cs = []
        for mr in mrs:
            xs.append(mr.cs['coordinates'][0])
            ys.append(mr.cs['coordinates'][1])
            ss.append(0.01 * mr.cs['resources'] ** 2 + 2)
            cs.append('b')
        plt.scatter(xs, ys, s=ss, c=cs, alpha=0.5, label='moved resources')
        plt.xlim(-5*d, 5*d)
        plt.ylim(-5*d, 5*d)
        plt.title('Step {}'.format(cnt))
        plt.legend()
        for handle in plt.legend().legendHandles:
            handle.set_sizes([100])
        plt.pause(0.001)
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
