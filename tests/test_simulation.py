from src.simulation.simulation import run_simulation


def test_simulation_seed():
    lib1, skipped_steps1, uncaught_errors1 = run_simulation(steps=20, seed=123)
    lib2, skipped_steps2, uncaught_errors2 = run_simulation(steps=20, seed=123)
    assert lib1.get_all_isbns() == lib2.get_all_isbns()
    assert skipped_steps1 == skipped_steps2
    assert uncaught_errors1 == uncaught_errors2


def test_simulation_no_uncaught_errors():
    lib, skipped_steps, uncaught_errors = run_simulation(steps=100, seed=777)
    assert uncaught_errors == 0
