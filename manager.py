
from models import Coach, Athlete, Exercise, WorkoutPlan

class FitnessManager:
    def __init__(self):
        self.coaches = []
        self.athletes = []
        self.plans = []
        self.exercises = []

    # ---------- Helper methods ----------

    def find_by_name(self, items, name, item_type):
        for item in items:
            if item.name == name:
                return item

        raise ValueError(f"{item_type} not found.")

    def get_rows(self, kind):
        if kind == "coaches":
            return [
                (c.name, c.specialty)
                for c in self.coaches
            ]

        if kind == "athletes":
            return [
                (
                    a.name,
                    str(a.age),
                    a.coach.name if a.coach else ""
                )
                for a in self.athletes
            ]

        if kind == "plans":
            return [
                (p.name, p.day, p.athlete.name)
                for p in self.plans
            ]

        if kind == "exercises":
            return [
                (
                    e.name,
                    str(e.sets),
                    str(e.reps),
                    str(e.weight),
                    p.name
                )
                for p in self.plans
                for e in p.exercises
            ]

        return []

    # ---------- Coaches ----------

    def add_coach(self, data):
        coach = Coach(data["Name"], data["Specialty"])
        self.coaches.append(coach)

    def update_coach(self, index, data):
        coach = self.coaches[index]
        coach.name = data["Name"]
        coach.specialty = data["Specialty"]

    def delete_coach(self, index):
        coach = self.coaches[index]

        if any(a.coach is coach for a in self.athletes):
            raise ValueError(
                "This coach has athletes. Reassign them first."
            )

        self.coaches.pop(index)

    # ---------- Athletes ----------

    def add_athlete(self, data):
        try:
            age = int(data["Age"])
            if age <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Age must be a positive integer.")

        coach = self.find_by_name(
            self.coaches, data["Coach"], "Coach"
        )

        athlete = Athlete(data["Name"], age, coach)
        self.athletes.append(athlete)

    def update_athlete(self, index, data):
        try:
            age = int(data["Age"])
            if age <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Age must be a positive integer.")

        athlete = self.athletes[index]
        coach = self.find_by_name(
            self.coaches, data["Coach"], "Coach"
        )

        athlete.name = data["Name"]
        athlete.age = age
        athlete.coach = coach

    def delete_athlete(self, index):
        athlete = self.athletes[index]

        if athlete.workout_plan is not None:
            raise ValueError(
                "Delete this athlete's workout plan first."
            )

        self.athletes.pop(index)

    # ---------- Workout plans ----------

    def add_plan(self, data):
        athlete = self.find_by_name(
            self.athletes, data["Athlete"], "Athlete"
        )

        if athlete.workout_plan is not None:
            raise ValueError(
                "This athlete already has a workout plan."
            )

        plan = WorkoutPlan(data["Name"], data["Day"], athlete)
        self.plans.append(plan)
        athlete.workout_plan = plan

    def update_plan(self, index, data):
        plan = self.plans[index]
        athlete = self.find_by_name(
            self.athletes, data["Athlete"], "Athlete"
        )

        if athlete is not plan.athlete and athlete.workout_plan:
            raise ValueError(
                "This athlete already has a workout plan."
            )

        plan.athlete.workout_plan = None

        plan.name = data["Name"]
        plan.day = data["Day"]
        plan.athlete = athlete

        athlete.workout_plan = plan

    def delete_plan(self, index):
        plan = self.plans[index]

        if plan.exercises:
            raise ValueError(
                "Delete this plan's exercises first."
            )

        plan.athlete.workout_plan = None
        self.plans.pop(index)

    # ---------- Exercises ----------

    def get_exercise(self, index):
        all_exercises = [
            exercise
            for plan in self.plans
            for exercise in plan.exercises
        ]

        return all_exercises[index]

    def validate_exercise_data(self, data):
        try:
            sets = int(data["Sets"])
            reps = int(data["Reps"])
            weight = float(data["Weight"])

            if sets <= 0 or reps <= 0 or weight < 0:
                raise ValueError

        except ValueError:
            raise ValueError(
                "Sets and reps must be positive integers; "
                "weight must be zero or greater."
            )

        return sets, reps, weight

    def add_exercise(self, data):
        plan = self.find_by_name(
            self.plans, data["Workout Plan"], "Workout plan"
        )

        sets, reps, weight = self.validate_exercise_data(data)

        exercise = Exercise(
            data["Name"], sets, reps, weight
        )

        plan.exercises.append(exercise)
        self.exercises.append(exercise)

    def update_exercise(self, index, data):
        exercise = self.get_exercise(index)

        plan = self.find_by_name(
            self.plans, data["Workout Plan"], "Workout plan"
        )

        sets, reps, weight = self.validate_exercise_data(data)

        exercise.name = data["Name"]
        exercise.sets = sets
        exercise.reps = reps
        exercise.weight = weight

        for old_plan in self.plans:
            if exercise in old_plan.exercises:
                old_plan.exercises.remove(exercise)
                break

        plan.exercises.append(exercise)

    def delete_exercise(self, index):
        exercise = self.get_exercise(index)

        for plan in self.plans:
            if exercise in plan.exercises:
                plan.exercises.remove(exercise)
                break

        if exercise in self.exercises:
            self.exercises.remove(exercise)

    # ---------- Generic CRUD ----------

    def create(self, kind, data):
        operations = {
            "coaches": self.add_coach,
            "athletes": self.add_athlete,
            "plans": self.add_plan,
            "exercises": self.add_exercise
        }

        operations[kind](data)

    def update(self, kind, index, data):
        operations = {
            "coaches": self.update_coach,
            "athletes": self.update_athlete,
            "plans": self.update_plan,
            "exercises": self.update_exercise
        }

        operations[kind](index, data)

    def delete(self, kind, index):
        operations = {
            "coaches": self.delete_coach,
            "athletes": self.delete_athlete,
            "plans": self.delete_plan,
            "exercises": self.delete_exercise
        }

        operations[kind](index)



