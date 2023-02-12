# GraphQL

- query langauge for application programming interfaces (APIs)
- alternative to REST
- prioritizes giving clients exactly the data they need and no more
- offer greater flexibility for querying (complex) data structures

## Pros

- queries can be construced so that they require a single (HTTP) round trip
- allows to query only those fields required for the application -> reduce payload size

## Cons

- queries can get complex
- shifts much of the work of data query to the server side
- rate limiting and pricing is more difficult
- caching is complex
- performance degradation due to inefficient queries (DOS)

## What is GraphQL

- enables **declarative data fetching**
  - as a user, I can precisely declare what information I am interested in
  - e.g.: *"give me all usernames of all users"*
- the server exposes a **single HTTP** endpoint that gets queried


## Examples

### Basic query

`{ status }` -> `{ status: 'available' }`

### Nesting

```
{
    hero {
      name
      height
    }
}
```

```
{
    hero: {
        name: "Luke Skywalker",
        height: 1.74
    }
}

```

### Lists

`{ friends { name } }`

```
{
    friends:
        [
            { name: "Luke Skywalker" },
            { name: "Han Solo" },
            { name: "R2D2" }
        ]
}

```

### Lookups

```
# Gimme the hero with the id 1000
{
    hero(id: "1000") { id name }
}
```

```
{
    hero:
        { id: "1000",
        { name: "Luke Skywalker" }
}

```

### Multiple types

```
# Search users and comments for the word john
{
search(q: "john") {
    id
    ... on User { name }
    ... on Comment { body author { name } }
    }
}

```

### Playground

- https://api.spacex.land/graphql/
