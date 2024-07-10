document.addEventListener("DOMContentLoaded", function () {
  const loginOption = document.getElementById('loginOption');
  const registerOption = document.getElementById('registerOption');
  const registerFields = document.getElementById('registerFields');
  const submitButton = document.getElementById('submitButton');
  const form = document.getElementById('loginRegisterForm');

  loginOption.addEventListener('click', function () {
    submitButton.textContent = 'Login';
    form.action = "{{ url_for('auth.login') }}";
    registerFields.style.display = 'none';
    // hide register fields
    document.getElementById('email').value = '';  // clean email field
    document.getElementById('email').removeAttribute('required');  // remove required attribute
  });

  registerOption.addEventListener('click', function () {
    submitButton.textContent = 'Register';
    form.action = "{{ url_for('auth.register') }}";
    registerFields.style.display = 'block';
    // display register fields
    document.getElementById('email').setAttribute('required', true);
  });
});