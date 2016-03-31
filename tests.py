from particle import Particle
from simulator import NBodySimulator
from animator import NBodyAnimator
from utils import typecheck




##################
# Particle Tests #
##################

def test_particle_init():
    p = Particle(1., 2., 3., 4., 5.)
    assert p.m == 1.
    assert p.x == 2.
    assert p.y == 3.
    assert p.vx == 4.
    assert p.vy == 5.


def test_particle_init__bad_m():
    try:
        p = Particle("yo", 2., 2., 2., 2.)
    except TypeError:
        pass


def test_particle_init__m_lt_0():
    try:
        p = Particle(-1.0, 2., 2., 2., 2.)
    except ValueError:
        pass


def test_particle_init__bad_x0():
    try:
        p = Particle(2., "yo", 2., 2., 2.)
    except TypeError:
        pass


def test_particle_init__bad_y0():
    try:
        p = Particle(2., 2., "yo", 2., 2.)
    except TypeError:
        pass


def test_particle_init__bad_vx0():
    try:
        p = Particle(2., 2., 2., "yo", 2.)
    except TypeError:
        pass


def test_particle_init__bad_vy0():
    try:
        p = Particle(2., 2., 2., 2., "yo")
    except TypeError:
        pass


def test_particle_update_pos():
    p = Particle(1., 2., 3., 2., 2.)
    p.update_pos(1.0)
    assert p.x == 4.0
    assert p.y == 5.0
    p.update_pos(2.0)
    assert p.x == 8.0
    assert p.y == 9.0


def test_particle_update_pos__h_lt_0():
    try:
        p = Particle(1., 2., 2., 2., 2.)
        p.update_pos(-1.0)
    except ValueError:
        pass


def test_particle_update():
    p = Particle(1., 2., 3., 2., 2.)
    dvx, dvy, h = -2.0, 2.0, 1.0
    p.update(dvx, dvy, h)
    assert p.x == 4.0
    assert p.y == 5.0
    assert p.vx == 0.0
    assert p.vy == 4.0


def test_particle_update__h_lt_0():
    try:
        p = Particle(1., 2., 2., 2., 2.)
        p.update(-2.0, 2.0, -1.0)
    except ValueError:
        pass


def test_particle_update__bad_dvx():
    try:
        p = Particle(1., 2., 2., 2., 2.)
        p.update("lol", 2.0, -1.0)
    except TypeError:
        pass


def test_particle_update__bad_dvy():
    try:
        p = Particle(1., 2., 2., 2., 2.)
        p.update(-2.0, "lol", -1.0)
    except TypeError:
        pass


def test_particle_update__bad_dvy():
    try:
        p = Particle(1., 2., 2., 2., 2.)
        p.update(-2.0, 2.0, "lol")
    except TypeError:
        pass


def test_particle_dist():
    p = Particle(1., 2., 2., 2., 2.)
    p2 = Particle(1., 5., 6., 2., 2.)
    p3 = Particle(1., 2., 6., 2., 2.)
    assert p.dist(p2) == 5.0
    assert p2.dist(p) == 5.0
    assert p.dist(p3) == 4.0
    assert p3.dist(p) == 4.0
    assert p2.dist(p3) == 3.0
    assert p3.dist(p2) == 3.0


def test_particle_dist__bad_particle2():
    try:
        p = Particle(1., 2., 2., 2., 2.)
        p2 = "wrong"
        p.dist(p2)
    except TypeError:
        pass


def test_particle_copy():
    p = Particle(1., 2., 3., 2., 2.)
    p2 = p.copy()
    assert p.m == p2.m
    assert p.x == p2.x
    assert p.y == p2.y
    assert p.vx == p2.vx
    assert p.vy == p2.vy
    assert p != p2


########################
# NBodySimulator Tests #
########################

def test_nbodysimulator_init():
    nbs = NBodySimulator(N=30, speed=1.0)
    assert len(nbs.particles) == 30
    assert nbs.N == 30
    for p in nbs.particles:
        typecheck([p, p.m, p.x, p.y, p.vx, p.vy], [Particle, float, float, float, float, float])
    # Test all ways of instantiating a simulator
    nbs = NBodySimulator(N=50)
    nbs = NBodySimulator(speed=2.0)
    nbs = NBodySimulator()

def test_nbodysimulator_init__N_lt_0():
    try:
        nbs = NBodySimulator(N=-50, speed=1.0)
    except ValueError:
        pass


def test_nbodysimulator_init__bad_N():
    try:
        nbs = NBodySimulator(N="lol", speed=1.0)
    except TypeError:
        pass


def test_nbodysimulator_init__bad_speed():
    try:
        nbs = NBodySimulator(N=5, speed="lol")
    except TypeError:
        pass

def test_nbodysimulator_init__speed_lt_0():
    try:
        nbs = NBodySimulator(N=5, speed=-1.0)
    except ValueError:
        pass


def test_nbodysimulator_gforce():
    nbs = NBodySimulator(N=2, speed=1.0)
    f_method = nbs.gforce(nbs.particles[0], nbs.particles[1])
    
    r = nbs.particles[0].dist(nbs.particles[1])
    dx = nbs.particles[0].x - nbs.particles[1].x
    dy = nbs.particles[0].y - nbs.particles[1].y
    f = - nbs.particles[0].m * nbs.particles[1].m / (r**2 + nbs.a**2)
    assert f_method[0] == f * dx
    assert f_method[1] == f * dy


def test_nbodysimulator_gforce__bad_p1():
    try:
        nbs = NBodySimulator()
        nbs.gforce("lol", nbs.particles[0])
    except TypeError:
        pass


def test_nbodysimulator_gforce__bad_p1():
    try:
        nbs = NBodySimulator()
        nbs.gforce(nbs.particles[0], "lol")
    except TypeError:
        pass


def test_nbodysimulator_take_step():
    nbs = NBodySimulator(speed=0.0)
    particles = nbs.particles[:]
    nbs.take_step()
    for i in range(len(particles)):
        assert(particles[i].x == nbs.particles[i].x)
        assert(particles[i].y == nbs.particles[i].y)
        assert(particles[i].vx == nbs.particles[i].vx)
        assert(particles[i].vy == nbs.particles[i].vy)


def test_nbodysimulator_get_particle_locations():
    nbs = NBodySimulator()
    locs = nbs.getParticleLocations()
    for i in range(len(nbs.particles)):
        assert nbs.particles[i].x == locs[0][i]
        assert nbs.particles[i].y == locs[1][i]
    nbs.take_step()
    locs = nbs.getParticleLocations()
    for i in range(len(nbs.particles)):
        assert nbs.particles[i].x == locs[0][i]
        assert nbs.particles[i].y == locs[1][i]


def test_nbodysimulator_get_particle_masses():
    nbs = NBodySimulator(N=3, speed=2.0)
    masses = nbs.getParticleMasses()
    for i in range(len(nbs.particles)):
        assert nbs.particles[i].m == masses[i]


#######################
# NBodyAnimator Tests #
#######################

def test_nbodyanimator_init():
    nba = NBodyAnimator(numpoints=5, speed=1.0)
    assert nba.numpoints == 5
    assert nba.speed == 1.0
    assert nba.pause == False
    assert nba.stop == False


def test_nbodyanimator_init__bad_numpoints():
    try:
        nba = NBodyAnimator(numpoints="lol", speed=1.0)
    except TypeError:
        pass


def test_nbodyanimator_init__numpoints_lt_0():
    try:
        nba = NBodyAnimator(numpoints=-5, speed=1.0)
    except ValueError:
        pass


def test_nbodyanimator_init__bad_speed():
    try:
        nba = NBodyAnimator(numpoints=5, speed="lol")
    except TypeError:
        pass


def test_nbodyanimator_init__speed_lt_0():
    try:
        nba = NBodyAnimator(numpoints=5, speed=-1.0)
    except ValueError:
        pass


def test_nbodyanimator_data_stream():
    nba = NBodyAnimator(numpoints=10, speed=1.0)
    data = next(nba.stream)
    assert len(data) == 4
    assert len(data[0]) == 10
    data2 = next(nba.stream)
    assert len(data) == len(data2)
    assert len(data[0]) == len(data2[0])
    # Make sure the masses and colors are identical between iterations

    # If our speed is zero, the stream should never change.
    nba2 = NBodyAnimator(numpoints=10, speed=0.0)
    data = next(nba.stream)
    data2 = next(nba.stream)
    for i in range(len(data)):
        for j in range(len(data[0])):
            assert data[i][j] == data2[i][j]
