# TypeScrypt

1. [TL;DR](#tldr)
1. [Best practices](#best-practices)
   1. [Use local modules](#use-local-modules)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

TypeScript is intentionally and strictly a superset of JavaScript with optional Type checking.<br/>
It compiles into JavaScript, so JavaScript is what one is _actually_ going to execute.

TypeScript:

- Provides an _optional_ type system for JavaScript with compile time type safety.<br/>
  Types are completely optional and inferred if not explicitly specified, and (working) js code compiles correctly with
  TypeScript as-is.
- Provides planned features from future JavaScript editions to current JavaScript engines.
- Tries to protect the user from nonsensical portions of JavaScript that never worked.

  <details>

  ```ts
  [] + [];      // JavaScript: "", TypeScript: Error
  {} + [];      // JS: 0, TS: Error
  [] + {};      // JS: "[object Object]", TS: Error
  {} + {};      // JS: NaN or [object Object][object Object], TS: Error
  "hello" - 1;  // JS: NaN, TS: Error

  function add(a,b) {
      return
          a + b;  // JS: undefined, TS: Error: 'unreachable code detected'
  }
  ```

  </details>

`undefined` specifies something hasn't been initialized.<br/>
`null` specifies something is currently unavailable.

Quickly test stuff in the [playground].

```ts
// single-line comment
/* comment block */
/* comment blocks
 * can span
 * multiple lines */
/** JSDOC block */
/**
 * JSDOC blocks
 * can span multiple lines
 * and start with double '*'
 */

var foo = 123;
const bar: string = '123';
let list: boolean[] = [true, false, false];              // array declaration format 1
const stringList: array<string> = [true, false, false];  // array declaration format 2
var keyed_numbers: { [key: string]: number };            // object declaration
interface Point2D {
    x: number;
    y: number;
};
let point2D: Point2D = { x: 0, y: 10 };
function iTakePoint2D(point: Point2D) { /* do something */ };

// Ternary operator.
// (condition) ? valueIfTrue : valueIfFalse
const key = dict.has(key) ? dict.get(key)! : 'default';
const nestedValue = mark >= 75 ? '75+' : mark >= 61 && mark < 75 ? '65-74' : '-64';

// Explicitly convert values into true booleans (one of true|false).
const hasName = !!name;

// Assert some value is non-null and non-undefined in contexts where the type checker is unable to conclude that fact.
const keyName = keyPair_output.apply(kp => kp.keyName!);

// Remove undefined values from arrays.
const cleanArray = originalArray.filter(item => item !== undefined);

// Provide fallback values in case the primary value is `null` or `undefined`.
// value ?? fallback
const prettyPrint = options.prettyPrint ?? true;

const transformedString = "";
// replace a substring
transformedString = sourceString?.replace("substring", "replacement");
// replace the first match of a regexp
transformedString = sourceString?.replace(/regex/, "replacementFor1");
// replace all matches of a regexp
transformedString = sourceString?.replace(/regex/g, "replacementForAll");
// Transform only the first character of a string to lowercase.
transformedString = sourceString?.replace(/-?\w/g, match => match.toLowerCase());

/**
 * Construct a copy of an array with duplicate items removed.
 * Where duplicate items exist, only the first instance will be kept.
 * Converts an array to a Set, removing duplicates faster than any native loop, then uses the spread syntax to convert
 * that Set back into a new array.
 * By making the function use a generic type, it can be used with any type of array.
 */
function removeDups<T>(array: T[]): T[] {
    return [...new Set(array)];
}
```

## Best practices

- Always use `===` and `!==` to check **value equality**, except for `null` checks.
- Use [deep-equal] to check **objects' structural equality**.

  <details>

  ```ts
  import * as deepEqual from "deep-equal";
  console.log(deepEqual({a:123},{a:123}));
  ```

  </details>

### Use local modules

As of NPM version 2.0.0, one can provide paths to local directories containing packages.

Local paths can be set via `npm install -S` using any of the following forms:

- `../foo/bar`
- `./foo/bar`
- `~/foo/bar`
- `/foo/bar`

Paths will be normalized to a **relative** path and added to the `package.json` file:

```json
{
  "name": "baz",
  "dependencies": {
    "bar": "file:../foo/bar",
    "@custom/lib": "file://../lib"
  }
}
```

> Packages linked by local path will **not** have their own dependencies installed when running `npm install`.<br/>
> To do that, `npm install` must be executed from inside the local paths.

## Further readings

- [Website]
- [Codebase]
- [Documentation]
- [TypeScript Deep Dive]
- [Contributors Coding Guidelines]
- The [deep-equal] package
- [How To Initialize An Empty Typed Object In TypeScript?]
- [Top 12 Most Useful Typescript Utility Types]
- [How to Break a String into Multiple Lines in TypeScript]
- [How to Add an Item to an Array in TypeScript if Not Undefined]
- [Local Paths]
- [Mastering Typescript Import from Path]

### Sources

- [Nullish Coalescing: The ?? Operator in TypeScript]
- [Remove duplicates from array in typescript]

<!--
  Reference
  ═╬═Time══
  -->

<!-- Upstream -->
[codebase]: https://github.com/microsoft/TypeScript/
[documentation]: https://www.typescriptlang.org/docs/
[local paths]: https://docs.npmjs.com/cli/v11/configuring-npm/package-json#local-paths
[website]: https://www.typescriptlang.org/
[playground]: https://www.typescriptlang.org/play/

<!-- Others -->
[contributors coding guidelines]: https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines
[deep-equal]: https://www.npmjs.com/package/deep-equal
[how to add an item to an array in typescript if not undefined]: https://www.webdevtutor.net/blog/typescript-add-item-to-array-if-not-undefined
[how to break a string into multiple lines in typescript]: https://www.webdevtutor.net/blog/typescript-break-string-into-multiple-lines
[how to initialize an empty typed object in typescript?]: https://timmousk.com/blog/typescript-empty-object/
[mastering typescript import from path]: https://www.webdevtutor.net/blog/typescript-import-from-path
[nullish coalescing: the ?? operator in typescript]: https://mariusschulz.com/blog/nullish-coalescing-the-operator-in-typescript
[remove duplicates from array in typescript]: https://stackoverflow.com/questions/63322597/remove-duplicates-from-array-in-typescript#76633098
[top 12 most useful typescript utility types]: https://timmousk.com/blog/typescript-utility-types/
[typescript deep dive]: https://basarat.gitbook.io/typescript
