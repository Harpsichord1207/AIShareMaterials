# Prompt 1: Code Review Request

## Task Description

Please review the following Python code and provide feedback on:

1. **Code Quality** - Readability, naming conventions, structure
2. **Performance** - Any potential bottlenecks or optimizations
3. **Security** - Potential vulnerabilities or security issues
4. **Best Practices** - Adherence to Python best practices

## Code to Review

```python
def process_data(data):
    result = []
    for i in range(len(data)):
        if data[i] != None:
            if type(data[i]) == str:
                result.append(data[i].upper())
            else:
                result.append(data[i])
    return result
```

## Expected Output Format

Please structure your review as:

- **Issues Found**: List of problems with severity
- **Recommendations**: Specific improvements
- **Refactored Code**: Improved version of the code
