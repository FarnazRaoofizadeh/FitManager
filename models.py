class Coach:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty

class Athlete:
    def __init__(self, name, age, coach):
        self.name = name
        self.age = age
        self.coach = coach
        self.workout_plan = None

class Exercise:
    def __init__(self, name, sets, reps, weight):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

class WorkoutPlan:
    def __init__(self, name, day, athlete):
        self.name = name
        self.day = day
        self.athlete = athlete
        self.exercises = []




