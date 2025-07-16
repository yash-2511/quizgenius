// AI Quiz Generator JavaScript

class QuizGenerator {
    constructor() {
        this.currentQuiz = null;
        this.userAnswers = {};
        this.quizSubmitted = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadQuizHistory();
    }

    bindEvents() {
        // File upload form
        const uploadForm = document.getElementById('upload-form');
        uploadForm.addEventListener('submit', (e) => this.handleFileUpload(e));

        // File input change
        const fileInput = document.getElementById('file-input');
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Quiz submission
        const submitBtn = document.getElementById('submit-quiz');
        submitBtn.addEventListener('click', () => this.submitQuiz());

        // New quiz button
        const newQuizBtn = document.getElementById('new-quiz');
        newQuizBtn.addEventListener('click', () => this.resetToUpload());

        // Drag and drop functionality
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        const uploadSection = document.getElementById('upload-section');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadSection.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadSection.addEventListener(eventName, () => {
                uploadSection.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadSection.addEventListener(eventName, () => {
                uploadSection.classList.remove('dragover');
            }, false);
        });

        uploadSection.addEventListener('drop', (e) => this.handleDrop(e), false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            const fileInput = document.getElementById('file-input');
            fileInput.files = files;
            this.handleFileSelect({ target: fileInput });
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            const maxSize = 16 * 1024 * 1024; // 16MB
            if (file.size > maxSize) {
                this.showError('File size too large. Maximum size is 16MB.');
                return;
            }

            const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!allowedTypes.includes(file.type)) {
                this.showError('Invalid file type. Please upload PDF or DOCX files only.');
                return;
            }

            // Update upload button text
            const uploadBtn = document.getElementById('upload-btn');
            uploadBtn.innerHTML = `<i class="fas fa-upload me-2"></i>Generate Quiz from "${file.name}"`;
        }
    }

    async handleFileUpload(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('file-input');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showError('Please select a file to upload.');
            return;
        }

        try {
            this.showProgress('Uploading file...', 25);
            
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Upload failed');
            }

            this.showProgress('Extracting text...', 50);
            
            const result = await response.json();
            
            if (result.success) {
                this.showProgress('Generating quiz...', 75);
                
                // Small delay to show progress
                setTimeout(() => {
                    this.showProgress('Loading quiz...', 100);
                    this.loadQuiz(result.quiz_id);
                }, 500);
            } else {
                throw new Error(result.error || 'Failed to generate quiz');
            }

        } catch (error) {
            console.error('Upload error:', error);
            this.showError(error.message);
            this.hideProgress();
        }
    }

    async loadQuiz(quizId) {
        try {
            const response = await fetch(`/quiz/${quizId}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to load quiz');
            }

            const data = await response.json();
            
            if (data.success) {
                this.currentQuiz = data.quiz;
                this.displayQuiz(data);
                this.loadQuizHistory(); // Refresh history
            } else {
                throw new Error(data.error || 'Failed to load quiz');
            }

        } catch (error) {
            console.error('Quiz loading error:', error);
            this.showError(error.message);
        } finally {
            this.hideProgress();
        }
    }

    displayQuiz(data) {
        this.hideError();
        this.hideUpload();
        this.hideProgress();
        
        const quizSection = document.getElementById('quiz-section');
        const quizTitle = document.getElementById('quiz-title');
        const quizInfo = document.getElementById('quiz-info');
        const quizContent = document.getElementById('quiz-content');
        const quizActions = document.getElementById('quiz-actions');

        // Update header
        quizTitle.innerHTML = `<i class="fas fa-question-circle me-2"></i>Quiz: ${data.filename}`;
        quizInfo.textContent = `${data.quiz.questions.length} Questions`;

        // Generate quiz HTML
        let html = '';
        data.quiz.questions.forEach((question, index) => {
            html += `
                <div class="quiz-question" data-question="${index}">
                    <h5 class="mb-3">${index + 1}. ${question.question}</h5>
                    <div class="quiz-options">
                        ${question.options.map((option, optionIndex) => `
                            <div class="quiz-option" data-question="${index}" data-option="${optionIndex}">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" 
                                           name="question_${index}" id="q${index}_o${optionIndex}" 
                                           value="${optionIndex}">
                                    <label class="form-check-label" for="q${index}_o${optionIndex}">
                                        ${option}
                                    </label>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="quiz-explanation" style="display: none;">
                        <strong>Explanation:</strong> ${question.explanation}
                    </div>
                </div>
            `;
        });

        quizContent.innerHTML = html;
        quizContent.classList.add('quiz-content');

        // Bind option click events
        this.bindQuizEvents();

        // Show quiz and actions
        quizSection.style.display = 'block';
        quizActions.style.display = 'block';
        quizSection.classList.add('animate-slide-in');

        // Reset state
        this.userAnswers = {};
        this.quizSubmitted = false;
    }

    bindQuizEvents() {
        const options = document.querySelectorAll('.quiz-option');
        options.forEach(option => {
            option.addEventListener('click', (e) => {
                if (this.quizSubmitted) return;
                
                const questionIndex = parseInt(option.dataset.question);
                const optionIndex = parseInt(option.dataset.option);
                
                // Remove selection from other options in this question
                const questionOptions = document.querySelectorAll(`[data-question="${questionIndex}"]`);
                questionOptions.forEach(opt => {
                    if (opt.classList.contains('quiz-option')) {
                        opt.classList.remove('selected');
                        const radio = opt.querySelector('input[type="radio"]');
                        if (radio) radio.checked = false;
                    }
                });
                
                // Select this option
                option.classList.add('selected');
                const radio = option.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;
                
                // Store answer
                this.userAnswers[questionIndex] = optionIndex;
            });
        });
    }

    submitQuiz() {
        if (this.quizSubmitted) return;
        
        const totalQuestions = this.currentQuiz.questions.length;
        const answeredQuestions = Object.keys(this.userAnswers).length;
        
        if (answeredQuestions < totalQuestions) {
            if (!confirm(`You have only answered ${answeredQuestions} out of ${totalQuestions} questions. Submit anyway?`)) {
                return;
            }
        }

        this.quizSubmitted = true;
        this.showResults();
    }

    showResults() {
        let correctAnswers = 0;
        const totalQuestions = this.currentQuiz.questions.length;

        this.currentQuiz.questions.forEach((question, index) => {
            const userAnswer = this.userAnswers[index];
            const correctAnswer = question.correct_answer;
            const isCorrect = userAnswer === correctAnswer;
            
            if (isCorrect) correctAnswers++;

            // Update question display
            const questionDiv = document.querySelector(`[data-question="${index}"].quiz-question`);
            const options = questionDiv.querySelectorAll('.quiz-option');
            const explanation = questionDiv.querySelector('.quiz-explanation');

            options.forEach((option, optionIndex) => {
                option.style.pointerEvents = 'none';
                
                if (optionIndex === correctAnswer) {
                    option.classList.add('correct');
                } else if (optionIndex === userAnswer && userAnswer !== correctAnswer) {
                    option.classList.add('incorrect');
                }
            });

            // Show explanation
            explanation.style.display = 'block';
        });

        // Show score
        const percentage = Math.round((correctAnswers / totalQuestions) * 100);
        const scoreText = document.getElementById('score-text');
        scoreText.innerHTML = `
            You scored <strong>${correctAnswers}/${totalQuestions}</strong> (${percentage}%)
            ${percentage >= 80 ? '<i class="fas fa-trophy text-warning ms-2"></i>' : ''}
        `;

        const resultsDiv = document.getElementById('quiz-results');
        resultsDiv.style.display = 'block';
        resultsDiv.classList.add('animate-slide-in');

        // Hide submit button
        const submitBtn = document.getElementById('submit-quiz');
        submitBtn.style.display = 'none';
    }

    async loadQuizHistory() {
        try {
            const response = await fetch('/quizzes');
            
            if (!response.ok) return;

            const data = await response.json();
            
            if (data.success && data.quizzes.length > 0) {
                this.displayQuizHistory(data.quizzes);
            }

        } catch (error) {
            console.error('Error loading quiz history:', error);
        }
    }

    displayQuizHistory(quizzes) {
        const historyDiv = document.getElementById('quiz-history');
        
        let html = '';
        quizzes.slice(0, 5).forEach(quiz => {
            const date = new Date(quiz.created_at).toLocaleString();
            html += `
                <div class="quiz-history-item" data-quiz-id="${quiz.quiz_id}">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${quiz.filename}</strong>
                            <small class="text-muted d-block">${quiz.question_count} questions</small>
                        </div>
                        <small class="text-muted">${date}</small>
                    </div>
                </div>
            `;
        });

        historyDiv.innerHTML = html;

        // Bind click events
        const historyItems = historyDiv.querySelectorAll('.quiz-history-item');
        historyItems.forEach(item => {
            item.addEventListener('click', () => {
                const quizId = item.dataset.quizId;
                this.loadQuiz(quizId);
            });
        });
    }

    showProgress(text, progress = 0) {
        const progressSection = document.getElementById('progress-section');
        const progressText = document.getElementById('progress-text');
        const progressDetail = document.getElementById('progress-detail');
        const progressBar = progressSection.querySelector('.progress-bar');

        progressText.textContent = text;
        progressDetail.textContent = progress < 100 ? 'This may take a few moments' : 'Almost done!';
        progressBar.style.width = `${progress}%`;

        this.hideError();
        this.hideUpload();
        progressSection.style.display = 'block';
    }

    hideProgress() {
        const progressSection = document.getElementById('progress-section');
        progressSection.style.display = 'none';
    }

    showError(message) {
        const errorSection = document.getElementById('error-section');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        errorSection.classList.add('animate-slide-in');
        
        this.hideProgress();
        this.showUpload();
    }

    hideError() {
        const errorSection = document.getElementById('error-section');
        errorSection.style.display = 'none';
    }

    showUpload() {
        const uploadSection = document.getElementById('upload-section');
        uploadSection.style.display = 'block';
    }

    hideUpload() {
        const uploadSection = document.getElementById('upload-section');
        uploadSection.style.display = 'none';
    }

    resetToUpload() {
        // Reset form
        const uploadForm = document.getElementById('upload-form');
        uploadForm.reset();
        
        const uploadBtn = document.getElementById('upload-btn');
        uploadBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Generate Quiz';

        // Hide quiz section
        const quizSection = document.getElementById('quiz-section');
        const submitBtn = document.getElementById('submit-quiz');
        const resultsDiv = document.getElementById('quiz-results');
        
        quizSection.style.display = 'none';
        submitBtn.style.display = 'inline-block';
        resultsDiv.style.display = 'none';

        // Show upload section
        this.showUpload();
        this.hideError();
        this.hideProgress();

        // Reset state
        this.currentQuiz = null;
        this.userAnswers = {};
        this.quizSubmitted = false;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new QuizGenerator();
});
