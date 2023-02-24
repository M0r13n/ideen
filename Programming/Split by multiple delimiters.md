- Pythons `str.split()` can only split by a single delimiter
- but you can you `re.split()` instead:
```python
>>> a = 'Beautiful, is; better*than\nugly'
>>> re.split('; |, |\*|\n', a)
['Beautiful', 'is', 'better', 'than', 'ugly']
```