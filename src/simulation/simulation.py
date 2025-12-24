import random

from src.library.library import Library, LibraryPanel
from src.simulation.event_handlers import SimulationEventHandlers, Event


def run_simulation(steps: int = 15, seed: int | None = None) -> tuple[Library, int, int]:
    if seed:
        random.seed(seed)
    print(f"Симуляция (seed={seed})")

    library = Library()
    panel = LibraryPanel(library)

    event_handlers = SimulationEventHandlers(panel).get_event_handlers()

    skipped_operations_count = 0
    uncaught_errors_count = 0

    for step in range(1, steps + 1):
        event = random.choice(list(Event))
        print(f"\nШаг {step}: {event.name}")
        try:
            condition, handler = event_handlers[event]
            if condition():
                handler()
            else:
                print("!! Недостаточно книг для выполнения шага !!")
                skipped_operations_count += 1
        except Exception as e:
            print(f"Ошибка!!1! {e}")
            uncaught_errors_count += 1

    print(f"\nВот и всё...\nВ библиотеке осталось {len(library.get_all_isbns())} книг(а/и)")
    print(f"Шагов пропущено: {skipped_operations_count}, Ошибок не поймано: {uncaught_errors_count}")
    return library, skipped_operations_count, uncaught_errors_count


if __name__ == "__main__":
    run_simulation(steps=1000)
