import random

class CodeSnippet:
    def __init__(self, code_string, language="python"):
        self.code_string = code_string
        self.language = language

    def __str__(self):
        return f"CodeSnippet (\n{self.code_string}\n)"

class CodeGenerator:
    def generate_simple_function(self, name="process_data"):
        templates = [
            f"def {name}(data):\n    result = []\n    for item in data:\n        result.append(item * 2)\n    return result",
            f"def {name}(items):\n    total = 0\n    for i in items:\n        total += i\n    print(f\"Total: {{total}}\")\n    return total",
            f"def {name}(user_input):\n    query = f\"SELECT * FROM users WHERE username = '{{user_input}}'\"\n    print(f\"Executing: {{query}}\") # Potential SQL Injection\n    return query",
            f"def {name}(data):\n    eval(data) # Dangerous eval usage\n    return 'Done'",
            f"def {name}(param):\n    # This function looks fine\n    return param[::-1]"
        ]
        code = random.choice(templates)
        print(f"[CodeGenerator] Generated code snippet for '{name}'.")
        return CodeSnippet(code)

class SecurityAuditor:
    def analyze_code(self, code_snippet):
        print(f"[SecurityAuditor] Analyzing code snippet for vulnerabilities...")
        issues = []

        # Rule 1: Check for 'eval()' function usage
        if 'eval(' in code_snippet.code_string:
            issues.append("High severity: 'eval()' function detected. Potential for arbitrary code execution.")

        # Rule 2: Check for potential SQL injection patterns (simplified)
        if "SELECT * FROM" in code_snippet.code_string and "'{{user_input}}'" in code_snippet.code_string:
            issues.append("High severity: Potential SQL Injection vulnerability detected. User input directly used in SQL query.")

        # Rule 3: Check for direct print of sensitive info (example)
        if "print(f\"Executing:" in code_snippet.code_string:
            issues.append("Medium severity: Direct printing of execution string might expose sensitive query details.")

        # Rule 4: Check for excessively long lines (basic code quality)
        for line in code_snippet.code_string.split('\n'):
            if len(line) > 80:
                issues.append(f"Low severity: Line exceeds 80 characters: '{line.strip()[:50]}...' ")

        if not issues:
            print("[SecurityAuditor] No significant security or quality issues found.")
            return True, "No issues found."
        else:
            print("[SecurityAuditor] Issues detected in code snippet:")
            for issue in issues:
                print(f"  - {issue}")
            return False, issues

# --- Simulation --- 
if __name__ == "__main__":
    generator = CodeGenerator()
    auditor = SecurityAuditor()

    print("\n--- Running Code Generation and Security Audit Simulation ---")
    for i in range(4):
        function_name = f"func_{i}"
        generated_code = generator.generate_simple_function(function_name)
        print(f"\n{generated_code}")
        
        passed, feedback = auditor.analyze_code(generated_code)
        print(f"Audit Result for '{function_name}': {'PASS' if passed else 'FAIL'}\n")
