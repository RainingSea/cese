def generate_report(books) -> str:
    report_lines = [f"{book.title} by {book.author} - {book.genre} ({book.year}) - Rating: {book.rating}\nNotes: {book.notes}" for book in books]
    return "\n".join(report_lines)