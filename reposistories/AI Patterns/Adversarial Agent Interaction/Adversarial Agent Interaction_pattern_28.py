import random
import difflib

class Essay:
    def __init__(self, student_id, content):
        self.student_id = student_id
        self.content = content
        self.plagiarism_score = 0.0
        self.status = "PENDING_CHECK"

    def __repr__(self):
        return f"Essay(Student:{self.student_id}, Status:{self.status}, Plagiarism:{self.plagiarism_score:.2f}%)"

class EssayWriter:
    def write_essay(self, student_id, topic, creativity_level=0.5):
        print(f"EssayWriter: Student {student_id} is writing an essay on '{topic}'...")
        base_content = f"This essay discusses {topic}. "
        if creativity_level < 0.3:
            base_content += "It is a well-known fact that this topic has many facets. "
            base_content += "The implications are far-reaching and impact society significantly. "
            base_content += "Therefore, understanding its nuances is crucial for academic success. "
            base_content += "In conclusion, the subject matter is complex but rewarding to study."
        elif creativity_level < 0.7:
            base_content += "Exploring this topic reveals several interesting points. "
            base_content += "Various perspectives exist, contributing to a rich discussion. "
            base_content += "The analysis presented here aims to shed light on key aspects. "
            base_content += "Ultimately, the insights gained are valuable for future research."
        else:
            base_content += "My unique perspective on this topic highlights novel connections. "
            base_content += "Innovative ideas emerge when approaching the subject from a fresh angle. "
            base_content += "This analysis seeks to challenge conventional wisdom and offer new interpretations. "
            base_content += "The conclusion synthesizes diverse thoughts into a coherent framework."

        words = base_content.split()
        if random.random() < 0.2:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx] + "x"
        return Essay(student_id, " ".join(words))

class PlagiarismChecker:
    def __init__(self, known_sources):
        self.known_sources = known_sources

    def evaluate_essay(self, essay):
        max_similarity = 0.0
        flagged_source = None
        for source_text in self.known_sources:
            s = difflib.SequenceMatcher(None, essay.content, source_text)
            similarity = s.ratio() * 100
            if similarity > max_similarity:
                max_similarity = similarity
                flagged_source = source_text

        essay.plagiarism_score = max_similarity
        if max_similarity > 70.0:
            essay.status = "FLAGGED_PLAGIARISM"
            print(f"PlagiarismChecker: !!! Essay from {essay.student_id} flagged for high similarity ({max_similarity:.2f}%) to a known source.")
            return False, f"Highly similar to: '{flagged_source[:50]}...'"
        else:
            essay.status = "CLEAN"
            print(f"PlagiarismChecker: Essay from {essay.student_id} appears clean (Similarity: {max_similarity:.2f}%).")
            return True, ""

if __name__ == "__main__":
    original_text_1 = "This essay discusses the importance of environmental conservation. It is a well-known fact that this topic has many facets. The implications are far-reaching and impact society significantly. Therefore, understanding its nuances is crucial for academic success. In conclusion, the subject matter is complex but rewarding to study."
    original_text_2 = "Artificial intelligence is transforming various industries. Exploring this topic reveals several interesting points. Various perspectives exist, contributing to a rich discussion. The analysis presented here aims to shed light on key aspects. Ultimately, the insights gained are valuable for future research."

    essay_writer = EssayWriter()
    plagiarism_checker = PlagiarismChecker(known_sources=[original_text_1, original_text_2])

    student_essays = [
        (101, "Environmental Conservation", 0.2),
        (102, "The Future of AI", 0.6),
        (103, "Quantum Computing Breakthroughs", 0.9),
    ]

    for student_id, topic, creativity in student_essays:
        generated_essay = essay_writer.write_essay(student_id, topic, creativity)
        is_clean, reason = plagiarism_checker.evaluate_essay(generated_essay)
        print(f"Result for {generated_essay}: {generated_essay.status}")
        if not is_clean:
            print(f"Reason: {reason}")
        print("-" * 30)