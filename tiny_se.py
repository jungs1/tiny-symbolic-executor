from z3 import Solver, BitVec, BoolVal, sat, BoolRef


class TinySymbolicExecutionEngine:
    """
    A class for symbolic execution of Python functions using the Z3 solver.
    """

    def __init__(self):
        self.solver = Solver()
        self.trace = []

    def add_constraint(self, condition: bool | BoolRef) -> None:
        if isinstance(condition, bool):
            # Convert Python bool to Z3 Bool
            condition = BoolVal(condition)
        self.trace.append(condition)
        self.solver.add(condition)

    def is_path_feasible(self) -> bool:
        return self.solver.check() == sat

    def execute_path(self, func: callable, *args: object, **kwargs: object) -> None:
        with self.override_bool():
            try:
                func(*args, **kwargs)
            except AssertionError:
                if self.is_path_feasible():
                    print("Assertion failed under:", self.solver.model())
                else:
                    print("Unreachable code encountered.")
            except Exception as e:
                print(f"Exception during execution: {e}")

    def override_bool(self):
        class BoolOverride:
            def __enter__(inner_self) -> None:
                # Override __bool__ to add constraints to the solver
                setattr(
                    BoolRef,
                    "__bool__",
                    lambda condition: self._bool_override(condition),
                )

            def __exit__(inner_self, exc_type, exc_val, exc_tb) -> None:
                # Reset to original behavior
                setattr(
                    BoolRef, "__bool__", lambda self: self.simplify().as_long() != 0
                )

        return BoolOverride()

    def _bool_override(self, condition: BoolRef) -> bool:
        self.add_constraint(condition)
        return self.is_path_feasible()


def test_function_1(x, y):
    z = 2 * x
    if z == y:
        if y == x + 10:
            assert False


def test_function_2(x, y, z):
    if x > 10:
        if y > 10:
            if z > 10:
                assert False


if __name__ == "__main__":
    engine = TinySymbolicExecutionEngine()
    x = BitVec("x", 32)
    y = BitVec("y", 32)
    engine.execute_path(test_function_1, x, y)
