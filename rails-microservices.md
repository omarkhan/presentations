title: Microservices with Rails
author:
  name: Omar Khan
  url: http://omarkhan.me/
controls: false
style: style.css

--

# Microservices with Rails

--

### @\_\_omar\_\_

- Backend lead at [Playlab Games](http://www.playlab.com/)
- Deploying ruby code to millions of users every day

--

### Scope of this talk

- What are microservices?
- Do you want them?
- How do you do it?
- Lessons learned

--

### Microservices at Playlab

- Currently migrating to microservices on the backend
  - Data persistence
  - User authentication
  - In-app purchase verification
- Mostly rails, some nodejs
- Work in progress!

--

# What are microservices?

--

# Service-Oriented Architecture (SOA)?

--

### Service-Oriented Architecture (SOA)?

![SOA book](images/soa-book.jpg)

--

### What I'm going to talk about:

- Taking a big monolithic web application and splitting it up into little
  pieces, or **microservices**.
- Each microservice runs as a separate process
- Services communicate over the network (http)

--

# Why would I want to do this?

--

### Why would I want to do this?

- Separation of concerns
- Contain failures
- Scale services independently
- Use the right tool for each job

--

### Why would I *not* want to do this?

- Increased ops workload
- These goals can all be achieved in a monolithic codebase, if you have the
  discipline

--

### Rule of thumb

```ruby
def is_this_a_good_idea?
  if ops_wizard? or using_heroku?
    'go for it'
  else
    'probably not'
  end
end
```

--

### Where to start

- Identify the main things your application does
- Try to keep services as separate as possible (best if they don't have to talk
  to each other)
- Start with something easy
- Settle on some common identifiers: user ids, etc.

--

### Checklist

- Good test coverage
- Automated deploys
- Monitoring
- Documentation

--

# Example

--

# Lessons learned

--

### Lessons learned

- Still early days
- Looking good so far

--

### Code quality

- Great opportunity to refactor/rewrite
- Lint all new code, heavily
  - rubocop
  - reek
  - pronto
- Small codebases are easier to understand and maintain

--

### Backward compatibility

- Modify the monolith to call the new microservices
- Modify the new services to call the monolith
- Hack your way through: access the same data stores
- Much easier if you don't have to deal with this at all

--

### DevOps

- Automate everything
- Make it easy to roll back changes
- Use heroku or other PaaS if you can
- Containerize
- Monitoring is essential

--

### Development

Use docker and [fig](https://docs.docker.com/compose/) (AKA docker-compose)

    app:
      build: .
      volumes:
        - '.:/usr/src/app'
      environment:
        RAILS_ENV: development
      links:
        - database
        - redis
      ports:
        - '3000:3000'

    database:
      image: postgres

    redis:
      image: redis
