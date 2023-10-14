function toggleDescription(button) {
    const content = button.parentElement.nextElementSibling;
    content.style.display = content.style.display === 'none' || content.style.display === '' ? 'block' : 'none';
    button.innerText = button.innerText === '+' ? '×' : '+';
}
