import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_accepts_title_with_maximum_length():
    title = 'a' * 200
    question = Question(title=title)
    assert question.title == title

def test_rejects_points_outside_valid_range():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=101)

def test_new_question_starts_without_choices():
    question = Question(title='q1')
    assert question.choices == []

def test_added_choices_receive_sequential_ids():
    question = Question(title='q1')
    first = question.add_choice('a')
    second = question.add_choice('b')
    assert first.id == 1
    assert second.id == 2

def test_rejects_empty_choice_text():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')

def test_rejects_choice_text_longer_than_100_characters():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

def test_remove_choice_by_id_keeps_the_others():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.remove_choice_by_id(2)
    assert [choice.text for choice in question.choices] == ['a', 'c']

def test_remove_choice_by_id_rejects_unknown_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception, match='Invalid choice id 5'):
        question.remove_choice_by_id(5)

def test_remove_all_choices_clears_every_choice():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert question.choices == []

def test_set_correct_choices_marks_only_the_given_ids():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.set_correct_choices([1, 3])
    assert [choice.is_correct for choice in question.choices] == [True, False, True]

@pytest.fixture
def question_with_choices():
    question = Question(title='Which are fruits?', points=5, max_selections=2)
    question.add_choice('apple', True)
    question.add_choice('carrot', False)
    question.add_choice('banana', True)
    return question

def test_grades_only_the_correct_selected_choices(question_with_choices):
    graded = question_with_choices.correct_selected_choices([1, 2])
    assert graded == [1]

def test_grades_every_selected_correct_choice(question_with_choices):
    graded = question_with_choices.correct_selected_choices([1, 3])
    assert graded == [1, 3]

def test_rejects_more_selections_than_allowed(question_with_choices):
    with pytest.raises(Exception, match='Cannot select more than 2 choices'):
        question_with_choices.correct_selected_choices([1, 2, 3])