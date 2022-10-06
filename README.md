A library of classes for [HAR](https://github.com/ahmadnassri/har-spec/blob/master/versions/1.2.md) data using [pyserde](https://pypi.org/project/pyserde/).

The library is focused on providing a [F-Algebra](#f-algebra-classes) for `HAR` data and associated [morphisms](#morphisms) but also contains [canonical types](#CanonicalBasic-types) for basic usages.

## F-Algebra classes
There is one generic-ish class for every `HAR` type and are affixed with `F`.
All nested `HAR` types have been replaced with type parameters.
Some types have no nested `HAR` types and so have no generic parameters but are included for completeness.

There is one edge case for post data.
Since some of the parameters defined in the spec are mutually exclusive there are two classes for post data.
`PostDataParamF` for `ParamF` based post data, and `PostDataTextF` for text based post data.
There is a union type `PostDataF` combining the two for type hints but it cannot be constructed.

All of these types are Functory, by providing a `nmap` function that takes a function for each of the generic parameters.
For example, see the `ResponseF` class below.
```python
class ResponseF(Generic[A, B, C]):
   ...
   statusText: str
   httpVersion: str
   cookies: List[A]
   headers: List[B]
   content: C
   ...

   def nmap(
       self: "ResponseF[A, B, C]",
       f: Func[A, W],
       g: Func[B, X],
       h: Func[C, Y],
   ) -> "ResponseF[W, X, Y]":
       return replace(
           self,  # type: ignore[arg-type]
           cookies=list(map(f, self.cookies)),
           headers=list(map(g, self.headers)),
           content=h(self.content),
       )
```

## Morphisms
Currently there are just 2 helper morphisms.
`harf_cata` is a general catamorphsim, and `harf` which helps you build an algebra for `harf_cata` by taking explicit functions for each `HAR` type.

For example, if you wanted to count the number of times the string `"key"` is in headers you could do the following
```python
harf(
    default=0,
    header=lambda h: h.count("key"),
    request=lambda r: sum(r.headers),
    response=lambda r: sum(r.headers),
    entry=lambda e: e.request + e.response,
    log=lambda l: sum(l.entries),
)(har_data)
```

## Canonical/Basic types
For simple usages there are also type aliases for the canonical `HAR` structure.
I.E. `Response = ResponseF[Cookie, Header, Content]`
