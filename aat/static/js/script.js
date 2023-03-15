if (document.getElementById('preview')){

    var form = document.getElementById('qt1-form');
    form.addEventListener('input', function(){
        
        template = document.getElementById('question_template').value;
        answersString = document.getElementById('correct_answers').value;
        answersList = []

        if (answersString.trim().length > 0){
            for (answer of answersString.split(',')){
                answersList.push(answer.trim());
            }
        }
        
        for (answer of answersList){
            if (answer.trim().length > 0){
                template = template.replace('BLANK', answer)
            }
        }
    
        document.getElementById('preview').value = template;
    });
}