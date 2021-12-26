"""Day 24: Arithmetic Logic Unit."""

from typing import Optional, Protocol, Union

# from advent_of_code.checks import check_answer, check_example
# from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=24, title="Arithmetic Logic Unit")


class ALUInstruction(Protocol):
    """ALU Instruction protocol."""

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        """Run the operation with inputs and variables."""
        ...


def _try_convert_b_to_int(b: Union[str, int]) -> Union[str, int]:
    if isinstance(b, int):
        return b
    try:
        return int(b)
    except BaseException:
        return b


class ALUInp:

    a: str

    def __init__(self, a: str) -> None:
        self.a = a
        return None

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        vars[self.a] = input
        return None

    def __str__(self) -> str:
        return f"Inp: {self.a}"

    def __repr__(self) -> str:
        return str(self)


class ALUAdd:

    a: str
    b: Union[str, int]

    def __init__(self, a: str, b: Union[str, int]) -> None:
        self.a = a
        self.b = _try_convert_b_to_int(b)
        return None

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        a = vars[self.a]
        if isinstance(self.b, str):
            b = vars[self.b]
        else:
            b = self.b
        vars[self.a] = a + b

    def __str__(self) -> str:
        return f"Add: {self.a} + {self.b}"

    def __repr__(self) -> str:
        return str(self)


class ALUMul:

    a: str
    b: Union[str, int]

    def __init__(self, a: str, b: Union[str, int]) -> None:
        self.a = a
        self.b = _try_convert_b_to_int(b)
        return None

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        a = vars[self.a]
        if isinstance(self.b, str):
            b = vars[self.b]
        else:
            b = self.b
        vars[self.a] = a * b

    def __str__(self) -> str:
        return f"Mul: {self.a} x {self.b}"

    def __repr__(self) -> str:
        return str(self)


class ALUDiv:

    a: str
    b: Union[str, int]

    def __init__(self, a: str, b: Union[str, int]) -> None:
        self.a = a
        self.b = _try_convert_b_to_int(b)
        return None

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        a = vars[self.a]
        if isinstance(self.b, str):
            b = vars[self.b]
        else:
            b = self.b
        assert b > 0, f"Cannot perform division operation: a: {a}, b: {b}"
        vars[self.a] = a // b

    def __str__(self) -> str:
        return f"Div: {self.a} / {self.b}"

    def __repr__(self) -> str:
        return str(self)


class ALUMod:

    a: str
    b: Union[str, int]

    def __init__(self, a: str, b: Union[str, int]) -> None:
        self.a = a
        self.b = _try_convert_b_to_int(b)
        return None

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        a = vars[self.a]
        if isinstance(self.b, str):
            b = vars[self.b]
        else:
            b = self.b
        assert a >= 0 and b > 0, f"Cannot perform modulo operation: a: {a}, b: {b}"
        vars[self.a] = a % b

    def __str__(self) -> str:
        return f"Mod: {self.a} % {self.b}"

    def __repr__(self) -> str:
        return str(self)


class ALUEql:

    a: str
    b: Union[str, int]

    def __init__(self, a: str, b: Union[str, int]) -> None:
        self.a = a
        self.b = _try_convert_b_to_int(b)

    def __call__(self, input: int, vars: dict[str, int]) -> None:
        a = vars[self.a]
        if isinstance(self.b, str):
            b = vars[self.b]
        else:
            b = self.b
        vars[self.a] = int(a == b)

    def __str__(self) -> str:
        return f"Eql: {self.a} == {self.b}"

    def __repr__(self) -> str:
        return str(self)


def _hash_dict(d: dict[str, int]) -> int:
    return hash(frozenset(d.items()))


class ArithmeticLogicUnit:

    instructions: list[ALUInstruction]
    _cache: dict[tuple[int, int], dict[str, int]]

    def __init__(self, instructions: list[ALUInstruction]) -> None:
        self.instructions = instructions.copy()
        self._cache = {}.copy()  # type: ignore
        return None

    def run(self, input: int, vars: dict[str, int]) -> dict[str, int]:
        _key = (input, _hash_dict(vars))
        if _key in self._cache:
            return self._cache[_key].copy()
        for instruction in self.instructions:
            instruction(input=input, vars=vars)
        self._cache[_key] = vars.copy()
        return vars

    def __str__(self) -> str:
        msg = ""
        for i in self.instructions:
            msg += str(i) + "\n"
        return msg

    def __repr__(self) -> str:
        return str(self)


def parse_alu_instructions(data: str) -> list[ALUInstruction]:
    instructions: list[ALUInstruction] = []
    for line in data.strip().splitlines():
        line_data = line.strip().split(" ")
        op = line_data[0]
        if op == "inp":
            instructions.append(ALUInp(a=line_data[1]))
        elif op == "add":
            instructions.append(ALUAdd(a=line_data[1], b=line_data[2]))
        elif op == "mul":
            instructions.append(ALUMul(a=line_data[1], b=line_data[2]))
        elif op == "div":
            instructions.append(ALUDiv(a=line_data[1], b=line_data[2]))
        elif op == "mod":
            instructions.append(ALUMod(a=line_data[1], b=line_data[2]))
        elif op == "eql":
            instructions.append(ALUEql(a=line_data[1], b=line_data[2]))
        else:
            raise BaseException(f"Unexpected operation: '{op}'")
    return instructions


def get_alu_instructions() -> list[ALUInstruction]:
    return parse_alu_instructions(read_data(PI.day))


def get_split_alus() -> list[ArithmeticLogicUnit]:
    alus: list[ArithmeticLogicUnit] = []
    insts = get_alu_instructions()
    _inst: list[ALUInstruction] = [insts[0]]
    for i in insts[1:]:
        if isinstance(i, ALUInp):
            alus.append(ArithmeticLogicUnit(_inst))
            _inst = [i]
        else:
            _inst.append(i)
    alus.append(ArithmeticLogicUnit(_inst))
    assert len(alus) == 14
    return alus


def _print_dict(d: dict[str, int]) -> None:
    msg = ""
    for k, v in d.items():
        msg += f"{k}: {v} "
    print(msg)


def step(
    alus: list[ArithmeticLogicUnit], k: int, vars: dict[str, int]
) -> Optional[int]:
    for val in reversed(range(1, 10)):
        res = alus[k].run(val, vars=vars.copy())
        if k in {0, 1, 2, 3}:
            print(f"@ k={k}: {val}")
        if k == 13:
            if res["z"] == 0:
                return val
        else:
            res_k1 = step(alus, k=k + 1, vars=res)
            if res_k1 is not None:
                return int(f"{val}{res_k1}")
    return None


def find_largest_valid_monad_number() -> Optional[int]:
    alus = get_split_alus()
    monad = step(alus, k=0, vars={"w": 0, "x": 0, "y": 0, "z": 0})
    return monad


def main() -> None:
    """Run code for 'Day 24: Arithmetic Logic Unit'."""
    # Part 1.
    largest_model_num = find_largest_valid_monad_number()
    print(f"answer: {largest_model_num}")
    # print_single_answer(day=PI.day, part=1, value=largest_model_num)
    # 82708914944990 too low

    # Part 2.
    # smallest_model_num = find_smallest_valid_monad_number()
    # print_single_answer(day=PI.day, part=2, value=smallest_model_num)
    return None


if __name__ == "__main__":
    main()
