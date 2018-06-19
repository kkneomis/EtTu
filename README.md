# Et tu?

This application helps students learn about basic cryptography.  
It references the caesar cipher (http://www.practicalcryptography.com/ciphers/caesar-cipher/) and the subsitution cipher (https://en.wikipedia.org/wiki/Substitution_cipher)

## Rest api
__To get the cleartext__
```
/problem/{level}/{id}   
```
level is easy, medium, or hard

__Caesar ciphered text__
```
/problem/{level}/{id}/rot
```

__Substitution ciphered text__
```
/problem/{level}/{id}/rot
```