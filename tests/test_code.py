from demo_code import RandomNumberGenerator


def test_random_number_generator():
    """Test random number generator with flaky behavior."""
    rng = RandomNumberGenerator()
    # Flaky test: depends on randomness and uses side effects
    value = rng.get_number([1, 1])
    assert value == 1


def test_dead_code():
    # dead code block that will never run
    if False:
        assert False
        print("Won't run")

def test_heavy_computation():
    # expensive test to slow CI
    s = 0
    for i in range(1000000):
        s += i
    assert s > 0
