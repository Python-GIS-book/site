---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region -->
# Solutions to lesson questions

## Chapter 1

1.1
```python
math.sin(math.pi)
```

1.2 
```python
my_variable = "Python is cool!"
print(my_variable)
```

1.3 
```python
# Solutions may vary
first_variable = "Python"
second_variable = " is cool!"

print(first_variable + second_variable)  # Works
print(5 * first_variable)                # Works
print(first_variable - second_variable)  # Fails
```

1.4 
```python
for i in range(2, 9, 3):
    print(i)
```

1.5
```bash
11
7
11
15
11
```

1.6
```python
weather = "rain"

if weather == "rain":
    print("Wear a raincoat")
    print("Wear rain boots")
else:
    print("No rainwear needed")
```

1.7
```python
'B'
```

1.8
```python
weather = "rain"
wind_speed = 20
comfort_limit = 18

# If it is windy or raining, print "stay at home", else print "go out and enjoy the weather!"
if (weather == "rain") or (wind_speed >= comfort_limit):
    print("Just stay at home")
else:
    print("Go out and enjoy the weather! :)")
```

1.9
```python
def hello(name, age):
    return "Hello, my name is " + name + ". I am " + str(age) + " years old."

output = hello(name="Dave", age=41)
print(output)
```
<!-- #endregion -->
