import tkinter as tk

class ArticleViewer:
    def __init__(self, article):
        self.article = article

    def show(self):
        viewer = tk.Toplevel()
        viewer.title(self.article.title)

        title_label = tk.Label(viewer, text=self.article.title, font=("Helvetica", 16))
        title_label.pack()

        author_label = tk.Label(viewer, text=f"Author: {self.article.author}")
        author_label.pack()

        description_label = tk.Label(viewer, text=self.article.description)
        description_label.pack()

        close_button = tk.Button(viewer, text="Close", command=viewer.destroy)
        close_button.pack()

        viewer.mainloop()