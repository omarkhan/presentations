title: The Test Pyramid
author:
  name: Omar Khan
  url: http://omarkhan.me/
controls: false
style: style.css

--

# The Test Pyramid

--

### @\_\_omar\_\_

- Engineer at [Instructure](http://www.instructure.com/)
- Full-stack web dev
- Learnt these things the hard way

--

### About this talk

- Basic principles of software testing
- Practical focus
- Real-world examples
- Emphasis on unit testing
- Goal: happiness!

--

# Disclaimer

## This is all just some guy's opinion

--

# First things first

## What is testing?

--

### What is testing?

- Manual testing
- Automated testing

--

# Q: Why test?

--

### Q: Why test?

A: To check that our software works!

--

### Q: Why write automated tests?

A: To check that our software works, faster!

--

# Are there other benefits to automated testing?

--

### Automated testing:

- allows us to spot regressions immediately
- helps us make changes faster and with confidence
- helps us write better software (we'll revisit this later)

--

# How do we write automated tests?

--

### Example: testing a web application

- **Automate the manual tests:** browser automation

--

### Example: testing a web application

- Browser automation: functional tests
- **Testing `GET /index.html`**

--

### Example: testing a web application

- Browser automation: functional tests
- Individual requests: integration tests
- **Testing a javascript date formatting helper**

--

### Example: testing a web application

- Browser automation: functional tests
- Individual requests: integration tests
- Functions: unit tests

--

### The test pyramid

![Test pyramid](images/testing-pyramid.png)

from [rubyplus.com](https://rubyplus.com/)

-- 

### Examples: functional tests

```ruby
it "should show error message if wrong credentials are used", priority: "2" do
  get "/login"
  fill_in_login_form("fake@user.com", "fakepass")
  assert_flash_error_message("Invalid username")
end
```

--

### Examples: integration tests

```ruby
it "should inform the user CAS validation denied" do
  stubby("no\n\n")

  get login_url
  redirect_until(cas_redirect_url)

  get '/login/cas', params: {ticket: 'ST-abcd'}
  expect(response).to redirect_to(login_url)
  expect(flash[:delegated_message]).to match(/There was a problem logging in/)
end
```

--

### Examples: unit tests

```js
test('calculateAppointmentGroupEventStatus gives "Reserved" string when reserved', () => {
  calendarEvent.calendarEvent.reserved = true;
  equal(calendarEvent.calculateAppointmentGroupEventStatus(), 'Reserved');
});
```

--

### Why is it a pyramid?

![Test pyramid](images/testing-pyramid.png)

--

### Why is it a pyramid?

- More unit tests than integration tests
- More integration tests than functional tests
- More functional tests than manual tests

--

# Why?

--

### Example: manual test failure

> Hey Omar, this login page isn't working!

--

### Example: functional test failure

```
Excuse an Assignment Gradebook Grid 'ex' can be used to excuse assignments
Failure/Error: expect(excused.text).to eq 'EX'

  expected: "EX"
       got: "submission commentsnEX"
```

--

### Example: integration test failure

```
ConversationsController conversation should leave starryness alone when left out of update
Failure/Error: expect(json["starred"]).to be_truthy

  expected: truthy value
       got: nil
```

--

### Example: unit test failure

```
#add: 1 + 1 should equal 2
Failure/Error: expect(result).to eq 2

  expected: 2
       got: 3
```

--

# What makes a good unit test?

--

### It tests one thing

```ruby
describe '#double' do
  it 'multiplies the input by 2' do
    expect(subject.double(2)).to eq(4)
  end
end
```

--

### It tests one thing

**No:**

```ruby
it "should have an interesting state machine" do
  enrollment_model
  allow(@user).to receive(:dashboard_messages).and_return(Message.none)
  expect(@enrollment.state).to eql(:invited)
  @enrollment.accept
  expect(@enrollment.state).to eql(:active)
  @enrollment.reject
  expect(@enrollment.state).to eql(:rejected)
  Score.where(enrollment_id: @enrollment).delete_all
  @enrollment.destroy_permanently!
  enrollment_model
  @enrollment.complete
  expect(@enrollment.state).to eql(:completed)
  @enrollment.destroy_permanently!
  enrollment_model
  @enrollment.reject
  expect(@enrollment.state).to eql(:rejected)
  @enrollment.destroy_permanently!
  enrollment_model
  @enrollment.accept
  expect(@enrollment.state).to eql(:active)
end

```

--

### We care if it fails

```ruby
describe '#double' do
  it 'multiplies the input by 2' do
    expect(subject.double(2)).to eq(4)
  end
end
```

--

### We care if it fails

**No:**

```ruby
describe '#action' do
  it 'returns an error response' do
    expect(response.status).to eq(422)
    expect(response.body).to eq('Oh no, there is something wrong with your input! You should probably check that you included all the parameters this endpoint expects.')
  end
end
```

--

### It's not affected by changes elsewhere in the code

```ruby
describe '#score' do
  let(:scoring_algorithm) { 'StubbedAlgorithm' }
  let(:expected_score) { 1 }

  before do
    stubbed_algorithm = stubbed_scoring_algorithm.new(expected_score)
    allow(scoring_service).to receive(:scoring_algorithm).and_return(stubbed_algorithm)
  end

  it 'returns the result of the scoring_algorithm multiplied by points_possible' do
    expect(scoring_service.score).to eq expected_score * session_item.points_possible
  end
end
```

--

### It's not affected by changes elsewhere in the code

**No:**

```ruby
context "drop scores" do
  before(:once) do
    course_with_teacher
    course_with_student(course: @course)
    @group = @course.assignment_groups.create!(:name => "some group", :group_weight => 50, :rules => "drop_lowest:1")
    @assignment = @group.assignments.build(:title => "some assignments", :points_possible => 10)
    @assignment.context = @course
    @assignment.save!
    @assignment2 = @group.assignments.build(:title => "some assignment 2", :points_possible => 40)
    @assignment2.context = @course
    @assignment2.save!
  end

  it "should drop high scores for groups when specified" do
    @enrollment = @user.enrollments.first
    @group.update_attribute(:rules, "drop_highest:1")
    expect(@enrollment.reload.computed_current_score).to eql(nil)
    @submission = @assignment.grade_student(@user, grade: "9", grader: @teacher)
    expect(@submission[0].score).to eql(9.0)
    expect(@enrollment.reload.computed_current_score).to eql(90.0)
    @submission2 = @assignment2.grade_student(@user, grade: "20", grader: @teacher)
    expect(@submission2[0].score).to eql(20.0)
    expect(@enrollment.reload.computed_current_score).to eql(50.0)
    @group.update_attribute(:rules, nil)
    expect(@enrollment.reload.computed_current_score).to eql(58.0)
  end
end
```

--

### We're not stating the obvious

**No:**

```js
it('renders the component', function () {
  expect(React.isValidElement(<MyComponent />)).to.be.true
})
```

--

### Good unit test checklist

- It tests one thing
- We care if it fails
- It's not affected by changes elsewhere in the code
- We're not stating the obvious

--

### Integration test checklist

- Cannot be written as a unit test
- Tests a minimum number of units at the same time (ideally 2)

--

### Functional test checklist

- Cannot be written as a unit test
- Cannot be written as an integration test

--

### Manual test checklist

Er... we haven't got around to automating this yet.

--

# How does this help us write better software?

--

### How does this help us write better software?

- Unit tests help us separate concerns
- If you're having trouble writing a good unit test, you might want to rethink
  your design
- If writing good unit tests is easy, your code is probably quite nice!

--

### How does this make us happy?

- Move fast, without breaking things!
- Have confidence in your code

--

### Final words

- It's an art, not a science
- Practicality beats purity
- Learn from open source!
