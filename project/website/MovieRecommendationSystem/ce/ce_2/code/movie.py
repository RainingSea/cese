class Movie:
    def __init__(self, title: str, description: str, rating: float):
        self.title = title
        self.description = description
        self.rating = rating

    def save(self):
        with open('movies.txt', 'a') as file:
            file.write(f"{self.title}|{self.description}|{self.rating}\n")

    @staticmethod
    def load(title: str):
        with open('movies.txt', 'r') as file:
            for line in file:
                movie_data = line.strip().split('|')
                if movie_data[0] == title:
                    return Movie(movie_data[0], movie_data[1], float(movie_data[2]))
        return None