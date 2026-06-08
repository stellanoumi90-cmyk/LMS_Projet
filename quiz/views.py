from django.shortcuts import render, get_object_or_404
from .models import Quiz

# Vue pour lister les quiz
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

# Vue pour passer un quiz spécifique
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        score = 0
        total = questions.count()
        results = []
        
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            correct_choice = question.choices.filter(is_correct=True).first()
            
            is_right = False
            if selected_choice_id and int(selected_choice_id) == correct_choice.id:
                score += 1
                is_right = True
                
            results.append({
                'question': question.text,
                'correct_choice': correct_choice.text if correct_choice else "Non définie",
                'is_right': is_right
            })
            
        return render(request, 'quiz/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total,
            'results': results
        })

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})
