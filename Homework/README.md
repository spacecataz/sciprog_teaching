# Assignments

Homeworks 1-6 are typical assignments to give to class.

## Future ideas:

- Timing of operations: how slow are if-then statements vs. other logical
statements?  This would be interesting to test.
- Break up Burton/scripting into two parts (currently both in HW 5.)


Example of timing- which is faster?

```
if ( a and b and c):
    do something
```

or

```
if a:
    if b:
        if c:
    else:
        if c:
else:
    if b:
        if c:
    else:
        if c:
```