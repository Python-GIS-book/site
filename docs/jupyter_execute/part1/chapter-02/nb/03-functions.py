#!/usr/bin/env python
# coding: utf-8

# # Functions
# 
# In this lesson we introduce functions as a way of making blocks of code for a specific task that are easy to use and re-use in your programs.

# ## What is a function?
# 
# A *{term}`function`* is a block of organized, reusable code that can make your programs more effective, easier to read, and simple to manage. You can think functions as little self-contained programs that can perform a specific task that you can use repeatedly in your code. One of the basic principles in good programming is "do not to repeat yourself". In other words, you should avoid having duplicate lines of code in your scripts. Functions are a good way to avoid such situations and they can save you a lot of time and effort as you don't need to tell the computer repeatedly what to do every time it does a common task, such as converting temperatures from Fahrenheit to Celsius. During the course we have already used some functions such as the `print()` command which is actually a built-in function in Python.

# ## Anatomy of a function
# 
# Let's consider the task from the first lesson when we converted temperatures from Celsius to Fahrenheit.
# Such an operation is a fairly common task when dealing with temperature data.
# Thus we might need to repeat such calculations quite often when analysing or comparing weather or climate data between the US and Europe, for example.
# 
# ### Our first function
# 
# Let's define our first function called `celsius_to_fahr`. Figure 1.10 explains the main elements of a function.

# In[1]:


def celsius_to_fahr(temp):
    return 9 / 5 * temp + 32


# ![**Figure 1.10** An example function with annotation of its important elements.](../img/Function_anatomy-400.png)
# 
# The function definition opens with the keyword `def` followed by the name of the function and a list of parameter names in parentheses.
# The body of the function — the statements that are executed when it runs — is indented below the definition line.
# 
# When we call the function, the values we pass to it are assigned to the corresponding parameter variables so that we can use them inside the function (e.g., the variable `temp` in this function example).
# Inside the function, we use a `return` statement to define the value that should be given back when the function is used, or called.

# ## Calling functions
# 
# ### Using our new function
# 
# Now let's try using our function.
# Calling our self-defined function is no different from calling any other function such as `print()`.
# You need to call it with its name and provide your value(s) as the required parameter(s) inside the parentheses.
# Here, we can define a variable `freezing_point` that is the temperature in degrees Fahrenheit we get when using our function with the temperature 0°C (the temperature at which water freezes). We can then print that value to confirm. We should get a temperature of 32°F.

# In[2]:


freezing_point = celsius_to_fahr(0)


# In[3]:


print("The freezing point of water in Fahrenheit is:", freezing_point)


# We can do the same thing with the boiling point of water in degrees Celsius (100°C). Just like with other functions, we can use our new function directly within something like the `print()` function to print out the boiling point of water in degrees Fahrenheit.

# In[4]:


print("The boiling point of water in Fahrenheit is:", celsius_to_fahr(100))


# ### Let's make another function
# 
# Now that we know how to create a function to convert Celsius to Fahrenheit, let’s create another function called `kelvins_to_celsius`. We can define this just like we did with our `celsius_to_fahr()` function, noting that the Celsius temperature is just the temperature in Kelvins minus 273.15. Just to avoid confusion this time, let's call the temperature variable used in the function `temp_kelvins`.

# In[5]:


def kelvins_to_celsius(temp_kelvins):
    return temp_kelvins - 273.15


# ### Using our second function
# 
# Let's use it in the same way as the earlier one by defining a new variable `absolute_zero` that is the Celsius temperature of 0 Kelvins. Note that we can also use the parameter name `temp_kelvins` when calling the function to explicitly state which variable values is being used. Again, let's print the result to confirm everything works.

# In[6]:


absolute_zero = kelvins_to_celsius(temp_kelvins=0)


# In[7]:


print("Absolute zero in Celsius is:", absolute_zero)


# #### Check your understanding
# 
# Let's see how things are going so far with functions. Think about how you could:
# 
# - Create a new function called `hello` with 2 parameters
#     - Parameter 1 should be called `name` and you should assign some text to this parameter this when using the function
#     - Parameter 2 should be called `age` and you should provide a number value for this parameter when using the function
# 
# When using your function, the value that is returned should be a character string stating the `name` and `age` that were provided, which you can assign to a variable called `output`.
# Printing out `output` should produce something like the following:
# 
# ```python
# print(output)
# 'Hello, my name is Dave. I am 39 years old.'
# ```

# In[8]:


# Example solution


def hello(name, age):
    return "Hello, my name is " + name + ". I am " + str(age) + " years old."


output = hello(name="Dave", age=39)
print(output)


# ### Variable names and functions
# 
# A common point of confusion for new programmers is understanding how variable names in functions relate to those defined elsewhere in your notebooks.
# When defining a function, the variable names given in the function definition exist and will only be used when the function is called.
# That might seem confusing, but as it turns out, this is an excellent feature in Python that can save you from much suffering.
# Let's try to understand this by way of an example.
# 
# Let us define a new function called `times2` that accepts a single value `number` and returns that number multiplied by 2.

# In[ ]:


def times2(number):
    new_number = number * 2
    return new_number


# So here we have defined our function to accept `number` as its only parameter, calculate `new_number`, and return that value.
# As you can see below, the variables defined in the function exist only in its *namespace*.
# Let's confirm that.

# In[ ]:


print(number)


# In[ ]:


print(new_number)


# Here, in the *global namespace* we get a `NameError` when trying to access the variables `number` or `new_number` because they have only been defined within the `times2()` function.
# 
# Perhaps, however, you are thinking we have not yet called the function, and maybe then these values will be defined.
# Let's try that.

# In[ ]:


times2(number=5)


# In[ ]:


print(number)


# As you can see `number` is still not defined in the global namespace, where values such as `freezing_point` have been defined.
# 
# Why does Python work this way?
# Well, as it turns out, the benefit of having a separate namespace for functions is that we can define a variable in the global namespace, such as `number` and not need to worry about its name within a function, or the use of a function changing its value.
# Inside the function, the value that is passed will be known as `number`, but modifying that value will not alter a variable of the same name in the global namespace.
# Let's have a look at another example using a modified `times2()` function we can call `times2v2()`.

# In[ ]:


def times2v2(number):
    number = number * 2
    return number


# Here, we pass in a value as `number` and modify the value that is passed in before returning it.
# This might not be a good idea in some cases because it could cause confusion, but it is perfectly valid code.
# 
# Let's now define a variable `number` in the global namespace and use our function to multiply it by 2.

# In[ ]:


number = 15


# In[ ]:


times2v2(number=number)


# In[ ]:


number


# As you can see, the value of the variable `number` in the global namespace was set to 15 and remains 15 after using the `times2v2()` function.
# Although there is a variable inside that function with the same name as the value in the global namespace, using the function assigns the value of `number` inside the function and manipulates that value only inside the function.
# 
# ```{caution}
# Be aware that it is possible to access variable values in functions that have been defined in the global namespace, even if the value is not passed to the function.
# This is because Python will search for variables defined with a given name first inside the function, and then outside the function (the search domain is known as the variable's *scope*).
# If such a value is found, it can be used by the function, which could be dangerous.
# ```
# 
# Let's look at an example of behavior in a function that may be unexpected.

# In[ ]:


def my_function(value):
    value = number + 20
    return value


# In[ ]:


print(my_function(11))


# You were perhaps expecting to see a value of 31 returned by `my_function()`, but that does not occur because `value` is assigned `number + 20` in the function.
# Although `number` was not passed to `my_function()` it is defined in the global namespace and thus can be used by our example function.
# Since `number = 15` we get a value of 35 returned when using `my_function()`.
# Conclusion: Be careful!
# 
# For those who are interested, more information about namespaces and variables scopes can be found on the [Real Python website](https://realpython.com/python-namespaces-scope/).

# ### Functions within a function
# 
# What about converting Kelvins to Fahrenheit?
# We could write out a new formula for it, but we don’t need to.
# Instead, we can do the conversion using the two functions we have already created and calling those from the function we are now creating. Let's create a new function `kelvins_to_fahr` that takes the temperature in Kelvins as the parameter value `temp_kelvins` and uses our `kelvins_to_celsius` and `celsius_to_fahr` functions within the new function to convert temperatures from Kelvins to degrees Fahrenheit.

# In[9]:


def kelvins_to_fahr(temp_kelvins):
    temp_celsius = kelvins_to_celsius(temp_kelvins)
    temp_fahr = celsius_to_fahr(temp_celsius)
    return temp_fahr


# ### Using our combined functions
# 
# Now let's use the function to calculate the temperature of absolute zero in degrees Fahrenheit. We can then print that value to the screen again.

# In[10]:


absolute_zero_fahr = kelvins_to_fahr(temp_kelvins=0)


# In[11]:


print("Absolute zero in Fahrenheit is:", absolute_zero_fahr)


# ## Documenting functions with docstrings
# 
# A documentation string, or a *{term}`docstring`* is a block of text that describes what a specific function, library, or script does and how to use it. Surprise surprise, PEP 8 contains [more guidance about documentation strings](https://www.python.org/dev/peps/pep-0008/#documentation-strings) [^pep8_docstring], and docstrings even have [their own guide page](https://www.python.org/dev/peps/pep-0257/) [^pep257]. Let's look an an example from our of our functions above.
# 
# ```python
# def kelvins_to_celsius(temp_kelvins):
#     """Converts temperature in Kelvins to degrees Celsius."""
#     return temp_kelvins - 273.15
# ```
# 
# Here you can see a short bit of text explaining in simple language what this function does. In this case our function is quite simple, but the docstring still helps remove uncertainty about what it can be used to do. So, what can we see in this example?
# 
# - A docstring is always the first statement in a module or a function.
# - Docstrings are written using `"""triple double quotation marks"""`.
# - Short docstrings [can be written on a single line](https://www.python.org/dev/peps/pep-0257/#one-line-docstrings) [^pep257_one_line].
# 
# Seems simple enough, right? We can also provide more detailed docstrings, which can be particularly helpful when using functions with multiple parameters. Let's expand the docstring above to provide more information about this function.
# 
# ```python
# def kelvins_to_celsius(temp_kelvins):
#     """
#     Converts temperature in Kelvins to degrees Celsius.
# 
#     Parameters
#     ----------
#     temp_kelvins: <numerical>
#         Temperature in Kelvins
# 
#     Returns
#     -------
#     <float>
#         Converted temperature.
#     """
#     return temp_kelvins - 273.15
# ```
# 
# Here you can now see more information about the expected values for the parameters and what will be returned when using the function. This level of documentation is not needed for every function, but clearly it can be useful, especially when you have multiple parameters. Note here that the suggested format is to have the quotation marks on their own separate lines.

# ## Exercises
# 
# Add exercises.

# ## Footnotes
# 
# [^pep8_docstring]: <https://www.python.org/dev/peps/pep-0008/#documentation-strings>
# [^pep257]: <https://www.python.org/dev/peps/pep-0257/>
# [^pep257_one_line]: <https://www.python.org/dev/peps/pep-0257/#one-line-docstrings>
