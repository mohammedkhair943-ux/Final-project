import json
import math
from collections import Counter

ROLE_SKILLS = {
    "Python Developer": ["python", "oop", "data structures", "git", "apis", "testing"],
    "Software Engineer": ["python", "oop", "data structures", "algorithms", "git", "databases"],
    "Data Analyst": ["python", "sql", "statistics", "data visualization", "excel", "pandas"],
    "Machine Learning Engineer": ["python", "statistics", "linear algebra", "machine learning",
                                  "data structures", "pandas", "numpy"],
    "Web Developer": ["python", "html", "css", "javascript", "apis", "databases"],
}

TRAINING_DATA = [
    (["python","oop","data structures","git","apis","testing"], "Python Developer"),
    (["python","oop","data structures","algorithms","git","databases"], "Software Engineer"),
    (["python","sql","statistics","data visualization","excel","pandas"], "Data Analyst"),
    (["python","statistics","linear algebra","machine learning","pandas","numpy"], "Machine Learning Engineer"),
    (["python","html","css","javascript","apis","databases"], "Web Developer"),
    (["python","oop","git","apis"], "Python Developer"),
    (["python","data structures","algorithms","git"], "Software Engineer"),
    (["python","sql","statistics","excel"], "Data Analyst"),
    (["python","statistics","machine learning","numpy"], "Machine Learning Engineer"),
    (["html","css","javascript","apis"], "Web Developer"),
    (["python","oop","data structures","algorithms"], "Software Engineer"),
    (["python","sql","pandas","data visualization"], "Data Analyst"),
    (["python","statistics","linear algebra","numpy","pandas"], "Machine Learning Engineer"),
    (["python","oop","apis","testing"], "Python Developer"),
    (["html","css","javascript","databases"], "Web Developer"),
]

def vectorize(skills):
    vocabulary = sorted({s for profile, _ in TRAINING_DATA for s in profile})
    current = set(skills)
    return [1 if s in current else 0 for s in vocabulary], vocabulary

def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    ma = math.sqrt(sum(x*x for x in a))
    mb = math.sqrt(sum(y*y for y in b))
    return dot / (ma*mb) if ma and mb else 0.0

class KNNRoleModel:
    def __init__(self, training_data, k=3):
        self.training_data = training_data
        self.k = k

    def predict(self, user_skills):
        user_vector, vocabulary = vectorize(user_skills)
        neighbors = []
        for profile, role in self.training_data:
            pset = set(profile)
            vector = [1 if s in pset else 0 for s in vocabulary]
            similarity = cosine_similarity(user_vector, vector)
            neighbors.append((similarity, role))
        neighbors.sort(reverse=True, key=lambda x: x[0])
        top = neighbors[:self.k]
        votes = Counter()
        for similarity, role in top:
            votes[role] += similarity
        ranked = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        return ranked, top

class SkillProfile:
    def __init__(self, skills=None):
        self.skills = set(skills or [])

    def add(self, skill):
        self.skills.add(skill.strip().lower())

    def remove(self, skill):
        skill = skill.strip().lower()

        if skill == "all":
            self.skills.clear()
            print("All skills removed.")
        else:
            self.skills.discard(skill)
            print("Skill removed if it existed.")

    def save(self, filename="skillgap_data.json"):
        with open(filename, "w") as f:
            json.dump(sorted(self.skills), f, indent=2)

    def load(self, filename="skillgap_data.json"):
        try:
            with open(filename, "r") as f:
                self.skills = set(json.load(f))
        except FileNotFoundError:
            pass

class SkillGapAnalyzer:
    def __init__(self, role_skills):
        self.role_skills = role_skills

    def analyze(self, skills, role):
        required = set(self.role_skills[role])
        current = set(skills)
        matched = current & required
        missing = required - current
        coverage = len(matched) / len(required) * 100
        return matched, missing, coverage

def main():
    profile = SkillProfile()
    profile.load()
    model = KNNRoleModel(TRAINING_DATA)
    analyzer = SkillGapAnalyzer(ROLE_SKILLS)

    while True:
        print("\n=== SkillGap ML ===")
        print("1. Add skill")
        print("2. View skills")
        print("3. Remove skill")
        print("4. ML role prediction")
        print("5. Analyze a target role")
        print("6. Save and exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            profile.add(input("Skill: "))
            print("Skill added.")

        elif choice == "2":
            print("\nYour skills:")
            for skill in sorted(profile.skills):
                print("-", skill)
            if not profile.skills:
                print("No skills added yet.")

        elif choice == "3":
            profile.remove(input("Skill to remove: "))

        elif choice == "4":
            if not profile.skills:
                print("Add some skills first.")
                continue
            ranked, neighbors = model.predict(profile.skills)
            print("\n=== ML Role Prediction ===")
            for role, score in ranked:
                print(f"{role}: {score:.3f}")
            print("\nNearest training examples:")
            for similarity, role in neighbors:
                print(f"{role} | similarity={similarity:.3f}")
            print("\nPrediction uses K-nearest neighbors and cosine similarity.")

        elif choice == "5":
            roles = list(ROLE_SKILLS)
            for i, role in enumerate(roles, 1):
                print(f"{i}. {role}")
            try:
                role = roles[int(input("Choose role: ")) - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue
            matched, missing, coverage = analyzer.analyze(profile.skills, role)
            print(f"\n{role}")
            print(f"Skill coverage: {coverage:.1f}%")
            print("Matched:", ", ".join(sorted(matched)) or "None")
            print("Missing:", ", ".join(sorted(missing)) or "None")

        elif choice == "6":
            profile.save()
            print("Profile saved. Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
