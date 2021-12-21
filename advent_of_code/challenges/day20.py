"""Day 20: Trench Map."""

from itertools import product
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

from advent_of_code.checks import check_answer, check_example
from advent_of_code.cli_output import print_single_answer
from advent_of_code.data import output_dir, read_data
from advent_of_code.utils import PuzzleInfo

PI = PuzzleInfo(day=20, title="Trench Map")


def parse_data(data: str) -> tuple[list[bool], np.ndarray]:
    """Parse puzzle input into the enhancement algorithm and starting image.

    Args:
        data (str): Raw data as a string.

    Returns:
        tuple[list[bool], np.ndarray]: Enhancement algorithm and starting image.
    """
    split_data = data.strip().splitlines()
    algorithm = [x == "#" for x in split_data.pop(0).strip()]
    assert len(algorithm) == 512
    _blank = split_data.pop(0).strip()
    assert len(_blank) == 0
    rows: list[list[str]] = []
    for line in split_data:
        rows.append(list(line.strip()))
    ary = np.array(rows)
    ary[ary == "#"] = 1
    ary[ary == "."] = 0
    ary = ary.astype(bool)
    return algorithm, ary


def _get_example_input() -> tuple[list[bool], np.ndarray]:
    return parse_data(read_data(PI.day, name="example-input.txt"))


def _get_puzzle_input() -> tuple[list[bool], np.ndarray]:
    return parse_data(read_data(PI.day))


def print_image(ary: np.ndarray) -> None:
    """Print an image to console."""
    ary = ary.copy().astype(str)
    ary[ary == "True"] = "#"
    ary[ary == "False"] = "."
    img = ""
    for row in range(ary.shape[0]):
        img += "".join(ary[row, :]) + "\n"
    print(img)
    return None


def plot_image(img: np.ndarray, title: Optional[str] = None) -> None:
    """Plot an image."""
    plt.imshow(img, cmap="binary")
    if title is not None:
        plt.title(title)
    plt.show()
    return None


def plot_video(imgs: list[np.ndarray], video_path: Optional[Path] = None) -> None:
    """Make a video of a series of images.

    Args:
        imgs (list[np.ndarray]): Series of images.
        video_path (Optional[Path], optional): If supplied, the video will be saved to
        file instead of shown in-real-time. Defaults to None.
    """
    fig, ax = plt.subplots()

    def _update(i: int) -> None:
        ax.imshow(imgs[i], cmap="binary")
        ax.set_title(f"frame {i}")
        return None

    ani = FuncAnimation(fig, _update, len(imgs))
    if video_path is None:
        plt.show()
    else:
        writer = PillowWriter(fps=3)
        ani.save(str(video_path), writer=writer)

    return None


def _preprocess_image(img: np.ndarray, pad_value: bool, p: int = 2) -> np.ndarray:
    """Make a copy, turn into boolean, and add some padding."""
    _img = img.copy().astype(bool)
    return np.pad(_img, p, mode="constant", constant_values=pad_value)


def _get_surrounding_positions(i: int, j: int) -> list[tuple[int, int]]:
    pos: list[tuple[int, int]] = []
    for a in range(i - 1, i + 2):
        for b in range(j - 1, j + 2):
            pos.append((a, b))
    return pos


def _get_surrounding_values(
    ary: np.ndarray, i: int, j: int, pad_val: bool
) -> list[bool]:
    values: list[bool] = []
    dims = ary.shape
    for a, b in _get_surrounding_positions(i, j):
        if a < 0 or b < 0 or a >= dims[0] or b >= dims[1]:
            values.append(pad_val)
        else:
            values.append(ary[a, b])
    return values


def _convert_image_values_to_index(vals: list[bool]) -> int:
    assert len(vals) == 9
    return int("".join([str(int(x)) for x in vals]), base=2)


def _trim_zeros(img: np.ndarray) -> np.ndarray:
    """Remove rows or columns from the edges that are all zeros."""
    res = img.copy()
    for _ in range(4):
        res = np.rot90(res)
        for _ in range(res.shape[0]):
            if np.all(res[0, :] == False):  # noqa: E712
                res = res[1:, :]
            else:
                break
    return res


def enhance_image(
    img: np.ndarray, alg: list[bool], pad_val: bool = False
) -> np.ndarray:
    """Enhance an image using an algorithm.

    Args:
        img (np.ndarray): Starting image.
        alg (list[bool]): Enhancement algorithm.
        pad_val (bool, optional): Value to use for padding. Defaults to False.

    Returns:
        np.ndarray: Enhanced image.
    """
    img = _preprocess_image(img, pad_value=pad_val, p=2)
    output = np.zeros_like(img, dtype=bool)
    dims = img.shape
    for i, j in product(range(dims[0]), range(dims[1])):
        values = _get_surrounding_values(img, i, j, pad_val=pad_val)
        idx = _convert_image_values_to_index(values)
        output[i, j] = alg[idx]
    return _trim_zeros(output)


def enhance_image_n(
    img: np.ndarray,
    alg: list[bool],
    n: int = 2,
    plot: bool = False,
    video: bool = False,
    video_path: Optional[Path] = None,
) -> np.ndarray:
    """Enhance an image multiple times.

    Args:
        img (np.ndarray): Starting image.
        alg (list[bool]): Enhancement algorithm
        n (int, optional): Number of iterations. Defaults to 2.
        plot (bool, optional): Should each image be plotted? Defaults to False.
        video (bool, optional): Should the series of enhanced images be compiled into a
        movie? Defaults to False.
        video_path (Optional[Path], optional): If provided, the video will be saved to
        file instead of shown in-real-time. Defaults to None.

    Returns:
        np.ndarray: Final enhanced image.
    """
    video_imgs: list[np.ndarray] = []
    if video:
        plot = False  # Only one or the other
        video_imgs.append(img.copy())
    if plot:
        plot_image(img, title="Starting image")

    init_pad_value = alg[0]
    pad_val = False

    for i in range(n):
        img = enhance_image(img, alg, pad_val=pad_val)

        if init_pad_value:
            pad_val = not pad_val

        if video:
            video_imgs.append(img.copy())
        elif plot:
            plot_image(img.copy(), title=f"Enhancement {i+1}")
    if video:
        plot_video(video_imgs, video_path=video_path)
    return img


def main() -> None:
    """Run code for 'Day 20: Trench Map'."""
    # Part 1.
    # Examples.
    ex_alg, ex_img = _get_example_input()
    check_example(10, np.sum(ex_img))
    ex_enhanced = enhance_image(ex_img, ex_alg)
    check_example(24, np.sum(ex_enhanced))
    ex_enhanced_2 = enhance_image(ex_enhanced, ex_alg)
    check_example(35, np.sum(ex_enhanced_2))
    ex_enhanced_2 = enhance_image_n(ex_img, ex_alg, n=2, plot=False)
    check_example(35, np.sum(ex_enhanced_2))
    # Real
    algorithm, starting_image = _get_puzzle_input()
    enhanced_image = enhance_image_n(starting_image, algorithm, n=2, plot=False)
    total_lit_pixels = np.sum(enhanced_image)
    print_single_answer(day=PI.day, part=1, value=total_lit_pixels)
    check_answer(5786, total_lit_pixels, day=PI.day, part=1)

    # Part 2.
    # Examples.
    ex_alg, ex_img = _get_example_input()
    ex_enhanced_50 = enhance_image_n(ex_img, ex_alg, n=50)
    check_example(3351, np.sum(ex_enhanced_50))
    # Real
    algorithm, starting_image = _get_puzzle_input()
    video_path = output_dir() / f"day{PI.day}-p2.gif"
    enhanced_image = enhance_image_n(
        starting_image, algorithm, n=50, video=True, video_path=video_path
    )
    total_lit_pixels = np.sum(enhanced_image)
    print_single_answer(day=PI.day, part=2, value=total_lit_pixels)
    check_answer(16757, total_lit_pixels, day=PI.day, part=2)
    return None


if __name__ == "__main__":
    main()
