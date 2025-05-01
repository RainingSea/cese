from data_storage import DataStorage

class KnowledgeManager:
    def __init__(self):
        self.data_storage = DataStorage()
        self.theories = self.data_storage.load_data('theories')
        self.concepts = self.data_storage.load_data('concepts')
        self.experiments = self.data_storage.load_data('experiments')

    def add_knowledge(self, type: str, knowledge: str):
        if type == 'theories':
            self.theories.append(knowledge)
        elif type == 'concepts':
            self.concepts.append(knowledge)
        elif type == 'experiments':
            self.experiments.append(knowledge)
        else:
            raise ValueError("Invalid type specified.")
        self.data_storage.save_data(type, knowledge)

    def update_knowledge(self, type: str, old_knowledge: str, new_knowledge: str):
        if type == 'theories':
            index = self.theories.index(old_knowledge)
            self.theories[index] = new_knowledge
        elif type == 'concepts':
            index = self.concepts.index(old_knowledge)
            self.concepts[index] = new_knowledge
        elif type == 'experiments':
            index = self.experiments.index(old_knowledge)
            self.experiments[index] = new_knowledge
        else:
            raise ValueError("Invalid type specified.")
        self.save_all()

    def retrieve_knowledge(self, type: str):
        if type == 'theories':
            return self.theories
        elif type == 'concepts':
            return self.concepts
        elif type == 'experiments':
            return self.experiments
        else:
            raise ValueError("Invalid type specified.")

    def save_all(self):
        for theory in self.theories:
            self.data_storage.save_data('theories', theory)
        for concept in self.concepts:
            self.data_storage.save_data('concepts', concept)
        for experiment in self.experiments:
            self.data_storage.save_data('experiments', experiment)