from src.simulation.simulation import run_simulation


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    while True:
        try:
            steps, seed = map(int, input("Введите кол-во шагов и сид через пробел: ").split(" "))
            break
        except ValueError:
            ...
    run_simulation(steps, seed)


if __name__ == "__main__":
    main()
