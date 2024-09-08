document.getElementById('predictionForm').addEventListener('submit', function(event) {
    // Basic validation for all fields
    let valid = true;
    document.querySelectorAll('.error').forEach(function(el) {
        el.textContent = '';
    });

    const fields = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'];
    fields.forEach(function(field) {
        const input = document.getElementById(field);
        if (input.value.trim() === '' || isNaN(input.value)) {
            valid = false;
            document.getElementById(field + 'Error').textContent = 'This field is required and must be a valid number.';
        }
    });

    if (!valid) {
        event.preventDefault();
    }
});