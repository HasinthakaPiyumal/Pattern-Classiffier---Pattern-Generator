import random

class CodeGenerator:
    """An agent that generates Python code snippets, some potentially vulnerable."""
    def generate_code(self, complexity_level: int) -> str:
        templates = [
            "def safe_add(a, b):\n    return a + b",
            "def vulnerable_eval(expression):\n    # Potential vulnerability: eval() can execute arbitrary code\n    return eval(expression)",
            "def safe_multiply(x, y):\n    result = x * y\n    return result",
            "import os\ndef vulnerable_os_command(command):\n    # Potential vulnerability: os.system() can execute arbitrary commands\n    os.system(command)",
            "def safe_format_string(name):\n    return f'Hello, {name}!'",
            "import subprocess\ndef vulnerable_p_open(cmd_args):\n    # Potential vulnerability: subprocess.run with shell=True or unsanitized input\n    subprocess.run(cmd_args, shell=True)",
            "def vulnerable_sql_query(username):\n    # Potential SQL Injection risk if username is not sanitized\n    query = f\"SELECT * FROM users WHERE username = '{username}'\"\n    return query",
            "def safe_data_process(data):\n    return [d*2 for d in data]"
        ]
        # Simulate different complexity levels by biasing towards more complex/potentially vulnerable for higher levels
        if complexity_level > 5:
            # Include more vulnerable templates at higher complexity
            return random.choice(templates + [templates[1], templates[3], templates[5], templates[6]]) 
        return random.choice(templates)

class SecurityAuditor:
    """An adversarial agent (Safeguard) that critically screens generated code for security vulnerabilities."""
    def audit_code(self, code: str) -> list[str]:
        issues = []
        # Real-world usage: Automated static analysis for security vulnerabilities
        if "eval(" in code:
            issues.append("Found 'eval()': Potential arbitrary code execution vulnerability.")
        if "os.system(" in code:
            issues.append("Found 'os.system()': Potential arbitrary command execution vulnerability.")
        if "subprocess.run(" in code and "shell=True" in code:
            issues.append("Found 'subprocess.run(..., shell=True)': Potential command injection vulnerability.")
        # Simplified SQL injection pattern detection
        if "SELECT * FROM" in code and "WHERE" in code and "'" in code and "username" in code:
             issues.append("Found potential SQL Injection pattern in database query.")
        
        # In a real system, this would involve more sophisticated AST analysis or security linters.
        return issues

# --- Simulation of Adversarial Agent Interaction in Software Development --- 

def simulate_code_development_cycle(num_iterations: int):
    """Simulates a cycle of code generation and adversarial security auditing."""
    generator = CodeGenerator()
    auditor = SecurityAuditor()

    print("--- Starting Code Development & Security Audit Simulation ---")
    print("Real-world usage: This pattern is used in CI/CD pipelines for automated security scanning (SAST).")
    print("Simulation pattern: Repeatedly generating code and having an independent agent validate its security.")

    for i in range(1, num_iterations + 1):
        print(f"\nIteration {i}:")
        complexity = random.randint(1, 10)
        generated_code = generator.generate_code(complexity)
        print(f"Code Generator produced (Complexity {complexity}):\n---\n{generated_code[:150]}...\n---") # Show first 150 chars

        audit_findings = auditor.audit_code(generated_code)

        if audit_findings:
            print("\n!!! Security Auditor detected issues !!!")
            for issue in audit_findings:
                print(f"- {issue}")
            print("Action required: Code rejected due to security concerns. Requires developer review/refactoring.")
        else:
            print("\nSecurity Auditor found no critical issues. Code approved for further development stages (e.g., testing).")

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    simulate_code_development_cycle(5) # Simulate 5 code generation and audit cycles