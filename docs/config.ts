//https://github.com/sennett-lau/readme-project-structure-generator.git
export const projectStructure = {
        src: {
            library: {
                collections: {
                    "book_collection.py": "BaseBookCollection, ImmutableBookCollection, BookCollection",
                    "index_dict.py": "IndexDict"
                },
                "book.py": "Book, Genres",
                "library.py": "LibraryABC, Library, LibraryPanel"
            },
            simulation: {
               "event_handlers.py": "Event, SimulationEventHandlers",
               "simulation.py": "run_simulation",
               "utils.py": "generate_random_book, get_isbn, get_random_title"
            },
            'main.py': 'Входная точка в программу',
        },
        'tests': 'Тесты для всего'
}
